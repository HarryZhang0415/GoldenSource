"""IORB Standard Model."""

from datetime import date as dateType
from typing import Optional

from pydantic import Field

from datamart_core.provider.abstract.data import Data
from datamart_core.provider.abstract.query_params import QueryParams
from datamart_core.provider.utils.descriptions import (
    DATA_DESCRIPTIONS,
    QUERY_DESCRIPTIONS,
)


class IORBQueryParams(QueryParams):
    """IORB Query."""

    start_date: Optional[dateType] = Field(
        default=None,
        description=QUERY_DESCRIPTIONS.get("start_date", ""),
    )
    end_date: Optional[dateType] = Field(
        default=None,
        description=QUERY_DESCRIPTIONS.get("end_date", ""),
    )


class IORBData(Data):
    """IORB Data."""

    date: dateType = Field(description=DATA_DESCRIPTIONS.get("date", ""))
    rate: Optional[float] = Field(description="IORB rate.")