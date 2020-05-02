import logging

import pytest

from tartiflette import Directive, Resolver, create_engine

logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
async def ttftt_engine():
    sdl = """
    directive @appendArgumentName on ARGUMENT_DEFINITION
    directive @prependArgumentName on ARGUMENT_DEFINITION

    type Query {
      hello(
        identifier: String! = "Unknown" @prependArgumentName @appendArgumentName
      ): String!
    }
    """

    @Directive("appendArgumentName", schema_name="test_issue365")
    class AppendArgumentNameDirective:
        @staticmethod
        async def on_argument_execution(
            directive_args,
            next_directive,
            parent_node,
            argument_definition_node,
            argument_node,
            value,
            ctx,
        ):
            return await next_directive(
                parent_node,
                argument_definition_node,
                argument_node,
                f"{value}.{argument_definition_node.name.value}",
                ctx,
            )

    @Directive("prependArgumentName", schema_name="test_issue365")
    class PrependArgumentNameDirective:
        @staticmethod
        async def on_argument_execution(
            directive_args,
            next_directive,
            parent_node,
            argument_definition_node,
            argument_node,
            value,
            ctx,
        ):
            return await next_directive(
                parent_node,
                argument_definition_node,
                argument_node,
                f"{argument_definition_node.name.value}.{value}",
                ctx,
            )

    @Resolver("Query.hello", schema_name="test_issue365")
    async def resolve_query_hello(parent, args, ctx, info):
        return f"Hello < {args['identifier']} >"

    return await create_engine(sdl, schema_name="test_issue365")


@pytest.mark.asyncio
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
async def test_issue365(ttftt_engine, query, variables, expected):
    assert await ttftt_engine.execute(query, variables=variables) == expected
