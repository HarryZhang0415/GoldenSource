from datetime import date

import pytest
from datamart_core.app.service.user_service import UserService
from datamart_polygon.models.balance_sheet import PolygonBalanceSheetFetcher
from datamart_polygon.models.cash_flow import PolygonCashFlowStatementFetcher
from datamart_polygon.models.company_news import PolygonCompanyNewsFetcher
from datamart_polygon.models.crypto_historical import PolygonCryptoHistoricalFetcher
from datamart_polygon.models.currency_historical import PolygonCurrencyHistoricalFetcher
from datamart_polygon.models.currency_pairs import PolygonCurrencyPairsFetcher
from datamart_polygon.models.equity_historical import PolygonEquityHistoricalFetcher
from datamart_polygon.models.equity_nbbo import PolygonEquityNBBOFetcher
from datamart_polygon.models.income_statement import PolygonIncomeStatementFetcher
from datamart_polygon.models.index_historical import (
    PolygonIndexHistoricalFetcher,
)
from datamart_polygon.models.market_indices import (
    PolygonMarketIndicesFetcher,
)
from datamart_polygon.models.market_snapshots import PolygonMarketSnapshotsFetcher

test_credentials = UserService().default_user_settings.credentials.model_dump(
    mode="json"
)


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_headers": [("User-Agent", None)],
        "filter_query_parameters": [
            ("apiKey", "MOCK_API_KEY"),
        ],
    }


@pytest.mark.record_http
def test_polygon_equity_historical_fetcher(credentials=test_credentials):
    params = {
        "symbol": "AAPL",
        "start_date": date(2023, 1, 1),
        "end_date": date(2023, 1, 10),
        "interval": "1d",
    }

    fetcher = PolygonEquityHistoricalFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_polygon_market_indices_fetcher(credentials=test_credentials):
    params = {
        "symbol": "NDX",
        "start_date": date(2023, 1, 1),
        "end_date": date(2023, 5, 10),
    }

    fetcher = PolygonMarketIndicesFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_polygon_index_historical_fetcher(credentials=test_credentials):
    params = {
        "symbol": "NDX",
        "start_date": date(2023, 1, 1),
        "end_date": date(2023, 5, 10),
    }

    fetcher = PolygonIndexHistoricalFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_polygon_company_news_fetcher(credentials=test_credentials):
    params = {"symbol": "AAPL"}

    fetcher = PolygonCompanyNewsFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_polygon_balance_sheet_fetcher(credentials=test_credentials):
    params = {"symbol": "AAPL"}

    fetcher = PolygonBalanceSheetFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_polygon_income_statement_fetcher(credentials=test_credentials):
    params = {"symbol": "AAPL"}

    fetcher = PolygonIncomeStatementFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_polygon_cash_flow_statement_fetcher(credentials=test_credentials):
    params = {"symbol": "AAPL"}

    fetcher = PolygonCashFlowStatementFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_polygon_crypto_historical_fetcher(credentials=test_credentials):
    params = {
        "symbol": "BTCUSD",
        "start_date": date(2023, 1, 1),
        "end_date": date(2023, 1, 10),
    }

    fetcher = PolygonCryptoHistoricalFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_polygon_currency_historical_fetcher(credentials=test_credentials):
    params = {
        "symbol": "EURUSD",
        "start_date": date(2023, 1, 1),
        "end_date": date(2023, 1, 10),
    }

    fetcher = PolygonCurrencyHistoricalFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_polygon_currency_pairs_fetcher(credentials=test_credentials):
    params = {"date": date(2023, 1, 1)}

    fetcher = PolygonCurrencyPairsFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_polygon_equity_nbbo_fetcher(credentials=test_credentials):
    params = {"symbol": "SPY", "limit": 1000}

    fetcher = PolygonEquityNBBOFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_polygon_market_snapshots_fetcher(credentials=test_credentials):
    params = {}

    fetcher = PolygonMarketSnapshotsFetcher()
    result = fetcher.test(params, credentials)
    assert result is None
