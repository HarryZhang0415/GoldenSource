"""Biztoc provider module."""

from datamart_biztoc.models.world_news import BiztocWorldNewsFetcher
from datamart_core.provider.abstract.provider import Provider

biztoc_provider = Provider(
    name="biztoc",
    website="https://api.biztoc.com/#biztoc-default",
    description="""BizToc uses Rapid API for its REST API.
    You may sign up for your free account at https://rapidapi.com/thma/api/biztoc.

    The Base URL for all requests is:

        https://biztoc.p.rapidapi.com/

    If you're not a developer but would still like to use Biztoc outside of the main website,
    we've partnered with DataMart, allowing you to pull in BizToc's news stream in their Terminal.""",
    credentials=["api_key"],
    fetcher_dict={
        "WorldNews": BiztocWorldNewsFetcher,
    },
)
