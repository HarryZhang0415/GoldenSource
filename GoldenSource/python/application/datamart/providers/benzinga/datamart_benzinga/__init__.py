"""Benzinga provider module."""

from datamart_benzinga.models.analyst_search import BenzingaAnalystSearchFetcher
from datamart_benzinga.models.company_news import BenzingaCompanyNewsFetcher
from datamart_benzinga.models.price_target import BenzingaPriceTargetFetcher
from datamart_benzinga.models.world_news import BenzingaWorldNewsFetcher
from datamart_core.provider.abstract.provider import Provider

benzinga_provider = Provider(
    name="benzinga",
    website="https://www.benzinga.com/",
    description="""Benzinga is a financial data provider that offers an API
    focused on information that moves the market.""",
    credentials=["api_key"],
    fetcher_dict={
        "AnalystSearch": BenzingaAnalystSearchFetcher,
        "CompanyNews": BenzingaCompanyNewsFetcher,
        "WorldNews": BenzingaWorldNewsFetcher,
        "PriceTarget": BenzingaPriceTargetFetcher,
    },
)
