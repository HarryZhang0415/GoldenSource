"""Yahoo Finance provider module."""

from datamart_core.provider.abstract.provider import Provider
from datamart_yfinance.models.active import YFActiveFetcher
from datamart_yfinance.models.aggressive_small_caps import YFAggressiveSmallCapsFetcher
from datamart_yfinance.models.available_indices import YFinanceAvailableIndicesFetcher
from datamart_yfinance.models.balance_sheet import YFinanceBalanceSheetFetcher
from datamart_yfinance.models.cash_flow import YFinanceCashFlowStatementFetcher
from datamart_yfinance.models.company_news import YFinanceCompanyNewsFetcher
from datamart_yfinance.models.crypto_historical import YFinanceCryptoHistoricalFetcher
from datamart_yfinance.models.currency_historical import YFinanceCurrencyHistoricalFetcher
from datamart_yfinance.models.equity_historical import YFinanceEquityHistoricalFetcher
from datamart_yfinance.models.equity_profile import YFinanceEquityProfileFetcher
from datamart_yfinance.models.equity_quote import YFinanceEquityQuoteFetcher
from datamart_yfinance.models.etf_info import YFinanceEtfInfoFetcher
from datamart_yfinance.models.futures_curve import YFinanceFuturesCurveFetcher
from datamart_yfinance.models.futures_historical import YFinanceFuturesHistoricalFetcher
from datamart_yfinance.models.gainers import YFGainersFetcher
from datamart_yfinance.models.growth_tech_equities import YFGrowthTechEquitiesFetcher
from datamart_yfinance.models.historical_dividends import (
    YFinanceHistoricalDividendsFetcher,
)
from datamart_yfinance.models.income_statement import YFinanceIncomeStatementFetcher
from datamart_yfinance.models.index_historical import (
    YFinanceIndexHistoricalFetcher,
)
from datamart_yfinance.models.key_executives import YFinanceKeyExecutivesFetcher
from datamart_yfinance.models.key_metrics import YFinanceKeyMetricsFetcher
from datamart_yfinance.models.losers import YFLosersFetcher
from datamart_yfinance.models.price_target_consensus import (
    YFinancePriceTargetConsensusFetcher,
)
from datamart_yfinance.models.share_statistics import YFinanceShareStatisticsFetcher
from datamart_yfinance.models.undervalued_growth_equities import (
    YFUndervaluedGrowthEquitiesFetcher,
)
from datamart_yfinance.models.undervalued_large_caps import YFUndervaluedLargeCapsFetcher

yfinance_provider = Provider(
    name="yfinance",
    website="https://finance.yahoo.com/",
    description="""Yahoo! Finance is a web-based platform that offers financial news,
    data, and tools for investors and individuals interested in tracking and analyzing
    financial markets and assets.""",
    fetcher_dict={
        "AvailableIndices": YFinanceAvailableIndicesFetcher,
        "BalanceSheet": YFinanceBalanceSheetFetcher,
        "CashFlowStatement": YFinanceCashFlowStatementFetcher,
        "CompanyNews": YFinanceCompanyNewsFetcher,
        "CryptoHistorical": YFinanceCryptoHistoricalFetcher,
        "CurrencyHistorical": YFinanceCurrencyHistoricalFetcher,
        "EquityActive": YFActiveFetcher,
        "EquityAggressiveSmallCaps": YFAggressiveSmallCapsFetcher,
        "EquityGainers": YFGainersFetcher,
        "EquityHistorical": YFinanceEquityHistoricalFetcher,
        "EquityInfo": YFinanceEquityProfileFetcher,
        "EquityLosers": YFLosersFetcher,
        "EquityQuote": YFinanceEquityQuoteFetcher,
        "EquityUndervaluedGrowth": YFUndervaluedGrowthEquitiesFetcher,
        "EquityUndervaluedLargeCaps": YFUndervaluedLargeCapsFetcher,
        "EtfHistorical": YFinanceEquityHistoricalFetcher,
        "EtfInfo": YFinanceEtfInfoFetcher,
        "FuturesCurve": YFinanceFuturesCurveFetcher,
        "FuturesHistorical": YFinanceFuturesHistoricalFetcher,
        "GrowthTechEquities": YFGrowthTechEquitiesFetcher,
        "HistoricalDividends": YFinanceHistoricalDividendsFetcher,
        "IncomeStatement": YFinanceIncomeStatementFetcher,
        "IndexHistorical": YFinanceIndexHistoricalFetcher,
        "KeyExecutives": YFinanceKeyExecutivesFetcher,
        "KeyMetrics": YFinanceKeyMetricsFetcher,
        "MarketIndices": YFinanceIndexHistoricalFetcher,
        "PriceTargetConsensus": YFinancePriceTargetConsensusFetcher,
        "ShareStatistics": YFinanceShareStatisticsFetcher,
    },
)
