"""The OBBject."""

from re import sub
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Dict,
    Generic,
    Hashable,
    List,
    Literal,
    Optional,
    Set,
    TypeVar,
    Union,
)

import pandas as pd
import requests
from numpy import ndarray
from pydantic import BaseModel, Field, PrivateAttr

from datamart_core.app.model.abstract.error import DataMartError
from datamart_core.app.model.abstract.tagged import Tagged
from datamart_core.app.model.abstract.warning import Warning_
from datamart_core.app.model.charts.chart import Chart
from datamart_core.app.utils import basemodel_to_df
from datamart_core.provider.abstract.data import Data

if TYPE_CHECKING:
    from datamart_core.app.query import Query

    try:
        from polars import DataFrame as PolarsDataFrame  # type: ignore
    except ImportError:
        PolarsDataFrame = None

T = TypeVar("T")


class OBBject(Tagged, Generic[T]):
    """DataMart object."""

    accessors: ClassVar[Set[str]] = set()
    _user_settings: ClassVar[Optional[BaseModel]] = None
    _system_settings: ClassVar[Optional[BaseModel]] = None

    results: Optional[T] = Field(
        default=None,
        description="Serializable results.",
    )
    provider: Optional[str] = Field(  # type: ignore
        default=None,
        description="Provider name.",
    )
    warnings: Optional[List[Warning_]] = Field(
        default=None,
        description="List of warnings.",
    )
    chart: Optional[Chart] = Field(
        default=None,
        description="Chart object.",
    )
    extra: Dict[str, Any] = Field(
        default_factory=dict,
        description="Extra info.",
    )
    _route: str = PrivateAttr(
        default=None,
    )
    _standard_params: Optional[Dict[str, Any]] = PrivateAttr(
        default_factory=dict,
    )

    def __repr__(self) -> str:
        """Human readable representation of the object."""
        items = [
            f"{k}: {v}"[:83] + ("..." if len(f"{k}: {v}") > 83 else "")
            for k, v in self.model_dump().items()
        ]
        return f"{self.__class__.__name__}\n\n" + "\n".join(items)

    @classmethod
    def results_type_repr(cls, params: Optional[Any] = None) -> str:
        """Return the results type representation."""
        results_field = cls.model_fields.get("results")
        type_repr = "Any"
        if results_field:
            type_ = params[0] if params else results_field.annotation
            type_repr = getattr(type_, "__name__", str(type_))

            if json_schema_extra := getattr(results_field, "json_schema_extra", {}):
                model = json_schema_extra.get("model", "Any")

                if json_schema_extra.get("is_union"):
                    return f"Union[List[{model}], {model}]"
                if json_schema_extra.get("has_list"):
                    return f"List[{model}]"

                return model

            if "typing." in str(type_):
                unpack_optional = sub(r"Optional\[(.*)\]", r"\1", str(type_))
                type_repr = sub(
                    r"(\w+\.)*(\w+)?(\, NoneType)?",
                    r"\2",
                    unpack_optional,
                )

        return type_repr

    @classmethod
    def model_parametrized_name(cls, params: Any) -> str:
        """Return the model name with the parameters."""
        return f"OBBject[{cls.results_type_repr(params)}]"

    def to_df(
        self, index: Optional[Union[str, None]] = "date", sort_by: Optional[str] = None
    ) -> pd.DataFrame:
        """Alias for `to_dataframe`."""
        return self.to_dataframe(index=index, sort_by=sort_by)

    def to_dataframe(
        self, index: Optional[Union[str, None]] = "date", sort_by: Optional[str] = None
    ) -> pd.DataFrame:
        """Convert results field to pandas dataframe.

        Supports converting creating pandas DataFrames from the following
        serializable data formats:

        - List[BaseModel]
        - List[Dict]
        - List[List]
        - List[str]
        - List[int]
        - List[float]
        - Dict[str, Dict]
        - Dict[str, List]
        - Dict[str, BaseModel]

        Parameters
        ----------
        index : Optional[str]
            Column name to use as index.
        sort_by : Optional[str]
            Column name to sort by.

        Returns
        -------
        pd.DataFrame
            Pandas dataframe.
        """

        def is_list_of_basemodel(items: Union[List[T], T]) -> bool:
            return isinstance(items, list) and all(
                isinstance(item, BaseModel) for item in items
            )

        if self.results is None or not self.results:
            raise DataMartError("Results not found.")

        if isinstance(self.results, pd.DataFrame):
            return self.results

        try:
            res = self.results
            df = None
            sort_columns = True

            # List[Dict]
            if isinstance(res, list) and len(res) == 1 and isinstance(res[0], dict):
                r = res[0]
                dict_of_df = {}

                for k, v in r.items():
                    # Dict[str, List[BaseModel]]
                    if is_list_of_basemodel(v):
                        dict_of_df[k] = basemodel_to_df(v, index)
                        sort_columns = False
                    # Dict[str, Any]
                    else:
                        dict_of_df[k] = pd.DataFrame(v)

                df = pd.concat(dict_of_df, axis=1)

            # List[BaseModel]
            elif is_list_of_basemodel(res):
                dt: Union[List[Data], Data] = res  # type: ignore
                df = basemodel_to_df(dt, index)
                sort_columns = False
            # List[List | str | int | float] | Dict[str, Dict | List | BaseModel]
            else:
                try:
                    df = pd.DataFrame(res)  # type: ignore[call-overload]
                    # Set index, if any
                    if df is not None and index is not None and index in df.columns:
                        df.set_index(index, inplace=True)

                except ValueError:
                    if isinstance(res, dict):
                        df = pd.DataFrame([res])

            if df is None:
                raise DataMartError("Unsupported data format.")

            # Drop columns that are all NaN, but don't rearrange columns
            if sort_columns:
                df.sort_index(axis=1, inplace=True)
            df = df.dropna(axis=1, how="all")

            # Sort by specified column
            if sort_by:
                df.sort_values(by=sort_by, inplace=True)

        except DataMartError as e:
            raise e
        except ValueError as ve:
            raise DataMartError(
                f"ValueError: {ve}. Ensure the data format matches the expected format."
            ) from ve
        except TypeError as te:
            raise DataMartError(
                f"TypeError: {te}. Check the data types in your results."
            ) from te
        except Exception as ex:
            raise DataMartError(f"An unexpected error occurred: {ex}") from ex

        return df

    def to_polars(self) -> "PolarsDataFrame":
        """Convert results field to polars dataframe."""
        try:
            from polars import from_pandas  # type: ignore # pylint: disable=import-outside-toplevel
        except ImportError as exc:
            raise ImportError(
                "Please install polars: `pip install polars pyarrow`  to use this method."
            ) from exc

        return from_pandas(self.to_dataframe(index=None))

    def to_numpy(self) -> ndarray:
        """Convert results field to numpy array."""
        return self.to_dataframe(index=None).to_numpy()

    def to_dict(
        self,
        orient: Literal[
            "dict", "list", "series", "split", "tight", "records", "index"
        ] = "list",
    ) -> Union[Dict[Hashable, Any], List[Dict[Hashable, Any]]]:
        """Convert results field to a dictionary using any of pandas to_dict options.

        Parameters
        ----------
        orient : Literal["dict", "list", "series", "split", "tight", "records", "index"]
            Value to pass to `.to_dict()` method


        Returns
        -------
        Union[Dict[Hashable, Any], List[Dict[Hashable, Any]]]
            Dictionary of lists or list of dictionaries if orient is "records".
        """
        df = self.to_dataframe(index=None)
        if (
            orient == "list"
            and isinstance(self.results, dict)
            and all(
                isinstance(value, dict)
                for value in self.results.values()  # pylint: disable=no-member
            )
        ):
            df = df.T
        results = df.to_dict(orient=orient)
        if isinstance(results, dict) and orient == "list" and "index" in results:
            del results["index"]
        return results

    def show(self, **kwargs: Any) -> None:
        """Display chart."""
        # pylint: disable=no-member
        if not self.chart or not self.chart.fig:
            raise DataMartError("Chart not found.")
        show_function: Callable = getattr(self.chart.fig, "show")
        show_function(**kwargs)

    @classmethod
    async def from_query(cls, query: "Query") -> "OBBject":
        """Create OBBject from query.

        Parameters
        ----------
        query : Query
            Initialized query object.

        Returns
        -------
        OBBject[ResultsType]
            OBBject with results.
        """
        return cls(results=await query.execute())
    
    @classmethod
    def from_response(cls, response: requests.models.Response) -> "OBBject":
        """Create OBBject from json. The json is directly from api calls

        Parameters
        ----------
        res_json : json
            Initialized res_json object.

        Returns
        -------
        OBBject[ResultsType]
            OBBject with results.
        """
        if response.status_code != 200:
            raise DataMartError(f"Error: {response.status_code} {response.reason}")
        
        gson = response.json()

        results = gson.get("results", None)
        provider = gson.get("provider", None)
        warnings = gson.get("warnings", None)
        chart = gson.get("chart", None)
        extra = gson.get("extra", None)

        return cls(results=results, provider=provider, warnings=warnings, chart=chart, extra=extra)