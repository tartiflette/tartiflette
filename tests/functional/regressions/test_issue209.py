import pytest

from tartiflette import Directive, Engine, Resolver


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


@Directive("validateLimit", schema_name="test_issue209")
class ValidateLimitDirective:
    @staticmethod
    async def on_argument_execution(
        directive_args, next_directive, argument_definition, args, ctx, info
    ):
        value = await next_directive(argument_definition, args, ctx, info)
        if value > directive_args["limit"]:
            raise LimitReachedException("Limit has been reached")
        return value


@Resolver("Query.aList", schema_name="test_issue209")
async def resolver_query_a_list(parent, args, ctx, info):
    nb_items = args["nbItems"]
    return [f"{nb_items}.{index}" for index in range(nb_items)]


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


_TTFTT_ENGINE = Engine(_SDL, schema_name="test_issue209")


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
                        "locations": [{"line": 3, "column": 15}],
                        "type": "bad_request",
                    }
                ],
            },
        )
    ],
)
async def test_issue209(query, expected):

    assert await _TTFTT_ENGINE.execute(query) == expected
