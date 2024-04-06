### THIS FILE IS AUTO-GENERATED. DO NOT EDIT. ###

from datamart_core.app.static.container import Container
from datamart_core.app.model.obbject import OBBject
from datamart_core.app.model.custom_parameter import DataMartCustomParameter
import datetime
from typing import Union, Optional, Literal
from typing_extensions import Annotated
from datamart_core.app.static.utils.decorators import exception_handler, validate

from datamart_core.app.static.utils.filters import filter_inputs


class ROUTER_regulators_cftc(Container):
    """/regulators/cftc
    cot
    cot_search
    """

    def __repr__(self) -> str:
        return self.__doc__ or ""

    @exception_handler
    @validate
    def cot(
        self,
        id: Annotated[
            str,
            DataMartCustomParameter(
                description="The series ID string for the report. Default report is Two-Year Treasury Note Futures."
            ),
        ] = "042601",
        start_date: Annotated[
            Union[datetime.date, None, str],
            DataMartCustomParameter(
                description="Start date of the data, in YYYY-MM-DD format."
            ),
        ] = None,
        end_date: Annotated[
            Union[datetime.date, None, str],
            DataMartCustomParameter(
                description="Start date of the data, in YYYY-MM-DD format."
            ),
        ] = None,
        transform: Annotated[
            Literal["diff", "rdiff", "cumul", "normalize", None],
            DataMartCustomParameter(
                description="Transform the data as difference, percent change, cumulative, or normalize."
            ),
        ] = None,
        collapse: Annotated[
            Literal["daily", "weekly", "monthly", "quarterly", "annual", None],
            DataMartCustomParameter(
                description="Collapse the frequency of the time series."
            ),
        ] = None,
        provider: Annotated[
            Optional[Literal["nasdaq"]],
            DataMartCustomParameter(
                description="The provider to use for the query, by default None.\n    If None, the provider specified in defaults is selected or 'nasdaq' if there is\n    no default."
            ),
        ] = None,
        **kwargs
    ) -> OBBject:
        """Commitment of Traders Reports.

        Parameters
        ----------
        id : str
            The series ID string for the report. Default report is Two-Year Treasury Note Futures.
        start_date : Union[datetime.date, None, str]
            Start date of the data, in YYYY-MM-DD format.
        end_date : Union[datetime.date, None, str]
            Start date of the data, in YYYY-MM-DD format.
        transform : Literal['diff', 'rdiff', 'cumul', 'normalize', None]
            Transform the data as difference, percent change, cumulative, or normalize.
        collapse : Literal['daily', 'weekly', 'monthly', 'quarterly', 'annual', None]
            Collapse the frequency of the time series.
        provider : Optional[Literal['nasdaq']]
            The provider to use for the query, by default None.
            If None, the provider specified in defaults is selected or 'nasdaq' if there is
            no default.
        data_type : Optional[Literal['F', 'FO', 'CITS']]

                    The type of data to reuturn. Default is "FO".

                    F = Futures only

                    FO = Futures and Options

                    CITS = Commodity Index Trader Supplemental. Only valid for commodities.
                     (provider: nasdaq)
        legacy_format : Optional[bool]
            Returns the legacy format of report. Default is False. (provider: nasdaq)
        report_type : Optional[Literal['ALL', 'CHG', 'OLD', 'OTR']]

                    The type of report to return. Default is "ALL".

                    ALL = All

                    CHG = Change in Positions

                    OLD = Old Crop Years

                    OTR = Other Crop Years
                     (provider: nasdaq)
        measure : Optional[Literal['CR', 'NT', 'OI', 'CHG']]

                    The measure to return. Default is None.

                    CR = Concentration Ratios

                    NT = Number of Traders

                    OI = Percent of Open Interest

                    CHG = Change in Positions. Only valid when data_type is "CITS".
                     (provider: nasdaq)

        Returns
        -------
        OBBject
            results : List[COT]
                Serializable results.
            provider : Optional[Literal['nasdaq']]
                Provider name.
            warnings : Optional[List[Warning_]]
                List of warnings.
            chart : Optional[Chart]
                Chart object.
            extra : Dict[str, Any]
                Extra info.

        COT
        ---
        date : date
            The date of the data.

        Examples
        --------
        >>> from datamart import market
        >>> market.regulators.cftc.cot(provider='nasdaq')
        >>> # Get the Commitment of Traders Report for Gold.
        >>> market.regulators.cftc.cot(id='GC=F', provider='nasdaq')
        >>> # Enter the report ID by the Nasdaq Data Link Code.
        >>> market.regulators.cftc.cot(id='088691', provider='nasdaq')
        >>> # Get the report for futures only.
        >>> market.regulators.cftc.cot(id='088691', data_type='F', provider='nasdaq')
        """  # noqa: E501

        return self._run(
            "/regulators/cftc/cot",
            **filter_inputs(
                provider_choices={
                    "provider": self._get_provider(
                        provider,
                        "/regulators/cftc/cot",
                        ("nasdaq",),
                    )
                },
                standard_params={
                    "id": id,
                    "start_date": start_date,
                    "end_date": end_date,
                    "transform": transform,
                    "collapse": collapse,
                },
                extra_params=kwargs,
            )
        )

    @exception_handler
    @validate
    def cot_search(
        self,
        query: Annotated[
            str, DataMartCustomParameter(description="Search query.")
        ] = "",
        use_cache: Annotated[
            Optional[bool],
            DataMartCustomParameter(
                description="Whether or not to use cache. If True, cache will store for seven days."
            ),
        ] = True,
        provider: Annotated[
            Optional[Literal["nasdaq"]],
            DataMartCustomParameter(
                description="The provider to use for the query, by default None.\n    If None, the provider specified in defaults is selected or 'nasdaq' if there is\n    no default."
            ),
        ] = None,
        **kwargs
    ) -> OBBject:
        """Curated Commitment of Traders Reports.

        Search a list of curated Commitment of Traders Reports series information.


        Parameters
        ----------
        query : str
            Search query.
        use_cache : Optional[bool]
            Whether or not to use cache. If True, cache will store for seven days.
        provider : Optional[Literal['nasdaq']]
            The provider to use for the query, by default None.
            If None, the provider specified in defaults is selected or 'nasdaq' if there is
            no default.

        Returns
        -------
        OBBject
            results : List[COTSearch]
                Serializable results.
            provider : Optional[Literal['nasdaq']]
                Provider name.
            warnings : Optional[List[Warning_]]
                List of warnings.
            chart : Optional[Chart]
                Chart object.
            extra : Dict[str, Any]
                Extra info.

        COTSearch
        ---------
        code : str
            CFTC Code of the report.
        name : str
            Name of the underlying asset.
        category : Optional[str]
            Category of the underlying asset.
        subcategory : Optional[str]
            Subcategory of the underlying asset.
        units : Optional[str]
            The units for one contract.
        symbol : Optional[str]
            Symbol representing the entity requested in the data.

        Examples
        --------
        >>> from datamart import market
        >>> market.regulators.cftc.cot_search(provider='nasdaq')
        >>> market.regulators.cftc.cot_search(query='gold', provider='nasdaq')
        """  # noqa: E501

        return self._run(
            "/regulators/cftc/cot_search",
            **filter_inputs(
                provider_choices={
                    "provider": self._get_provider(
                        provider,
                        "/regulators/cftc/cot_search",
                        ("nasdaq",),
                    )
                },
                standard_params={
                    "query": query,
                    "use_cache": use_cache,
                },
                extra_params=kwargs,
            )
        )