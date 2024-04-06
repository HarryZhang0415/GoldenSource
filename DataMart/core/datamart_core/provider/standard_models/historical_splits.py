"""Historical Splits Standard Model."""

from datetime import date as dateType
from typing import Optional

from pydantic import Field, field_validator

from datamart_core.provider.abstract.data import Data
from datamart_core.provider.abstract.query_params import QueryParams
from datamart_core.provider.utils.descriptions import (
    DATA_DESCRIPTIONS,
    QUERY_DESCRIPTIONS,
)


class HistoricalSplitsQueryParams(QueryParams):
    """Historical Splits Query."""

    symbol: str = Field(description=QUERY_DESCRIPTIONS.get("symbol", ""))

    @field_validator("symbol", mode="before", check_fields=False)
    @classmethod
    def to_upper(cls, v: str) -> str:
        """Convert field to uppercase."""
        return v.upper()


class HistoricalSplitsData(Data):
    """Historical Splits Data."""

    date: dateType = Field(description=DATA_DESCRIPTIONS.get("date", ""))
    numerator: Optional[float] = Field(
        default=None,
        description="Numerator of the split.",
    )
    denominator: Optional[float] = Field(
        default=None,
        description="Denominator of the split.",
    )
    split_ratio: Optional[str] = Field(
        default=None,
        description="Split ratio.",
    )
