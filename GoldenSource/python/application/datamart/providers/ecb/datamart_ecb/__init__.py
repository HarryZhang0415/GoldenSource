"""ECB provider module."""

from datamart_core.provider.abstract.provider import Provider
from datamart_ecb.models.balance_of_payments import ECBBalanceOfPaymentsFetcher
from datamart_ecb.models.currency_reference_rates import ECBCurrencyReferenceRatesFetcher
from datamart_ecb.models.eu_yield_curve import ECBEUYieldCurveFetcher

ecb_provider = Provider(
    name="ECB",
    website="https://data.ecb.europa.eu/",
    description="""The ECB Data Portal provides access to all official ECB statistics.
    The portal also provides options to download data and comprehensive metadata for each dataset.
    Statistical publications and dashboards offer a compilation of key data on selected topics.""",
    fetcher_dict={
        "BalanceOfPayments": ECBBalanceOfPaymentsFetcher,
        "CurrencyReferenceRates": ECBCurrencyReferenceRatesFetcher,
        "EUYieldCurve": ECBEUYieldCurveFetcher,
    },
)
