import asyncio

import pytest

from tartiflette import Directive, Engine, Subscription
from tartiflette.directive import CommonDirective
from tartiflette.types.exceptions.tartiflette import MultipleException


@Directive("validateMaxLength", schema_name="test_issue139")
class ValidateMaxLengthDirective(CommonDirective):
    @staticmethod
    async def on_argument_execution(
        directive_args, next_directive, argument_definition, args, ctx, info
    ):
        limit = directive_args["limit"]
        value = await next_directive(argument_definition, args, ctx, info)
        argument_length = len(value)
        if argument_length > limit:
            raise Exception(
                f"Value of argument < {argument_definition.name} > on field "
                f"< {info.schema_field.name} > is too long ({argument_length}/"
                f"{limit})."
            )
        return value


@Directive("validateChoices", schema_name="test_issue139")
class ValidateChoicesDirective(CommonDirective):
    @staticmethod
    async def on_argument_execution(
        directive_args, next_directive, argument_definition, args, ctx, info
    ):
        choices = directive_args["choices"]
        value = await next_directive(argument_definition, args, ctx, info)
        if value not in choices:
            raise Exception(
                f"Value of argument < {argument_definition.name} > on field "
                f"< {info.schema_field.name} > is not a valid option "
                f"< {value} >. Allowed values are {choices}."
            )
        return value


@Subscription("Subscription.newSearch", schema_name="test_issue139")
async def subscription_new_search(*_, **__):
    for i in range(2):
        yield {"name": f"Human #{i}"}
        await asyncio.sleep(1)


_SDL = """
directive @validateMaxLength(
  limit: Int!
) on ARGUMENT_DEFINITION

directive @validateChoices(
  choices: [String!]
) on ARGUMENT_DEFINITION

type Human {
  name: String!
}

type Query {
  search(
     query: String! @validateMaxLength(limit: 5)
     kind: String! @validateChoices(choices: ["ACTOR", "DIRECTOR"])
  ): [Human]
}

type Subscription {
  newSearch(
     query: String! @validateMaxLength(limit: 5)
     kind: String! @validateChoices(choices: ["ACTOR", "DIRECTOR"])
  ): [Human]
}
"""


_TTFTT_ENGINE = Engine(_SDL, schema_name="test_issue139")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            query {
              search(query: "Query too long", kind: "INVALID_KIND") {
                name
              }
            }
            """,
            {
                "data": {"search": None},
                "errors": [
                    {
                        "message": "Value of argument < query > on field "
                        "< search > is too long (14/5).",
                        "path": ["search"],
                        "locations": [{"line": 3, "column": 15}],
                    },
                    {
                        "message": "Value of argument < kind > on field "
                        "< search > is not a valid option "
                        "< INVALID_KIND >. Allowed values are "
                        "['ACTOR', 'DIRECTOR'].",
                        "path": ["search"],
                        "locations": [{"line": 3, "column": 15}],
                    },
                ],
            },
        )
    ],
)
async def test_issue139_query(query, expected):
    assert await _TTFTT_ENGINE.execute(query) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query,exceptions",
    [
        (
            """
            subscription {
              newSearch(query: "Query too long", kind: "INVALID_KIND") {
                name
              }
            }
            """,
            [
                "Value of argument < query > on field < newSearch > is too "
                "long (14/5).",
                "Value of argument < kind > on field < newSearch > is not a "
                "valid option < INVALID_KIND >. Allowed values are "
                "['ACTOR', 'DIRECTOR'].",
            ],
        )
    ],
)
async def test_issue139_subscription_exceptions(query, exceptions):
    with pytest.raises(MultipleException) as excinfo:
        async for _ in _TTFTT_ENGINE.subscribe(query):
            pass

    for exception, expected in zip(excinfo.value.exceptions, exceptions):
        assert str(exception) == expected
