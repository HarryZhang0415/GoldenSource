"""FRED provider module."""

from datamart_core.provider.abstract.provider import Provider
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

fred_provider = Provider(
    name="fred",
    website="https://fred.stlouisfed.org/",
    description="""Federal Reserve Economic Data is a database maintained by the
     Research division of the Federal Reserve Bank of St. Louis that has more than
     816,000 economic time series from various sources.""",
    credentials=["api_key"],
    fetcher_dict={
        "ConsumerPriceIndex": FREDConsumerPriceIndexFetcher,
        "USYieldCurve": FREDYieldCurveFetcher,
        "SOFR": FREDSOFRFetcher,
        "ESTR": FREDESTRFetcher,
        "SONIA": FREDSONIAFetcher,
        "AMERIBOR": FREDAMERIBORFetcher,
        "FEDFUNDS": FREDFEDFetcher,
        "PROJECTIONS": FREDPROJECTIONFetcher,
        "IORB": FREDIORBFetcher,
        "DiscountWindowPrimaryCreditRate": FREDDiscountWindowPrimaryCreditRateFetcher,
        "EuropeanCentralBankInterestRates": FREDEuropeanCentralBankInterestRatesFetcher,
        "ICEBofA": FREDICEBofAFetcher,
        "MoodyCorporateBondIndex": FREDMoodyCorporateBondIndexFetcher,
        "CommercialPaper": FREDCommercialPaperFetcher,
        "FredSearch": FredSearchFetcher,
        "FredSeries": FredSeriesFetcher,
        "FredRegional": FredRegionalDataFetcher,
        "SpotRate": FREDSpotRateFetcher,
        "HighQualityMarketCorporateBond": FREDHighQualityMarketCorporateBondFetcher,
        "TreasuryConstantMaturity": FREDTreasuryConstantMaturityFetcher,
        "SelectedTreasuryConstantMaturity": FREDSelectedTreasuryConstantMaturityFetcher,
        "SelectedTreasuryBill": FREDSelectedTreasuryBillFetcher,
    },
)
