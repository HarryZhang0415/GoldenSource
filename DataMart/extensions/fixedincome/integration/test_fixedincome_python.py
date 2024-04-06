"""Test fixed income extension."""

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
        ({"start_date": "2023-01-01", "end_date": "2023-06-06", "provider": "fmp"}),
    ],
)
@pytest.mark.integration
def test_fixedincome_government_treasury_rates(params, market):
    result = market.fixedincome.government.treasury_rates(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        ({"date": "2023-01-01", "inflation_adjusted": True, "provider": "fred"}),
    ],
)
@pytest.mark.integration
def test_fixedincome_government_us_yield_curve(params, market):
    result = market.fixedincome.government.us_yield_curve(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        ({"start_date": "2023-01-01", "end_date": "2023-06-06"}),
        (
            {
                "period": "overnight",
                "provider": "fred",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
            }
        ),
    ],
)
@pytest.mark.integration
def test_fixedincome_sofr(params, market):
    result = market.fixedincome.sofr(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        ({"start_date": "2023-01-01", "end_date": "2023-06-06"}),
        (
            {
                "parameter": "volume_weighted_trimmed_mean_rate",
                "provider": "fred",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
            }
        ),
    ],
)
@pytest.mark.integration
def test_fixedincome_rate_estr(params, market):
    result = market.fixedincome.rate.estr(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        ({"start_date": "2023-01-01", "end_date": "2023-06-06"}),
        (
            {
                "parameter": "rate",
                "provider": "fred",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
            }
        ),
    ],
)
@pytest.mark.integration
def test_fixedincome_rate_sonia(params, market):
    result = market.fixedincome.rate.sonia(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        ({"start_date": "2023-01-01", "end_date": "2023-06-06"}),
        (
            {
                "parameter": "overnight",
                "provider": "fred",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
            }
        ),
    ],
)
@pytest.mark.integration
def test_fixedincome_rate_ameribor(params, market):
    result = market.fixedincome.rate.ameribor(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        (
            {
                "parameter": "weekly",
                "provider": "fred",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
            }
        ),
        (
            {
                "provider": "federal_reserve",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
            }
        ),
    ],
)
@pytest.mark.integration
def test_fixedincome_rate_effr(params, market):
    result = market.fixedincome.rate.effr(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        ({}),
        ({"long_run": True, "provider": "fred"}),
    ],
)
@pytest.mark.integration
def test_fixedincome_rate_effr_forecast(params, market):
    result = market.fixedincome.rate.effr_forecast(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        ({"start_date": "2023-01-01", "end_date": "2023-06-06"}),
    ],
)
@pytest.mark.integration
def test_fixedincome_rate_iorb(params, market):
    result = market.fixedincome.rate.iorb(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        ({"start_date": "2023-01-01", "end_date": "2023-06-06"}),
        (
            {
                "parameter": "daily_excl_weekend",
                "provider": "fred",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
            }
        ),
    ],
)
@pytest.mark.integration
def test_fixedincome_rate_dpcredit(params, market):
    params = {p: v for p, v in params.items() if v}

    result = market.fixedincome.rate.dpcredit(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        (
            {
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
                "interest_rate_type": "lending",
            }
        )
    ],
)
@pytest.mark.integration
def test_fixedincome_rate_ecb(params, market):
    params = {p: v for p, v in params.items() if v}

    result = market.fixedincome.rate.ecb(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        ({"start_date": "2023-01-01", "end_date": "2023-06-06", "index_type": "yield"}),
        (
            {
                "category": "all",
                "area": "us",
                "grade": "non_sovereign",
                "options": True,
                "provider": "fred",
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
                "index_type": "yield",
            }
        ),
    ],
)
@pytest.mark.integration
def test_fixedincome_corporate_ice_bofa(params, market):
    params = {p: v for p, v in params.items() if v}

    result = market.fixedincome.corporate.ice_bofa(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [({"start_date": "2023-01-01", "end_date": "2023-06-06", "index_type": "aaa"})],
)
@pytest.mark.integration
def test_fixedincome_corporate_moody(params, market):
    params = {p: v for p, v in params.items() if v}

    result = market.fixedincome.corporate.moody(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        (
            {
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
                "maturity": "30d",
                "category": "financial",
                "grade": "aa",
                "provider": "fred",
            }
        )
    ],
)
@pytest.mark.integration
def test_fixedincome_corporate_commercial_paper(params, market):
    params = {p: v for p, v in params.items() if v}

    result = market.fixedincome.corporate.commercial_paper(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        (
            {
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
                "maturity": [10.0],
                "category": "spot_rate",
                "provider": "fred",
            }
        ),
        (
            {
                "start_date": None,
                "end_date": None,
                "maturity": 5.5,
                "category": ["spot_rate"],
            }
        ),
        (
            {
                "start_date": None,
                "end_date": None,
                "maturity": "1,5.5,10",
                "category": "spot_rate,par_yield",
            }
        ),
    ],
)
@pytest.mark.integration
def test_fixedincome_corporate_spot_rates(params, market):
    params = {p: v for p, v in params.items() if v}

    result = market.fixedincome.corporate.spot_rates(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [({"date": "2023-01-01", "yield_curve": "spot"})],
)
@pytest.mark.integration
def test_fixedincome_corporate_hqm(params, market):
    params = {p: v for p, v in params.items() if v}

    result = market.fixedincome.corporate.hqm(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [({"start_date": "2023-01-01", "end_date": "2023-06-06", "maturity": "3m"})],
)
@pytest.mark.integration
def test_fixedincome_spreads_tcm(params, market):
    params = {p: v for p, v in params.items() if v}

    result = market.fixedincome.spreads.tcm(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        (
            {
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
                "maturity": "10y",
                "provider": "fred",
            }
        )
    ],
)
@pytest.mark.integration
def test_fixedincome_spreads_tcm_effr(params, market):
    params = {p: v for p, v in params.items() if v}

    result = market.fixedincome.spreads.tcm_effr(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        (
            {
                "start_date": "2023-01-01",
                "end_date": "2023-06-06",
                "maturity": "3m",
                "provider": "fred",
            }
        )
    ],
)
@pytest.mark.integration
def test_fixedincome_spreads_treasury_effr(params, market):
    params = {p: v for p, v in params.items() if v}

    result = market.fixedincome.spreads.treasury_effr(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        (
            {
                "rating": "aaa",
                "provider": "ecb",
                "date": "2023-01-01",
                "yield_curve_type": "spot_rate",
            }
        ),
    ],
)
@pytest.mark.integration
def test_fixedincome_government_eu_yield_curve(params, market):
    params = {p: v for p, v in params.items() if v}

    result = market.fixedincome.government.eu_yield_curve(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@parametrize(
    "params",
    [
        (
            {
                "start_date": "2023-09-01",
                "end_date": "2023-11-16",
                "cusip": None,
                "page_size": None,
                "page_num": None,
                "security_type": None,
                "provider": "government_us",
            }
        ),
        (
            {
                "start_date": "2023-09-01",
                "end_date": "2023-11-16",
                "cusip": None,
                "page_size": None,
                "page_num": None,
                "security_type": "Bond",
                "provider": "government_us",
            }
        ),
    ],
)
@pytest.mark.integration
def test_fixedincome_government_treasury_auctions(params, market):
    params = {p: v for p, v in params.items() if v}

    result = market.fixedincome.government.treasury_auctions(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@pytest.mark.parametrize(
    "params",
    [
        (
            {
                "date": "2023-11-16",
                "cusip": None,
                "security_type": "bond",
                "provider": "government_us",
            }
        ),
        (
            {
                "date": "2023-12-28",
                "cusip": None,
                "security_type": "bill",
                "provider": "government_us",
            }
        ),
        (
            {
                "date": None,
                "provider": "tmx",
                "govt_type": "federal",
                "issue_date_min": None,
                "issue_date_max": None,
                "last_traded_min": None,
                "maturity_date_min": None,
                "maturity_date_max": None,
                "use_cache": True,
            }
        ),
    ],
)
@pytest.mark.integration
def test_fixedincome_government_treasury_prices(params, market):
    params = {p: v for p, v in params.items() if v}

    result = market.fixedincome.government.treasury_prices(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0


@pytest.mark.parametrize(
    "params",
    [
        (
            {
                "provider": "tmx",
                "issuer_name": "federal",
                "issue_date_min": None,
                "issue_date_max": None,
                "last_traded_min": None,
                "coupon_min": 3,
                "coupon_max": None,
                "currency": None,
                "issued_amount_min": None,
                "issued_amount_max": None,
                "maturity_date_min": None,
                "maturity_date_max": None,
                "isin": None,
                "lei": None,
                "country": None,
                "use_cache": False,
            }
        )
    ],
)
@pytest.mark.integration
def test_fixedincome_corporate_bond_prices(params, market):
    params = {p: v for p, v in params.items() if v}

    result = market.fixedincome.corporate.bond_prices(**params)
    assert result
    assert isinstance(result, OBBject)
    assert len(result.results) > 0