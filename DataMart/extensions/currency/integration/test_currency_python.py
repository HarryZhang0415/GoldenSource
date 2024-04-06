"""Test currency extension."""

import pytest
from extensions.tests.conftest import parametrize
from datamart_core.app.model.obbject import OBBject

# pylint: disable=redefined-outer-name
# pylint: disable=inconsistent-return-statements


@pytest.fixture(scope="session")
def market(pytestconfig):
    """Fixture to setup market."""

    if pytestconfig.getoption("markexpr") != "not integration":
        import datamart  # pylint: disable=import-outside-toplevel

        return datamart.market


@parametrize(
    "params",
    [
        (
            {
                "provider": "polygon",
                "symbol": "USDJPY",
                "date": "2023-10-12",
                "search": "",
                "active": True,
                "order": "asc",
                "sort": "currency_name",
                "limit": 100,
            }
        ),
        (
            {
                "provider": "fmp",
            }
        ),
        (
            {
                "provider": "intrinio",
            }
        ),
    ],
)
@pytest.mark.integration
def test_currency_search(params, market):
    result = market.currency.search(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        (
            {
                "symbol": "EURUSD",
                "interval": "1d",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
                "provider": "fmp",
            }
        ),
        (
            {
                "interval": "1h",
                "provider": "fmp",
                "symbol": "EURUSD,USDJPY",
                "start_date": None,
                "end_date": None,
            }
        ),
        (
            {
                "interval": "1m",
                "sort": "desc",
                "limit": 49999,
                "provider": "polygon",
                "symbol": "EURUSD",
                "start_date": "2023-01-01",
                "end_date": "2023-01-10",
            }
        ),
        (
            {
                "interval": "1d",
                "sort": "desc",
                "limit": 49999,
                "provider": "polygon",
                "symbol": "EURUSD",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
            }
        ),
        (
            {
                "interval": "1d",
                "provider": "yfinance",
                "symbol": "EURUSD",
                "start_date": "2023-01-01",
                "end_date": "2023-01-10",
            }
        ),
        (
            {
                "interval": "1m",
                "provider": "yfinance",
                "symbol": "EURUSD",
                "start_date": None,
                "end_date": None,
            }
        ),
        (
            {
                "interval": "1h",
                "provider": "tiingo",
                "symbol": "EURUSD",
                "start_date": "2023-05-21",
                "end_date": "2023-06-06",
            }
        ),
        (
            {
                "interval": "1d",
                "provider": "tiingo",
                "symbol": "EURUSD",
                "start_date": "2023-05-21",
                "end_date": "2023-06-06",
            }
        ),
    ],
)
@pytest.mark.integration
def test_currency_price_historical(params, market):
    result = market.currency.price.historical(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [({"provider": "ecb"})],
)
@pytest.mark.integration
def test_currency_reference_rates(params, market):
    result = market.currency.reference_rates(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.model_dump()["results"].items()) > 0


@parametrize(
    "params",
    [
        (
            {
                "provider": "fmp",
                "base": "USD,XAU",
                "counter_currencies": "EUR,JPY,GBP",
                "quote_type": "indirect",
            }
        ),
    ],
)
@pytest.mark.integration
def test_currency_snapshots(params, market):
    result = market.currency.snapshots(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0
