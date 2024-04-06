### THIS FILE IS AUTO-GENERATED. DO NOT EDIT. ###

from datamart_core.app.static.container import Container
from datamart_core.app.model.obbject import OBBject
from datamart_core.app.model.custom_parameter import (
    DataMartCustomParameter,
    DataMartCustomChoices,
)
import datetime
from typing import List, Union, Optional, Literal
from typing_extensions import Annotated
from datamart_core.app.static.utils.decorators import exception_handler, validate

from datamart_core.app.static.utils.filters import filter_inputs


class ROUTER_fixedincome_corporate(Container):
    """/fixedincome/corporate
    bond_prices
    commercial_paper
    hqm
    ice_bofa
    moody
    spot_rates
    """

    def __repr__(self) -> str:
        return self.__doc__ or ""

    @exception_handler
    @validate
    def bond_prices(
        self,
        country: Annotated[
            Optional[str],
            DataMartCustomParameter(
                description="The country to get data. Matches partial name."
            ),
        ] = None,
        issuer_name: Annotated[
            Optional[str],
            DataMartCustomParameter(
                description="Name of the issuer.  Returns partial matches and is case insensitive."
            ),
        ] = None,
        isin: Annotated[
            Union[List, str, None],
            DataMartCustomParameter(
                description="International Securities Identification Number(s) of the bond(s)."
            ),
        ] = None,
        lei: Annotated[
            Optional[str],
            DataMartCustomParameter(
                description="Legal Entity Identifier of the issuing entity."
            ),
        ] = None,
        currency: Annotated[
            Union[List, str, None],
            DataMartCustomParameter(
                description="Currency of the bond. Formatted as the 3-letter ISO 4217 code (e.g. GBP, EUR, USD)."
            ),
        ] = None,
        coupon_min: Annotated[
            Optional[float],
            DataMartCustomParameter(description="Minimum coupon rate of the bond."),
        ] = None,
        coupon_max: Annotated[
            Optional[float],
            DataMartCustomParameter(description="Maximum coupon rate of the bond."),
        ] = None,
        issued_amount_min: Annotated[
            Optional[int],
            DataMartCustomParameter(description="Minimum issued amount of the bond."),
        ] = None,
        issued_amount_max: Annotated[
            Optional[str],
            DataMartCustomParameter(description="Maximum issued amount of the bond."),
        ] = None,
        maturity_date_min: Annotated[
            Optional[datetime.date],
            DataMartCustomParameter(description="Minimum maturity date of the bond."),
        ] = None,
        maturity_date_max: Annotated[
            Optional[datetime.date],
            DataMartCustomParameter(description="Maximum maturity date of the bond."),
        ] = None,
        provider: Annotated[
            Optional[Literal["tmx"]],
            DataMartCustomParameter(
                description="The provider to use for the query, by default None.\n    If None, the provider specified in defaults is selected or 'tmx' if there is\n    no default."
            ),
        ] = None,
        **kwargs
    ) -> OBBject:
        """Corporate Bond Prices.

        Parameters
        ----------
        country : Optional[str]
            The country to get data. Matches partial name.
        issuer_name : Optional[str]
            Name of the issuer.  Returns partial matches and is case insensitive.
        isin : Union[List, str, None]
            International Securities Identification Number(s) of the bond(s).
        lei : Optional[str]
            Legal Entity Identifier of the issuing entity.
        currency : Union[List, str, None]
            Currency of the bond. Formatted as the 3-letter ISO 4217 code (e.g. GBP, EUR, USD).
        coupon_min : Optional[float]
            Minimum coupon rate of the bond.
        coupon_max : Optional[float]
            Maximum coupon rate of the bond.
        issued_amount_min : Optional[int]
            Minimum issued amount of the bond.
        issued_amount_max : Optional[str]
            Maximum issued amount of the bond.
        maturity_date_min : Optional[datetime.date]
            Minimum maturity date of the bond.
        maturity_date_max : Optional[datetime.date]
            Maximum maturity date of the bond.
        provider : Optional[Literal['tmx']]
            The provider to use for the query, by default None.
            If None, the provider specified in defaults is selected or 'tmx' if there is
            no default.
        issue_date_min : Optional[datetime.date]
            Filter by the minimum original issue date. (provider: tmx)
        issue_date_max : Optional[datetime.date]
            Filter by the maximum original issue date. (provider: tmx)
        last_traded_min : Optional[datetime.date]
            Filter by the minimum last trade date. (provider: tmx)
        use_cache : bool
            All bond data is sourced from a single JSON file that is updated daily. The file is cached for one day to eliminate downloading more than once. Caching will significantly speed up subsequent queries. To bypass, set to False. (provider: tmx)

        Returns
        -------
        OBBject
            results : List[BondPrices]
                Serializable results.
            provider : Optional[Literal['tmx']]
                Provider name.
            warnings : Optional[List[Warning_]]
                List of warnings.
            chart : Optional[Chart]
                Chart object.
            extra : Dict[str, Any]
                Extra info.

        BondPrices
        ----------
        isin : Optional[str]
            International Securities Identification Number of the bond.
        lei : Optional[str]
            Legal Entity Identifier of the issuing entity.
        figi : Optional[str]
            FIGI of the bond.
        cusip : Optional[str]
            CUSIP of the bond.
        coupon_rate : Optional[float]
            Coupon rate of the bond.
        ytm : Optional[float]
            Yield to maturity (YTM) is the rate of return anticipated on a bond if it is held until the maturity date. It takes into account the current market price, par value, coupon rate and time to maturity. It is assumed that all coupons are reinvested at the same rate. Values are returned as a normalized percent. (provider: tmx)
        price : Optional[float]
            The last price for the bond. (provider: tmx)
        highest_price : Optional[float]
            The highest price for the bond on the last traded date. (provider: tmx)
        lowest_price : Optional[float]
            The lowest price for the bond on the last traded date. (provider: tmx)
        total_trades : Optional[int]
            Total number of trades on the last traded date. (provider: tmx)
        last_traded_date : Optional[date]
            Last traded date of the bond. (provider: tmx)
        maturity_date : Optional[date]
            Maturity date of the bond. (provider: tmx)
        issue_date : Optional[date]
            Issue date of the bond. This is the date when the bond first accrues interest. (provider: tmx)
        issuer_name : Optional[str]
            Name of the issuing entity. (provider: tmx)

        Examples
        --------
        >>> from datamart import market
        >>> market.fixedincome.corporate.bond_prices(provider='tmx')
        """  # noqa: E501

        return self._run(
            "/fixedincome/corporate/bond_prices",
            **filter_inputs(
                provider_choices={
                    "provider": self._get_provider(
                        provider,
                        "/fixedincome/corporate/bond_prices",
                        ("tmx",),
                    )
                },
                standard_params={
                    "country": country,
                    "issuer_name": issuer_name,
                    "isin": isin,
                    "lei": lei,
                    "currency": currency,
                    "coupon_min": coupon_min,
                    "coupon_max": coupon_max,
                    "issued_amount_min": issued_amount_min,
                    "issued_amount_max": issued_amount_max,
                    "maturity_date_min": maturity_date_min,
                    "maturity_date_max": maturity_date_max,
                },
                extra_params=kwargs,
            )
        )

    @exception_handler
    @validate
    def commercial_paper(
        self,
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
        maturity: Annotated[
            Literal["overnight", "7d", "15d", "30d", "60d", "90d"],
            DataMartCustomParameter(description="The maturity."),
        ] = "30d",
        category: Annotated[
            Literal["asset_backed", "financial", "nonfinancial"],
            DataMartCustomParameter(description="The category."),
        ] = "financial",
        grade: Annotated[
            Literal["aa", "a2_p2"], DataMartCustomParameter(description="The grade.")
        ] = "aa",
        provider: Annotated[
            Optional[Literal["fred"]],
            DataMartCustomParameter(
                description="The provider to use for the query, by default None.\n    If None, the provider specified in defaults is selected or 'fred' if there is\n    no default."
            ),
        ] = None,
        **kwargs
    ) -> OBBject:
        """Commercial Paper.

        Commercial paper (CP) consists of short-term, promissory notes issued primarily by corporations.
        Maturities range up to 270 days but average about 30 days.
        Many companies use CP to raise cash needed for current transactions,
        and many find it to be a lower-cost alternative to bank loans.


        Parameters
        ----------
        start_date : Union[datetime.date, None, str]
            Start date of the data, in YYYY-MM-DD format.
        end_date : Union[datetime.date, None, str]
            End date of the data, in YYYY-MM-DD format.
        maturity : Literal['overnight', '7d', '15d', '30d', '60d', '90d']
            The maturity.
        category : Literal['asset_backed', 'financial', 'nonfinancial']
            The category.
        grade : Literal['aa', 'a2_p2']
            The grade.
        provider : Optional[Literal['fred']]
            The provider to use for the query, by default None.
            If None, the provider specified in defaults is selected or 'fred' if there is
            no default.

        Returns
        -------
        OBBject
            results : List[CommercialPaper]
                Serializable results.
            provider : Optional[Literal['fred']]
                Provider name.
            warnings : Optional[List[Warning_]]
                List of warnings.
            chart : Optional[Chart]
                Chart object.
            extra : Dict[str, Any]
                Extra info.

        CommercialPaper
        ---------------
        date : date
            The date of the data.
        rate : Optional[float]
            Commercial Paper Rate.

        Examples
        --------
        >>> from datamart import market
        >>> market.fixedincome.corporate.commercial_paper(provider='fred')
        >>> market.fixedincome.corporate.commercial_paper(maturity='15d', provider='fred')
        """  # noqa: E501

        return self._run(
            "/fixedincome/corporate/commercial_paper",
            **filter_inputs(
                provider_choices={
                    "provider": self._get_provider(
                        provider,
                        "/fixedincome/corporate/commercial_paper",
                        ("fred",),
                    )
                },
                standard_params={
                    "start_date": start_date,
                    "end_date": end_date,
                    "maturity": maturity,
                    "category": category,
                    "grade": grade,
                },
                extra_params=kwargs,
            )
        )

    @exception_handler
    @validate
    def hqm(
        self,
        date: Annotated[
            Union[datetime.date, None, str],
            DataMartCustomParameter(description="A specific date to get data for."),
        ] = None,
        yield_curve: Annotated[
            Literal["spot", "par"],
            DataMartCustomParameter(description="The yield curve type."),
        ] = "spot",
        provider: Annotated[
            Optional[Literal["fred"]],
            DataMartCustomParameter(
                description="The provider to use for the query, by default None.\n    If None, the provider specified in defaults is selected or 'fred' if there is\n    no default."
            ),
        ] = None,
        **kwargs
    ) -> OBBject:
        """High Quality Market Corporate Bond.

        The HQM yield curve represents the high quality corporate bond market, i.e.,
        corporate bonds rated AAA, AA, or A.  The HQM curve contains two regression terms.
        These terms are adjustment factors that blend AAA, AA, and A bonds into a single HQM yield curve
        that is the market-weighted average (MWA) quality of high quality bonds.


        Parameters
        ----------
        date : Union[datetime.date, None, str]
            A specific date to get data for.
        yield_curve : Literal['spot', 'par']
            The yield curve type.
        provider : Optional[Literal['fred']]
            The provider to use for the query, by default None.
            If None, the provider specified in defaults is selected or 'fred' if there is
            no default.

        Returns
        -------
        OBBject
            results : List[HighQualityMarketCorporateBond]
                Serializable results.
            provider : Optional[Literal['fred']]
                Provider name.
            warnings : Optional[List[Warning_]]
                List of warnings.
            chart : Optional[Chart]
                Chart object.
            extra : Dict[str, Any]
                Extra info.

        HighQualityMarketCorporateBond
        ------------------------------
        date : date
            The date of the data.
        rate : Optional[float]
            HighQualityMarketCorporateBond Rate.
        maturity : str
            Maturity.
        yield_curve : Literal['spot', 'par']
            The yield curve type.
        series_id : Optional[str]
            FRED series id. (provider: fred)

        Examples
        --------
        >>> from datamart import market
        >>> market.fixedincome.corporate.hqm(provider='fred')
        >>> market.fixedincome.corporate.hqm(yield_curve='par', provider='fred')
        """  # noqa: E501

        return self._run(
            "/fixedincome/corporate/hqm",
            **filter_inputs(
                provider_choices={
                    "provider": self._get_provider(
                        provider,
                        "/fixedincome/corporate/hqm",
                        ("fred",),
                    )
                },
                standard_params={
                    "date": date,
                    "yield_curve": yield_curve,
                },
                extra_params=kwargs,
            )
        )

    @exception_handler
    @validate
    def ice_bofa(
        self,
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
        index_type: Annotated[
            Literal["yield", "yield_to_worst", "total_return", "spread"],
            DataMartCustomParameter(description="The type of series."),
        ] = "yield",
        provider: Annotated[
            Optional[Literal["fred"]],
            DataMartCustomParameter(
                description="The provider to use for the query, by default None.\n    If None, the provider specified in defaults is selected or 'fred' if there is\n    no default."
            ),
        ] = None,
        **kwargs
    ) -> OBBject:
        """ICE BofA US Corporate Bond Indices.

        The ICE BofA US Corporate Index tracks the performance of US dollar denominated investment grade corporate debt
        publicly issued in the US domestic market. Qualifying securities must have an investment grade rating (based on an
        average of Moody’s, S&P and Fitch), at least 18 months to final maturity at the time of issuance, at least one year
        remaining term to final maturity as of the rebalance date, a fixed coupon schedule and a minimum amount
        outstanding of $250 million. The ICE BofA US Corporate Index is a component of the US Corporate Master Index.


        Parameters
        ----------
        start_date : Union[datetime.date, None, str]
            Start date of the data, in YYYY-MM-DD format.
        end_date : Union[datetime.date, None, str]
            End date of the data, in YYYY-MM-DD format.
        index_type : Literal['yield', 'yield_to_worst', 'total_return', 'spread']
            The type of series.
        provider : Optional[Literal['fred']]
            The provider to use for the query, by default None.
            If None, the provider specified in defaults is selected or 'fred' if there is
            no default.
        category : Literal['all', 'duration', 'eur', 'usd']
            The type of category. (provider: fred)
        area : Literal['asia', 'emea', 'eu', 'ex_g10', 'latin_america', 'us']
            The type of area. (provider: fred)
        grade : Literal['a', 'aa', 'aaa', 'b', 'bb', 'bbb', 'ccc', 'crossover', 'high_grade', 'high_yield', 'non_financial', 'non_sovereign', 'private_sector', 'public_sector']
            The type of grade. (provider: fred)
        options : bool
            Whether to include options in the results. (provider: fred)

        Returns
        -------
        OBBject
            results : List[ICEBofA]
                Serializable results.
            provider : Optional[Literal['fred']]
                Provider name.
            warnings : Optional[List[Warning_]]
                List of warnings.
            chart : Optional[Chart]
                Chart object.
            extra : Dict[str, Any]
                Extra info.

        ICEBofA
        -------
        date : date
            The date of the data.
        rate : Optional[float]
            ICE BofA US Corporate Bond Indices Rate.

        Examples
        --------
        >>> from datamart import market
        >>> market.fixedincome.corporate.ice_bofa(provider='fred')
        >>> market.fixedincome.corporate.ice_bofa(index_type='yield_to_worst', provider='fred')
        """  # noqa: E501

        return self._run(
            "/fixedincome/corporate/ice_bofa",
            **filter_inputs(
                provider_choices={
                    "provider": self._get_provider(
                        provider,
                        "/fixedincome/corporate/ice_bofa",
                        ("fred",),
                    )
                },
                standard_params={
                    "start_date": start_date,
                    "end_date": end_date,
                    "index_type": index_type,
                },
                extra_params=kwargs,
            )
        )

    @exception_handler
    @validate
    def moody(
        self,
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
        index_type: Annotated[
            Literal["aaa", "baa"],
            DataMartCustomParameter(description="The type of series."),
        ] = "aaa",
        provider: Annotated[
            Optional[Literal["fred"]],
            DataMartCustomParameter(
                description="The provider to use for the query, by default None.\n    If None, the provider specified in defaults is selected or 'fred' if there is\n    no default."
            ),
        ] = None,
        **kwargs
    ) -> OBBject:
        """Moody Corporate Bond Index.

        Moody's Aaa and Baa are investment bonds that acts as an index of
        the performance of all bonds given an Aaa or Baa rating by Moody's Investors Service respectively.
        These corporate bonds often are used in macroeconomics as an alternative to the federal ten-year
        Treasury Bill as an indicator of the interest rate.


        Parameters
        ----------
        start_date : Union[datetime.date, None, str]
            Start date of the data, in YYYY-MM-DD format.
        end_date : Union[datetime.date, None, str]
            End date of the data, in YYYY-MM-DD format.
        index_type : Literal['aaa', 'baa']
            The type of series.
        provider : Optional[Literal['fred']]
            The provider to use for the query, by default None.
            If None, the provider specified in defaults is selected or 'fred' if there is
            no default.
        spread : Optional[Literal['treasury', 'fed_funds']]
            The type of spread. (provider: fred)

        Returns
        -------
        OBBject
            results : List[MoodyCorporateBondIndex]
                Serializable results.
            provider : Optional[Literal['fred']]
                Provider name.
            warnings : Optional[List[Warning_]]
                List of warnings.
            chart : Optional[Chart]
                Chart object.
            extra : Dict[str, Any]
                Extra info.

        MoodyCorporateBondIndex
        -----------------------
        date : date
            The date of the data.
        rate : Optional[float]
            Moody Corporate Bond Index Rate.

        Examples
        --------
        >>> from datamart import market
        >>> market.fixedincome.corporate.moody(provider='fred')
        >>> market.fixedincome.corporate.moody(index_type='baa', provider='fred')
        """  # noqa: E501

        return self._run(
            "/fixedincome/corporate/moody",
            **filter_inputs(
                provider_choices={
                    "provider": self._get_provider(
                        provider,
                        "/fixedincome/corporate/moody",
                        ("fred",),
                    )
                },
                standard_params={
                    "start_date": start_date,
                    "end_date": end_date,
                    "index_type": index_type,
                },
                extra_params=kwargs,
            )
        )

    @exception_handler
    @validate
    def spot_rates(
        self,
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
        maturity: Annotated[
            Union[float, str, List[Union[float, str]]],
            DataMartCustomParameter(
                description="Maturities in years. Multiple comma separated items allowed for provider(s): fred."
            ),
        ] = 10.0,
        category: Annotated[
            Union[str, List[str]],
            DataMartCustomParameter(
                description="Rate category. Options: spot_rate, par_yield. Multiple comma separated items allowed for provider(s): fred."
            ),
            DataMartCustomChoices(choices=["par_yield", "spot_rate"]),
        ] = "spot_rate",
        provider: Annotated[
            Optional[Literal["fred"]],
            DataMartCustomParameter(
                description="The provider to use for the query, by default None.\n    If None, the provider specified in defaults is selected or 'fred' if there is\n    no default."
            ),
        ] = None,
        **kwargs
    ) -> OBBject:
        """Spot Rates.

        The spot rates for any maturity is the yield on a bond that provides a single payment at that maturity.
        This is a zero coupon bond.
        Because each spot rate pertains to a single cashflow, it is the relevant interest rate
        concept for discounting a pension liability at the same maturity.


        Parameters
        ----------
        start_date : Union[datetime.date, None, str]
            Start date of the data, in YYYY-MM-DD format.
        end_date : Union[datetime.date, None, str]
            End date of the data, in YYYY-MM-DD format.
        maturity : Union[float, str, List[Union[float, str]]]
            Maturities in years. Multiple comma separated items allowed for provider(s): fred.
        category : Union[str, List[str]]
            Rate category. Options: spot_rate, par_yield. Multiple comma separated items allowed for provider(s): fred.
        provider : Optional[Literal['fred']]
            The provider to use for the query, by default None.
            If None, the provider specified in defaults is selected or 'fred' if there is
            no default.

        Returns
        -------
        OBBject
            results : List[SpotRate]
                Serializable results.
            provider : Optional[Literal['fred']]
                Provider name.
            warnings : Optional[List[Warning_]]
                List of warnings.
            chart : Optional[Chart]
                Chart object.
            extra : Dict[str, Any]
                Extra info.

        SpotRate
        --------
        date : date
            The date of the data.
        rate : Optional[float]
            Spot Rate.

        Examples
        --------
        >>> from datamart import market
        >>> market.fixedincome.corporate.spot_rates(provider='fred')
        >>> market.fixedincome.corporate.spot_rates(maturity='10,20,30,50', provider='fred')
        """  # noqa: E501

        return self._run(
            "/fixedincome/corporate/spot_rates",
            **filter_inputs(
                provider_choices={
                    "provider": self._get_provider(
                        provider,
                        "/fixedincome/corporate/spot_rates",
                        ("fred",),
                    )
                },
                standard_params={
                    "start_date": start_date,
                    "end_date": end_date,
                    "maturity": maturity,
                    "category": category,
                },
                extra_params=kwargs,
                info={
                    "maturity": {"multiple_items_allowed": ["fred"]},
                    "category": {"multiple_items_allowed": ["fred"]},
                },
            )
        )