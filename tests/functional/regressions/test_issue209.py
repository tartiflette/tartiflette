from typing import Any, Callable, Dict, Optional, Union

import pytest

from tartiflette import Directive, Resolver


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


def bakery(schema_name):
    @Directive("validateLimit", schema_name=schema_name)
    class ValidateLimitDirective:
        @staticmethod
        async def on_post_argument_coercion(
            directive_args: Dict[str, Any],
            next_directive: Callable,
            parent_node: Union["FieldNode", "DirectiveNode"],
            argument_definition_node: "InputValueDefinitionNode",
            value: Any,
            ctx: Optional[Any],
        ):
            value = await next_directive(
                parent_node, argument_definition_node, value, ctx,
            )
            if value > directive_args["limit"]:
                raise LimitReachedException("Limit has been reached")
            return value

    @Resolver("Query.aList", schema_name=schema_name)
    async def resolver_query_a_list(parent, args, ctx, info):
        nb_items = args["nbItems"]
        return [f"{nb_items}.{index}" for index in range(nb_items)]


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    directive @validateLimit(
      limit: Int!
    ) on ARGUMENT_DEFINITION | INPUT_FIELD_DEFINITION

    type Query {
      aList(
        nbItems: Int! @validateLimit(limit: 2)
      ): [String!]
    }
    """,
    bakery=bakery,
)
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
async def test_issue209(schema_stack, query, expected):
    assert await schema_stack.execute(query) == expected
