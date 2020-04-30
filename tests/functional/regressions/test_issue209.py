from typing import Any, Callable, Dict, Optional, Union

import pytest

from tartiflette import Directive, Resolver, create_engine


class LimitReachedException(Exception):
    def coerce_value(self, *_args, path=None, locations=None, **_kwargs):
        computed_locations = []
        try:
            for location in locations:
                computed_locations.append(location.collect_value())
        except AttributeError:
            pass
        except TypeError:
            pass

        return {
            "message": "Limit reached",
            "path": path,
            "locations": computed_locations,
            "type": "bad_request",
        }


_SDL = """
directive @validateLimit(
  limit: Int!
) on ARGUMENT_DEFINITION | INPUT_FIELD_DEFINITION

type Query {
  aList(
    nbItems: Int! @validateLimit(limit: 2)
  ): [String!]
}
"""


@pytest.fixture(scope="module")
async def ttftt_engine():
    @Directive("validateLimit", schema_name="test_issue209")
    class ValidateLimitDirective:
        @staticmethod
        async def on_argument_execution(
            directive_args: Dict[str, Any],
            next_directive: Callable,
            parent_node: Union["FieldNode", "DirectiveNode"],
            argument_definition_node: "InputValueDefinitionNode",
            argument_node: Optional["ArgumentNode"],
            value: Any,
            ctx: Optional[Any],
        ):
            value = await next_directive(
                parent_node,
                argument_definition_node,
                argument_node,
                value,
                ctx,
            )
            if value > directive_args["limit"]:
                raise LimitReachedException("Limit has been reached")
            return value

    @Resolver("Query.aList", schema_name="test_issue209")
    async def resolver_query_a_list(parent, args, ctx, info):
        nb_items = args["nbItems"]
        return [f"{nb_items}.{index}" for index in range(nb_items)]

    return await create_engine(sdl=_SDL, schema_name="test_issue209")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            query {
              aList(nbItems: 3)
            }
            """,
            {
                "data": {"aList": None},
                "errors": [
                    {
                        "message": "Limit reached",
                        "path": ["aList"],
                        "locations": [{"line": 3, "column": 21}],
                        "type": "bad_request",
                    }
                ],
            },
        )
    ],
)
async def test_issue209(ttftt_engine, query, expected):
    assert await ttftt_engine.execute(query) == expected
