import pytest


def test_engine(clean_registry):
    from tartiflette.engine import Engine
    from tartiflette.schema.registry import SchemaRegistry

    e = Engine("type Query { a:String }")

    assert e._parser is not None
    assert SchemaRegistry.find_schema() is not None

    ee = Engine("type Query { a:String }", "Bob")

    assert ee._parser is not None
    assert SchemaRegistry.find_schema("Bob") is not None


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
