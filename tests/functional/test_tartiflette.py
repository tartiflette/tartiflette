from unittest.mock import Mock

import pytest

from tartiflette import Resolver, create_engine


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
    async def func_field_resolver(*_args, **_kwargs):
        mock_one()
        return None

    @Resolver("RootQuery.testField")
    async def func_testfield_resolver(*_args, **_kwargs):
        return {}

    @Resolver("RootQuery.defaultField")
    async def func_default_query_resolver(*_args, **_kwargs):
        mock_two()
        return 1

    ttftt = await create_engine(schema_sdl)

    result = await ttftt.execute(
        """
    query Test{
        testField {
            field
        }
    }
    """,
        operation_name="Test",
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

    ttftt = await create_engine(schema_sdl)

    result = await ttftt.execute(
        """
    query Test{
        rootField {
            nestedField {
                endField
            }
        }
    }
    """,
        operation_name="Test",
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

    ttftt = await create_engine(schema_sdl)

    result = await ttftt.execute(
        """
    query Test{
        hello
    }
    """,
        operation_name="Test",
    )

    assert {"data": {"hello": "world"}} == result

    # Try twice to be sure everything works mutliple times
    result = await ttftt.execute(
        """
        query Test{
            hello
        }
        """,
        operation_name="Test",
    )

    assert {"data": {"hello": "world"}} == result
