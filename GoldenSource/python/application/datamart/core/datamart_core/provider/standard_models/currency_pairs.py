"""Currency Available Pairs Standard Model."""

from pydantic import Field

from datamart_core.provider.abstract.data import Data
from datamart_core.provider.abstract.query_params import QueryParams


class CurrencyPairsQueryParams(QueryParams):
    """Currency Available Pairs Query."""


class CurrencyPairsData(Data):
    """Currency Available Pairs Data."""

    name: str = Field(description="Name of the currency pair.")
