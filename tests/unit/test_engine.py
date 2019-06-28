import asyncio

from unittest.mock import Mock

import pytest

from tartiflette import create_engine


@pytest.mark.asyncio
async def test_engine(clean_registry):
    from tartiflette.schema.registry import SchemaRegistry

    e = await create_engine("type Query { a:String }")
    s = SchemaRegistry.find_schema()

    assert e._parser is not None
    assert s is not None
    assert s.name == "default"

    ee = await create_engine("type Query { a:String }", "Bob")
    ss = SchemaRegistry.find_schema("Bob")

    assert ee._parser is not None
    assert ss is not None
    assert ss.name == "Bob"

    assert ss != s


@pytest.mark.asyncio
async def test_engine_execute(clean_registry):
    e = await create_engine("type Query { a:String }")

    result = await e.execute("query aquery { a }", operation_name="aquery")

    assert result == {"data": {"a": None}}


@pytest.mark.asyncio
async def test_engine_execute_parse_error(clean_registry):
    e = await create_engine("type Query { a: String }")

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
    def custom_error_coercer(exception, error):
        error["message"] = error["message"] + "Custom"
        return error

    e = await create_engine(
        "type Query { a: String }", error_coercer=custom_error_coercer
    )

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
    e = await create_engine("type Query { a: String }")

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
    e = await create_engine("type Query { a: String }")

    assert await e.execute("query { a {}") == {
        "data": None,
        "errors": [
            {
                "message": "1.12: syntax error, unexpected }",
                "path": None,
                "locations": [],
            }
        ],
    }


@pytest.mark.asyncio
async def test_engine_execute_unhandled_exception(clean_registry):
    e = await create_engine("type Query { a: Ninja } type Ninja { a: String }")

    assert (
        await e.execute(
            """
        fragment AFragment on Ninja { a }
        fragment AFragment on Ninja { a }
        query { a {} }
    """
        )
        == {
            "data": None,
            "errors": [
                {
                    "message": "4.20: syntax error, unexpected }",
                    "path": None,
                    "locations": [],
                }
            ],
        }
    )


@pytest.mark.asyncio
async def test_engine_execute_custom_resolver(clean_registry):
    a = Mock()

    async def custom_default_resolver(*args, **kwargs):
        a(args, kwargs)

        return "customed!"

    e = await create_engine(
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
    from tartiflette import Subscription, Resolver

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

    e = await create_engine(
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
    from tartiflette import Subscription, Resolver

    @Subscription("Subscription.counter", schema_name="subscribe_counter")
    async def _subscription_counter_subscription(
        parent_result, args, *_args, **_kwargs
    ):
        start_at = args["startAt"]
        while start_at > 0:
            await asyncio.sleep(0.01)
            start_at -= 1
            yield start_at

    e = await create_engine(
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
    from tartiflette import Subscription, Resolver

    @Subscription("Subscription.counter", schema_name="subscribe_counter")
    async def _subscription_counter_subscription(
        parent_result, args, *_args, **_kwargs
    ):
        start_at = args["startAt"]
        while start_at > 0:
            await asyncio.sleep(0.01)
            start_at -= 1
            yield start_at

    e = await create_engine(
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

    async for result in e.subscribe(
        "subscription { aliasCounter: counter(startAt: 4) }"
    ):
        assert result == {"data": {"aliasCounter": expected_values.pop()}}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl,expected,pass_to",
    [
        ("type Query { lol: Int }", "ok", "engine"),
        ("type Query { lol: Int }", "ok", "cook"),
        (None, Exception(), "None"),
    ],
)
async def test_engine_api_sdl(sdl, expected, pass_to, clean_registry):
    from tartiflette import Engine

    if pass_to == "engine":
        e = Engine(sdl)
    else:
        e = Engine()

    if isinstance(expected, Exception):
        with pytest.raises(Exception):
            if pass_to == "cook":
                await e.cook(sdl)
            else:
                await e.cook()
    else:
        if pass_to == "cook":
            await e.cook(sdl)
        else:
            await e.cook()
        assert e._schema is not None


async def bob():
    pass


def boby():
    pass


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "cdr,expected,pass_to",
    [
        (bob, "ok", "engine"),
        (bob, "ok", "cook"),
        (boby, Exception(), "engine"),
        (boby, Exception(), "cook"),
    ],
)
async def test_engine_api_cdr(cdr, expected, pass_to, clean_registry):
    from tartiflette import Engine

    sdl = "type Query { lol: Int }"

    if pass_to == "engine":
        e = Engine(sdl, custom_default_resolver=cdr)
    else:
        e = Engine()

    if isinstance(expected, Exception):
        with pytest.raises(Exception):
            if pass_to == "cook":
                await e.cook(sdl, custom_default_resolver=cdr)
            else:
                await e.cook()
    else:
        if pass_to == "cook":
            await e.cook(sdl, custom_default_resolver=cdr)
        else:
            await e.cook()
        assert e._schema is not None
