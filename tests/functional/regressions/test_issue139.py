import asyncio

from typing import Any, Callable, Dict, Optional, Union

import pytest

from tartiflette import Directive, Subscription, create_schema_with_operators
from tartiflette.types.exceptions.tartiflette import MultipleException
from tests.schema_stack import SchemaStack


@pytest.fixture(scope="module")
async def schema_stack():
    @Directive("validateMaxLength", schema_name="test_issue139")
    class ValidateMaxLengthDirective:
        @staticmethod
        async def on_post_argument_coercion(
            directive_args: Dict[str, Any],
            next_directive: Callable,
            parent_node: Union["FieldNode", "DirectiveNode"],
            argument_definition_node: "InputValueDefinitionNode",
            value: Any,
            ctx: Optional[Any],
        ):
            limit = directive_args["limit"]
            value = await next_directive(
                parent_node, argument_definition_node, value, ctx,
            )
            argument_length = len(value)
            if argument_length > limit:
                raise Exception(
                    "Value of argument "
                    f"< {argument_definition_node.name.value} > on field "
                    f"< {parent_node.name.value} > is too long "
                    f"({argument_length}/{limit})."
                )
            return value

    @Directive("validateChoices", schema_name="test_issue139")
    class ValidateChoicesDirective:
        @staticmethod
        async def on_post_argument_coercion(
            directive_args: Dict[str, Any],
            next_directive: Callable,
            parent_node: Union["FieldNode", "DirectiveNode"],
            argument_definition_node: "InputValueDefinitionNode",
            value: Any,
            ctx: Optional[Any],
        ):
            choices = directive_args["choices"]
            value = await next_directive(
                parent_node, argument_definition_node, value, ctx,
            )
            if value not in choices:
                raise Exception(
                    f"Value of argument "
                    f"< {argument_definition_node.name.value} > on field "
                    f"< {parent_node.name.value} > is not a valid option "
                    f"< {value} >. Allowed values are {choices}."
                )
            return value

    @Subscription("Subscription.newSearch", schema_name="test_issue139")
    async def subscription_new_search(*_, **__):
        for i in range(2):
            yield {"name": f"Human #{i}"}
            await asyncio.sleep(1)

    schema, execute, subscribe = await create_schema_with_operators(
        """
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
        """,
        name="test_issue139",
    )
    return SchemaStack("test_issue139", schema, execute, subscribe)


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
                        "message": "Value of argument < query > on field < search > is too long (14/5).",
                        "path": ["search"],
                        "locations": [{"line": 3, "column": 22}],
                    },
                    {
                        "message": "Value of argument < kind > on field < search > is not a valid option < INVALID_KIND >. Allowed values are ['ACTOR', 'DIRECTOR'].",
                        "path": ["search"],
                        "locations": [{"line": 3, "column": 47}],
                    },
                ],
            },
        )
    ],
)
async def test_issue139_query(schema_stack, query, expected):
    assert await schema_stack.execute(query) == expected


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
async def test_issue139_subscription_exceptions(
    schema_stack, query, exceptions
):
    with pytest.raises(MultipleException) as excinfo:
        async for _ in schema_stack.subscribe(query):
            pass

    for exception, expected in zip(excinfo.value.exceptions, exceptions):
        assert str(exception) == expected
