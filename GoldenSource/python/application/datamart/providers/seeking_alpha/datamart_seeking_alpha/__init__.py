"""Seeking Alpha Provider module."""

from datamart_core.provider.abstract.provider import Provider
from datamart_seeking_alpha.models.upcoming_release_days import (
    SAUpcomingReleaseDaysFetcher,
)

seeking_alpha_provider = Provider(
    name="seeking_alpha",
    website="https://seekingalpha.com",
    description="""Seeking Alpha is a data provider with access to news, analysis, and
    real-time alerts on stocks.""",
    fetcher_dict={
        "UpcomingReleaseDays": SAUpcomingReleaseDaysFetcher,
    },
)
