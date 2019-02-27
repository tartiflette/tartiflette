import asyncio

from unittest.mock import Mock

import pytest

from tartiflette.resolver.factory import default_error_coercer


def test_engine(clean_registry):
    from tartiflette.engine import Engine
    from tartiflette.schema.registry import SchemaRegistry

    e = Engine("type Query { a:String }")
    s = SchemaRegistry.find_schema()

    assert e._parser is not None
    assert s is not None
    assert s.name == "default"

    ee = Engine("type Query { a:String }", "Bob")
    ss = SchemaRegistry.find_schema("Bob")

    assert ee._parser is not None
    assert ss is not None
    assert ss.name == "Bob"

    assert ss != s


@pytest.mark.asyncio
async def test_engine_execute(clean_registry):
    from tartiflette.engine import Engine

    e = Engine("type Query { a:String }")

    result = await e.execute("query aquery { a }", operation_name="aquery")

    assert result == {"data": {"a": None}}


@pytest.mark.asyncio
async def test_engine_execute_parse_error(clean_registry):
    from tartiflette.engine import Engine

    e = Engine("type Query { a: String }")

    assert await e.execute("query { unknownNode1 unknownNode2 }") == {
        "data": None,
        "errors": [
            {
                "message": "field `Query.unknownNode1` was not found in GraphQL schema.",
                "path": ["unknownNode1"],
                "locations": [{"column": 9, "line": 1}],
            },
            {
                "message": "field `Query.unknownNode2` was not found in GraphQL schema.",
                "path": ["unknownNode2"],
                "locations": [{"column": 22, "line": 1}],
            },
        ],
    }


@pytest.mark.asyncio
async def test_engine_execute_custom_error_coercer(clean_registry):
    from tartiflette.engine import Engine

    def custom_error_coercer(exception):
        error = default_error_coercer(exception)
        error["message"] = error["message"] + "Custom"
        return error

    e = Engine("type Query { a: String }", error_coercer=custom_error_coercer)

    assert await e.execute("query { unknownNode1 unknownNode2 }") == {
        "data": None,
        "errors": [
            {
                "message": "field `Query.unknownNode1` was not found in GraphQL schema.Custom",
                "path": ["unknownNode1"],
                "locations": [{"column": 9, "line": 1}],
            },
            {
                "message": "field `Query.unknownNode2` was not found in GraphQL schema.Custom",
                "path": ["unknownNode2"],
                "locations": [{"column": 22, "line": 1}],
            },
        ],
    }


@pytest.mark.asyncio
async def test_engine_execute_empty_req_except(clean_registry):
    from tartiflette.engine import Engine

    e = Engine("type Query { a: String }")

    assert await e.execute("") == {
        "data": None,
        "errors": [
            {
                "message": "1.1: syntax error, unexpected EOF",
                "path": None,
                "locations": [],
            }
        ],
    }


@pytest.mark.asyncio
async def test_engine_execute_syntax_error(clean_registry):
    from tartiflette.engine import Engine

    e = Engine("type Query { a: String }")

    assert await e.execute("query { a { }") == {
        "data": None,
        "errors": [
            {
                "message": "1.12: unrecognized character \\xc2",
                "path": None,
                "locations": [],
            }
        ],
    }


@pytest.mark.asyncio
async def test_engine_execute_unhandled_exception(clean_registry):
    from tartiflette.engine import Engine

    e = Engine("type Query { a: Ninja } type Ninja { a: String }")

    assert (
        await e.execute(
            """
        fragment AFragment on Ninja { a }
        fragment AFragment on Ninja { a }
        query { a { } }
    """
        )
        == {
            "data": None,
            "errors": [
                {
                    "message": "4.20: unrecognized character \\xc2",
                    "path": None,
                    "locations": [],
                }
            ],
        }
    )


@pytest.mark.asyncio
async def test_engine_execute_custom_resolver(clean_registry):
    from tartiflette.engine import Engine

    a = Mock()

    async def custom_default_resolver(*args, **kwargs):
        a(args, kwargs)

        return "customed!"

    e = Engine(
        "type Query { a:String }",
        custom_default_resolver=custom_default_resolver,
    )

    assert (
        e._schema.find_type("Query").find_field("a").resolver._raw_func
        is custom_default_resolver
    )
    assert await e.execute("query { a }") == {"data": {"a": "customed!"}}
    assert a.called


@pytest.mark.asyncio
async def test_engine_subscribe(clean_registry):
    from tartiflette import Engine, Subscription, Resolver

    @Subscription("Subscription.counter", schema_name="subscribe_counter")
    async def _subscription_counter_subscription(
        parent_result, args, *_args, **_kwargs
    ):
        start_at = args["startAt"]
        while start_at > 0:
            await asyncio.sleep(0.01)
            start_at -= 1
            yield start_at

    @Resolver("Subscription.counter", schema_name="subscribe_counter")
    async def _subscription_counter_query(parent_result, *_args, **_kwargs):
        return parent_result

    e = Engine(
        """
        type Query {
          a: String
        }
        
        type Subscription {
          counter(startAt: Int!): Int!
        }
        """,
        schema_name="subscribe_counter",
    )

    expected_values = list(range(4))

    async for result in e.subscribe("subscription { counter(startAt: 4) }"):
        assert result == {"data": {"counter": expected_values.pop()}}


@pytest.mark.asyncio
async def test_engine_subscribe_with_default_resolver(clean_registry):
    from tartiflette import Engine, Subscription, Resolver

    @Subscription("Subscription.counter", schema_name="subscribe_counter")
    async def _subscription_counter_subscription(
        parent_result, args, *_args, **_kwargs
    ):
        start_at = args["startAt"]
        while start_at > 0:
            await asyncio.sleep(0.01)
            start_at -= 1
            yield start_at

    e = Engine(
        """
        type Query {
          a: String
        }

        type Subscription {
          counter(startAt: Int!): Int!
        }
        """,
        schema_name="subscribe_counter",
    )

    expected_values = list(range(4))

    async for result in e.subscribe("subscription { counter(startAt: 4) }"):
        assert result == {"data": {"counter": expected_values.pop()}}


@pytest.mark.asyncio
async def test_engine_subscribe_with_default_resolver_alias(clean_registry):
    from tartiflette import Engine, Subscription, Resolver

    @Subscription("Subscription.counter", schema_name="subscribe_counter")
    async def _subscription_counter_subscription(
        parent_result, args, *_args, **_kwargs
    ):
        start_at = args["startAt"]
        while start_at > 0:
            await asyncio.sleep(0.01)
            start_at -= 1
            yield start_at

    e = Engine(
        """
        type Query {
          a: String
        }

        type Subscription {
          counter(startAt: Int!): Int!
        }
        """,
        schema_name="subscribe_counter",
    )

    expected_values = list(range(4))

    async for result in e.subscribe("subscription { aliasCounter: counter(startAt: 4) }"):
        assert result == {"data": {"aliasCounter": expected_values.pop()}}
