"""SEC provider module."""

from datamart_core.provider.abstract.provider import Provider
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

sec_provider = Provider(
    name="sec",
    website="https://sec.gov",
    description="SEC is the public listings regulatory body for the United States.",
    credentials=None,
    fetcher_dict={
        "CikMap": SecCikMapFetcher,
        "CompanyFilings": SecCompanyFilingsFetcher,
        "EquityFTD": SecEquityFtdFetcher,
        "EquitySearch": SecEquitySearchFetcher,
        "EtfHoldings": SecEtfHoldingsFetcher,
        "Filings": SecCompanyFilingsFetcher,
        "Form13FHR": SecForm13FHRFetcher,
        "InstitutionsSearch": SecInstitutionsSearchFetcher,
        "RssLitigation": SecRssLitigationFetcher,
        "SchemaFiles": SecSchemaFilesFetcher,
        "SicSearch": SecSicSearchFetcher,
        "SymbolMap": SecSymbolMapFetcher,
    },
)
