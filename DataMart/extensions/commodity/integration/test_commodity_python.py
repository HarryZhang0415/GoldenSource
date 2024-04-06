"""Test Commodity extension."""

import pytest
from datamart_core.app.model.obbject import OBBject

# pylint: disable=redefined-outer-name


@pytest.fixture(scope="session")
def market(pytestconfig):  # pylint: disable=inconsistent-return-statements
    """Fixture to setup market."""
    if pytestconfig.getoption("markexpr") != "not integration":
        import datamart  # pylint: disable=import-outside-toplevel

        return datamart.market


@pytest.mark.parametrize(
    "params",
    [
        (
            {
                "asset": "gold",
                "start_date": None,
                "end_date": None,
                "collapse": None,
                "transform": None,
                "provider": "nasdaq",
            }
        ),
        (
            {
                "asset": "silver",
                "start_date": "1990-01-01",
                "end_date": "2023-01-01",
                "collapse": "monthly",
                "transform": "diff",
                "provider": "nasdaq",
            }
        ),
    ],
)
@pytest.mark.integration
def test_commodity_lbma_fixing(params, market):
    params = {p: v for p, v in params.items() if v}

    result = market.commodity.lbma_fixing(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0
