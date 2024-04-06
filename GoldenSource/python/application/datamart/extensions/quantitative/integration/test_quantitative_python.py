"""Test qa extension."""

import random
from typing import Literal

import pytest
from extensions.tests.conftest import parametrize
from datamart_core.app.model.obbject import OBBject


# pylint:disable=inconsistent-return-statements
@pytest.fixture(scope="session")
def market(pytestconfig):
    """Fixture to setup market."""
    if pytestconfig.getoption("markexpr") != "not integration":
        import datamart  # pylint:disable=import-outside-toplevel

        return datamart.market


# pylint:disable=redefined-outer-name

data: dict = {}


def get_stocks_data():
    import datamart  # pylint:disable=import-outside-toplevel

    if "stocks_data" in data:
        return data["stocks_data"]

    symbol = random.choice(["AAPL", "NVDA", "MSFT", "TSLA", "AMZN", "V"])  # noqa: S311
    provider = random.choice(["fmp", "polygon", "yfinance"])  # noqa: S311

    data["stocks_data"] = datamart.market.equity.price.historical(
        symbol=symbol, provider=provider
    ).results
    return data["stocks_data"]


def get_crypto_data():
    import datamart  # pylint:disable=import-outside-toplevel

    if "crypto_data" in data:
        return data["crypto_data"]

    # TODO : add more crypto providers and symbols
    symbol = random.choice(["BTCUSD"])  # noqa: S311
    provider = random.choice(["fmp"])  # noqa: S311

    data["crypto_data"] = datamart.market.crypto.price.historical(
        symbol=symbol, provider=provider
    ).results
    return data["crypto_data"]


def get_data(menu: Literal["equity", "crypto"]):
    funcs = {"equity": get_stocks_data, "crypto": get_crypto_data}
    return funcs[menu]()


@parametrize(
    "params, data_type",
    [
        ({"data": "", "target": "close"}, "equity"),
        ({"data": "", "target": "high"}, "crypto"),
    ],
)
@pytest.mark.integration
def test_quantitative_normality(params, data_type, market):
    params = {p: v for p, v in params.items() if v}
    params["data"] = get_data(data_type)

    result = market.quantitative.normality(**params)
    assert result
    assert isinstance(result, OBBject)


@parametrize(
    "params, data_type",
    [
        ({"data": "", "target": "close"}, "equity"),
        ({"data": "", "target": "high"}, "crypto"),
    ],
)
@pytest.mark.integration
def test_quantitative_capm(params, data_type, market):
    params = {p: v for p, v in params.items() if v}
    params["data"] = get_data(data_type)

    result = market.quantitative.capm(**params)
    assert result
    assert isinstance(result, OBBject)


@parametrize(
    "params, data_type",
    [
        (
            {
                "data": "",
                "target": "close",
                "threshold_start": "",
                "threshold_end": "",
            },
            "equity",
        ),
        (
            {
                "data": "",
                "target": "high",
                "threshold_start": "0.1",
                "threshold_end": "1.6",
            },
            "crypto",
        ),
    ],
)
@pytest.mark.integration
def test_quantitative_performance_omega_ratio(params, data_type, market):
    params = {p: v for p, v in params.items() if v}
    params["data"] = get_data(data_type)

    result = market.quantitative.performance.omega_ratio(**params)
    assert result
    assert isinstance(result, OBBject)


@parametrize(
    "params, data_type",
    [
        ({"data": "", "target": "close", "window": "5", "index": "date"}, "equity"),
        ({"data": "", "target": "high", "window": "10", "index": "date"}, "crypto"),
    ],
)
@pytest.mark.integration
def test_quantitative_rolling_kurtosis(params, data_type, market):
    params = {p: v for p, v in params.items() if v}
    params["data"] = get_data(data_type)

    result = market.quantitative.rolling.kurtosis(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params, data_type",
    [
        (
            {
                "data": "",
                "target": "close",
                "fuller_reg": "c",
                "kpss_reg": "ct",
            },
            "equity",
        ),
        (
            {
                "data": "",
                "target": "high",
                "fuller_reg": "ct",
                "kpss_reg": "c",
            },
            "crypto",
        ),
    ],
)
@pytest.mark.integration
def test_quantitative_unitroot_test(params, data_type, market):
    params = {p: v for p, v in params.items() if v}
    params["data"] = get_data(data_type)

    result = market.quantitative.unitroot_test(**params)
    assert result
    assert isinstance(result, OBBject)


@parametrize(
    "params, data_type",
    [
        (
            {
                "data": "",
                "target": "close",
                "rfr": "",
                "window": "100",
                "index": "date",
            },
            "equity",
        ),
        (
            {
                "data": "",
                "target": "high",
                "rfr": "0.5",
                "window": "100",
                "index": "date",
            },
            "crypto",
        ),
    ],
)
@pytest.mark.integration
def test_quantitative_performance_sharpe_ratio(params, data_type, market):
    params = {p: v for p, v in params.items() if v}
    params["data"] = get_data(data_type)

    result = market.quantitative.performance.sharpe_ratio(**params)
    assert result
    assert isinstance(result, OBBject)


@parametrize(
    "params, data_type",
    [
        (
            {
                "data": "",
                "target": "close",
                "target_return": "",
                "window": "100",
                "adjusted": "",
                "index": "date",
            },
            "equity",
        ),
        (
            {
                "data": "",
                "target": "close",
                "target_return": "",
                "window": "100",
                "adjusted": "true",
                "index": "date",
            },
            "crypto",
        ),
    ],
)
@pytest.mark.integration
def test_quantitative_performance_sortino_ratio(params, data_type, market):
    params = {p: v for p, v in params.items() if v}
    params["data"] = get_data(data_type)

    result = market.quantitative.performance.sortino_ratio(**params)
    assert result
    assert isinstance(result, OBBject)


@parametrize(
    "params, data_type",
    [
        ({"data": "", "target": "close", "window": "220", "index": "date"}, "equity"),
    ],
)
@pytest.mark.integration
def test_quantitative_rolling_skew(params, data_type, market):
    params = {p: v for p, v in params.items() if v}
    params["data"] = get_data(data_type)

    result = market.quantitative.rolling.skew(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params, data_type",
    [
        (
            {
                "data": "",
                "target": "close",
                "window": "10",
                "quantile_pct": "",
                "index": "date",
            },
            "equity",
        ),
        (
            {
                "data": "",
                "target": "high",
                "window": "50",
                "quantile_pct": "0.6",
                "index": "date",
            },
            "crypto",
        ),
    ],
)
@pytest.mark.integration
def test_quantitative_rolling_quantile(params, data_type, market):
    params = {p: v for p, v in params.items() if v}
    params["data"] = get_data(data_type)

    result = market.quantitative.rolling.quantile(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params, data_type",
    [
        ({"data": "", "target": "close"}, "equity"),
        ({"data": "", "target": "high"}, "crypto"),
    ],
)
@pytest.mark.integration
def test_quantitative_summary(params, data_type, market):
    params = {p: v for p, v in params.items() if v}
    params["data"] = get_data(data_type)

    result = market.quantitative.summary(**params)
    assert result
    assert isinstance(result, OBBject)


@parametrize(
    "params, data_type",
    [
        (
            {
                "data": "",
                "target": "close",
                "window": "10",
                "index": "date",
            },
            "equity",
        ),
        (
            {
                "data": "",
                "target": "high",
                "window": "50",
                "index": "date",
            },
            "crypto",
        ),
    ],
)
@pytest.mark.integration
def test_quantitative_rolling_stdev(params, data_type, market):
    params = {p: v for p, v in params.items() if v}
    params["data"] = get_data(data_type)

    result = market.quantitative.rolling.stdev(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params, data_type",
    [
        (
            {
                "data": "",
                "target": "close",
                "window": "10",
                "index": "date",
            },
            "equity",
        ),
        (
            {
                "data": "",
                "target": "high",
                "window": "50",
                "index": "date",
            },
            "crypto",
        ),
    ],
)
@pytest.mark.integration
def test_quantitative_rolling_mean(params, data_type, market):
    params = {p: v for p, v in params.items() if v}
    params["data"] = get_data(data_type)

    result = market.quantitative.rolling.mean(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params, data_type",
    [
        (
            {
                "data": "",
                "target": "close",
                "window": "10",
                "index": "date",
            },
            "equity",
        ),
        (
            {
                "data": "",
                "target": "high",
                "window": "50",
                "index": "date",
            },
            "crypto",
        ),
    ],
)
@pytest.mark.integration
def test_quantitative_rolling_variance(params, data_type, market):
    params = {p: v for p, v in params.items() if v}
    params["data"] = get_data(data_type)

    result = market.quantitative.rolling.variance(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params, data_type",
    [
        ({"data": "", "target": "close"}, "equity"),
    ],
)
@pytest.mark.integration
def test_quantitative_stats_skew(params, data_type, market):
    params = {p: v for p, v in params.items() if v}
    params["data"] = get_data(data_type)

    result = market.quantitative.stats.skew(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params, data_type",
    [
        ({"data": "", "target": "close"}, "equity"),
    ],
)
@pytest.mark.integration
def test_quantitative_stats_kurtosis(params, data_type, market):
    params = {p: v for p, v in params.items() if v}
    params["data"] = get_data(data_type)

    result = market.quantitative.stats.kurtosis(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params, data_type",
    [
        ({"data": "", "target": "close"}, "equity"),
    ],
)
@pytest.mark.integration
def test_quantitative_stats_variance(params, data_type, market):
    params = {p: v for p, v in params.items() if v}
    params["data"] = get_data(data_type)

    result = market.quantitative.stats.variance(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params, data_type",
    [
        ({"data": "", "target": "close"}, "equity"),
    ],
)
@pytest.mark.integration
def test_quantitative_stats_stdev(params, data_type, market):
    params = {p: v for p, v in params.items() if v}
    params["data"] = get_data(data_type)

    result = market.quantitative.stats.stdev(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params, data_type",
    [
        ({"data": "", "target": "close"}, "equity"),
    ],
)
@pytest.mark.integration
def test_quantitative_stats_mean(params, data_type, market):
    params = {p: v for p, v in params.items() if v}
    params["data"] = get_data(data_type)

    result = market.quantitative.stats.mean(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params, data_type",
    [
        (
            {
                "data": "",
                "target": "close",
                "quantile_pct": "",
            },
            "equity",
        ),
        (
            {
                "data": "",
                "target": "close",
                "quantile_pct": "0.6",
            },
            "crypto",
        ),
    ],
)
@pytest.mark.integration
def test_quantitative_stats_quantile(params, data_type, market):
    params = {p: v for p, v in params.items() if v}
    params["data"] = get_data(data_type)

    result = market.quantitative.stats.quantile(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0
