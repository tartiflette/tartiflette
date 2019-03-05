import logging

from typing import Any, Callable, Dict, Optional

import pytest

from tartiflette import Engine, Resolver
from tartiflette.directive import CommonDirective, Directive

logger = logging.getLogger(__name__)


@Directive("maxLength", schema_name="test_issue133")
class MaxLengthDirective(CommonDirective):
    @staticmethod
    async def on_argument_execution(
        directive_args: Dict[str, Any],
        next_directive: Callable,
        argument_definition: "GraphQLArgument",
        args: Dict[str, Any],
        ctx: Optional[Dict[str, Any]],
        info: "Info",
    ) -> Any:
        result = await next_directive(argument_definition, args, ctx, info)
        if len(result) > directive_args["limit"]:
            raise Exception(
                "Value of argument < %s > on field < %s > is too long ("
                "%s/%s)."
                % (
                    argument_definition.name,
                    info.schema_field.name,
                    len(result),
                    directive_args["limit"],
                )
            )
        return result


@Resolver("Query.search", schema_name="test_issue133")
async def _query_search_resolver(parent_result, args, *_, **__):
    return [args["query"]]


_SDL = """
directive @maxLength(
  limit: Int!
) on ARGUMENT_DEFINITION

type Query {
  search(
    query: String @maxLength(limit: 10)
  ): [String]
}
"""


_TTFTT_ENGINE = Engine(_SDL, schema_name="test_issue133")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            query {
              search(query: "Query too long")
            }
            """,
            {
                "data": {"search": None},
                "errors": [
                    {
                        "message": "Value of argument < query > on field < "
                        "search > is too long (14/10).",
                        "locations": [{"line": 3, "column": 15}],
                        "path": ["search"],
                    }
                ],
            },
        )
    ],
)
async def test_issue133(query, expected):
    assert await _TTFTT_ENGINE.execute(query) == expected
