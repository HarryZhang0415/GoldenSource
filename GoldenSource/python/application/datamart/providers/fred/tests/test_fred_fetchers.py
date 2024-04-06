"""Test FRED fetchers."""

import datetime

import pytest
from datamart_core.app.service.user_service import UserService
from datamart_fred.models.ameribor_rates import FREDAMERIBORFetcher
from datamart_fred.models.cp import FREDCommercialPaperFetcher
from datamart_fred.models.cpi import FREDConsumerPriceIndexFetcher
from datamart_fred.models.dwpcr_rates import FREDDiscountWindowPrimaryCreditRateFetcher
from datamart_fred.models.ecb_interest_rates import (
    FREDEuropeanCentralBankInterestRatesFetcher,
)
from datamart_fred.models.estr_rates import FREDESTRFetcher
from datamart_fred.models.fed_projections import FREDPROJECTIONFetcher
from datamart_fred.models.fed_rates import FREDFEDFetcher
from datamart_fred.models.ffrmc import FREDSelectedTreasuryConstantMaturityFetcher
from datamart_fred.models.hqm import FREDHighQualityMarketCorporateBondFetcher
from datamart_fred.models.ice_bofa import FREDICEBofAFetcher
from datamart_fred.models.iorb_rates import FREDIORBFetcher
from datamart_fred.models.moody import FREDMoodyCorporateBondIndexFetcher
from datamart_fred.models.regional import FredRegionalDataFetcher
from datamart_fred.models.search import (
    FredSearchFetcher,
)
from datamart_fred.models.series import FredSeriesFetcher
from datamart_fred.models.sofr_rates import FREDSOFRFetcher
from datamart_fred.models.sonia_rates import FREDSONIAFetcher
from datamart_fred.models.spot import FREDSpotRateFetcher
from datamart_fred.models.tbffr import FREDSelectedTreasuryBillFetcher
from datamart_fred.models.tmc import FREDTreasuryConstantMaturityFetcher
from datamart_fred.models.us_yield_curve import FREDYieldCurveFetcher

test_credentials = UserService().default_user_settings.credentials.model_dump(
    mode="json"
)


@pytest.fixture(scope="module")
def vcr_config():
    """VCR config."""
    return {
        "filter_headers": [("User-Agent", None)],
        "filter_query_parameters": [
            ("api_key", "MOCK_API_KEY"),
        ],
    }


@pytest.mark.record_http
def test_fredcpi_fetcher(credentials=test_credentials):
    """Test FREDConsumerPriceIndexFetcher."""
    params = {"country": "portugal,spain"}

    fetcher = FREDConsumerPriceIndexFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_fred_yield_curve_fetcher(credentials=test_credentials):
    """Test FREDYieldCurveFetcher."""
    params = {"date": datetime.date(2023, 12, 1)}

    fetcher = FREDYieldCurveFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_fredsofr_fetcher(credentials=test_credentials):
    """Test FREDSOFRFetcher."""
    params = {}

    fetcher = FREDSOFRFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_fredestr_fetcher(credentials=test_credentials):
    """Test FREDESTRFetcher."""
    params = {}

    fetcher = FREDESTRFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_fredsonia_fetcher(credentials=test_credentials):
    """Test FREDSONIAFetcher."""
    params = {}

    fetcher = FREDSONIAFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_fredameribor_fetcher(credentials=test_credentials):
    """Test FREDAMERIBORFetcher."""
    params = {}

    fetcher = FREDAMERIBORFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_fredfed_fetcher(credentials=test_credentials):
    """Test FREDFEDFetcher."""
    params = {}

    fetcher = FREDFEDFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_fredprojection_fetcher(credentials=test_credentials):
    """Test FREDPROJECTIONFetcher."""
    params = {}

    fetcher = FREDPROJECTIONFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_frediorb_fetcher(credentials=test_credentials):
    """Test FREDIORBFetcher."""
    params = {}

    fetcher = FREDIORBFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_fred_discount_window_primary_credit_rate_fetcher(credentials=test_credentials):
    """Test FREDDiscountWindowPrimaryCreditRateFetcher."""
    params = {
        "start_date": datetime.date(2023, 1, 1),
        "end_date": datetime.date(2023, 6, 6),
    }

    fetcher = FREDDiscountWindowPrimaryCreditRateFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_fred_european_central_bank_interest_rates_fetcher(
    credentials=test_credentials,
):
    """Test FREDEuropeanCentralBankInterestRatesFetcher."""
    params = {
        "start_date": datetime.date(2023, 1, 1),
        "end_date": datetime.date(2023, 6, 6),
    }

    fetcher = FREDEuropeanCentralBankInterestRatesFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_fredice_bof_a_fetcher(credentials=test_credentials):
    """Test FREDICEBofAFetcher."""
    params = {
        "start_date": datetime.date(2023, 1, 1),
        "end_date": datetime.date(2023, 6, 6),
    }

    fetcher = FREDICEBofAFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_fred_moody_corporate_bond_index_fetcher(credentials=test_credentials):
    """Test FREDMoodyCorporateBondIndexFetcher."""
    params = {
        "start_date": datetime.date(2023, 1, 1),
        "end_date": datetime.date(2023, 6, 6),
    }

    fetcher = FREDMoodyCorporateBondIndexFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_fred_commercial_paper_fetcher(credentials=test_credentials):
    """Test FREDCommercialPaperFetcher."""
    params = {
        "start_date": datetime.date(2023, 1, 1),
        "end_date": datetime.date(2023, 6, 6),
    }

    fetcher = FREDCommercialPaperFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_fred_spot_rate_fetcher(credentials=test_credentials):
    """Test FREDSpotRateFetcher."""
    params = {
        "start_date": datetime.date(2023, 1, 1),
        "end_date": datetime.date(2023, 6, 6),
    }

    fetcher = FREDSpotRateFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_fred_high_quality_market_corporate_bond_fetcher(credentials=test_credentials):
    """Test FREDHighQualityMarketCorporateBondFetcher."""
    params = {"date": datetime.date(2023, 1, 1)}

    fetcher = FREDHighQualityMarketCorporateBondFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_fred_treasury_constant_maturity_fetcher(credentials=test_credentials):
    """Test FREDTreasuryConstantMaturityFetcher."""
    params = {
        "start_date": datetime.date(2023, 1, 1),
        "end_date": datetime.date(2023, 6, 6),
    }

    fetcher = FREDTreasuryConstantMaturityFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_fred_selected_treasury_constant_maturity_fetcher(credentials=test_credentials):
    """Test FREDSelectedTreasuryConstantMaturityFetcher."""
    params = {
        "start_date": datetime.date(2023, 1, 1),
        "end_date": datetime.date(2023, 6, 6),
    }

    fetcher = FREDSelectedTreasuryConstantMaturityFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_fred_selected_treasury_bill_fetcher(credentials=test_credentials):
    """Test FREDSelectedTreasuryBillFetcher."""
    params = {
        "start_date": datetime.date(2023, 1, 1),
        "end_date": datetime.date(2023, 6, 6),
    }

    fetcher = FREDSelectedTreasuryBillFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_fred_search_fetcher(credentials=test_credentials):
    """Test FredSearchFetcher."""
    params = {"query": "Consumer Price Index"}

    fetcher = FredSearchFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_fred_series_fetcher(credentials=test_credentials):
    """Test FredSeriesFetcher."""
    params = {"symbol": "SP500", "filter_variable": "frequency", "filter_value": "w"}

    fetcher = FredSeriesFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_fred_regional_fetcher(credentials=test_credentials):
    """Test FredRegionalFetcher."""
    params = {
        "symbol": "942",
        "is_series_group": True,
        "start_date": datetime.date(1975, 1, 1),
        "frequency": "q",
        "units": "Index 1980:Q1=100",
        "region_type": "state",
        "season": "NSA",
    }

    fetcher = FredRegionalDataFetcher()
    result = fetcher.test(params, credentials)
    assert result is None
