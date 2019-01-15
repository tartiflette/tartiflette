from unittest.mock import Mock

import pytest

from tartiflette.engine import Engine
from tartiflette.resolver import Resolver


@pytest.mark.asyncio
async def test_tartiflette_execute_basic(clean_registry):
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

    mock_one = Mock()
    mock_two = Mock()

    @Resolver("Test.field")
    async def func_field_resolver(parent, arguments, request_ctx, info):
        mock_one()
        return None

    @Resolver("RootQuery.defaultField")
    async def func_default_query_resolver(
        parent, arguments, request_ctx, info
    ):
        mock_two()
        return

    ttftt = Engine(schema_sdl)

    result = await ttftt.execute(
        """
    query Test{
        testField {
            field
        }
    }
    """
    )

    assert result == {"data": {"testField": {"field": None}}}
    assert mock_one.called is True
    assert mock_two.called is False


@pytest.mark.asyncio
async def test_tartiflette_nested_resolvers(clean_registry):
    schema_sdl = """
    type Query {
        rootField: RootType
    }

    type RootType {
        nestedField: NestedType
    }

    type NestedType {
        endField: String
    }
    """

    @Resolver("Query.rootField")
    async def func_resolver(parent, arguments, request_ctx, info):
        return {"nestedField": "Nested ?"}

    @Resolver("RootType.nestedField")
    async def func_resolver(parent, arguments, request_ctx, info):
        return {"endField": "Another"}

    @Resolver("NestedType.endField")
    async def func_resolver(parent, arguments, request_ctx, info):
        return "Test"

    ttftt = Engine(schema_sdl)

    result = await ttftt.execute(
        """
    query Test{
        rootField {
            nestedField {
                endField
            }
        }
    }
    """
    )

    assert result == {
        "data": {"rootField": {"nestedField": {"endField": "Test"}}}
    }


@pytest.mark.asyncio
async def test_tartiflette_execute_hello_world(clean_registry):
    schema_sdl = """
    type Query {
        hello: String!
    }
    """

    @Resolver("Query.hello")
    async def func_field_resolver(parent, arguments, request_ctx, info):
        return "world"

    ttftt = Engine(schema_sdl)

    result = await ttftt.execute(
        """
    query Test{
        hello
    }
    """
    )

    assert {"data": {"hello": "world"}} == result

    # Try twice to be sure everything works mutliple times
    result = await ttftt.execute(
        """
        query Test{
            hello
        }
        """
    )

    assert {"data": {"hello": "world"}} == result
