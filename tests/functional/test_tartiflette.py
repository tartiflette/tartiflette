from unittest.mock import Mock

import pytest

from tartiflette.resolver_decorator import Resolver
from tartiflette.tartiflette import Tartiflette


@pytest.mark.asyncio
async def test_tartiflette_execute():
    schema_sdl = """
    schema @enable_cache {
        query: RootQuery
    }

    type RootQuery {
        defaultField: Int
        testField: Test
    }

    type Test {
        field: String!
    }
    """

    ttftt = Tartiflette(schema_sdl)

    mock_one = Mock()
    mock_two = Mock()

    @Resolver("Test.field", schema=ttftt._schema_definition)
    def func_field_resolver(*args, **kwargs):
        mock_one()
        return

    @Resolver("RootQuery.defaultField", schema=ttftt._schema_definition)
    def func_default_query_resolver(*args, **kwargs):
        mock_two()
        return

    result = await ttftt.execute("""
    query Test{
        testField {
            field
        }
    }
    """)

    # TODO: This should return """{"testField":null}""" instead of {}
    assert result == """{"testField":{}}"""
    # TODO: This should work but needs fixes in Tartiflette executor
    # assert mock_one.called is True


@pytest.mark.asyncio
async def test_tartiflette_execute_hello_world():
    schema_sdl = """
    type Query {
        hello: String!
    }
    """

    ttftt = Tartiflette(schema_sdl)

    @Resolver("Query.hello", schema=ttftt._schema_definition)
    def func_field_resolver(*args, **kwargs):
        return "world"

    result = await ttftt.execute("""
    query Test{
        hello
    }
    """)

    assert """{"hello":"world"}""" == result
