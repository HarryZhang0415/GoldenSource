### THIS FILE IS AUTO-GENERATED. DO NOT EDIT. ###

from datamart_core.app.static.container import Container
from datamart_core.app.model.obbject import OBBject
from datamart_core.app.model.custom_parameter import DataMartCustomParameter
import datetime
from typing import Union, Optional, Literal
from typing_extensions import Annotated
from datamart_core.app.static.utils.decorators import exception_handler, validate

from datamart_core.app.static.utils.filters import filter_inputs


class ROUTER_economy_gdp(Container):
    """/economy/gdp
    forecast
    nominal
    real
    """

    def __repr__(self) -> str:
        return self.__doc__ or ""

    @exception_handler
    @validate
    def forecast(
        self,
        period: Annotated[
            Literal["quarter", "annual"],
            DataMartCustomParameter(
                description="Time period of the data to return. Units for nominal GDP period. Either quarter or annual."
            ),
        ] = "annual",
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
        type: Annotated[
            Literal["nominal", "real"],
            DataMartCustomParameter(
                description="Type of GDP to get forecast of. Either nominal or real."
            ),
        ] = "real",
        provider: Annotated[
            Optional[Literal["oecd"]],
            DataMartCustomParameter(
                description="The provider to use for the query, by default None.\n    If None, the provider specified in defaults is selected or 'oecd' if there is\n    no default."
            ),
        ] = None,
        **kwargs
    ) -> OBBject:
        """Forecasted GDP Data.

        Parameters
        ----------
        period : Literal['quarter', 'annual']
            Time period of the data to return. Units for nominal GDP period. Either quarter or annual.
        start_date : Union[datetime.date, None, str]
            Start date of the data, in YYYY-MM-DD format.
        end_date : Union[datetime.date, None, str]
            End date of the data, in YYYY-MM-DD format.
        type : Literal['nominal', 'real']
            Type of GDP to get forecast of. Either nominal or real.
        provider : Optional[Literal['oecd']]
            The provider to use for the query, by default None.
            If None, the provider specified in defaults is selected or 'oecd' if there is
            no default.
        country : Literal['argentina', 'asia', 'australia', 'austria', 'belgium', 'brazil', 'bulgaria', 'canada', 'chile', 'china', 'colombia', 'costa_rica', 'croatia', 'czech_republic', 'denmark', 'estonia', 'euro_area_17', 'finland', 'france', 'germany', 'greece', 'hungary', 'iceland', 'india', 'indonesia', 'ireland', 'israel', 'italy', 'japan', 'korea', 'latvia', 'lithuania', 'luxembourg', 'mexico', 'netherlands', 'new_zealand', 'non-oecd', 'norway', 'oecd_total', 'peru', 'poland', 'portugal', 'romania', 'russia', 'slovak_republic', 'slovenia', 'south_africa', 'spain', 'sweden', 'switzerland', 'turkey', 'united_kingdom', 'united_states', 'world']
            Country to get GDP for. (provider: oecd)

        Returns
        -------
        OBBject
            results : List[GdpForecast]
                Serializable results.
            provider : Optional[Literal['oecd']]
                Provider name.
            warnings : Optional[List[Warning_]]
                List of warnings.
            chart : Optional[Chart]
                Chart object.
            extra : Dict[str, Any]
                Extra info.

        GdpForecast
        -----------
        date : Optional[date]
            The date of the data.
        value : Optional[float]
            Nominal GDP value on the date.

        Examples
        --------
        >>> from datamart import market
        >>> market.economy.gdp.forecast(provider='oecd')
        >>> market.economy.gdp.forecast(period='annual', type='real', provider='oecd')
        """  # noqa: E501

        return self._run(
            "/economy/gdp/forecast",
            **filter_inputs(
                provider_choices={
                    "provider": self._get_provider(
                        provider,
                        "/economy/gdp/forecast",
                        ("oecd",),
                    )
                },
                standard_params={
                    "period": period,
                    "start_date": start_date,
                    "end_date": end_date,
                    "type": type,
                },
                extra_params=kwargs,
            )
        )

    @exception_handler
    @validate
    def nominal(
        self,
        units: Annotated[
            Literal["usd", "usd_cap"],
            DataMartCustomParameter(
                description="The unit of measurement for the data. Units to get nominal GDP in. Either usd or usd_cap indicating per capita."
            ),
        ] = "usd",
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
        provider: Annotated[
            Optional[Literal["oecd"]],
            DataMartCustomParameter(
                description="The provider to use for the query, by default None.\n    If None, the provider specified in defaults is selected or 'oecd' if there is\n    no default."
            ),
        ] = None,
        **kwargs
    ) -> OBBject:
        """Nominal GDP Data.

        Parameters
        ----------
        units : Literal['usd', 'usd_cap']
            The unit of measurement for the data. Units to get nominal GDP in. Either usd or usd_cap indicating per capita.
        start_date : Union[datetime.date, None, str]
            Start date of the data, in YYYY-MM-DD format.
        end_date : Union[datetime.date, None, str]
            End date of the data, in YYYY-MM-DD format.
        provider : Optional[Literal['oecd']]
            The provider to use for the query, by default None.
            If None, the provider specified in defaults is selected or 'oecd' if there is
            no default.
        country : Literal['australia', 'austria', 'belgium', 'brazil', 'canada', 'chile', 'colombia', 'costa_rica', 'czech_republic', 'denmark', 'estonia', 'euro_area', 'european_union', 'finland', 'france', 'germany', 'greece', 'hungary', 'iceland', 'indonesia', 'ireland', 'israel', 'italy', 'japan', 'korea', 'latvia', 'lithuania', 'luxembourg', 'mexico', 'netherlands', 'new_zealand', 'norway', 'poland', 'portugal', 'russia', 'slovak_republic', 'slovenia', 'south_africa', 'spain', 'sweden', 'switzerland', 'turkey', 'united_kingdom', 'united_states', 'all']
            Country to get GDP for. (provider: oecd)

        Returns
        -------
        OBBject
            results : List[GdpNominal]
                Serializable results.
            provider : Optional[Literal['oecd']]
                Provider name.
            warnings : Optional[List[Warning_]]
                List of warnings.
            chart : Optional[Chart]
                Chart object.
            extra : Dict[str, Any]
                Extra info.

        GdpNominal
        ----------
        date : Optional[date]
            The date of the data.
        value : Optional[float]
            Nominal GDP value on the date.

        Examples
        --------
        >>> from datamart import market
        >>> market.economy.gdp.nominal(provider='oecd')
        >>> market.economy.gdp.nominal(units='usd', provider='oecd')
        """  # noqa: E501

        return self._run(
            "/economy/gdp/nominal",
            **filter_inputs(
                provider_choices={
                    "provider": self._get_provider(
                        provider,
                        "/economy/gdp/nominal",
                        ("oecd",),
                    )
                },
                standard_params={
                    "units": units,
                    "start_date": start_date,
                    "end_date": end_date,
                },
                extra_params=kwargs,
            )
        )

    @exception_handler
    @validate
    def real(
        self,
        units: Annotated[
            Literal["idx", "qoq", "yoy"],
            DataMartCustomParameter(
                description="The unit of measurement for the data. Either idx (indicating 2015=100), qoq (previous period) or yoy (same period, previous year).)"
            ),
        ] = "yoy",
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
        provider: Annotated[
            Optional[Literal["oecd"]],
            DataMartCustomParameter(
                description="The provider to use for the query, by default None.\n    If None, the provider specified in defaults is selected or 'oecd' if there is\n    no default."
            ),
        ] = None,
        **kwargs
    ) -> OBBject:
        """Real GDP Data.

        Parameters
        ----------
        units : Literal['idx', 'qoq', 'yoy']
            The unit of measurement for the data. Either idx (indicating 2015=100), qoq (previous period) or yoy (same period, previous year).)
        start_date : Union[datetime.date, None, str]
            Start date of the data, in YYYY-MM-DD format.
        end_date : Union[datetime.date, None, str]
            End date of the data, in YYYY-MM-DD format.
        provider : Optional[Literal['oecd']]
            The provider to use for the query, by default None.
            If None, the provider specified in defaults is selected or 'oecd' if there is
            no default.
        country : Literal['G20', 'G7', 'argentina', 'australia', 'austria', 'belgium', 'brazil', 'bulgaria', 'canada', 'chile', 'china', 'colombia', 'costa_rica', 'croatia', 'czech_republic', 'denmark', 'estonia', 'euro_area_19', 'europe', 'european_union_27', 'finland', 'france', 'germany', 'greece', 'hungary', 'iceland', 'india', 'indonesia', 'ireland', 'israel', 'italy', 'japan', 'korea', 'latvia', 'lithuania', 'luxembourg', 'mexico', 'netherlands', 'new_zealand', 'norway', 'oecd_total', 'poland', 'portugal', 'romania', 'russia', 'saudi_arabia', 'slovak_republic', 'slovenia', 'south_africa', 'spain', 'sweden', 'switzerland', 'turkey', 'united_kingdom', 'united_states', 'all']
            Country to get GDP for. (provider: oecd)

        Returns
        -------
        OBBject
            results : List[GdpReal]
                Serializable results.
            provider : Optional[Literal['oecd']]
                Provider name.
            warnings : Optional[List[Warning_]]
                List of warnings.
            chart : Optional[Chart]
                Chart object.
            extra : Dict[str, Any]
                Extra info.

        GdpReal
        -------
        date : Optional[date]
            The date of the data.
        value : Optional[float]
            Nominal GDP value on the date.

        Examples
        --------
        >>> from datamart import market
        >>> market.economy.gdp.real(provider='oecd')
        >>> market.economy.gdp.real(units='yoy', provider='oecd')
        """  # noqa: E501

        return self._run(
            "/economy/gdp/real",
            **filter_inputs(
                provider_choices={
                    "provider": self._get_provider(
                        provider,
                        "/economy/gdp/real",
                        ("oecd",),
                    )
                },
                standard_params={
                    "units": units,
                    "start_date": start_date,
                    "end_date": end_date,
                },
                extra_params=kwargs,
            )
        )