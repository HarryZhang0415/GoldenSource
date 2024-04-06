"""OECD provider module."""

from datamart_core.provider.abstract.provider import Provider
from datamart_oecd.models.composite_leading_indicator import OECDCLIFetcher
from datamart_oecd.models.gdp_forecast import OECDGdpForecastFetcher
from datamart_oecd.models.gdp_nominal import OECDGdpNominalFetcher
from datamart_oecd.models.gdp_real import OECDGdpRealFetcher
from datamart_oecd.models.long_term_interest_rate import OECDLTIRFetcher
from datamart_oecd.models.short_term_interest_rate import OECDSTIRFetcher
from datamart_oecd.models.unemployment import OECDUnemploymentFetcher

oecd_provider = Provider(
    name="oecd",
    website="https://stats.oecd.org/",
    description="""OECD""",
    fetcher_dict={
        "GdpNominal": OECDGdpNominalFetcher,
        "GdpReal": OECDGdpRealFetcher,
        "GdpForecast": OECDGdpForecastFetcher,
        "Unemployment": OECDUnemploymentFetcher,
        "CLI": OECDCLIFetcher,
        "STIR": OECDSTIRFetcher,
        "LTIR": OECDLTIRFetcher,
    },
)
