"""TMX Provider Module."""

from datamart_core.provider.abstract.provider import Provider
from datamart_tmx.models.available_indices import TmxAvailableIndicesFetcher
from datamart_tmx.models.bond_prices import TmxBondPricesFetcher
from datamart_tmx.models.calendar_earnings import TmxCalendarEarningsFetcher
from datamart_tmx.models.company_filings import TmxCompanyFilingsFetcher
from datamart_tmx.models.company_news import TmxCompanyNewsFetcher
from datamart_tmx.models.equity_historical import TmxEquityHistoricalFetcher
from datamart_tmx.models.equity_profile import TmxEquityProfileFetcher
from datamart_tmx.models.equity_quote import TmxEquityQuoteFetcher
from datamart_tmx.models.equity_search import TmxEquitySearchFetcher
from datamart_tmx.models.etf_countries import TmxEtfCountriesFetcher
from datamart_tmx.models.etf_holdings import TmxEtfHoldingsFetcher
from datamart_tmx.models.etf_info import TmxEtfInfoFetcher
from datamart_tmx.models.etf_search import TmxEtfSearchFetcher
from datamart_tmx.models.etf_sectors import TmxEtfSectorsFetcher
from datamart_tmx.models.gainers import TmxGainersFetcher
from datamart_tmx.models.historical_dividends import TmxHistoricalDividendsFetcher
from datamart_tmx.models.index_constituents import TmxIndexConstituentsFetcher
from datamart_tmx.models.index_sectors import TmxIndexSectorsFetcher
from datamart_tmx.models.index_snapshots import TmxIndexSnapshotsFetcher
from datamart_tmx.models.insider_trading import TmxInsiderTradingFetcher
from datamart_tmx.models.options_chains import TmxOptionsChainsFetcher
from datamart_tmx.models.price_target_consensus import TmxPriceTargetConsensusFetcher
from datamart_tmx.models.treasury_prices import TmxTreasuryPricesFetcher

tmx_provider = Provider(
    name="tmx",
    website="https://www.tmx.com/",
    description="""Unofficial TMX Data Provider Extension
        TMX Group Companies
         - Toronto Stock Exchange
         - TSX Venture Exchange
         - TSX Trust
         - Montréal Exchange
         - TSX Alpha Exchange
         - Shorcan
         - CDCC
         - CDS
         - TMX Datalinx
         - Trayport
    """,
    fetcher_dict={
        "AvailableIndices": TmxAvailableIndicesFetcher,
        "BondPrices": TmxBondPricesFetcher,
        "CalendarEarnings": TmxCalendarEarningsFetcher,
        "CompanyFilings": TmxCompanyFilingsFetcher,
        "CompanyNews": TmxCompanyNewsFetcher,
        "EquityHistorical": TmxEquityHistoricalFetcher,
        "EquityInfo": TmxEquityProfileFetcher,
        "EquityQuote": TmxEquityQuoteFetcher,
        "EquitySearch": TmxEquitySearchFetcher,
        "EtfSearch": TmxEtfSearchFetcher,
        "EtfHoldings": TmxEtfHoldingsFetcher,
        "EtfSectors": TmxEtfSectorsFetcher,
        "EtfCountries": TmxEtfCountriesFetcher,
        "EtfHistorical": TmxEquityHistoricalFetcher,
        "EtfInfo": TmxEtfInfoFetcher,
        "EquityGainers": TmxGainersFetcher,
        "HistoricalDividends": TmxHistoricalDividendsFetcher,
        "IndexConstituents": TmxIndexConstituentsFetcher,
        "IndexSectors": TmxIndexSectorsFetcher,
        "IndexSnapshots": TmxIndexSnapshotsFetcher,
        "InsiderTrading": TmxInsiderTradingFetcher,
        "OptionsChains": TmxOptionsChainsFetcher,
        "PriceTargetConsensus": TmxPriceTargetConsensusFetcher,
        "TreasuryPrices": TmxTreasuryPricesFetcher,
    },
)
