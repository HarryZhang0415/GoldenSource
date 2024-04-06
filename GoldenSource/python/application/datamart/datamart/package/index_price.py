### THIS FILE IS AUTO-GENERATED. DO NOT EDIT. ###

from datamart_core.app.static.container import Container
from datamart_core.app.model.obbject import OBBject
from datamart_core.app.model.custom_parameter import DataMartCustomParameter
import datetime
from typing import List, Union, Optional, Literal
from typing_extensions import Annotated
from datamart_core.app.static.utils.decorators import exception_handler, validate

from datamart_core.app.static.utils.filters import filter_inputs


class ROUTER_index_price(Container):
    """/index/price
    historical
    """

    def __repr__(self) -> str:
        return self.__doc__ or ""

    @exception_handler
    @validate
    def historical(
        self,
        symbol: Annotated[
            Union[str, List[str]],
            DataMartCustomParameter(
                description="Symbol to get data for. Multiple comma separated items allowed for provider(s): fmp, intrinio, polygon, yfinance."
            ),
        ],
        start_date: Annotated[
            Union[datetime.date, None, str],
            DataMartCustomParameter(
                description="Start date of the data, in YYYY-MM-DD format."
            ),
        ] = None,
        end_date: Annotated[
            Union[datetime.date, None, str],
            DataMartCustomParameter(
                description="End date of the data, in YYYY-MM-DD format."
            ),
        ] = None,
        interval: Annotated[
            Optional[str],
            DataMartCustomParameter(description="Time interval of the data to return."),
        ] = "1d",
        provider: Annotated[
            Optional[Literal["fmp", "intrinio", "polygon", "yfinance"]],
            DataMartCustomParameter(
                description="The provider to use for the query, by default None.\n    If None, the provider specified in defaults is selected or 'fmp' if there is\n    no default."
            ),
        ] = None,
        **kwargs
    ) -> OBBject:
        """Historical Index Levels.

        Parameters
        ----------
        symbol : Union[str, List[str]]
            Symbol to get data for. Multiple comma separated items allowed for provider(s): fmp, intrinio, polygon, yfinance.
        start_date : Union[datetime.date, None, str]
            Start date of the data, in YYYY-MM-DD format.
        end_date : Union[datetime.date, None, str]
            End date of the data, in YYYY-MM-DD format.
        interval : Optional[str]
            Time interval of the data to return.
        provider : Optional[Literal['fmp', 'intrinio', 'polygon', 'yfinance']]
            The provider to use for the query, by default None.
            If None, the provider specified in defaults is selected or 'fmp' if there is
            no default.
        limit : Optional[int]
            The number of data entries to return. (provider: intrinio, polygon)
        sort : Literal['asc', 'desc']
            Sort order of the data. This impacts the results in combination with the 'limit' parameter. The results are always returned in ascending order by date. (provider: polygon)

        Returns
        -------
        OBBject
            results : List[IndexHistorical]
                Serializable results.
            provider : Optional[Literal['fmp', 'intrinio', 'polygon', 'yfinance']]
                Provider name.
            warnings : Optional[List[Warning_]]
                List of warnings.
            chart : Optional[Chart]
                Chart object.
            extra : Dict[str, Any]
                Extra info.

        IndexHistorical
        ---------------
        date : Union[date, datetime]
            The date of the data.
        open : Optional[Annotated[float, Strict(strict=True)]]
            The open price.
        high : Optional[Annotated[float, Strict(strict=True)]]
            The high price.
        low : Optional[Annotated[float, Strict(strict=True)]]
            The low price.
        close : Optional[Annotated[float, Strict(strict=True)]]
            The close price.
        volume : Optional[int]
            The trading volume.
        vwap : Optional[float]
            Volume Weighted Average Price over the period. (provider: fmp)
        change : Optional[float]
            Change in the price from the previous close. (provider: fmp)
        change_percent : Optional[float]
            Change in the price from the previous close, as a normalized percent. (provider: fmp)
        transactions : Optional[Annotated[int, Gt(gt=0)]]
            Number of transactions for the symbol in the time period. (provider: polygon)

        Examples
        --------
        >>> from datamart import market
        >>> market.index.price.historical(symbol='^GSPC', provider='fmp')
        >>> # Not all providers have the same symbols.
        >>> market.index.price.historical(symbol='SPX', provider='intrinio')
        """  # noqa: E501

        return self._run(
            "/index/price/historical",
            **filter_inputs(
                provider_choices={
                    "provider": self._get_provider(
                        provider,
                        "/index/price/historical",
                        ("fmp", "intrinio", "polygon", "yfinance"),
                    )
                },
                standard_params={
                    "symbol": symbol,
                    "start_date": start_date,
                    "end_date": end_date,
                    "interval": interval,
                },
                extra_params=kwargs,
                info={
                    "symbol": {
                        "multiple_items_allowed": [
                            "fmp",
                            "intrinio",
                            "polygon",
                            "yfinance",
                        ]
                    }
                },
            )
        )
