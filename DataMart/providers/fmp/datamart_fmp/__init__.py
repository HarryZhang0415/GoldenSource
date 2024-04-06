"""FMP Provider Modules."""

from datamart_core.provider.abstract.provider import Provider
from datamart_fmp.models.analyst_estimates import FMPAnalystEstimatesFetcher
from datamart_fmp.models.available_indices import FMPAvailableIndicesFetcher
from datamart_fmp.models.balance_sheet import FMPBalanceSheetFetcher
from datamart_fmp.models.balance_sheet_growth import FMPBalanceSheetGrowthFetcher
from datamart_fmp.models.calendar_dividend import FMPCalendarDividendFetcher
from datamart_fmp.models.calendar_earnings import FMPCalendarEarningsFetcher
from datamart_fmp.models.calendar_splits import FMPCalendarSplitsFetcher
from datamart_fmp.models.cash_flow import FMPCashFlowStatementFetcher
from datamart_fmp.models.cash_flow_growth import FMPCashFlowStatementGrowthFetcher
from datamart_fmp.models.company_filings import FMPCompanyFilingsFetcher
from datamart_fmp.models.company_news import FMPCompanyNewsFetcher
from datamart_fmp.models.company_overview import FMPCompanyOverviewFetcher
from datamart_fmp.models.crypto_historical import FMPCryptoHistoricalFetcher
from datamart_fmp.models.crypto_search import FMPCryptoSearchFetcher
from datamart_fmp.models.currency_historical import FMPCurrencyHistoricalFetcher
from datamart_fmp.models.currency_pairs import FMPCurrencyPairsFetcher
from datamart_fmp.models.currency_snapshots import FMPCurrencySnapshotsFetcher
from datamart_fmp.models.discovery_filings import FMPDiscoveryFilingsFetcher
from datamart_fmp.models.earnings_call_transcript import FMPEarningsCallTranscriptFetcher
from datamart_fmp.models.economic_calendar import FMPEconomicCalendarFetcher
from datamart_fmp.models.equity_historical import FMPEquityHistoricalFetcher
from datamart_fmp.models.equity_ownership import FMPEquityOwnershipFetcher
from datamart_fmp.models.equity_peers import FMPEquityPeersFetcher
from datamart_fmp.models.equity_profile import FMPEquityProfileFetcher
from datamart_fmp.models.equity_quote import FMPEquityQuoteFetcher
from datamart_fmp.models.equity_screener import FMPEquityScreenerFetcher
from datamart_fmp.models.equity_valuation_multiples import (
    FMPEquityValuationMultiplesFetcher,
)
from datamart_fmp.models.etf_countries import FMPEtfCountriesFetcher
from datamart_fmp.models.etf_equity_exposure import FMPEtfEquityExposureFetcher
from datamart_fmp.models.etf_holdings import FMPEtfHoldingsFetcher
from datamart_fmp.models.etf_holdings_date import FMPEtfHoldingsDateFetcher
from datamart_fmp.models.etf_holdings_performance import FMPEtfHoldingsPerformanceFetcher
from datamart_fmp.models.etf_info import FMPEtfInfoFetcher
from datamart_fmp.models.etf_search import FMPEtfSearchFetcher
from datamart_fmp.models.etf_sectors import FMPEtfSectorsFetcher
from datamart_fmp.models.executive_compensation import FMPExecutiveCompensationFetcher
from datamart_fmp.models.financial_ratios import FMPFinancialRatiosFetcher
from datamart_fmp.models.historical_dividends import FMPHistoricalDividendsFetcher
from datamart_fmp.models.historical_employees import FMPHistoricalEmployeesFetcher
from datamart_fmp.models.historical_eps import FMPHistoricalEpsFetcher
from datamart_fmp.models.historical_splits import FMPHistoricalSplitsFetcher
from datamart_fmp.models.income_statement import FMPIncomeStatementFetcher
from datamart_fmp.models.income_statement_growth import FMPIncomeStatementGrowthFetcher
from datamart_fmp.models.index_constituents import FMPIndexConstituentsFetcher
from datamart_fmp.models.index_historical import FMPIndexHistoricalFetcher
from datamart_fmp.models.insider_trading import FMPInsiderTradingFetcher
from datamart_fmp.models.institutional_ownership import FMPInstitutionalOwnershipFetcher
from datamart_fmp.models.key_executives import FMPKeyExecutivesFetcher
from datamart_fmp.models.key_metrics import FMPKeyMetricsFetcher
from datamart_fmp.models.market_snapshots import FMPMarketSnapshotsFetcher
from datamart_fmp.models.price_performance import FMPPricePerformanceFetcher
from datamart_fmp.models.price_target import FMPPriceTargetFetcher
from datamart_fmp.models.price_target_consensus import FMPPriceTargetConsensusFetcher
from datamart_fmp.models.revenue_business_line import FMPRevenueBusinessLineFetcher
from datamart_fmp.models.revenue_geographic import FMPRevenueGeographicFetcher
from datamart_fmp.models.risk_premium import FMPRiskPremiumFetcher
from datamart_fmp.models.share_statistics import FMPShareStatisticsFetcher
from datamart_fmp.models.treasury_rates import FMPTreasuryRatesFetcher
from datamart_fmp.models.world_news import FMPWorldNewsFetcher

fmp_provider = Provider(
    name="fmp",
    website="https://financialmodelingprep.com/",
    description="""Financial Modeling Prep is a new concept that informs you about
    stock market information (news, currencies, and stock prices).""",
    credentials=["api_key"],
    fetcher_dict={
        "AnalystEstimates": FMPAnalystEstimatesFetcher,
        "AvailableIndices": FMPAvailableIndicesFetcher,
        "BalanceSheet": FMPBalanceSheetFetcher,
        "BalanceSheetGrowth": FMPBalanceSheetGrowthFetcher,
        "CalendarDividend": FMPCalendarDividendFetcher,
        "CalendarEarnings": FMPCalendarEarningsFetcher,
        "CalendarSplits": FMPCalendarSplitsFetcher,
        "CashFlowStatement": FMPCashFlowStatementFetcher,
        "CashFlowStatementGrowth": FMPCashFlowStatementGrowthFetcher,
        "CompanyFilings": FMPCompanyFilingsFetcher,
        "CompanyNews": FMPCompanyNewsFetcher,
        "CompanyOverview": FMPCompanyOverviewFetcher,
        "CryptoHistorical": FMPCryptoHistoricalFetcher,
        "CryptoSearch": FMPCryptoSearchFetcher,
        "CurrencyHistorical": FMPCurrencyHistoricalFetcher,
        "CurrencyPairs": FMPCurrencyPairsFetcher,
        "CurrencySnapshots": FMPCurrencySnapshotsFetcher,
        "DiscoveryFilings": FMPDiscoveryFilingsFetcher,
        "EarningsCallTranscript": FMPEarningsCallTranscriptFetcher,
        "EconomicCalendar": FMPEconomicCalendarFetcher,
        "EquityHistorical": FMPEquityHistoricalFetcher,
        "EquityOwnership": FMPEquityOwnershipFetcher,
        "EquityPeers": FMPEquityPeersFetcher,
        "EquityInfo": FMPEquityProfileFetcher,
        "EquityQuote": FMPEquityQuoteFetcher,
        "EquityScreener": FMPEquityScreenerFetcher,
        "EquityValuationMultiples": FMPEquityValuationMultiplesFetcher,
        "EtfCountries": FMPEtfCountriesFetcher,
        "EtfEquityExposure": FMPEtfEquityExposureFetcher,
        "EtfHoldings": FMPEtfHoldingsFetcher,
        "EtfHoldingsDate": FMPEtfHoldingsDateFetcher,
        "EtfHoldingsPerformance": FMPEtfHoldingsPerformanceFetcher,
        "EtfInfo": FMPEtfInfoFetcher,
        "EtfPricePerformance": FMPPricePerformanceFetcher,
        "EtfSearch": FMPEtfSearchFetcher,
        "EtfSectors": FMPEtfSectorsFetcher,
        "ExecutiveCompensation": FMPExecutiveCompensationFetcher,
        "FinancialRatios": FMPFinancialRatiosFetcher,
        "HistoricalDividends": FMPHistoricalDividendsFetcher,
        "HistoricalEmployees": FMPHistoricalEmployeesFetcher,
        "HistoricalEps": FMPHistoricalEpsFetcher,
        "HistoricalSplits": FMPHistoricalSplitsFetcher,
        "IncomeStatement": FMPIncomeStatementFetcher,
        "IncomeStatementGrowth": FMPIncomeStatementGrowthFetcher,
        "IndexConstituents": FMPIndexConstituentsFetcher,
        "IndexHistorical": FMPIndexHistoricalFetcher,
        "InsiderTrading": FMPInsiderTradingFetcher,
        "InstitutionalOwnership": FMPInstitutionalOwnershipFetcher,
        "KeyExecutives": FMPKeyExecutivesFetcher,
        "KeyMetrics": FMPKeyMetricsFetcher,
        "MarketIndices": FMPIndexHistoricalFetcher,
        "MarketSnapshots": FMPMarketSnapshotsFetcher,
        "PricePerformance": FMPPricePerformanceFetcher,
        "PriceTarget": FMPPriceTargetFetcher,
        "PriceTargetConsensus": FMPPriceTargetConsensusFetcher,
        "RevenueBusinessLine": FMPRevenueBusinessLineFetcher,
        "RevenueGeographic": FMPRevenueGeographicFetcher,
        "RiskPremium": FMPRiskPremiumFetcher,
        "ShareStatistics": FMPShareStatisticsFetcher,
        "TreasuryRates": FMPTreasuryRatesFetcher,
        "WorldNews": FMPWorldNewsFetcher,
        "EtfHistorical": FMPEquityHistoricalFetcher,
    },
)
