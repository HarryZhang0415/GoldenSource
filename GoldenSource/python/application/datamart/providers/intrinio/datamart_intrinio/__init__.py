"""Intrinio Provider Modules."""

from datamart_core.provider.abstract.provider import Provider
from datamart_intrinio.models.balance_sheet import IntrinioBalanceSheetFetcher
from datamart_intrinio.models.calendar_ipo import IntrinioCalendarIpoFetcher
from datamart_intrinio.models.cash_flow import IntrinioCashFlowStatementFetcher
from datamart_intrinio.models.company_filings import IntrinioCompanyFilingsFetcher
from datamart_intrinio.models.company_news import IntrinioCompanyNewsFetcher
from datamart_intrinio.models.currency_pairs import IntrinioCurrencyPairsFetcher
from datamart_intrinio.models.equity_historical import IntrinioEquityHistoricalFetcher
from datamart_intrinio.models.equity_info import IntrinioEquityInfoFetcher
from datamart_intrinio.models.equity_quote import IntrinioEquityQuoteFetcher
from datamart_intrinio.models.equity_search import IntrinioEquitySearchFetcher
from datamart_intrinio.models.etf_holdings import IntrinioEtfHoldingsFetcher
from datamart_intrinio.models.etf_info import IntrinioEtfInfoFetcher
from datamart_intrinio.models.etf_price_performance import (
    IntrinioEtfPricePerformanceFetcher,
)
from datamart_intrinio.models.etf_search import IntrinioEtfSearchFetcher
from datamart_intrinio.models.financial_ratios import IntrinioFinancialRatiosFetcher
from datamart_intrinio.models.fred_series import IntrinioFredSeriesFetcher
from datamart_intrinio.models.historical_attributes import (
    IntrinioHistoricalAttributesFetcher,
)
from datamart_intrinio.models.historical_dividends import (
    IntrinioHistoricalDividendsFetcher,
)
from datamart_intrinio.models.income_statement import IntrinioIncomeStatementFetcher
from datamart_intrinio.models.index_historical import IntrinioIndexHistoricalFetcher
from datamart_intrinio.models.insider_trading import IntrinioInsiderTradingFetcher

# from datamart_intrinio.models.institutional_ownership import (
#     IntrinioInstitutionalOwnershipFetcher,
# )
from datamart_intrinio.models.key_metrics import IntrinioKeyMetricsFetcher
from datamart_intrinio.models.latest_attributes import IntrinioLatestAttributesFetcher
from datamart_intrinio.models.market_snapshots import IntrinioMarketSnapshotsFetcher
from datamart_intrinio.models.options_chains import IntrinioOptionsChainsFetcher
from datamart_intrinio.models.options_unusual import IntrinioOptionsUnusualFetcher
from datamart_intrinio.models.reported_financials import IntrinioReportedFinancialsFetcher
from datamart_intrinio.models.search_attributes import (
    IntrinioSearchAttributesFetcher,
)
from datamart_intrinio.models.share_statistics import IntrinioShareStatisticsFetcher
from datamart_intrinio.models.world_news import IntrinioWorldNewsFetcher

intrinio_provider = Provider(
    name="intrinio",
    website="https://intrinio.com/",
    description="""Intrinio is a financial data platform that provides real-time and
    historical financial market data to businesses and developers through an API.""",
    credentials=["api_key"],
    fetcher_dict={
        "BalanceSheet": IntrinioBalanceSheetFetcher,
        "CalendarIpo": IntrinioCalendarIpoFetcher,
        "CashFlowStatement": IntrinioCashFlowStatementFetcher,
        "CompanyFilings": IntrinioCompanyFilingsFetcher,
        "CompanyNews": IntrinioCompanyNewsFetcher,
        "CurrencyPairs": IntrinioCurrencyPairsFetcher,
        "EquityHistorical": IntrinioEquityHistoricalFetcher,
        "EquityInfo": IntrinioEquityInfoFetcher,
        "EquityQuote": IntrinioEquityQuoteFetcher,
        "EquitySearch": IntrinioEquitySearchFetcher,
        "EtfHistorical": IntrinioEquityHistoricalFetcher,
        "EtfHoldings": IntrinioEtfHoldingsFetcher,
        "EtfInfo": IntrinioEtfInfoFetcher,
        "EtfPricePerformance": IntrinioEtfPricePerformanceFetcher,
        "EtfSearch": IntrinioEtfSearchFetcher,
        "FinancialRatios": IntrinioFinancialRatiosFetcher,
        "FredSeries": IntrinioFredSeriesFetcher,
        "HistoricalAttributes": IntrinioHistoricalAttributesFetcher,
        "HistoricalDividends": IntrinioHistoricalDividendsFetcher,
        "IncomeStatement": IntrinioIncomeStatementFetcher,
        "IndexHistorical": IntrinioIndexHistoricalFetcher,
        "InsiderTrading": IntrinioInsiderTradingFetcher,
        # "InstitutionalOwnership": IntrinioInstitutionalOwnershipFetcher, # Disabled due to unreliable Intrinio endpoint
        "KeyMetrics": IntrinioKeyMetricsFetcher,
        "LatestAttributes": IntrinioLatestAttributesFetcher,
        "MarketIndices": IntrinioIndexHistoricalFetcher,
        "MarketSnapshots": IntrinioMarketSnapshotsFetcher,
        "OptionsChains": IntrinioOptionsChainsFetcher,
        "OptionsUnusual": IntrinioOptionsUnusualFetcher,
        "ReportedFinancials": IntrinioReportedFinancialsFetcher,
        "SearchAttributes": IntrinioSearchAttributesFetcher,
        "ShareStatistics": IntrinioShareStatisticsFetcher,
        "WorldNews": IntrinioWorldNewsFetcher,
    },
)
