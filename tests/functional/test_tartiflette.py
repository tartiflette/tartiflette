from unittest.mock import Mock

import pytest

from tartiflette.resolver_decorator import Resolver
from tartiflette.tartiflette import Tartiflette


@pytest.mark.asyncio
async def test_tartiflette_execute_basic():
    schema_sdl = """
    schema {
        query: RootQuery
    }

    type RootQuery {
        defaultField: Int
        testField: Test
    }

    type Test {
        field: String
    }
    """

    ttftt = Tartiflette(schema_sdl)

    mock_one = Mock()
    mock_two = Mock()

    @Resolver("Test.field", schema=ttftt.schema_definition)
    async def func_field_resolver(*args, **kwargs):
        mock_one()
        return

    @Resolver("RootQuery.defaultField", schema=ttftt.schema_definition)
    async def func_default_query_resolver(*args, **kwargs):
        mock_two()
        return

    result = await ttftt.execute("""
    query Test{
        testField {
            field
        }
    }
    """)

    assert result == """{"testField":{"field":null}}"""
    assert mock_one.called is True
    assert mock_two.called is False


@pytest.mark.asyncio
async def test_tartiflette_execute_hello_world():
    schema_sdl = """
    type Query {
        hello: String!
    }
    """

    ttftt = Tartiflette(schema_sdl)

    @Resolver("Query.hello", schema=ttftt.schema_definition)
    async def func_field_resolver(*args, **kwargs):
        return "world"

    result = await ttftt.execute("""
    query Test{
        hello
    }
    """)

    assert """{"hello":"world"}""" == result
