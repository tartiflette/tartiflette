from unittest.mock import Mock

import pytest

from tartiflette import Resolver, create_schema_with_operationers


@pytest.mark.asyncio
async def test_tartiflette_execute_basic():
    mock_one = Mock()
    mock_two = Mock()

    @Resolver("Test.field", schema_name="test_tartiflette_execute_basic")
    async def resolve_test_field(*_args, **_kwargs):
        mock_one()
        return None

    @Resolver(
        "RootQuery.testField", schema_name="test_tartiflette_execute_basic"
    )
    async def resolve_root_query_test_field(*_args, **_kwargs):
        return {}

    @Resolver(
        "RootQuery.defaultField", schema_name="test_tartiflette_execute_basic"
    )
    async def resolve_root_query_default_field(*_args, **_kwargs):
        mock_two()
        return 1

    _, execute, __ = await create_schema_with_operationers(
        """
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
        """,
        name="test_tartiflette_execute_basic",
    )

    assert (
        await execute(
            """
            query Test {
                testField {
                    field
                }
            }
            """,
            operation_name="Test",
        )
        == {"data": {"testField": {"field": None}}}
    )
    assert mock_one.called is True
    assert mock_two.called is False


def tartiflette_nested_resolvers_bakery(schema_name):
    @Resolver("Query.rootField", schema_name=schema_name)
    async def resolve_query_root_field(parent, arguments, request_ctx, info):
        return {"nestedField": "Nested ?"}

    @Resolver("RootType.nestedField", schema_name=schema_name)
    async def resolve_root_type_nested_field(
        parent, arguments, request_ctx, info
    ):
        return {"endField": "Another"}

    @Resolver("NestedType.endField", schema_name=schema_name)
    async def resolve_nested_type_end_field(
        parent, arguments, request_ctx, info
    ):
        return "Test"


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    type Query {
        rootField: RootType
    }

    type RootType {
        nestedField: NestedType
    }

    type NestedType {
        endField: String
    }
    """,
    bakery=tartiflette_nested_resolvers_bakery,
)
async def test_tartiflette_nested_resolvers(schema_stack):
    assert (
        await schema_stack.execute(
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
        == {"data": {"rootField": {"nestedField": {"endField": "Test"}}}}
    )


def tartiflette_execute_hello_world_bakery(schema_name):
    @Resolver("Query.hello", schema_name=schema_name)
    async def resolve_query_hello(parent, arguments, request_ctx, info):
        return "world"


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    type Query {
        hello: String!
    }
    """,
    bakery=tartiflette_execute_hello_world_bakery,
)
async def test_tartiflette_execute_hello_world(schema_stack):
    assert (
        await schema_stack.execute(
            """
            query Test{
                hello
            }
            """,
            operation_name="Test",
        )
        == {"data": {"hello": "world"}}
    )

    assert (
        await schema_stack.execute(
            """
            query Test{
                hello
            }
            """,
            operation_name="Test",
        )
        == {"data": {"hello": "world"}}
    )
