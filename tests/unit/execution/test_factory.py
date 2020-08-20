from unittest.mock import Mock

import pytest

from tartiflette import (
    Resolver,
    Subscription,
    create_schema,
    executor_factory,
    subscriptor_factory,
)
from tartiflette.language.ast import DocumentNode
from tartiflette.language.parsers.libgraphqlparser import parse_to_document
from tartiflette.types.exceptions.tartiflette import (
    ImproperlyConfigured,
    NonCoroutine,
)
from tartiflette.validation.rules import UniqueOperationNamesRule


async def countdown_generator(parent, args, ctx, info):
    i = args["startAt"]
    while i > 0:
        yield {"countdown": i}
        i -= 1
    yield {"countdown": 0}


def test_executor_factory_with_unknown_schema():
    with pytest.raises(
        ImproperlyConfigured, match="< AnUnknown > schema isn't registered."
    ):
        executor_factory("AnUnknown")


def test_executor_factory_with_invalid_schema():
    with pytest.raises(
        ImproperlyConfigured,
        match=(
            "< schema > argument should be either a schema name or a "
            "GraphQLSchema instance."
        ),
    ):
        executor_factory({"A_Set_Instead_Of_GraphQLSchema"})


@pytest.mark.asyncio
async def test_executor_factory_with_schema(random_schema_name):
    schema = await create_schema(
        """
        type Query {
          hello(name: String!): String!
        }
        """,
        name=random_schema_name,
    )

    execute_1 = executor_factory(schema)
    execute_2 = executor_factory(schema.name)
    execute_3 = executor_factory(random_schema_name)


@pytest.mark.asyncio
async def test_executor_factory_with_invalid_error_coercer(random_schema_name):
    def my_error_coercer(exception, error):
        return {"message": "Oopsie"}

    schema = await create_schema(
        """
        type Query {
          hello(name: String!): String!
        }
        """,
        name=random_schema_name,
    )

    with pytest.raises(
        NonCoroutine,
        match="Given < error_coercer > is not a coroutine callable.",
    ):
        executor_factory(schema, error_coercer=my_error_coercer)


@pytest.mark.asyncio
async def test_executor_factory_with_error_coercer(random_schema_name):
    async def my_error_coercer(exception, error):
        return {"message": "Oopsie"}

    @Resolver("Query.hello", schema_name=random_schema_name)
    async def resolve_query_hello(*_, **__):
        raise Exception("Something went wrong.")

    schema = await create_schema(
        """
        type Query {
          hello(name: String!): String!
        }
        """,
        name=random_schema_name,
    )
    execute = executor_factory(schema, error_coercer=my_error_coercer)
    assert (
        await execute(
            """
            {
              hello(name: "John")
            }
            """
        )
        == {"data": None, "errors": [{"message": "Oopsie",},],}
    )


@pytest.mark.asyncio
async def test_executor_factory_with_cache_decorator(random_schema_name):
    cached = {}

    def my_cache_decorator(func):
        def wrapper(query, schema):
            query_hash = hash(query)
            cached_query = cached.get(query_hash)
            if cached_query:
                return cached_query

            result = func(query, schema)
            cached[query_hash] = result
            return result

        return wrapper

    @Resolver("Query.hello", schema_name=random_schema_name)
    async def resolve_query_hello(parent, args, ctx, info):
        return f"Hello {args['name']}!"

    schema = await create_schema(
        """
        type Query {
          hello(name: String!): String!
        }
        """,
        name=random_schema_name,
    )
    query = """
    {
      hello(name: "John")
    }
    """
    assert not cached
    execute = executor_factory(schema, cache_decorator=my_cache_decorator)
    assert await execute(query) == {
        "data": {"hello": "Hello John!",},
    }
    assert cached
    assert isinstance(cached[hash(query)], tuple)
    assert len(cached[hash(query)]) == 2
    assert isinstance(cached[hash(query)][0], DocumentNode)
    assert cached[hash(query)][1] == None


@pytest.mark.asyncio
async def test_executor_factory_with_parser(random_schema_name):
    mocked_parser = Mock(wraps=parse_to_document)

    schema = await create_schema(
        """
        type Query {
          hello(name: String!): String!
        }
        """,
        name=random_schema_name,
    )
    execute = executor_factory(schema, parser=mocked_parser)
    mocked_parser.assert_not_called()
    await execute(
        """
        {
          hello(name: "John")
        }
        """
    )
    mocked_parser.assert_called_once()


@pytest.mark.asyncio
async def test_executor_factory_with_rules(random_schema_name):
    mocked_rule = Mock(wraps=UniqueOperationNamesRule)

    schema = await create_schema(
        """
        type Query {
          hello(name: String!): String!
        }
        """,
        name=random_schema_name,
    )
    execute = executor_factory(schema, rules=[mocked_rule])
    mocked_rule.assert_not_called()
    await execute(
        """
        {
          hello(name: "John")
        }
        """
    )
    mocked_rule.assert_called_once()


@pytest.mark.asyncio
async def test_executor_factory_with_invalid_query(random_schema_name):
    schema = await create_schema(
        """
        type Query {
          hello(name: String!): String!
        }
        """,
        name=random_schema_name,
    )
    execute = executor_factory(schema)
    assert (
        await execute(
            """
            {
              unknown
            }
            """
        )
        == {
            "data": None,
            "errors": [
                {
                    "message": "Cannot query field < unknown > on type < Query >.",
                    "path": None,
                    "locations": [{"line": 3, "column": 15}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.3.1",
                        "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    },
                }
            ],
        }
    )


def test_subscriptor_factory_with_unknown_schema():
    with pytest.raises(
        ImproperlyConfigured, match="< AnUnknown > schema isn't registered."
    ):
        subscriptor_factory("AnUnknown")


def test_subscriptor_factory_with_invalid_schema():
    with pytest.raises(
        ImproperlyConfigured,
        match=(
            "< schema > argument should be either a schema name or a "
            "GraphQLSchema instance."
        ),
    ):
        subscriptor_factory({"A_Set_Instead_Of_GraphQLSchema"})


@pytest.mark.asyncio
async def test_subscriptor_factory_with_schema(random_schema_name):
    schema = await create_schema(
        """
        type Query {
          foo: String
        }

        type Subscription {
          countdown(startAt: Int!): Int!
        }
        """,
        name=random_schema_name,
    )

    subscribe_1 = subscriptor_factory(schema)
    subscribe_2 = subscriptor_factory(schema.name)
    subscribe_3 = subscriptor_factory(random_schema_name)


@pytest.mark.asyncio
async def test_subscriptor_factory_with_invalid_error_coercer(
    random_schema_name,
):
    def my_error_coercer(exception, error):
        return {"message": "Oopsie"}

    schema = await create_schema(
        """
        type Query {
          foo: String
        }

        type Subscription {
          countdown(startAt: Int!): Int!
        }
        """,
        name=random_schema_name,
    )

    with pytest.raises(
        NonCoroutine,
        match="Given < error_coercer > is not a coroutine callable.",
    ):
        subscriptor_factory(schema, error_coercer=my_error_coercer)


@pytest.mark.asyncio
async def test_subscriptor_factory_with_error_coercer(random_schema_name):
    async def my_error_coercer(exception, error):
        return {"message": "Oopsie"}

    @Subscription("Subscription.countdown", schema_name=random_schema_name)
    async def subscribe_countdown(*_, **__):
        if True:
            raise Exception("Something went wrong.")
        yield 1

    schema = await create_schema(
        """
        type Query {
          foo: String
        }

        type Subscription {
          countdown(startAt: Int!): Int!
        }
        """,
        name=random_schema_name,
    )
    subscribe = subscriptor_factory(schema, error_coercer=my_error_coercer)
    with pytest.raises(Exception, match="Something went wrong."):
        async for result in subscribe(
            """
            subscription {
              countdown(startAt: 3)
            }
            """
        ):
            pass


@pytest.mark.asyncio
async def test_subscriptor_factory_with_cache_decorator(random_schema_name):
    cached = {}

    def my_cache_decorator(func):
        def wrapper(query, schema):
            query_hash = hash(query)
            cached_query = cached.get(query_hash)
            if cached_query:
                return cached_query

            result = func(query, schema)
            cached[query_hash] = result
            return result

        return wrapper

    Subscription("Subscription.countdown", schema_name=random_schema_name)(
        countdown_generator
    )

    schema = await create_schema(
        """
        type Query {
          foo: String
        }

        type Subscription {
          countdown(startAt: Int!): Int!
        }
        """,
        name=random_schema_name,
    )
    query = """
    subscription {
      countdown(startAt: 0)
    }
    """
    assert not cached
    subscribe = subscriptor_factory(schema, cache_decorator=my_cache_decorator)
    async for result in subscribe(query):
        assert result == {
            "data": {"countdown": 0,},
        }
    assert cached
    assert isinstance(cached[hash(query)], tuple)
    assert len(cached[hash(query)]) == 2
    assert isinstance(cached[hash(query)][0], DocumentNode)
    assert cached[hash(query)][1] == None


@pytest.mark.asyncio
async def test_subscriptor_factory_with_parser(random_schema_name):
    mocked_parser = Mock(wraps=parse_to_document)

    Subscription("Subscription.countdown", schema_name=random_schema_name)(
        countdown_generator
    )

    schema = await create_schema(
        """
        type Query {
          foo: String
        }

        type Subscription {
          countdown(startAt: Int!): Int!
        }
        """,
        name=random_schema_name,
    )
    subscribe = subscriptor_factory(schema, parser=mocked_parser)
    mocked_parser.assert_not_called()
    async for result in subscribe(
        """
        subscription {
          countdown(startAt: 0)
        }
        """
    ):
        assert result == {
            "data": {"countdown": 0,},
        }
    mocked_parser.assert_called_once()


@pytest.mark.asyncio
async def test_subscriptor_factory_with_rules(random_schema_name):
    mocked_rule = Mock(wraps=UniqueOperationNamesRule)

    Subscription("Subscription.countdown", schema_name=random_schema_name)(
        countdown_generator
    )

    schema = await create_schema(
        """
        type Query {
          foo: String
        }

        type Subscription {
          countdown(startAt: Int!): Int!
        }
        """,
        name=random_schema_name,
    )
    subscribe = subscriptor_factory(schema, rules=[mocked_rule])
    mocked_rule.assert_not_called()
    async for result in subscribe(
        """
        subscription {
          countdown(startAt: 0)
        }
        """
    ):
        assert result == {
            "data": {"countdown": 0,},
        }
    mocked_rule.assert_called_once()


@pytest.mark.asyncio
async def test_subscriptor_factory_with_invalid_query(random_schema_name):
    Subscription("Subscription.countdown", schema_name=random_schema_name)(
        countdown_generator
    )

    schema = await create_schema(
        """
        type Query {
          foo: String
        }

        type Subscription {
          countdown(startAt: Int!): Int!
        }
        """,
        name=random_schema_name,
    )
    subscribe = subscriptor_factory(schema)
    async for result in subscribe(
        """
        subscription {
          unknown
        }
        """
    ):
        assert result == {
            "data": None,
            "errors": [
                {
                    "message": "Cannot query field < unknown > on type < Subscription >.",
                    "path": None,
                    "locations": [{"line": 3, "column": 11}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.3.1",
                        "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    },
                }
            ],
        }
