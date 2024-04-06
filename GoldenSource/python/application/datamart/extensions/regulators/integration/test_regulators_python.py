"""Test Regulators extension."""

import pytest
from extensions.tests.conftest import parametrize
from datamart_core.app.model.obbject import OBBject


# pylint: disable=inconsistent-return-statements
@pytest.fixture(scope="session")
def market(pytestconfig):
    """Fixture to setup market."""

    if pytestconfig.getoption("markexpr") != "not integration":
        import datamart  # pylint: disable=import-outside-toplevel

        return datamart.market


# pylint: disable=redefined-outer-name


@parametrize(
    "params",
    [
        ({"symbol": "TSLA", "provider": "sec"}),
        ({"symbol": "SQQQ", "provider": "sec"}),
    ],
)
@pytest.mark.integration
def test_regulators_sec_cik_map(params, market):
    result = market.regulators.sec.cik_map(**params)
    assert result
    assert isinstance(result, OBBject)
    assert hasattr(result.results, "cik")
    assert isinstance(result.results.cik, str)


@parametrize(
    "params",
    [
        ({"query": "berkshire hathaway", "provider": "sec", "use_cache": None}),
    ],
)
@pytest.mark.integration
def test_regulators_sec_institutions_search(params, market):
    result = market.regulators.sec.institutions_search(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        (
            {
                "query": "2022",
                "provider": "sec",
                "url": None,
                "use_cache": None,
            }
        ),
        (
            {
                "query": "",
                "provider": "sec",
                "url": "https://xbrl.fasb.org/us-gaap/2014/entire/",
                "use_cache": None,
            }
        ),
    ],
)
@pytest.mark.integration
def test_regulators_sec_schema_files(params, market):
    result = market.regulators.sec.schema_files(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results.files) > 0


@parametrize(
    "params",
    [
        ({"query": "0000909832", "provider": "sec", "use_cache": None}),
        ({"query": "0001067983", "provider": "sec", "use_cache": None}),
    ],
)
@pytest.mark.integration
def test_regulators_sec_symbol_map(params, market):
    result = market.regulators.sec.symbol_map(**params)
    assert result
    assert isinstance(result, OBBject)
    assert hasattr(result.results, "symbol")
    assert isinstance(result.results.symbol, str)


@parametrize(
    "params",
    [({"provider": "sec"})],
)
@pytest.mark.integration
def test_regulators_sec_rss_litigation(params, market):
    result = market.regulators.sec.rss_litigation(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [({"query": "oil", "use_cache": False, "provider": "sec"})],
)
@pytest.mark.integration
def test_regulators_sec_sic_search(params, market):
    result = market.regulators.sec.sic_search(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        ({"query": "grain", "provider": "nasdaq", "use_cache": None}),
    ],
)
@pytest.mark.integration
def test_regulators_cftc_cot_search(params, market):
    result = market.regulators.cftc.cot_search(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        (
            {
                "id": "13874P",
                "data_type": "FO",
                "legacy_format": True,
                "report_type": "ALL",
                "measure": "CR",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
                "transform": "diff",
                "collapse": "weekly",
                "provider": "nasdaq",
            }
        ),
    ],
)
@pytest.mark.integration
def test_regulators_cftc_cot(params, market):
    result = market.regulators.cftc.cot(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0
