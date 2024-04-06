### THIS FILE IS AUTO-GENERATED. DO NOT EDIT. ###

from datamart_core.app.static.container import Container
from datamart_core.app.model.obbject import OBBject
from datamart_core.app.model.custom_parameter import DataMartCustomParameter
from typing import List, Union, Optional, Literal
from typing_extensions import Annotated
from datamart_core.app.static.utils.decorators import exception_handler, validate

from datamart_core.app.static.utils.filters import filter_inputs


class ROUTER_currency(Container):
    """/currency
    /price
    reference_rates
    search
    snapshots
    """

    def __repr__(self) -> str:
        return self.__doc__ or ""

    @property
    def price(self):
        # pylint: disable=import-outside-toplevel
        from . import currency_price

        return currency_price.ROUTER_currency_price(command_runner=self._command_runner)

    @exception_handler
    @validate
    def reference_rates(
        self,
        provider: Annotated[
            Optional[Literal["ecb"]],
            DataMartCustomParameter(
                description="The provider to use for the query, by default None.\n    If None, the provider specified in defaults is selected or 'ecb' if there is\n    no default."
            ),
        ] = None,
        **kwargs
    ) -> OBBject:
        """Current, official, currency reference rates.

        Foreign exchange reference rates are the exchange rates set by a major financial institution or regulatory body,
        serving as a benchmark for the value of currencies around the world.
        These rates are used as a standard to facilitate international trade and financial transactions,
        ensuring consistency and reliability in currency conversion.
        They are typically updated on a daily basis and reflect the market conditions at a specific time.
        Central banks and financial institutions often use these rates to guide their own exchange rates,
        impacting global trade, loans, and investments.


        Parameters
        ----------
        provider : Optional[Literal['ecb']]
            The provider to use for the query, by default None.
            If None, the provider specified in defaults is selected or 'ecb' if there is
            no default.

        Returns
        -------
        OBBject
            results : CurrencyReferenceRates
                Serializable results.
            provider : Optional[Literal['ecb']]
                Provider name.
            warnings : Optional[List[Warning_]]
                List of warnings.
            chart : Optional[Chart]
                Chart object.
            extra : Dict[str, Any]
                Extra info.

        CurrencyReferenceRates
        ----------------------
        date : date
            The date of the data.
        EUR : Optional[float]
            Euro.
        USD : Optional[float]
            US Dollar.
        JPY : Optional[float]
            Japanese Yen.
        BGN : Optional[float]
            Bulgarian Lev.
        CZK : Optional[float]
            Czech Koruna.
        DKK : Optional[float]
            Danish Krone.
        GBP : Optional[float]
            Pound Sterling.
        HUF : Optional[float]
            Hungarian Forint.
        PLN : Optional[float]
            Polish Zloty.
        RON : Optional[float]
            Romanian Leu.
        SEK : Optional[float]
            Swedish Krona.
        CHF : Optional[float]
            Swiss Franc.
        ISK : Optional[float]
            Icelandic Krona.
        NOK : Optional[float]
            Norwegian Krone.
        TRY : Optional[float]
            Turkish Lira.
        AUD : Optional[float]
            Australian Dollar.
        BRL : Optional[float]
            Brazilian Real.
        CAD : Optional[float]
            Canadian Dollar.
        CNY : Optional[float]
            Chinese Yuan.
        HKD : Optional[float]
            Hong Kong Dollar.
        IDR : Optional[float]
            Indonesian Rupiah.
        ILS : Optional[float]
            Israeli Shekel.
        INR : Optional[float]
            Indian Rupee.
        KRW : Optional[float]
            South Korean Won.
        MXN : Optional[float]
            Mexican Peso.
        MYR : Optional[float]
            Malaysian Ringgit.
        NZD : Optional[float]
            New Zealand Dollar.
        PHP : Optional[float]
            Philippine Peso.
        SGD : Optional[float]
            Singapore Dollar.
        THB : Optional[float]
            Thai Baht.
        ZAR : Optional[float]
            South African Rand.

        Examples
        --------
        >>> from datamart import market
        >>> market.currency.reference_rates(provider='ecb')
        """  # noqa: E501

        return self._run(
            "/currency/reference_rates",
            **filter_inputs(
                provider_choices={
                    "provider": self._get_provider(
                        provider,
                        "/currency/reference_rates",
                        ("ecb",),
                    )
                },
                standard_params={},
                extra_params=kwargs,
            )
        )

    @exception_handler
    @validate
    def search(
        self,
        provider: Annotated[
            Optional[Literal["fmp", "intrinio", "polygon"]],
            DataMartCustomParameter(
                description="The provider to use for the query, by default None.\n    If None, the provider specified in defaults is selected or 'fmp' if there is\n    no default."
            ),
        ] = None,
        **kwargs
    ) -> OBBject:
        """Currency Search.

        Search available currency pairs.
        Currency pairs are the national currencies from two countries coupled for trading on
        the foreign exchange (FX) marketplace.
        Both currencies will have exchange rates on which the trade will have its position basis.
        All trading within the forex market, whether selling, buying, or trading, will take place through currency pairs.
        (ref: Investopedia)
        Major currency pairs include pairs such as EUR/USD, USD/JPY, GBP/USD, etc.


        Parameters
        ----------
        provider : Optional[Literal['fmp', 'intrinio', 'polygon']]
            The provider to use for the query, by default None.
            If None, the provider specified in defaults is selected or 'fmp' if there is
            no default.
        symbol : Optional[str]
            Symbol of the pair to search. (provider: polygon)
        date : Optional[datetime.date]
            A specific date to get data for. (provider: polygon)
        search : Optional[str]
            Search for terms within the ticker and/or company name. (provider: polygon)
        active : Optional[bool]
            Specify if the tickers returned should be actively traded on the queried date. (provider: polygon)
        order : Optional[Literal['asc', 'desc']]
            Order data by ascending or descending. (provider: polygon)
        sort : Optional[Literal['ticker', 'name', 'market', 'locale', 'currency_symbol', 'currency_name', 'base_currency_symbol', 'base_currency_name', 'last_updated_utc', 'delisted_utc']]
            Sort field used for ordering. (provider: polygon)
        limit : Optional[Annotated[int, Gt(gt=0)]]
            The number of data entries to return. (provider: polygon)

        Returns
        -------
        OBBject
            results : List[CurrencyPairs]
                Serializable results.
            provider : Optional[Literal['fmp', 'intrinio', 'polygon']]
                Provider name.
            warnings : Optional[List[Warning_]]
                List of warnings.
            chart : Optional[Chart]
                Chart object.
            extra : Dict[str, Any]
                Extra info.

        CurrencyPairs
        -------------
        name : str
            Name of the currency pair.
        symbol : Optional[str]
            Symbol of the currency pair. (provider: fmp)
        currency : Optional[str]
            Base currency of the currency pair. (provider: fmp)
        stock_exchange : Optional[str]
            Stock exchange of the currency pair. (provider: fmp)
        exchange_short_name : Optional[str]
            Short name of the stock exchange of the currency pair. (provider: fmp)
        code : Optional[str]
            Code of the currency pair. (provider: intrinio)
        base_currency : Optional[str]
            ISO 4217 currency code of the base currency. (provider: intrinio)
        quote_currency : Optional[str]
            ISO 4217 currency code of the quote currency. (provider: intrinio)
        market : Optional[str]
            Name of the trading market. Always 'fx'. (provider: polygon)
        locale : Optional[str]
            Locale of the currency pair. (provider: polygon)
        currency_symbol : Optional[str]
            The symbol of the quote currency. (provider: polygon)
        currency_name : Optional[str]
            Name of the quote currency. (provider: polygon)
        base_currency_symbol : Optional[str]
            The symbol of the base currency. (provider: polygon)
        base_currency_name : Optional[str]
            Name of the base currency. (provider: polygon)
        last_updated_utc : Optional[datetime]
            The last updated timestamp in UTC. (provider: polygon)
        delisted_utc : Optional[datetime]
            The delisted timestamp in UTC. (provider: polygon)

        Examples
        --------
        >>> from datamart import market
        >>> market.currency.search(provider='intrinio')
        >>> # Search for 'EURUSD' currency pair using 'intrinio' as provider.
        >>> market.currency.search(provider='intrinio', symbol='EURUSD')
        >>> # Search for actively traded currency pairs on the queried date using 'polygon' as provider.
        >>> market.currency.search(provider='polygon', date='2024-01-02', active=True)
        >>> # Search for terms  using 'polygon' as provider.
        >>> market.currency.search(provider='polygon', search='Euro zone')
        """  # noqa: E501

        return self._run(
            "/currency/search",
            **filter_inputs(
                provider_choices={
                    "provider": self._get_provider(
                        provider,
                        "/currency/search",
                        ("fmp", "intrinio", "polygon"),
                    )
                },
                standard_params={},
                extra_params=kwargs,
            )
        )

    @exception_handler
    @validate
    def snapshots(
        self,
        base: Annotated[
            Union[str, List[str]],
            DataMartCustomParameter(
                description="The base currency symbol. Multiple comma separated items allowed for provider(s): fmp."
            ),
        ] = "usd",
        quote_type: Annotated[
            Literal["direct", "indirect"],
            DataMartCustomParameter(
                description="Whether the quote is direct or indirect. Selecting 'direct' will return the exchange rate as the amount of domestic currency required to buy one unit of the foreign currency. Selecting 'indirect' (default) will return the exchange rate as the amount of foreign currency required to buy one unit of the domestic currency."
            ),
        ] = "indirect",
        counter_currencies: Annotated[
            Union[str, List[str], None],
            DataMartCustomParameter(
                description="An optional list of counter currency symbols to filter for. None returns all."
            ),
        ] = None,
        provider: Annotated[
            Optional[Literal["fmp"]],
            DataMartCustomParameter(
                description="The provider to use for the query, by default None.\n    If None, the provider specified in defaults is selected or 'fmp' if there is\n    no default."
            ),
        ] = None,
        **kwargs
    ) -> OBBject:
        """Snapshots of currency exchange rates from an indirect or direct perspective of a base currency.

        Parameters
        ----------
        base : Union[str, List[str]]
            The base currency symbol. Multiple comma separated items allowed for provider(s): fmp.
        quote_type : Literal['direct', 'indirect']
            Whether the quote is direct or indirect. Selecting 'direct' will return the exchange rate as the amount of domestic currency required to buy one unit of the foreign currency. Selecting 'indirect' (default) will return the exchange rate as the amount of foreign currency required to buy one unit of the domestic currency.
        counter_currencies : Union[str, List[str], None]
            An optional list of counter currency symbols to filter for. None returns all.
        provider : Optional[Literal['fmp']]
            The provider to use for the query, by default None.
            If None, the provider specified in defaults is selected or 'fmp' if there is
            no default.

        Returns
        -------
        OBBject
            results : List[CurrencySnapshots]
                Serializable results.
            provider : Optional[Literal['fmp']]
                Provider name.
            warnings : Optional[List[Warning_]]
                List of warnings.
            chart : Optional[Chart]
                Chart object.
            extra : Dict[str, Any]
                Extra info.

        CurrencySnapshots
        -----------------
        base_currency : str
            The base, or domestic, currency.
        counter_currency : str
            The counter, or foreign, currency.
        last_rate : float
            The exchange rate, relative to the base currency. Rates are expressed as the amount of foreign currency received from selling one unit of the base currency, or the quantity of foreign currency required to purchase one unit of the domestic currency. To inverse the perspective, set the 'quote_type' parameter as 'direct'.
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
            The change in the price from the previous close. (provider: fmp)
        change_percent : Optional[float]
            The change in the price from the previous close, as a normalized percent. (provider: fmp)
        ma50 : Optional[float]
            The 50-day moving average. (provider: fmp)
        ma200 : Optional[float]
            The 200-day moving average. (provider: fmp)
        year_high : Optional[float]
            The 52-week high. (provider: fmp)
        year_low : Optional[float]
            The 52-week low. (provider: fmp)
        last_rate_timestamp : Optional[datetime]
            The timestamp of the last rate. (provider: fmp)

        Examples
        --------
        >>> from datamart import market
        >>> market.currency.snapshots(provider='fmp')
        >>> # Get exchange rates from USD and XAU to EUR, JPY, and GBP using 'fmp' as provider.
        >>> market.currency.snapshots(provider='fmp', base='USD,XAU', counter_currencies='EUR,JPY,GBP', quote_type='indirect')
        """  # noqa: E501

        return self._run(
            "/currency/snapshots",
            **filter_inputs(
                provider_choices={
                    "provider": self._get_provider(
                        provider,
                        "/currency/snapshots",
                        ("fmp",),
                    )
                },
                standard_params={
                    "base": base,
                    "quote_type": quote_type,
                    "counter_currencies": counter_currencies,
                },
                extra_params=kwargs,
                info={"base": {"multiple_items_allowed": ["fmp"]}},
            )
        )