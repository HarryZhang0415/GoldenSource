### THIS FILE IS AUTO-GENERATED. DO NOT EDIT. ###

from datamart_core.app.static.container import Container
from datamart_core.app.model.obbject import OBBject
from datamart_core.app.model.custom_parameter import DataMartCustomParameter
from typing import Optional, Literal
from typing_extensions import Annotated
from datamart_core.app.static.utils.decorators import exception_handler, validate

from datamart_core.app.static.utils.filters import filter_inputs


class ROUTER_equity_darkpool(Container):
    """/equity/darkpool
    otc
    """

    def __repr__(self) -> str:
        return self.__doc__ or ""

    @exception_handler
    @validate
    def otc(
        self,
        symbol: Annotated[
            Optional[str],
            DataMartCustomParameter(description="Symbol to get data for."),
        ] = None,
        provider: Annotated[
            Optional[Literal["finra"]],
            DataMartCustomParameter(
                description="The provider to use for the query, by default None.\n    If None, the provider specified in defaults is selected or 'finra' if there is\n    no default."
            ),
        ] = None,
        **kwargs
    ) -> OBBject:
        """Get the weekly aggregate trade data for Over The Counter deals.

        ATS and non-ATS trading data for each ATS/firm
        with trade reporting obligations under FINRA rules.

        Parameters
        ----------
        symbol : Optional[str]
            Symbol to get data for.
        provider : Optional[Literal['finra']]
            The provider to use for the query, by default None.
            If None, the provider specified in defaults is selected or 'finra' if there is
            no default.
        tier : Literal['T1', 'T2', 'OTCE']
            "T1 - Securities included in the S&P 500, Russell 1000 and selected exchange-traded products;
                T2 - All other NMS stocks; OTC - Over-the-Counter equity securities (provider: finra)
        is_ats : bool
            ATS data if true, NON-ATS otherwise (provider: finra)

        Returns
        -------
        OBBject
            results : List[OTCAggregate]
                Serializable results.
            provider : Optional[Literal['finra']]
                Provider name.
            warnings : Optional[List[Warning_]]
                List of warnings.
            chart : Optional[Chart]
                Chart object.
            extra : Dict[str, Any]
                Extra info.

        OTCAggregate
        ------------
        update_date : date
            Most recent date on which total trades is updated based on data received from each ATS/OTC.
        share_quantity : float
            Aggregate weekly total number of shares reported by each ATS for the Symbol.
        trade_quantity : float
            Aggregate weekly total number of trades reported by each ATS for the Symbol

        Examples
        --------
        >>> from datamart import market
        >>> market.equity.darkpool.otc(provider='finra')
        >>> # Get OTC data for a symbol
        >>> market.equity.darkpool.otc(symbol='AAPL', provider='finra')
        """  # noqa: E501

        return self._run(
            "/equity/darkpool/otc",
            **filter_inputs(
                provider_choices={
                    "provider": self._get_provider(
                        provider,
                        "/equity/darkpool/otc",
                        ("finra",),
                    )
                },
                standard_params={
                    "symbol": symbol,
                },
                extra_params=kwargs,
            )
        )
