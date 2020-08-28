import pytest

from tartiflette import Resolver, create_schema
from tartiflette.types.exceptions.tartiflette import ImproperlyConfigured


def bakery(schema_name):
    @Resolver("Node.id", schema_name=schema_name)
    async def resolve_node_id(parent, args, ctx, info):
        return f"{info.parent_type.name}.{parent.get('id')}"

    @Resolver("Identifiable.id", schema_name=schema_name)
    async def resolve_identifiable_id(parent, args, ctx, info):
        return parent.get("id")

    @Resolver("Query.foo", schema_name=schema_name)
    async def resolve_query_foo(parent, args, ctx, info):
        return {"id": 1, "name": "Foo"}

    @Resolver("Query.bar", schema_name=schema_name)
    async def resolve_query_bar(parent, args, ctx, info):
        return {"id": 1, "name": "Bar"}


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    type Foo implements Named {
      name: String!
    }

    extend type Foo implements Node & Identifiable {
      id: ID!
    }

    type Bar implements Named {
      id: ID!
      name: String!
    }

    interface Node {
      id: ID!
    }

    interface Identifiable {
      id: ID!
    }

    interface Named {
      name: String!
    }

    type Query {
      foo: Foo!
      bar: Bar!
    }
    """,
    bakery=bakery,
)
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            {
              foo {
                id
                name
              }
            }
            """,
            {"data": {"foo": {"id": "Foo.1", "name": "Foo"}}},
        ),
        (
            """
            {
              bar {
                id
                name
              }
            }
            """,
            {"data": {"bar": {"id": "1", "name": "Bar"}}},
        ),
    ],
)
async def test_issue429(schema_stack, query, expected):
    assert await schema_stack.execute(query) == expected
