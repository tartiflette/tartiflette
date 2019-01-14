import pytest
from unittest.mock import Mock


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

    result = await e.execute("query aquery { a }")

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
                "locations": [
                    {
                        "column": 9,
                        "line": 1,
                    },
                ],
            },
            {
                "message": "field `Query.unknownNode2` was not found in GraphQL schema.",
                "path": ["unknownNode1", "unknownNode2"],
                "locations": [
                    {
                        "column": 22,
                        "line": 1,
                    },
                ],
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
                "message": "Server encountered an error.",
                "path": None,
                "locations": [],
            },
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
                "message": "Server encountered an error.",
                "path": None,
                "locations": [],
            },
        ],
    }


@pytest.mark.asyncio
async def test_engine_execute_unhandled_exception(clean_registry):
    from tartiflette.engine import Engine

    e = Engine("type Query { a: Ninja } type Ninja { a: String }")

    assert await e.execute("""
        fragment AFragment on Ninja { a }
        fragment AFragment on Ninja { a }
        query { a { } }
    """) == {
        "data": None,
        "errors": [
            {
                "message": "Server encountered an error.",
                "path": None,
                "locations": [],
            },
        ],
    }


@pytest.mark.asyncio
async def test_engine_execute_custom_resolver(clean_registry):
    from tartiflette.engine import Engine

    a = Mock()

    async def custom_default_resolver(*args, **kwargs):
        a(args, kwargs)

        return "customed!"

    e = Engine("type Query { a:String }", custom_default_resolver=custom_default_resolver)

    assert e._schema.find_type("Query").find_field("a").resolver._raw_func is custom_default_resolver
    assert await e.execute("query { a }") == {"data": {"a": "customed!"}}
    assert a.called
