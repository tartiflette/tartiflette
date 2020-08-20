import json as json_module

from functools import partial

import pytest

from tartiflette import Resolver
from tartiflette.language.parsers.libgraphqlparser import parse_to_document

_CALLED = False


def my_loader(a_str, *_args, **_kwargs):
    global _CALLED
    _CALLED = True
    return json_module.loads(a_str)


def bakery(schema_name):
    @Resolver("Query.hello", schema_name=schema_name)
    async def resolve_query_world(parent, args, ctx, info):
        return f"Hello {args['name']}"


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    type Query {
      hello(name: String!): String
    }
    """,
    query_parser=partial(parse_to_document, json_loader=my_loader),
    bakery=bakery,
)
async def test_issue362(schema_stack):
    assert not _CALLED
    assert (
        await schema_stack.execute(
            """
            query {
              hello(name: "John")
            }
            """
        )
        == {"data": {"hello": "Hello John"}}
    )
    assert _CALLED
