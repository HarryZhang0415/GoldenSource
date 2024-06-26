### THIS FILE IS AUTO-GENERATED. DO NOT EDIT. ###

from datamart_core.app.static.container import Container
from datamart_core.app.model.obbject import OBBject
from datamart_core.app.model.custom_parameter import DataMartCustomParameter
import datetime
from typing import List, Union, Optional, Literal
from typing_extensions import Annotated
from datamart_core.app.static.utils.decorators import exception_handler, validate

from datamart_core.app.static.utils.filters import filter_inputs


class ROUTER_derivatives_futures(Container):
    """/derivatives/futures
    curve
    historical
    """

    def __repr__(self) -> str:
        return self.__doc__ or ""

    @exception_handler
    @validate
    def curve(
        self,
        symbol: Annotated[
            str, DataMartCustomParameter(description="Symbol to get data for.")
        ],
        date: Annotated[
            Union[datetime.date, None, str],
            DataMartCustomParameter(description="A specific date to get data for."),
        ] = None,
        provider: Annotated[
            Optional[Literal["cboe", "yfinance"]],
            DataMartCustomParameter(
                description="The provider to use for the query, by default None.\n    If None, the provider specified in defaults is selected or 'cboe' if there is\n    no default."
            ),
        ] = None,
        **kwargs
    ) -> OBBject:
        """Futures Term Structure, current or historical.

        Parameters
        ----------
        symbol : str
            Symbol to get data for.
        date : Union[datetime.date, None, str]
            A specific date to get data for.
        provider : Optional[Literal['cboe', 'yfinance']]
            The provider to use for the query, by default None.
            If None, the provider specified in defaults is selected or 'cboe' if there is
            no default.

        Returns
        -------
        OBBject
            results : List[FuturesCurve]
                Serializable results.
            provider : Optional[Literal['cboe', 'yfinance']]
                Provider name.
            warnings : Optional[List[Warning_]]
                List of warnings.
            chart : Optional[Chart]
                Chart object.
            extra : Dict[str, Any]
                Extra info.

        FuturesCurve
        ------------
        expiration : str
            Futures expiration month.
        price : Optional[float]
            The close price.
        symbol : Optional[str]
            The trading symbol for the tenor of future. (provider: cboe)

        Examples
        --------
        >>> from datamart import market
        >>> market.derivatives.futures.curve(symbol='VX', provider='cboe')
        >>> # Enter a date to get the term structure from a historical date.
        >>> market.derivatives.futures.curve(symbol='NG', provider='yfinance', date='2023-01-01')
        """  # noqa: E501

        return self._run(
            "/derivatives/futures/curve",
            **filter_inputs(
                provider_choices={
                    "provider": self._get_provider(
                        provider,
                        "/derivatives/futures/curve",
                        ("cboe", "yfinance"),
                    )
                },
                standard_params={
                    "symbol": symbol,
                    "date": date,
                },
                extra_params=kwargs,
            )
        )

    @exception_handler
    @validate
    def historical(
        self,
        symbol: Annotated[
            Union[str, List[str]],
            DataMartCustomParameter(
                description="Symbol to get data for. Multiple comma separated items allowed for provider(s): yfinance."
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
        expiration: Annotated[
            Optional[str],
            DataMartCustomParameter(
                description="Future expiry date with format YYYY-MM"
            ),
        ] = None,
        provider: Annotated[
            Optional[Literal["yfinance"]],
            DataMartCustomParameter(
                description="The provider to use for the query, by default None.\n    If None, the provider specified in defaults is selected or 'yfinance' if there is\n    no default."
            ),
        ] = None,
        **kwargs
    ) -> OBBject:
        """Historical futures prices.

        Parameters
        ----------
        symbol : Union[str, List[str]]
            Symbol to get data for. Multiple comma separated items allowed for provider(s): yfinance.
        start_date : Union[datetime.date, None, str]
            Start date of the data, in YYYY-MM-DD format.
        end_date : Union[datetime.date, None, str]
            End date of the data, in YYYY-MM-DD format.
        expiration : Optional[str]
            Future expiry date with format YYYY-MM
        provider : Optional[Literal['yfinance']]
            The provider to use for the query, by default None.
            If None, the provider specified in defaults is selected or 'yfinance' if there is
            no default.
        interval : Literal['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1W', '1M', '1Q']
            Time interval of the data to return. (provider: yfinance)

        Returns
        -------
        OBBject
            results : List[FuturesHistorical]
                Serializable results.
            provider : Optional[Literal['yfinance']]
                Provider name.
            warnings : Optional[List[Warning_]]
                List of warnings.
            chart : Optional[Chart]
                Chart object.
            extra : Dict[str, Any]
                Extra info.

        FuturesHistorical
        -----------------
        date : datetime
            The date of the data.
        open : float
            The open price.
        high : float
            The high price.
        low : float
            The low price.
        close : float
            The close price.
        volume : float
            The trading volume.

        Examples
        --------
        >>> from datamart import market
        >>> market.derivatives.futures.historical(symbol='ES', provider='yfinance')
        >>> # Enter multiple symbols.
        >>> market.derivatives.futures.historical(symbol='ES,NQ', provider='yfinance')
        >>> # Enter expiration dates as "YYYY-MM".
        >>> market.derivatives.futures.historical(symbol='ES', provider='yfinance', expiration='2025-12')
        """  # noqa: E501

        return self._run(
            "/derivatives/futures/historical",
            **filter_inputs(
                provider_choices={
                    "provider": self._get_provider(
                        provider,
                        "/derivatives/futures/historical",
                        ("yfinance",),
                    )
                },
                standard_params={
                    "symbol": symbol,
                    "start_date": start_date,
                    "end_date": end_date,
                    "expiration": expiration,
                },
                extra_params=kwargs,
                info={"symbol": {"multiple_items_allowed": ["yfinance"]}},
            )
        )
