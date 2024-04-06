"""Tiingo provider module."""

from datamart_core.provider.abstract.provider import Provider
from datamart_tiingo.models.company_news import TiingoCompanyNewsFetcher
from datamart_tiingo.models.crypto_historical import TiingoCryptoHistoricalFetcher
from datamart_tiingo.models.currency_historical import TiingoCurrencyHistoricalFetcher
from datamart_tiingo.models.equity_historical import TiingoEquityHistoricalFetcher
from datamart_tiingo.models.trailing_dividend_yield import TiingoTrailingDivYieldFetcher
from datamart_tiingo.models.world_news import TiingoWorldNewsFetcher

tiingo_provider = Provider(
    name="tiingo",
    website="https://tiingo.com/",
    description="""""",
    credentials=["token"],
    fetcher_dict={
        "EquityHistorical": TiingoEquityHistoricalFetcher,
        "EtfHistorical": TiingoEquityHistoricalFetcher,
        "CompanyNews": TiingoCompanyNewsFetcher,
        "WorldNews": TiingoWorldNewsFetcher,
        "CryptoHistorical": TiingoCryptoHistoricalFetcher,
        "CurrencyHistorical": TiingoCurrencyHistoricalFetcher,
        "TrailingDividendYield": TiingoTrailingDivYieldFetcher,
    },
)
