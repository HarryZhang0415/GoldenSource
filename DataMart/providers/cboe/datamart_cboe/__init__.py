"""Cboe provider module."""

from datamart_cboe.models.available_indices import CboeAvailableIndicesFetcher
from datamart_cboe.models.equity_historical import CboeEquityHistoricalFetcher
from datamart_cboe.models.equity_quote import CboeEquityQuoteFetcher
from datamart_cboe.models.equity_search import CboeEquitySearchFetcher
from datamart_cboe.models.futures_curve import CboeFuturesCurveFetcher
from datamart_cboe.models.index_constituents import (
    CboeIndexConstituentsFetcher,
)
from datamart_cboe.models.index_historical import (
    CboeIndexHistoricalFetcher,
)
from datamart_cboe.models.index_search import CboeIndexSearchFetcher
from datamart_cboe.models.index_snapshots import CboeIndexSnapshotsFetcher
from datamart_cboe.models.options_chains import CboeOptionsChainsFetcher
from datamart_core.provider.abstract.provider import Provider

cboe_provider = Provider(
    name="cboe",
    website="https://www.cboe.com/",
    description="""Cboe is the world's go-to derivatives and exchange network,
    delivering cutting-edge trading, clearing and investment solutions to people
    around the world.""",
    credentials=None,
    fetcher_dict={
        "AvailableIndices": CboeAvailableIndicesFetcher,
        "EquityHistorical": CboeEquityHistoricalFetcher,
        "EquityQuote": CboeEquityQuoteFetcher,
        "EquitySearch": CboeEquitySearchFetcher,
        "EtfHistorical": CboeEquityHistoricalFetcher,
        "IndexConstituents": CboeIndexConstituentsFetcher,
        "FuturesCurve": CboeFuturesCurveFetcher,
        "IndexHistorical": CboeIndexHistoricalFetcher,
        "IndexSearch": CboeIndexSearchFetcher,
        "IndexSnapshots": CboeIndexSnapshotsFetcher,
        "MarketIndices": CboeIndexHistoricalFetcher,
        "OptionsChains": CboeOptionsChainsFetcher,
    },
)
