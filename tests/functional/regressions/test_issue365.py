import pytest

from tartiflette import Directive, Resolver


def bakery(schema_name):
    @Directive("appendArgumentName", schema_name=schema_name)
    class AppendArgumentNameDirective:
        @staticmethod
        async def on_post_argument_coercion(
            directive_args,
            next_directive,
            parent_node,
            argument_definition_node,
            value,
            ctx,
        ):
            return await next_directive(
                parent_node,
                argument_definition_node,
                f"{value}.{argument_definition_node.name.value}",
                ctx,
            )

    @Directive("prependArgumentName", schema_name=schema_name)
    class PrependArgumentNameDirective:
        @staticmethod
        async def on_post_argument_coercion(
            directive_args,
            next_directive,
            parent_node,
            argument_definition_node,
            value,
            ctx,
        ):
            return await next_directive(
                parent_node,
                argument_definition_node,
                f"{argument_definition_node.name.value}.{value}",
                ctx,
            )

    @Resolver("Query.hello", schema_name=schema_name)
    async def resolve_query_hello(parent, args, ctx, info):
        return f"Hello < {args['identifier']} >"


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    directive @appendArgumentName on ARGUMENT_DEFINITION
    directive @prependArgumentName on ARGUMENT_DEFINITION

    type Query {
      hello(
        identifier: String! = "Unknown" @prependArgumentName @appendArgumentName
      ): String!
    }
    """,
    bakery=bakery,
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """
            query {
              hello
            }
            """,
            {},
            {"data": {"hello": "Hello < identifier.Unknown.identifier >"}},
        ),
        (
            """
            query {
              hello(identifier: "John")
            }
            """,
            {},
            {"data": {"hello": "Hello < identifier.John.identifier >"}},
        ),
        (
            """
            query ($identifier: String! = "Oops") {
              hello(identifier: $identifier)
            }
            """,
            {},
            {"data": {"hello": "Hello < identifier.Oops.identifier >"}},
        ),
        (
            """
            query ($identifier: String! = "Unknown") {
              hello(identifier: $identifier)
            }
            """,
            {"identifier": "John"},
            {"data": {"hello": "Hello < identifier.John.identifier >"}},
        ),
    ],
)
async def test_issue365(schema_stack, query, variables, expected):
    assert await schema_stack.execute(query, variables=variables) == expected
