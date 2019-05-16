import logging

from typing import Any, Callable, Dict, Optional, Union

import pytest

from tartiflette import Directive, Resolver, create_engine
from tartiflette.constants import UNDEFINED_VALUE

logger = logging.getLogger(__name__)


_SDL = """
directive @maxLength(
  limit: Int!
) on ARGUMENT_DEFINITION

directive @validateChoices(
  choices: String!
) on ARGUMENT_DEFINITION

directive @debug on ARGUMENT_DEFINITION

directive @stop on ARGUMENT_DEFINITION

input MyInput {
  myInputArg: MyInputInput! @debug
}

input MyStopedInput {
  myInputArg: MyInputInput! @stop
}

input MyInputInput {
  myInputInputArg1: String! @validateChoices(choices: ["VALID"])
  myInputInputArg2: String! @validateChoices(choices: ["VALID"])
}

type Query {
  search(
    query: String @maxLength(limit: 10)
  ): [String]

  aField(
    myArg: MyInput! @debug
  ): String

  anotherField(
    myInputArg: String! @validateChoices(choices: ["VALID"])
    myArg: MyInput! @debug
  ): [String]

  stopedField(
    stopedArg: MyStopedInput!
  ): String
}
"""


@pytest.fixture(scope="module")
async def ttftt_engine():
    @Directive("maxLength", schema_name="test_issue133")
    class MaxLengthDirective:
        async def on_argument_execution(
            self,
            directive_args: Dict[str, Any],
            next_directive: Callable,
            parent_node: Union["FieldNode", "DirectiveNode"],
            argument_node: "ArgumentNode",
            value: Any,
            ctx: Optional[Any],
        ) -> Any:
            result = await next_directive(
                parent_node, argument_node, value, ctx
            )
            if len(result) > directive_args["limit"]:
                raise Exception(
                    "Value of argument < %s > on field < %s > is too long ("
                    "%s/%s)."
                    % (
                        argument_node.name.value,
                        parent_node.name.value,
                        len(result),
                        directive_args["limit"],
                    )
                )
            return result

    @Directive("validateChoices", schema_name="test_issue133")
    class ValidateChoicesDirective:
        async def on_argument_execution(
            self,
            directive_args: Dict[str, Any],
            next_directive: Callable,
            parent_node: Union["FieldNode", "DirectiveNode"],
            argument_node: "ArgumentNode",
            value: Any,
            ctx: Optional[Any],
        ) -> Any:
            result = await next_directive(
                parent_node, argument_node, value, ctx
            )
            if result not in directive_args["choices"]:
                raise Exception(
                    "Value of argument < %s > on field < %s > is invalid. "
                    "Valid options are < %s >."
                    % (
                        argument_node.name.value,
                        parent_node.name.value,
                        ", ".join(directive_args["choices"]),
                    )
                )
            return result

    @Directive("debug", schema_name="test_issue133")
    class DebugDirective:
        async def on_argument_execution(
            self,
            directive_args: Dict[str, Any],
            next_directive: Callable,
            parent_node: Union["FieldNode", "DirectiveNode"],
            argument_node: "ArgumentNode",
            value: Any,
            ctx: Optional[Any],
        ) -> Any:
            return await next_directive(parent_node, argument_node, value, ctx)

    @Directive("stop", schema_name="test_issue133")
    class StopDirective:
        async def on_argument_execution(
            self,
            directive_args: Dict[str, Any],
            next_directive: Callable,
            parent_node: Union["FieldNode", "DirectiveNode"],
            argument_node: "ArgumentNode",
            value: Any,
            ctx: Optional[Any],
        ) -> Any:
            return UNDEFINED_VALUE

    @Resolver("Query.search", schema_name="test_issue133")
    async def _query_search_resolver(parent, args, *_, **__):
        return [args["query"]]

    @Resolver("Query.aField", schema_name="test_issue133")
    async def _query_a_field_resolver(parent, args, *_, **__):
        return "aValue"

    @Resolver("Query.stopedField", schema_name="test_issue133")
    async def _query_stoped_field_resolver(parent, args, *_, **__):
        return (
            args.get("stopedArg", {})
            .get("myInputArg", {})
            .get("myInputInputArg1")
        )

    return await create_engine(_SDL, schema_name="test_issue133")


# TODO: fix the test once `on_post_input_coercion` has been defined and properly handled.
@pytest.mark.skip(
    reason="`on_post_input_coercion` aren't handled properly yet. The method's prototype need to be defined."
)
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
                        "message": "Value of argument < query > on field < search > is too long (14/10).",
                        "path": ["search"],
                        "locations": [{"line": 3, "column": 22}],
                    }
                ],
            },
        ),
        (
            """
            query {
              aField(myArg: {
                myInputArg: {
                  myInputInputArg1: "INVALID"
                  myInputInputArg2: "VALID"
                }
              })
            }
            """,
            {
                "data": {"aField": None},
                "errors": [
                    {
                        "message": "Value of argument < myInputInputArg1 > on field < aField > is invalid. Valid options are < VALID >.",
                        "locations": [{"line": 3, "column": 15}],
                        "path": ["aField"],
                    }
                ],
            },
        ),
        (
            """
            query {
              aField(myArg: {
                myInputArg: {
                  myInputInputArg1: "INVALID"
                  myInputInputArg2: "INVALID"
                }
              })
            }
            """,
            {
                "data": {"aField": None},
                "errors": [
                    {
                        "message": "Value of argument < myInputInputArg1 > on field < aField > is invalid. Valid options are < VALID >.",
                        "locations": [{"line": 3, "column": 15}],
                        "path": ["aField"],
                    },
                    {
                        "message": "Value of argument < myInputInputArg2 > on field < aField > is invalid. Valid options are < VALID >.",
                        "locations": [{"line": 3, "column": 15}],
                        "path": ["aField"],
                    },
                ],
            },
        ),
        (
            """
            query {
              anotherField(
                myInputArg: "INVALID",
                myArg: {
                  myInputArg: {
                    myInputInputArg1: "INVALID"
                    myInputInputArg2: "INVALID"
                  }
                }
              )
            }
            """,
            {
                "data": {"anotherField": None},
                "errors": [
                    {
                        "message": "Value of argument < myInputArg > on field < anotherField > is invalid. Valid options are < VALID >.",
                        "locations": [{"line": 3, "column": 15}],
                        "path": ["anotherField"],
                    },
                    {
                        "message": "Value of argument < myInputInputArg1 > on field < anotherField > is invalid. Valid options are < VALID >.",
                        "locations": [{"line": 3, "column": 15}],
                        "path": ["anotherField"],
                    },
                    {
                        "message": "Value of argument < myInputInputArg2 > on field < anotherField > is invalid. Valid options are < VALID >.",
                        "locations": [{"line": 3, "column": 15}],
                        "path": ["anotherField"],
                    },
                ],
            },
        ),
        (
            """
            query {
              stopedField(stopedArg: {
                myInputArg: {
                  myInputInputArg1: "INVALID"
                  myInputInputArg2: "VALID"
                }
              })
            }
            """,
            {"data": {"stopedField": None}},
        ),
    ],
)
async def test_issue133(query, expected, ttftt_engine):
    assert await ttftt_engine.execute(query) == expected
