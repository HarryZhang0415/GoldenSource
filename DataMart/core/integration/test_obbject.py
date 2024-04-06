import contextlib
import sys

import pytest

with contextlib.suppress(ImportError):
    import polars as pl

with contextlib.suppress(ImportError):
    import pandas as pd

with contextlib.suppress(ImportError):
    import numpy as np

with contextlib.suppress(ImportError):
    from datamart_charting.core.datamart_figure import DataMartFigure


# pylint: disable=inconsistent-return-statements
@pytest.fixture(scope="session")
def market(pytestconfig):
    """Fixture to setup market."""

    if pytestconfig.getoption("markexpr") != "not integration":
        import datamart  # pylint: disable=import-outside-toplevel

        return datamart.market


# pylint: disable=redefined-outer-name


@pytest.mark.skipif("pandas" not in sys.modules, reason="pandas not installed")
@pytest.mark.integration
def test_to_dataframe(market):
    """Test obbject to dataframe."""

    stocks_df = market.equity.price.historical("AAPL", provider="fmp").to_dataframe()
    assert isinstance(stocks_df, pd.DataFrame)


@pytest.mark.skipif("polars" not in sys.modules, reason="polars not installed")
@pytest.mark.integration
def test_to_polars(market):
    """Test obbject to polars."""

    crypto_pl = market.crypto.price.historical("BTC-USD", provider="fmp").to_polars()
    assert isinstance(crypto_pl, pl.DataFrame)


@pytest.mark.skipif("numpy" not in sys.modules, reason="numpy not installed")
@pytest.mark.integration
def test_to_numpy(market):
    """Test obbject to numpy array."""

    cpi_np = market.economy.cpi(
        country=["portugal", "spain", "switzerland"], frequency="annual"
    ).to_numpy()
    assert isinstance(cpi_np, np.ndarray)


@pytest.mark.integration
def test_to_dict(market):
    """Test obbject to dict."""

    fed_dict = market.fixedincome.rate.ameribor(start_date="2020-01-01").to_dict()
    assert isinstance(fed_dict, dict)


@pytest.mark.skipif(
    "datamart_charting" not in sys.modules, reason="datamart_charting not installed"
)
@pytest.mark.integration
def test_to_chart(market):
    """Test obbject to chart."""

    res = market.equity.price.historical("AAPL", provider="fmp")
    res.charting.to_chart(render=False)
    assert isinstance(res.chart.fig, DataMartFigure)


@pytest.mark.skipif(
    "datamart_charting" not in sys.modules, reason="datamart_charting not installed"
)
@pytest.mark.integration
def test_show(market):
    """Test obbject to chart."""

    stocks_data = market.equity.price.historical("AAPL", provider="fmp", chart=True)
    assert isinstance(stocks_data.chart.fig, DataMartFigure)
    assert stocks_data.chart.fig.show() is None
