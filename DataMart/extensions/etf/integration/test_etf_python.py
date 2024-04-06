"""Test etf extension."""

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
        ({"query": None, "provider": "fmp"}),
        (
            {
                "query": "vanguard",
                "provider": "tmx",
                "div_freq": "quarterly",
                "sort_by": "return_1y",
                "use_cache": False,
            }
        ),
        (
            {
                "query": "vanguard",
                "provider": "intrinio",
                "exchange": "arcx",
            }
        ),
    ],
)
@pytest.mark.integration
def test_etf_search(params, market):
    params = {p: v for p, v in params.items() if v}

    result = market.etf.search(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        (
            {
                "adjustment": "unadjusted",
                "extended_hours": True,
                "provider": "alpha_vantage",
                "symbol": "SPY",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
                "interval": "15m",
            }
        ),
        (
            {
                "provider": "cboe",
                "symbol": "SPY",
                "start_date": None,
                "end_date": None,
                "interval": "1m",
                "use_cache": False,
            }
        ),
        (
            {
                "provider": "cboe",
                "symbol": "SPY",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
                "interval": "1d",
                "use_cache": False,
            }
        ),
        (
            {
                "provider": "fmp",
                "symbol": "SPY",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
                "interval": "1d",
            }
        ),
        (
            {
                "timezone": "UTC",
                "source": "realtime",
                "start_time": None,
                "end_time": None,
                "provider": "intrinio",
                "symbol": "SPY",
                "start_date": "2023-06-01",
                "end_date": "2023-06-03",
                "interval": "1h",
            }
        ),
        (
            {
                "timezone": None,
                "source": "delayed",
                "start_time": None,
                "end_time": None,
                "provider": "intrinio",
                "symbol": "AAPL",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
                "interval": "1d",
            }
        ),
        (
            {
                "sort": "desc",
                "limit": "49999",
                "adjustment": "unadjusted",
                "provider": "polygon",
                "symbol": "SPY",
                "start_date": "2023-01-01",
                "end_date": "2023-01-03",
                "interval": "1m",
                "extended_hours": False,
            }
        ),
        (
            {
                "sort": "desc",
                "limit": "49999",
                "adjustment": "splits_only",
                "provider": "polygon",
                "symbol": "SPY",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
                "interval": "1d",
                "extended_hours": False,
            }
        ),
        (
            {
                "extended_hours": False,
                "include_actions": False,
                "adjustment": "splits_and_dividends",
                "provider": "yfinance",
                "symbol": "SPY",
                "start_date": "2023-06-01",
                "end_date": "2023-06-03",
                "interval": "1h",
                "adjusted": True,
                "prepost": False,
            }
        ),
        (
            {
                "extended_hours": False,
                "include_actions": True,
                "adjustment": "splits_only",
                "provider": "yfinance",
                "symbol": "SPY",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
                "interval": "1d",
                "adjusted": False,
                "prepost": False,
            }
        ),
        (
            {
                "provider": "tiingo",
                "symbol": "SPY",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
                "interval": "1d",
            }
        ),
        (
            {
                "provider": "tiingo",
                "symbol": "SPY",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
                "interval": "1M",
            }
        ),
        (
            {
                "provider": "tradier",
                "symbol": "SPY",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
                "interval": "1M",
                "extended_hours": False,
            }
        ),
        (
            {
                "provider": "tradier",
                "symbol": "SPY,DJIA",
                "start_date": None,
                "end_date": None,
                "interval": "15m",
                "extended_hours": False,
            }
        ),
        (
            {
                "provider": "tmx",
                "symbol": "SPY:US",
                "start_date": "2023-01-01",
                "end_date": "2023-12-31",
                "interval": "1d",
                "adjustment": "splits_only",
            }
        ),
    ],
)
@pytest.mark.integration
def test_etf_historical(params, market):
    result = market.equity.price.historical(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        ({"symbol": "IOO", "provider": "fmp"}),
        ({"symbol": "XIU", "provider": "tmx", "use_cache": False}),
        ({"symbol": "QQQ", "provider": "yfinance"}),
        ({"symbol": "IOO,QQQ", "provider": "intrinio"}),
    ],
)
@pytest.mark.integration
def test_etf_info(params, market):
    params = {p: v for p, v in params.items() if v}

    result = market.etf.info(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        ({"symbol": "IOO", "provider": "fmp"}),
        ({"symbol": "XIU", "provider": "tmx", "use_cache": False}),
    ],
)
@pytest.mark.integration
def test_etf_sectors(params, market):
    params = {p: v for p, v in params.items() if v}

    result = market.etf.sectors(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        ({"symbol": "QQQ", "cik": None, "provider": "fmp"}),
    ],
)
@pytest.mark.integration
def test_etf_holdings_date(params, market):
    params = {p: v for p, v in params.items() if v}

    result = market.etf.holdings_date(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        (
            {
                "symbol": "IOO",
                "date": "2023-03-31",
                "cik": None,
                "provider": "fmp",
            }
        ),
        (
            {
                "symbol": "SILJ",
                "date": "2019-12-31",
                "cik": None,
                "provider": "fmp",
            }
        ),
        (
            {
                "symbol": "TQQQ",
                "date": None,
                "provider": "sec",
                "use_cache": False,
            }
        ),
        (
            {
                "symbol": "QQQ",
                "date": "2021-06-30",
                "provider": "sec",
                "use_cache": False,
            }
        ),
        (
            {
                "symbol": "XIU",
                "provider": "tmx",
                "use_cache": False,
            }
        ),
        (
            {
                "symbol": "DJIA",
                "provider": "intrinio",
            }
        ),
    ],
)
@pytest.mark.integration
def test_etf_holdings(params, market):
    params = {p: v for p, v in params.items() if v}

    result = market.etf.holdings(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        ({"symbol": "SPY,VOO,QQQ,IWM,IWN,GOVT,JNK", "provider": "fmp"}),
        ({"symbol": "SPY,VOO,QQQ,IWM,IWN,GOVT,JNK", "provider": "finviz"}),
        (
            {
                "symbol": "SPY,VOO,QQQ,IWM,IWN,GOVT,JNK",
                "return_type": "trailing",
                "adjustment": "splits_and_dividends",
                "provider": "intrinio",
            }
        ),
    ],
)
@pytest.mark.integration
def test_etf_price_performance(params, market):
    params = {p: v for p, v in params.items() if v}

    result = market.etf.price_performance(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        ({"symbol": "IOO", "provider": "fmp"}),
        ({"symbol": "XIU", "provider": "tmx", "use_cache": False}),
    ],
)
@pytest.mark.integration
def test_etf_countries(params, market):
    params = {p: v for p, v in params.items() if v}

    result = market.etf.countries(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [({"sort": "desc", "limit": 10})],
)
@pytest.mark.integration
def test_etf_discovery_gainers(params, market):
    params = {p: v for p, v in params.items() if v}

    result = market.etf.discovery.gainers(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [({"sort": "desc", "limit": 10})],
)
@pytest.mark.integration
def test_etf_discovery_losers(params, market):
    params = {p: v for p, v in params.items() if v}

    result = market.etf.discovery.losers(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [({"sort": "desc", "limit": 10})],
)
@pytest.mark.integration
def test_etf_discovery_active(params, market):
    params = {p: v for p, v in params.items() if v}

    result = market.etf.discovery.active(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        ({"symbol": "SPY", "provider": "fmp"}),
        ({"symbol": "QQQ", "provider": "fmp"}),
    ],
)
@pytest.mark.integration
def test_etf_holdings_performance(params, market):
    params = {p: v for p, v in params.items() if v}

    result = market.etf.holdings_performance(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        ({"symbol": "SPY,VOO,QQQ,IWM,IWN", "provider": "fmp"}),
    ],
)
@pytest.mark.integration
def test_etf_equity_exposure(params, market):
    params = {p: v for p, v in params.items() if v}

    result = market.etf.equity_exposure(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0
