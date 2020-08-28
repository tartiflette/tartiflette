from unittest.mock import Mock

import pytest

from tartiflette import Resolver, create_schema_with_operators
from tartiflette.schema.bakery import SchemaBakery
from tartiflette.schema.factory import _import_builtins, create_schema
from tartiflette.types.exceptions.tartiflette import (
    ImproperlyConfigured,
    NonAwaitableResolver,
)


@pytest.mark.asyncio
async def test_resolver_decorator(clean_registry):
    schema_sdl = """
    schema {
        query: RootQuery
    }

    type Foo {
        a: String
    }

    type Bar {
        b: String
    }

    type Baz {
        c: String
    }

    union Group = Foo | Bar | Baz

    interface Something {
        oneField: [Int]
        anotherField: [String]
        aLastOne: [[Date!]]!
    }

    input UserInfo {
        name: String
        dateOfBirth: [Date]
        graphQLFan: Boolean!
    }

    type RootQuery {
        defaultField: Int
    }

    # Query has been replaced by RootQuery as entrypoint
    type Query {
        nonDefaultField: String
    }

    \"\"\"
    This is a docstring for the Test Object Type.
    \"\"\"
    type Test {
        \"\"\"
        This is a field description :D
        \"\"\"
        field(input: UserInfo): String!
        anotherField: [Int]
        fieldWithDefaultValueArg(test: String = "default"): ID
        simpleField: Date
    }
    """

    _, schema_sdl = await _import_builtins([], schema_sdl, "default")

    clean_registry.register_sdl("default", schema_sdl)

    mock_one = Mock()
    mock_two = Mock()

    @Resolver("Test.field")
    async def func_field_resolver(*args, **kwargs):
        mock_one()
        return

    @Resolver("RootQuery.defaultField")
    async def func_default_resolver(*args, **kwargs):
        mock_two()
        return

    with pytest.raises(NonAwaitableResolver):

        @Resolver("Test.simpleField")
        def func_default_resolver(*args, **kwargs):
            pass

    generated_schema = await SchemaBakery.bake("default")

    assert (
        generated_schema.get_field_by_name("Test.field").resolver is not None
    )
    assert callable(generated_schema.get_field_by_name("Test.field").resolver)
    assert mock_one.called is False
    assert (
        generated_schema.get_field_by_name("RootQuery.defaultField").resolver
        is not None
    )
    assert callable(
        generated_schema.get_field_by_name("RootQuery.defaultField").resolver
    )
    assert mock_two.called is False


@pytest.mark.asyncio
async def test_resolver_decorator_interface_with_type_resolver():
    @Resolver(
        "Node.id",
        type_resolver=lambda *_, **__: "Nodeuh",
        schema_name="test_resolver_decorator_interface_with_type_resolver",
    )
    async def resolve_node_id(parent, args, ctx, info):
        return f"{info.parent_type.name}.{parent.get('id')}"

    with pytest.raises(
        ImproperlyConfigured,
        match=(
            "< type_resolver > parameter shouldn't be defined on < Node > "
            "interface type."
        ),
    ):
        await create_schema(
            sdl="""
            interface Node {
              id: ID!
            }

            type Query {
              node(id: ID!): Node
            }
            """,
            name="test_resolver_decorator_interface_with_type_resolver",
        )


@pytest.mark.asyncio
async def test_resolver_decorator_type_resolver_on_non_abstract():
    @Resolver(
        "Foo.id",
        type_resolver=lambda *_, **__: "Fooeuh",
        schema_name="test_resolver_decorator_type_resolver_on_non_abstract",
    )
    async def resolve_foo_id(parent, args, ctx, info):
        return f"{info.parent_type.name}.{parent.get('id')}"

    with pytest.raises(
        ImproperlyConfigured,
        match=(
            "type_resolver > parameter shouldn't be defined on non abastract "
            "< Foo.id > field."
        ),
    ):
        await create_schema(
            sdl="""
            type Foo {
              id: ID!
            }

            type Query {
              foo(id: ID!): Foo
            }
            """,
            name="test_resolver_decorator_type_resolver_on_non_abstract",
        )


@pytest.mark.asyncio
async def test_resolver_decorator_type_resolver_on_abstract():
    @Resolver(
        "Query.node",
        type_resolver=lambda *_, **__: "Foo",
        schema_name="test_resolver_decorator_type_resolver_on_abstract",
    )
    async def resolve_query_node(parent, args, ctx, info):
        return {"id": "1"}

    schema, execute, _ = await create_schema_with_operators(
        sdl="""
        interface Node {
          id: ID!
        }

        type Foo implements Node {
          id: ID!
        }

        type Query {
          node(id: ID!): Node
        }
        """,
        name="test_resolver_decorator_type_resolver_on_abstract",
    )

    assert await execute('{ node(id: "1") { __typename id } }') == {
        "data": {"node": {"__typename": "Foo", "id": "1"}}
    }
