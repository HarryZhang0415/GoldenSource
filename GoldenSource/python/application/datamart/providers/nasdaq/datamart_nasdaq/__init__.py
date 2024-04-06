"""Nasdaq provider module."""

from datamart_core.provider.abstract.provider import Provider
from datamart_nasdaq.models.calendar_dividend import NasdaqCalendarDividendFetcher
from datamart_nasdaq.models.calendar_earnings import NasdaqCalendarEarningsFetcher
from datamart_nasdaq.models.calendar_ipo import NasdaqCalendarIpoFetcher
from datamart_nasdaq.models.cot import NasdaqCotFetcher
from datamart_nasdaq.models.cot_search import NasdaqCotSearchFetcher
from datamart_nasdaq.models.economic_calendar import NasdaqEconomicCalendarFetcher
from datamart_nasdaq.models.equity_search import NasdaqEquitySearchFetcher
from datamart_nasdaq.models.historical_dividends import NasdaqHistoricalDividendsFetcher
from datamart_nasdaq.models.lbma_fixing import NasdaqLbmaFixingFetcher
from datamart_nasdaq.models.sp500_multiples import NasdaqSP500MultiplesFetcher
from datamart_nasdaq.models.top_retail import NasdaqTopRetailFetcher

nasdaq_provider = Provider(
    name="nasdaq",
    website="https://data.nasdaq.com",
    description="""Positioned at the nexus of technology and the capital markets, Nasdaq
provides premier platforms and services for global capital markets and beyond with
unmatched technology, insights and markets expertise.""",
    credentials=["api_key"],
    fetcher_dict={
        "CalendarDividend": NasdaqCalendarDividendFetcher,
        "CalendarEarnings": NasdaqCalendarEarningsFetcher,
        "CalendarIpo": NasdaqCalendarIpoFetcher,
        "COT": NasdaqCotFetcher,
        "COTSearch": NasdaqCotSearchFetcher,
        "EconomicCalendar": NasdaqEconomicCalendarFetcher,
        "EquitySearch": NasdaqEquitySearchFetcher,
        "HistoricalDividends": NasdaqHistoricalDividendsFetcher,
        "LbmaFixing": NasdaqLbmaFixingFetcher,
        "SP500Multiples": NasdaqSP500MultiplesFetcher,
        "TopRetail": NasdaqTopRetailFetcher,
    },
)
