from unittest.mock import Mock

import pytest

from tartiflette import Resolver, create_engine


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

    mock_one = Mock()
    mock_two = Mock()

    @Resolver("Test.field", schema_name="test_tartiflette_execute_basic")
    async def func_field_resolver(*_args, **_kwargs):
        mock_one()
        return None

    @Resolver(
        "RootQuery.testField", schema_name="test_tartiflette_execute_basic"
    )
    async def func_testfield_resolver(*_args, **_kwargs):
        return {}

    @Resolver(
        "RootQuery.defaultField", schema_name="test_tartiflette_execute_basic"
    )
    async def func_default_query_resolver(*_args, **_kwargs):
        mock_two()
        return 1

    ttftt = await create_engine(
        schema_sdl, schema_name="test_tartiflette_execute_basic"
    )

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
async def test_tartiflette_nested_resolvers():
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

    @Resolver(
        "Query.rootField", schema_name="test_tartiflette_nested_resolvers"
    )
    async def func_resolver(parent, arguments, request_ctx, info):
        return {"nestedField": "Nested ?"}

    @Resolver(
        "RootType.nestedField", schema_name="test_tartiflette_nested_resolvers"
    )
    async def func_resolver(parent, arguments, request_ctx, info):
        return {"endField": "Another"}

    @Resolver(
        "NestedType.endField", schema_name="test_tartiflette_nested_resolvers"
    )
    async def func_resolver(parent, arguments, request_ctx, info):
        return "Test"

    ttftt = await create_engine(
        schema_sdl, schema_name="test_tartiflette_nested_resolvers"
    )

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
async def test_tartiflette_execute_hello_world():
    schema_sdl = """
    type Query {
        hello: String!
    }
    """

    @Resolver(
        "Query.hello", schema_name="test_tartiflette_execute_hello_world"
    )
    async def func_field_resolver(parent, arguments, request_ctx, info):
        return "world"

    ttftt = await create_engine(
        schema_sdl, schema_name="test_tartiflette_execute_hello_world"
    )

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
