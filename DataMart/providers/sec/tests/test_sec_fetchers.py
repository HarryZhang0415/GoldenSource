import pytest
from datamart_core.app.service.user_service import UserService
from datamart_sec.models.cik_map import SecCikMapFetcher
from datamart_sec.models.company_filings import SecCompanyFilingsFetcher
from datamart_sec.models.equity_ftd import SecEquityFtdFetcher
from datamart_sec.models.equity_search import SecEquitySearchFetcher
from datamart_sec.models.etf_holdings import SecEtfHoldingsFetcher
from datamart_sec.models.form_13FHR import SecForm13FHRFetcher
from datamart_sec.models.institutions_search import SecInstitutionsSearchFetcher
from datamart_sec.models.rss_litigation import SecRssLitigationFetcher
from datamart_sec.models.schema_files import SecSchemaFilesFetcher
from datamart_sec.models.sic_search import SecSicSearchFetcher
from datamart_sec.models.symbol_map import SecSymbolMapFetcher

test_credentials = UserService().default_user_settings.credentials.dict()


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_headers": [("User-Agent", None)],
        "filter_query_parameters": [
            None,
        ],
    }


@pytest.mark.record_http
def test_sec_etf_holdings_fetcher(credentials=test_credentials):
    params = {"symbol": "TQQQ", "use_cache": False}

    fetcher = SecEtfHoldingsFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_sec_sic_search_fetcher(credentials=test_credentials):
    params = {"query": "oil", "use_cache": False}

    fetcher = SecSicSearchFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_sec_symbol_map_fetcher(credentials=test_credentials):
    params = {"query": "0000909832"}

    fetcher = SecSymbolMapFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_sec_equity_ftd_fetcher(credentials=test_credentials):
    params = {"symbol": "AAPL", "limit": 1}

    fetcher = SecEquityFtdFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_sec_equity_search_fetcher(credentials=test_credentials):
    params = {"query": "trust", "use_cache": False}

    fetcher = SecEquitySearchFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_sec_company_filings_fetcher(credentials=test_credentials):
    params = {"symbol": "AAPL", "type": "10-K", "use_cache": False}

    fetcher = SecCompanyFilingsFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_sec_institutions_search_fetcher(credentials=test_credentials):
    params = {"query": "Investment Trust", "use_cache": False}

    fetcher = SecInstitutionsSearchFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_sec_schema_files_fetcher(credentials=test_credentials):
    params = {"query": "2022"}

    fetcher = SecSchemaFilesFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_sec_rss_litigation_fetcher(credentials=test_credentials):
    params = {}

    fetcher = SecRssLitigationFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_sec_cik_map_fetcher(credentials=test_credentials):
    params = {"symbol": "OXY"}

    fetcher = SecCikMapFetcher()
    result = fetcher.test(params, credentials)
    assert result is None


@pytest.mark.record_http
def test_sec_form_13FHR_fetcher(credentials=test_credentials):
    params = {"symbol": "NVDA"}

    fetcher = SecForm13FHRFetcher()
    result = fetcher.test(params, credentials)
    assert result is None
