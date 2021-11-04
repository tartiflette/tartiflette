from typing import Any, Callable, Dict, Optional, Union

import pytest

from tartiflette import Directive, Resolver, create_engine

_SDL = """
directive @maxValue(limit: Int!) on ARGUMENT_DEFINITION | INPUT_FIELD_DEFINITION
directive @increment(step: Int! = 1) on ARGUMENT_DEFINITION | FIELD
directive @truncate(
  limit: Int! = 10 @maxValue(limit: 11) @increment
) on FIELD_DEFINITION | FIELD
directive @lowercase on FIELD_DEFINITION | FIELD
directive @uppercase on FIELD_DEFINITION | FIELD
directive @uppercase2 on FIELD_DEFINITION | FIELD
directive @uppercased on FIELD_DEFINITION | FIELD

type Person {
  id: Int!
  name: String! @truncate(limit: 5)
  nickname: String @truncate
  hobby: String @uppercased
}

type Query {
  person(id: Int!): Person
}
"""


@pytest.fixture(scope="module")
async def ttftt_engine():
    @Directive("maxValue", schema_name="test_directives_arguments")
    class MaxValueDirective:
        async def on_argument_execution(
            self,
            directive_args: Dict[str, Any],
            next_directive: Callable,
            parent_node: Union["FieldNode", "DirectiveNode"],
            argument_definition_node: "InputValueDefinitionNode",
            argument_node: Optional["ArgumentNode"],
            value: Any,
            ctx: Optional[Any],
        ):
            result = await next_directive(
                parent_node,
                argument_definition_node,
                argument_node,
                value,
                ctx,
            )
            if isinstance(result, (int, float)) and result > directive_args["limit"]:
                raise ValueError(f"{result} > {directive_args['limit']}")
            return result

        async def on_field_execution(
            self,
            directive_args: Dict[str, Any],
            next_resolver: Callable,
            parent: Optional[Any],
            args: Dict[str, Any],
            ctx: Optional[Any],
            info: "ResolveInfo",
        ):
            result = await next_resolver(parent, args, ctx, info)
            if result > directive_args["limit"]:
                raise ValueError(f"{result} > {directive_args['limit']}")
            return result

    @Directive("increment", schema_name="test_directives_arguments")
    class IncrementDirective:
        async def on_argument_execution(
            self,
            directive_args: Dict[str, Any],
            next_directive: Callable,
            parent_node: Union["FieldNode", "DirectiveNode"],
            argument_definition_node: "InputValueDefinitionNode",
            argument_node: Optional["ArgumentNode"],
            value: Any,
            ctx: Optional[Any],
        ):
            result = await next_directive(
                parent_node,
                argument_definition_node,
                argument_node,
                value,
                ctx,
            )
            if isinstance(result, (int, float)):
                return result + directive_args["step"]
            if isinstance(result, list):
                return [
                    value + directive_args["step"]
                    if isinstance(value, (int, float))
                    else value
                    for value in result
                ]
            return result

        async def on_field_execution(
            self,
            directive_args: Dict[str, Any],
            next_resolver: Callable,
            parent: Optional[Any],
            args: Dict[str, Any],
            ctx: Optional[Any],
            info: "ResolveInfo",
        ):
            result = await next_resolver(parent, args, ctx, info)
            return result + directive_args["step"]

    @Directive("truncate", schema_name="test_directives_arguments")
    class TruncateDirective:
        async def on_field_execution(
            self,
            directive_args: Dict[str, Any],
            next_resolver: Callable,
            parent: Optional[Any],
            args: Dict[str, Any],
            ctx: Optional[Any],
            info: "ResolveInfo",
        ):
            result = await next_resolver(parent, args, ctx, info)
            return (
                result[: directive_args["limit"]]
                if isinstance(result, str)
                else result
            )

    @Directive("lowercase", schema_name="test_directives_arguments")
    class LowercaseDirective:
        async def on_field_execution(
            self,
            directive_args: Dict[str, Any],
            next_resolver: Callable,
            parent: Optional[Any],
            args: Dict[str, Any],
            ctx: Optional[Any],
            info: "ResolveInfo",
        ):
            result = await next_resolver(parent, args, ctx, info)
            return result.lower() if isinstance(result, str) else result

    @Directive("uppercase2", schema_name="test_directives_arguments")
    @Directive("uppercase", schema_name="test_directives_arguments")
    class UppercaseDirective:
        async def on_field_execution(
            self,
            directive_args: Dict[str, Any],
            next_resolver: Callable,
            parent: Optional[Any],
            args: Dict[str, Any],
            ctx: Optional[Any],
            info: "ResolveInfo",
        ):
            result = await next_resolver(parent, args, ctx, info)
            return result.upper() if isinstance(result, str) else result

    @Directive("uppercased", schema_name="test_directives_arguments")
    class UppercasedDirective:
        async def on_field_execution(
            self,
            directive_args: Dict[str, Any],
            next_resolver: Callable,
            parent: Optional[Any],
            args: Dict[str, Any],
            ctx: Optional[Any],
            info: "ResolveInfo",
        ):
            result = await next_resolver(parent, args, ctx, info)
            return result.upper() if isinstance(result, str) else result

    @Resolver("Query.person", schema_name="test_directives_arguments")
    async def resolve_query_person(parent, args, ctx, info):
        return {
            "id": args["id"],
            "name": "Person.name",
            "nickname": "Person.nickname",
            "hobby": "Sport",
        }

    return await create_engine(_SDL, schema_name="test_directives_arguments")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            {
              person(id: 1) {
                id
                name
                nickname
                hobby
              }
            }
            """,
            {
                "data": {
                    "person": {
                        "id": 1,
                        "name": "Person",
                        "nickname": "Person.nick",
                        "hobby": "SPORT",
                    }
                }
            },
        ),
        (
            """
            {
              person(id: 1) {
                id @increment(step: 2)
                name @truncate(limit: 4)
                nickname @truncate(limit: 6)
                hobby
              }
            }
            """,
            {
                "data": {
                    "person": {
                        "id": 3,
                        "name": "Perso",
                        "nickname": "Person.",
                        "hobby": "SPORT",
                    }
                }
            },
        ),
        (
            """
            {
              person(id: 1) {
                id @increment(step: 2)
                name @truncate(limit: 4)
                nickname @truncate(limit: 11)
                hobby
              }
            }
            """,
            {
                "data": {
                    "person": {
                        "id": 3,
                        "name": "Perso",
                        "nickname": None,
                        "hobby": "SPORT",
                    }
                },
                "errors": [
                    {
                        "message": "12 > 11",
                        "path": ["person", "nickname"],
                        "locations": [{"line": 6, "column": 36}],
                    }
                ],
            },
        ),
        (
            """
            {
              person(id: 1) {
                id @increment(step: 2)
                name @truncate(limit: 4)
                nickname @truncate(limit: 6)
                hobby @lowercase
              }
            }
            """,
            {
                "data": {
                    "person": {
                        "id": 3,
                        "name": "Perso",
                        "nickname": "Person.",
                        "hobby": "sport",
                    }
                }
            },
        ),
        (
            """
            {
              person(id: 1) {
                id @increment(step: 2)
                name @truncate(limit: 4)
                nickname @truncate(limit: 6) @uppercase
                hobby @lowercase @uppercase
              }
            }
            """,
            {
                "data": {
                    "person": {
                        "id": 3,
                        "name": "Perso",
                        "nickname": "PERSON.",
                        "hobby": "sport",
                    }
                }
            },
        ),
        (
            """
            fragment PersonFields on Person {
              hobby @uppercase
            }

            {
              person(id: 1) {
                id @increment(step: 2)
                name @truncate(limit: 4)
                nickname @truncate(limit: 6) @uppercase
                hobby @lowercase @uppercase
                ...PersonFields
                hobby @lowercase
              }
            }
            """,
            {
                "data": {
                    "person": {
                        "id": 3,
                        "name": "Perso",
                        "nickname": "PERSON.",
                        "hobby": "sport",
                    }
                }
            },
        ),
        (
            """
            fragment PersonFields on Person {
              hobby @uppercase
            }

            {
              person(id: 1) {
                id @increment(step: 2)
                name @truncate(limit: 4)
                nickname @truncate(limit: 6) @lowercase @uppercase
                hobby @lowercase
                ...PersonFields
                hobby @lowercase
                ... on Person {
                  hobby @uppercase
                }
              }
            }
            """,
            {
                "data": {
                    "person": {
                        "id": 3,
                        "name": "Perso",
                        "nickname": "person.",
                        "hobby": "sport",
                    }
                }
            },
        ),
        (
            """
            fragment PersonFields on Person {
              hobby @uppercase
            }

            {
              person(id: 1) {
                id @increment(step: 2)
                name @truncate(limit: 4)
                nickname @truncate(limit: 6) @uppercase @lowercase @uppercase2
                hobby @lowercase
                ...PersonFields
                hobby @lowercase
                ...PersonFields
              }
            }
            """,
            {
                "data": {
                    "person": {
                        "id": 3,
                        "name": "Perso",
                        "nickname": "PERSON.",
                        "hobby": "sport",
                    }
                }
            },
        ),
    ],
)
async def test_directives_arguments(ttftt_engine, query, expected):
    assert await ttftt_engine.execute(query) == expected
