"""Federal Reserve provider module."""

from datamart_core.provider.abstract.provider import Provider
from datamart_federal_reserve.models.fed_rates import FederalReserveFEDFetcher
from datamart_federal_reserve.models.money_measures import (
    FederalReserveMoneyMeasuresFetcher,
)
from datamart_federal_reserve.models.treasury_rates import (
    FederalReserveTreasuryRatesFetcher,
)

federal_reserve_provider = Provider(
    name="federal_reserve",
    website="https://www.federalreserve.gov/data.htm",
    description=(),
    fetcher_dict={
        "TreasuryRates": FederalReserveTreasuryRatesFetcher,
        "MoneyMeasures": FederalReserveMoneyMeasuresFetcher,
        "FEDFUNDS": FederalReserveFEDFetcher,
    },
)
