"""Finviz provider module."""

from datamart_core.provider.abstract.provider import Provider
from datamart_finviz.models.compare_groups import FinvizCompareGroupsFetcher
from datamart_finviz.models.equity_profile import FinvizEquityProfileFetcher
from datamart_finviz.models.key_metrics import FinvizKeyMetricsFetcher
from datamart_finviz.models.price_performance import FinvizPricePerformanceFetcher
from datamart_finviz.models.price_target import FinvizPriceTargetFetcher

finviz_provider = Provider(
    name="finviz",
    website="https://finviz.com",
    description="Unofficial Finviz API - https://github.com/lit26/finvizfinance/releases",
    credentials=None,
    fetcher_dict={
        "CompareGroups": FinvizCompareGroupsFetcher,
        "EtfPricePerformance": FinvizPricePerformanceFetcher,
        "EquityInfo": FinvizEquityProfileFetcher,
        "KeyMetrics": FinvizKeyMetricsFetcher,
        "PricePerformance": FinvizPricePerformanceFetcher,
        "PriceTarget": FinvizPriceTargetFetcher,
    },
)
