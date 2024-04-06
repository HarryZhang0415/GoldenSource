"""Test economy extension."""

import pytest
from extensions.tests.conftest import parametrize
from datamart_core.app.model.obbject import OBBject


@pytest.fixture(scope="session")
def market(pytestconfig):  # pylint: disable=inconsistent-return-statements
    """Fixture to setup market."""

    if pytestconfig.getoption("markexpr") != "not integration":
        import datamart  # pylint: disable=import-outside-toplevel

        return datamart.market


# pylint: disable=redefined-outer-name


@parametrize(
    "params",
    [
        ({"symbol": "dowjones", "provider": "fmp"}),
        ({"symbol": "BUKBUS", "provider": "cboe"}),
        ({"symbol": "^TX60", "provider": "tmx", "use_cache": False}),
    ],
)
@pytest.mark.integration
def test_index_constituents(params, market):
    result = market.index.constituents(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        (
            {
                "interval": "1d",
                "provider": "cboe",
                "symbol": "AAVE100",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
                "use_cache": False,
            }
        ),
        (
            {
                "interval": "1d",
                "provider": "fmp",
                "symbol": "^DJI",
                "start_date": "2024-01-01",
                "end_date": "2024-02-05",
            }
        ),
        (
            {
                "interval": "1h",
                "provider": "fmp",
                "symbol": "^DJI,^NDX",
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
                "symbol": "NDX",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
            }
        ),
        (
            {
                "interval": "1d",
                "sort": "desc",
                "limit": 49999,
                "provider": "polygon",
                "symbol": "NDX",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
            }
        ),
        (
            {
                "interval": "1d",
                "provider": "yfinance",
                "symbol": "DJI",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
            }
        ),
        (
            {
                "interval": "1d",
                "provider": "intrinio",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
                "symbol": "DJI",
                "limit": 100,
            }
        ),
    ],
)
@pytest.mark.integration
def test_index_price_historical(params, market):
    result = market.index.price.historical(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        (
            {
                "interval": "1d",
                "provider": "cboe",
                "symbol": "AAVE100",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
                "use_cache": False,
            }
        ),
        (
            {
                "interval": "1d",
                "provider": "fmp",
                "symbol": "^DJI",
                "start_date": "2024-01-01",
                "end_date": "2024-02-05",
            }
        ),
        (
            {
                "interval": "1m",
                "sort": "desc",
                "limit": 49999,
                "provider": "polygon",
                "symbol": "NDX",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
            }
        ),
        (
            {
                "interval": "1d",
                "sort": "desc",
                "limit": 49999,
                "provider": "polygon",
                "symbol": "NDX",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
            }
        ),
        (
            {
                "interval": "1d",
                "provider": "yfinance",
                "symbol": "DJI",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
            }
        ),
        (
            {
                "interval": "1d",
                "provider": "intrinio",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
                "symbol": "DJI",
                "limit": 100,
            }
        ),
    ],
)
@pytest.mark.integration
@pytest.mark.skip(reason="Deprecating this endpoint")
def test_index_market(params, market):
    result = market.index.market(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        ({}),
        ({"provider": "cboe", "use_cache": False}),
        ({"provider": "fmp"}),
        ({"provider": "yfinance"}),
        ({"provider": "tmx", "use_cache": False}),
    ],
)
@pytest.mark.integration
def test_index_available(params, market):
    result = market.index.available(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        (
            {
                "query": "D",
                "is_symbol": True,
                "provider": "cboe",
                "use_cache": False,
            }
        ),
    ],
)
@pytest.mark.integration
def test_index_search(params, market):
    result = market.index.search(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        ({"region": "us", "provider": "cboe"}),
        ({"provider": "tmx", "region": "ca", "use_cache": False}),
    ],
)
@pytest.mark.integration
def test_index_snapshots(params, market):
    result = market.index.snapshots(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        (
            {
                "series_name": "pe_month",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
                "collapse": "monthly",
                "transform": "diff",
                "provider": "nasdaq",
            }
        ),
    ],
)
@pytest.mark.integration
def test_index_sp500_multiples(params, market):
    result = market.index.sp500_multiples(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        ({"symbol": "^TX60", "provider": "tmx"}),
    ],
)
@pytest.mark.integration
def test_index_sectors(params, market):
    result = market.index.sectors(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0
