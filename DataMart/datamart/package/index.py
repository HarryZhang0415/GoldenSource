### THIS FILE IS AUTO-GENERATED. DO NOT EDIT. ###

from datamart_core.app.static.container import Container
from datamart_core.app.model.obbject import OBBject
from datamart_core.app.model.custom_parameter import DataMartCustomParameter
import datetime
from typing import List, Union, Optional, Literal
from warnings import warn, simplefilter
from typing_extensions import Annotated, deprecated
from datamart_core.app.static.utils.decorators import exception_handler, validate

from datamart_core.app.static.utils.filters import filter_inputs

from datamart_core.app.deprecation import DataMartDeprecationWarning


class ROUTER_index(Container):
    """/index
    available
    constituents
    market
    /price
    search
    sectors
    snapshots
    sp500_multiples
    """

    def __repr__(self) -> str:
        return self.__doc__ or ""

    @exception_handler
    @validate
    def available(
        self,
        provider: Annotated[
            Optional[Literal["cboe", "fmp", "tmx", "yfinance"]],
            DataMartCustomParameter(
                description="The provider to use for the query, by default None.\n    If None, the provider specified in defaults is selected or 'cboe' if there is\n    no default."
            ),
        ] = None,
        **kwargs
    ) -> OBBject:
        """All indices available from a given provider.

        Parameters
        ----------
        provider : Optional[Literal['cboe', 'fmp', 'tmx', 'yfinance']]
            The provider to use for the query, by default None.
            If None, the provider specified in defaults is selected or 'cboe' if there is
            no default.
        use_cache : bool
            When True, the Cboe Index directory will be cached for 24 hours. Set as False to bypass. (provider: cboe);
            Whether to use a cached request. Index data is from a single JSON file, updated each day after close. It is cached for one day. To bypass, set to False. (provider: tmx)

        Returns
        -------
        OBBject
            results : List[AvailableIndices]
                Serializable results.
            provider : Optional[Literal['cboe', 'fmp', 'tmx', 'yfinance']]
                Provider name.
            warnings : Optional[List[Warning_]]
                List of warnings.
            chart : Optional[Chart]
                Chart object.
            extra : Dict[str, Any]
                Extra info.

        AvailableIndices
        ----------------
        name : Optional[str]
            Name of the index.
        currency : Optional[str]
            Currency the index is traded in.
        symbol : Optional[str]
            Symbol for the index. (provider: cboe, tmx, yfinance)
        description : Optional[str]
            Description for the index. Valid only for US indices. (provider: cboe)
        data_delay : Optional[int]
            Data delay for the index. Valid only for US indices. (provider: cboe)
        open_time : Optional[datetime.time]
            Opening time for the index. Valid only for US indices. (provider: cboe)
        close_time : Optional[datetime.time]
            Closing time for the index. Valid only for US indices. (provider: cboe)
        time_zone : Optional[str]
            Time zone for the index. Valid only for US indices. (provider: cboe)
        tick_days : Optional[str]
            The trading days for the index. Valid only for US indices. (provider: cboe)
        tick_frequency : Optional[str]
            The frequency of the index ticks. Valid only for US indices. (provider: cboe)
        tick_period : Optional[str]
            The period of the index ticks. Valid only for US indices. (provider: cboe)
        stock_exchange : Optional[str]
            Stock exchange where the index is listed. (provider: fmp)
        exchange_short_name : Optional[str]
            Short name of the stock exchange where the index is listed. (provider: fmp)
        code : Optional[str]
            ID code for keying the index in the DataMart Terminal. (provider: yfinance)

        Examples
        --------
        >>> from datamart import market
        >>> market.index.available(provider='fmp')
        >>> market.index.available(provider='yfinance')
        """  # noqa: E501

        return self._run(
            "/index/available",
            **filter_inputs(
                provider_choices={
                    "provider": self._get_provider(
                        provider,
                        "/index/available",
                        ("cboe", "fmp", "tmx", "yfinance"),
                    )
                },
                standard_params={},
                extra_params=kwargs,
            )
        )

    @exception_handler
    @validate
    def constituents(
        self,
        symbol: Annotated[
            str, DataMartCustomParameter(description="Symbol to get data for.")
        ],
        provider: Annotated[
            Optional[Literal["cboe", "fmp", "tmx"]],
            DataMartCustomParameter(
                description="The provider to use for the query, by default None.\n    If None, the provider specified in defaults is selected or 'cboe' if there is\n    no default."
            ),
        ] = None,
        **kwargs
    ) -> OBBject:
        """Index Constituents.

        Parameters
        ----------
        symbol : str
            Symbol to get data for.
        provider : Optional[Literal['cboe', 'fmp', 'tmx']]
            The provider to use for the query, by default None.
            If None, the provider specified in defaults is selected or 'cboe' if there is
            no default.
        use_cache : bool
            Whether to use a cached request. Index data is from a single JSON file, updated each day after close. It is cached for one day. To bypass, set to False. (provider: tmx)

        Returns
        -------
        OBBject
            results : List[IndexConstituents]
                Serializable results.
            provider : Optional[Literal['cboe', 'fmp', 'tmx']]
                Provider name.
            warnings : Optional[List[Warning_]]
                List of warnings.
            chart : Optional[Chart]
                Chart object.
            extra : Dict[str, Any]
                Extra info.

        IndexConstituents
        -----------------
        symbol : str
            Symbol representing the entity requested in the data.
        name : Optional[str]
            Name of the constituent company in the index.
        security_type : Optional[str]
            The type of security represented. (provider: cboe)
        last_price : Optional[float]
            Last price for the symbol. (provider: cboe)
        open : Optional[float]
            The open price. (provider: cboe)
        high : Optional[float]
            The high price. (provider: cboe)
        low : Optional[float]
            The low price. (provider: cboe)
        close : Optional[float]
            The close price. (provider: cboe)
        volume : Optional[int]
            The trading volume. (provider: cboe)
        prev_close : Optional[float]
            The previous close price. (provider: cboe)
        change : Optional[float]
            Change in price. (provider: cboe)
        change_percent : Optional[float]
            Change in price as a normalized percentage. (provider: cboe)
        tick : Optional[str]
            Whether the last sale was an up or down tick. (provider: cboe)
        last_trade_time : Optional[datetime]
            Last trade timestamp for the symbol. (provider: cboe)
        asset_type : Optional[str]
            Type of asset. (provider: cboe)
        sector : Optional[str]
            Sector the constituent company in the index belongs to. (provider: fmp)
        sub_sector : Optional[str]
            Sub-sector the constituent company in the index belongs to. (provider: fmp)
        headquarter : Optional[str]
            Location of the headquarter of the constituent company in the index. (provider: fmp)
        date_first_added : Optional[Union[str, date]]
            Date the constituent company was added to the index. (provider: fmp)
        cik : Optional[int]
            Central Index Key (CIK) for the requested entity. (provider: fmp)
        founded : Optional[Union[str, date]]
            Founding year of the constituent company in the index. (provider: fmp)
        market_value : Optional[float]
            The quoted market value of the asset. (provider: tmx)

        Examples
        --------
        >>> from datamart import market
        >>> market.index.constituents(symbol='dowjones', provider='fmp')
        >>> # Providers other than FMP will use the ticker symbol.
        >>> market.index.constituents(symbol='BEP50P', provider='cboe')
        """  # noqa: E501

        return self._run(
            "/index/constituents",
            **filter_inputs(
                provider_choices={
                    "provider": self._get_provider(
                        provider,
                        "/index/constituents",
                        ("cboe", "fmp", "tmx"),
                    )
                },
                standard_params={
                    "symbol": symbol,
                },
                extra_params=kwargs,
            )
        )

    @exception_handler
    @validate
    @deprecated(
        "This endpoint is deprecated; use `/index/price/historical` instead. Deprecated in DataMart Market V4.1 to be removed in V4.3.",
        category=DataMartDeprecationWarning,
    )
    def market(
        self,
        symbol: Annotated[
            Union[str, List[str]],
            DataMartCustomParameter(
                description="Symbol to get data for. Multiple comma separated items allowed for provider(s): cboe, fmp, intrinio, polygon, yfinance."
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
            Optional[Literal["cboe", "fmp", "intrinio", "polygon", "yfinance"]],
            DataMartCustomParameter(
                description="The provider to use for the query, by default None.\n    If None, the provider specified in defaults is selected or 'cboe' if there is\n    no default."
            ),
        ] = None,
        **kwargs
    ) -> OBBject:
        """Historical Market Indices.

        Parameters
        ----------
        symbol : Union[str, List[str]]
            Symbol to get data for. Multiple comma separated items allowed for provider(s): cboe, fmp, intrinio, polygon, yfinance.
        start_date : Union[datetime.date, None, str]
            Start date of the data, in YYYY-MM-DD format.
        end_date : Union[datetime.date, None, str]
            End date of the data, in YYYY-MM-DD format.
        interval : Optional[str]
            Time interval of the data to return.
        provider : Optional[Literal['cboe', 'fmp', 'intrinio', 'polygon', 'yfinance'...
            The provider to use for the query, by default None.
            If None, the provider specified in defaults is selected or 'cboe' if there is
            no default.
        use_cache : bool
            When True, the company directories will be cached for 24 hours and are used to validate symbols. The results of the function are not cached. Set as False to bypass. (provider: cboe)
        limit : Optional[int]
            The number of data entries to return. (provider: intrinio, polygon)
        sort : Literal['asc', 'desc']
            Sort order of the data. This impacts the results in combination with the 'limit' parameter. The results are always returned in ascending order by date. (provider: polygon)

        Returns
        -------
        OBBject
            results : List[MarketIndices]
                Serializable results.
            provider : Optional[Literal['cboe', 'fmp', 'intrinio', 'polygon', 'yfinance']]
                Provider name.
            warnings : Optional[List[Warning_]]
                List of warnings.
            chart : Optional[Chart]
                Chart object.
            extra : Dict[str, Any]
                Extra info.

        MarketIndices
        -------------
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
        calls_volume : Optional[float]
            Number of calls traded during the most recent trading period. Only valid if interval is 1m. (provider: cboe)
        puts_volume : Optional[float]
            Number of puts traded during the most recent trading period. Only valid if interval is 1m. (provider: cboe)
        total_options_volume : Optional[float]
            Total number of options traded during the most recent trading period. Only valid if interval is 1m. (provider: cboe)
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
        >>> market.index.market(symbol='^IBEX', provider='fmp')
        """  # noqa: E501

        simplefilter("always", DeprecationWarning)
        warn(
            "This endpoint is deprecated; use `/index/price/historical` instead. Deprecated in DataMart Market V4.1 to be removed in V4.3.",
            category=DeprecationWarning,
            stacklevel=2,
        )

        return self._run(
            "/index/market",
            **filter_inputs(
                provider_choices={
                    "provider": self._get_provider(
                        provider,
                        "/index/market",
                        ("cboe", "fmp", "intrinio", "polygon", "yfinance"),
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
                            "cboe",
                            "fmp",
                            "intrinio",
                            "polygon",
                            "yfinance",
                        ]
                    }
                },
            )
        )

    @property
    def price(self):
        # pylint: disable=import-outside-toplevel
        from . import index_price

        return index_price.ROUTER_index_price(command_runner=self._command_runner)

    @exception_handler
    @validate
    def search(
        self,
        query: Annotated[
            str, DataMartCustomParameter(description="Search query.")
        ] = "",
        is_symbol: Annotated[
            bool,
            DataMartCustomParameter(description="Whether to search by ticker symbol."),
        ] = False,
        provider: Annotated[
            Optional[Literal["cboe"]],
            DataMartCustomParameter(
                description="The provider to use for the query, by default None.\n    If None, the provider specified in defaults is selected or 'cboe' if there is\n    no default."
            ),
        ] = None,
        **kwargs
    ) -> OBBject:
        """Filters indices for rows containing the query.

        Parameters
        ----------
        query : str
            Search query.
        is_symbol : bool
            Whether to search by ticker symbol.
        provider : Optional[Literal['cboe']]
            The provider to use for the query, by default None.
            If None, the provider specified in defaults is selected or 'cboe' if there is
            no default.
        use_cache : bool
            When True, the Cboe Index directory will be cached for 24 hours. Set as False to bypass. (provider: cboe)

        Returns
        -------
        OBBject
            results : List[IndexSearch]
                Serializable results.
            provider : Optional[Literal['cboe']]
                Provider name.
            warnings : Optional[List[Warning_]]
                List of warnings.
            chart : Optional[Chart]
                Chart object.
            extra : Dict[str, Any]
                Extra info.

        IndexSearch
        -----------
        symbol : str
            Symbol representing the entity requested in the data.
        name : str
            Name of the index.
        description : Optional[str]
            Description for the index. (provider: cboe)
        data_delay : Optional[int]
            Data delay for the index. Valid only for US indices. (provider: cboe)
        currency : Optional[str]
            Currency for the index. (provider: cboe)
        time_zone : Optional[str]
            Time zone for the index. Valid only for US indices. (provider: cboe)
        open_time : Optional[datetime.time]
            Opening time for the index. Valid only for US indices. (provider: cboe)
        close_time : Optional[datetime.time]
            Closing time for the index. Valid only for US indices. (provider: cboe)
        tick_days : Optional[str]
            The trading days for the index. Valid only for US indices. (provider: cboe)
        tick_frequency : Optional[str]
            Tick frequency for the index. Valid only for US indices. (provider: cboe)
        tick_period : Optional[str]
            Tick period for the index. Valid only for US indices. (provider: cboe)

        Examples
        --------
        >>> from datamart import market
        >>> market.index.search(provider='cboe')
        >>> market.index.search(query='SPX', provider='cboe')
        """  # noqa: E501

        return self._run(
            "/index/search",
            **filter_inputs(
                provider_choices={
                    "provider": self._get_provider(
                        provider,
                        "/index/search",
                        ("cboe",),
                    )
                },
                standard_params={
                    "query": query,
                    "is_symbol": is_symbol,
                },
                extra_params=kwargs,
            )
        )

    @exception_handler
    @validate
    def sectors(
        self,
        symbol: Annotated[
            str, DataMartCustomParameter(description="Symbol to get data for.")
        ],
        provider: Annotated[
            Optional[Literal["tmx"]],
            DataMartCustomParameter(
                description="The provider to use for the query, by default None.\n    If None, the provider specified in defaults is selected or 'tmx' if there is\n    no default."
            ),
        ] = None,
        **kwargs
    ) -> OBBject:
        """Index Sectors. Sector weighting of an index.

        Parameters
        ----------
        symbol : str
            Symbol to get data for.
        provider : Optional[Literal['tmx']]
            The provider to use for the query, by default None.
            If None, the provider specified in defaults is selected or 'tmx' if there is
            no default.
        use_cache : bool
            Whether to use a cached request. All Index data comes from a single JSON file that is updated daily. To bypass, set to False. If True, the data will be cached for 1 day. (provider: tmx)

        Returns
        -------
        OBBject
            results : List[IndexSectors]
                Serializable results.
            provider : Optional[Literal['tmx']]
                Provider name.
            warnings : Optional[List[Warning_]]
                List of warnings.
            chart : Optional[Chart]
                Chart object.
            extra : Dict[str, Any]
                Extra info.

        IndexSectors
        ------------
        sector : str
            The sector name.
        weight : float
            The weight of the sector in the index.

        Examples
        --------
        >>> from datamart import market
        >>> market.index.sectors(symbol='^TX60', provider='tmx')
        """  # noqa: E501

        return self._run(
            "/index/sectors",
            **filter_inputs(
                provider_choices={
                    "provider": self._get_provider(
                        provider,
                        "/index/sectors",
                        ("tmx",),
                    )
                },
                standard_params={
                    "symbol": symbol,
                },
                extra_params=kwargs,
            )
        )

    @exception_handler
    @validate
    def snapshots(
        self,
        region: Annotated[
            str,
            DataMartCustomParameter(
                description="The region of focus for the data - i.e., us, eu."
            ),
        ] = "us",
        provider: Annotated[
            Optional[Literal["cboe", "tmx"]],
            DataMartCustomParameter(
                description="The provider to use for the query, by default None.\n    If None, the provider specified in defaults is selected or 'cboe' if there is\n    no default."
            ),
        ] = None,
        **kwargs
    ) -> OBBject:
        """Index Snapshots. Current levels for all indices from a provider, grouped by `region`.

        Parameters
        ----------
        region : str
            The region of focus for the data - i.e., us, eu.
        provider : Optional[Literal['cboe', 'tmx']]
            The provider to use for the query, by default None.
            If None, the provider specified in defaults is selected or 'cboe' if there is
            no default.
        use_cache : bool
            Whether to use a cached request. Index data is from a single JSON file, updated each day after close. It is cached for one day. To bypass, set to False. (provider: tmx)

        Returns
        -------
        OBBject
            results : List[IndexSnapshots]
                Serializable results.
            provider : Optional[Literal['cboe', 'tmx']]
                Provider name.
            warnings : Optional[List[Warning_]]
                List of warnings.
            chart : Optional[Chart]
                Chart object.
            extra : Dict[str, Any]
                Extra info.

        IndexSnapshots
        --------------
        symbol : str
            Symbol representing the entity requested in the data.
        name : Optional[str]
            Name of the index.
        currency : Optional[str]
            Currency of the index.
        price : Optional[float]
            Current price of the index.
        open : Optional[float]
            The open price.
        high : Optional[float]
            The high price.
        low : Optional[float]
            The low price.
        close : Optional[float]
            The close price.
        volume : Optional[int]
            The trading volume.
        prev_close : Optional[float]
            The previous close price.
        change : Optional[float]
            Change in value of the index.
        change_percent : Optional[float]
            Change, in normalized percentage points, of the index.
        bid : Optional[float]
            Current bid price. (provider: cboe)
        ask : Optional[float]
            Current ask price. (provider: cboe)
        last_trade_time : Optional[datetime]
            Last trade timestamp for the symbol. (provider: cboe)
        status : Optional[str]
            Status of the market, open or closed. (provider: cboe)
        year_high : Optional[float]
            The 52-week high of the index. (provider: tmx)
        year_low : Optional[float]
            The 52-week low of the index. (provider: tmx)
        return_mtd : Optional[float]
            The month-to-date return of the index, as a normalized percent. (provider: tmx)
        return_qtd : Optional[float]
            The quarter-to-date return of the index, as a normalized percent. (provider: tmx)
        return_ytd : Optional[float]
            The year-to-date return of the index, as a normalized percent. (provider: tmx)
        total_market_value : Optional[float]
            The total quoted market value of the index. (provider: tmx)
        number_of_constituents : Optional[int]
            The number of constituents in the index. (provider: tmx)
        constituent_average_market_value : Optional[float]
            The average quoted market value of the index constituents. (provider: tmx)
        constituent_median_market_value : Optional[float]
            The median quoted market value of the index constituents. (provider: tmx)
        constituent_top10_market_value : Optional[float]
            The sum of the top 10 quoted market values of the index constituents. (provider: tmx)
        constituent_largest_market_value : Optional[float]
            The largest quoted market value of the index constituents. (provider: tmx)
        constituent_largest_weight : Optional[float]
            The largest weight of the index constituents, as a normalized percent. (provider: tmx)
        constituent_smallest_market_value : Optional[float]
            The smallest quoted market value of the index constituents. (provider: tmx)
        constituent_smallest_weight : Optional[float]
            The smallest weight of the index constituents, as a normalized percent. (provider: tmx)

        Examples
        --------
        >>> from datamart import market
        >>> market.index.snapshots(provider='tmx')
        >>> market.index.snapshots(region='us', provider='cboe')
        """  # noqa: E501

        return self._run(
            "/index/snapshots",
            **filter_inputs(
                provider_choices={
                    "provider": self._get_provider(
                        provider,
                        "/index/snapshots",
                        ("cboe", "tmx"),
                    )
                },
                standard_params={
                    "region": region,
                },
                extra_params=kwargs,
            )
        )

    @exception_handler
    @validate
    def sp500_multiples(
        self,
        series_name: Annotated[
            Literal[
                "shiller_pe_month",
                "shiller_pe_year",
                "pe_year",
                "pe_month",
                "dividend_year",
                "dividend_month",
                "dividend_growth_quarter",
                "dividend_growth_year",
                "dividend_yield_year",
                "dividend_yield_month",
                "earnings_year",
                "earnings_month",
                "earnings_growth_year",
                "earnings_growth_quarter",
                "real_earnings_growth_year",
                "real_earnings_growth_quarter",
                "earnings_yield_year",
                "earnings_yield_month",
                "real_price_year",
                "real_price_month",
                "inflation_adjusted_price_year",
                "inflation_adjusted_price_month",
                "sales_year",
                "sales_quarter",
                "sales_growth_year",
                "sales_growth_quarter",
                "real_sales_year",
                "real_sales_quarter",
                "real_sales_growth_year",
                "real_sales_growth_quarter",
                "price_to_sales_year",
                "price_to_sales_quarter",
                "price_to_book_value_year",
                "price_to_book_value_quarter",
                "book_value_year",
                "book_value_quarter",
            ],
            DataMartCustomParameter(
                description="The name of the series. Defaults to 'pe_month'."
            ),
        ] = "pe_month",
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
        """Historical S&P 500 multiples and Shiller PE ratios.

        Parameters
        ----------
        series_name : Literal['shiller_pe_month', 'shiller_pe_year', 'pe_year', 'pe_month', 'd...
            The name of the series. Defaults to 'pe_month'.
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

        Returns
        -------
        OBBject
            results : List[SP500Multiples]
                Serializable results.
            provider : Optional[Literal['nasdaq']]
                Provider name.
            warnings : Optional[List[Warning_]]
                List of warnings.
            chart : Optional[Chart]
                Chart object.
            extra : Dict[str, Any]
                Extra info.

        SP500Multiples
        --------------
        date : date
            The date of the data.

        Examples
        --------
        >>> from datamart import market
        >>> market.index.sp500_multiples(provider='nasdaq')
        >>> market.index.sp500_multiples(series_name='shiller_pe_year', provider='nasdaq')
        """  # noqa: E501

        return self._run(
            "/index/sp500_multiples",
            **filter_inputs(
                provider_choices={
                    "provider": self._get_provider(
                        provider,
                        "/index/sp500_multiples",
                        ("nasdaq",),
                    )
                },
                standard_params={
                    "series_name": series_name,
                    "start_date": start_date,
                    "end_date": end_date,
                    "transform": transform,
                    "collapse": collapse,
                },
                extra_params=kwargs,
            )
        )