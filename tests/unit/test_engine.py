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
async def test_engine_execute_empty_req_except(clean_registry):
    from tartiflette.engine import Engine

    e = Engine("type Query { a:String }")

    with pytest.raises(Exception):
        await e.execute("")


@pytest.mark.asyncio
async def test_engine_execute_syntax_error(clean_registry):
    from tartiflette.engine import Engine

    e = Engine("type Query { a:String }")

    with pytest.raises(Exception):
        await e.execute("query { a { }")


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
