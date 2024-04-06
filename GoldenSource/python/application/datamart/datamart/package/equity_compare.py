### THIS FILE IS AUTO-GENERATED. DO NOT EDIT. ###

from datamart_core.app.static.container import Container
from datamart_core.app.model.obbject import OBBject
from datamart_core.app.model.custom_parameter import DataMartCustomParameter
from typing import Optional, Literal
from typing_extensions import Annotated
from datamart_core.app.static.utils.decorators import exception_handler, validate

from datamart_core.app.static.utils.filters import filter_inputs


class ROUTER_equity_compare(Container):
    """/equity/compare
    peers
    """

    def __repr__(self) -> str:
        return self.__doc__ or ""

    @exception_handler
    @validate
    def peers(
        self,
        symbol: Annotated[
            str, DataMartCustomParameter(description="Symbol to get data for.")
        ],
        provider: Annotated[
            Optional[Literal["fmp"]],
            DataMartCustomParameter(
                description="The provider to use for the query, by default None.\n    If None, the provider specified in defaults is selected or 'fmp' if there is\n    no default."
            ),
        ] = None,
        **kwargs
    ) -> OBBject:
        """Get the closest peers for a given company.

        Peers consist of companies trading on the same exchange, operating within the same sector
        and with comparable market capitalizations.

        Parameters
        ----------
        symbol : str
            Symbol to get data for.
        provider : Optional[Literal['fmp']]
            The provider to use for the query, by default None.
            If None, the provider specified in defaults is selected or 'fmp' if there is
            no default.

        Returns
        -------
        OBBject
            results : EquityPeers
                Serializable results.
            provider : Optional[Literal['fmp']]
                Provider name.
            warnings : Optional[List[Warning_]]
                List of warnings.
            chart : Optional[Chart]
                Chart object.
            extra : Dict[str, Any]
                Extra info.

        EquityPeers
        -----------
        peers_list : List[str]
            A list of equity peers based on sector, exchange and market cap.

        Examples
        --------
        >>> from datamart import market
        >>> market.equity.compare.peers(symbol='AAPL', provider='fmp')
        """  # noqa: E501

        return self._run(
            "/equity/compare/peers",
            **filter_inputs(
                provider_choices={
                    "provider": self._get_provider(
                        provider,
                        "/equity/compare/peers",
                        ("fmp",),
                    )
                },
                standard_params={
                    "symbol": symbol,
                },
                extra_params=kwargs,
            )
        )
