"""Composite Leading Indicator Standard Model."""

from datetime import date as dateType
from typing import Optional

from pydantic import Field

from datamart_core.provider.abstract.data import Data
from datamart_core.provider.abstract.query_params import QueryParams
from datamart_core.provider.utils.descriptions import (
    DATA_DESCRIPTIONS,
    QUERY_DESCRIPTIONS,
)


class CLIQueryParams(QueryParams):
    """Composite Leading Indicator Query."""

    start_date: Optional[dateType] = Field(
        default=None, description=QUERY_DESCRIPTIONS.get("start_date")
    )
    end_date: Optional[dateType] = Field(
        default=None, description=QUERY_DESCRIPTIONS.get("end_date")
    )


class CLIData(Data):
    """Composite Leading Indicator Data."""

    date: Optional[dateType] = Field(
        default=None, description=DATA_DESCRIPTIONS.get("date")
    )
    value: Optional[float] = Field(default=None, description="CLI value")
    country: Optional[str] = Field(
        default=None,
        description="Country for which CLI is given",
    )
