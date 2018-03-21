from unittest.mock import Mock

import pytest

from tartiflette.sdl.query_resolver import QueryResolver
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

    @QueryResolver("Test.field", schema=ttftt._schema_definition)
    def func_field_resolver(*args, **kwargs):
        mock_one()
        return

    @QueryResolver("defaultField", schema=ttftt._schema_definition)
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

    assert result == """{"testField":{}}"""
    assert mock_one.called is True
    # assert mock_two.called is True


