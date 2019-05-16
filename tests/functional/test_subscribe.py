import asyncio

import pytest

from tartiflette import Resolver, Subscription, create_engine
from tartiflette.types.exceptions.tartiflette import (
    NonAsyncGeneratorSubscription,
    NotSubscriptionField,
)

_SDL = """
type Query {
  search(query: String!): [String!]
}

type MySubscription {
  newSearch(query: String!): [String!]
  customSearch(query: String!): [String!]
}

schema {
  query: Query
  subscription: MySubscription
}
"""

_SEARCHS = [
    ["Search #1"],
    ["Search #2"],
    ["Search #3"],
    ["Search #4"],
    ["Search #5"],
]


@pytest.fixture(scope="module")
async def ttftt_engine():
    @Subscription("MySubscription.newSearch", schema_name="test_subscribe")
    @Subscription("MySubscription.customSearch", schema_name="test_subscribe")
    async def subscription_new_search(*_, **__):
        for search in _SEARCHS:
            yield {"newSearch": search}
            await asyncio.sleep(0.01)

    @Resolver("MySubscription.customSearch", schema_name="test_subscribe")
    async def resolver_subscription_custom_search(parent, args, ctx, info):
        return [f"{search} #c" for search in parent["newSearch"]]

    return await create_engine(sdl=_SDL, schema_name="test_subscribe")


@pytest.mark.asyncio
async def test_subscribe_error(ttftt_engine):
    i = 0

    async for result in ttftt_engine.subscribe(
        """
        subscription ($query: String!) {
          newSearch(query: $query)
        }
        """
    ):
        i += 1
        assert result == {
            "data": None,
            "errors": [
                {
                    "message": "Variable < $query > of required type < String! > was not provided.",
                    "path": None,
                    "locations": [{"line": 2, "column": 23}],
                }
            ],
        }

    assert i == 1


@pytest.mark.asyncio
async def test_subscribe(ttftt_engine):
    i = 0
    async for result in ttftt_engine.subscribe(
        """
        subscription {
          newSearch(query: "A query")
        }
        """
    ):
        i += 1
        assert result == {"data": {"newSearch": [f"Search #{i}"]}}

    assert i == 5


@pytest.mark.asyncio
async def test_subscribe_aliases(ttftt_engine):
    i = 0
    async for result in ttftt_engine.subscribe(
        """
        subscription {
          aSearch: newSearch(query: "A query")
        }
        """
    ):
        i += 1
        assert result == {"data": {"aSearch": [f"Search #{i}"]}}

    assert i == 5


@pytest.mark.asyncio
async def test_subscribe_custom_search(ttftt_engine):
    i = 0
    async for result in ttftt_engine.subscribe(
        """
        subscription {
          customSearch(query: "A query")
        }
        """
    ):
        i += 1
        assert result == {"data": {"customSearch": [f"Search #{i} #c"]}}

    assert i == 5


@pytest.mark.asyncio
async def test_subscribe_custom_search_aliases(ttftt_engine):
    i = 0
    async for result in ttftt_engine.subscribe(
        """
        subscription {
          aSearch: customSearch(query: "A query")
        }
        """
    ):
        i += 1
        assert result == {"data": {"aSearch": [f"Search #{i} #c"]}}

    assert i == 5


@pytest.mark.asyncio
async def test_subscribe_non_async_generator_implementation():
    with pytest.raises(
        NonAsyncGeneratorSubscription,
        match=r"The subscription < .* > given is not an awaitable generator.",
    ):

        async def subscription_search(*_, **__):
            return 1

        Subscription(
            "Query.search", schema_name="test_subscribe_non_subscription_field"
        )(subscription_search)

        await create_engine(
            _SDL, schema_name="test_subscribe_non_subscription_field"
        )


@pytest.mark.asyncio
async def test_subscribe_non_subscription_field():
    with pytest.raises(
        NotSubscriptionField,
        match="Field < Query.search > isn't a subscription field.",
    ):

        async def subscription_query_search(*_, **__):
            yield {}

        Subscription(
            "Query.search", schema_name="test_subscribe_non_subscription_field"
        )(subscription_query_search)

        await create_engine(
            _SDL, schema_name="test_subscribe_non_subscription_field"
        )
