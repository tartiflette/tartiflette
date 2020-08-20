import asyncio

import pytest

from tartiflette import (
    Resolver,
    Subscription,
    create_schema,
    create_schema_with_operationers,
)
from tartiflette.types.exceptions.tartiflette import (
    NonAsyncGeneratorSubscription,
    NotSubscriptionField,
)
from tests.schema_stack import SchemaStack

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
async def schema_stack():
    @Subscription("MySubscription.newSearch", schema_name="test_subscribe")
    async def subscription_new_search(*_, **__):
        for search in _SEARCHS:
            yield {"newSearch": search}
            await asyncio.sleep(0.01)

    class MySubscriptionCustomSearchSubscriber:
        async def __call__(self, *_, **__):
            for search in _SEARCHS:
                yield {"newSearch": search}
                await asyncio.sleep(0.01)

    Subscription("MySubscription.customSearch", schema_name="test_subscribe")(
        MySubscriptionCustomSearchSubscriber()
    )

    @Resolver("MySubscription.customSearch", schema_name="test_subscribe")
    async def resolver_subscription_custom_search(parent, args, ctx, info):
        return [f"{search} #c" for search in parent["newSearch"]]

    schema, execute, subscribe = await create_schema_with_operationers(
        _SDL, name="test_subscribe"
    )
    return SchemaStack("test_subscribe", schema, execute, subscribe)


@pytest.mark.asyncio
async def test_subscribe_error(schema_stack):
    i = 0

    async for result in schema_stack.subscribe(
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
async def test_subscribe(schema_stack):
    i = 0
    async for result in schema_stack.subscribe(
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
async def test_subscribe_aliases(schema_stack):
    i = 0
    async for result in schema_stack.subscribe(
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
async def test_subscribe_custom_search(schema_stack):
    i = 0
    async for result in schema_stack.subscribe(
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
async def test_subscribe_custom_search_aliases(schema_stack):
    i = 0
    async for result in schema_stack.subscribe(
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

        await create_schema(_SDL, name="test_subscribe_non_subscription_field")


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

        await create_schema(_SDL, name="test_subscribe_non_subscription_field")
