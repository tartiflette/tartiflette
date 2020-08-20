from typing import Any, Callable, Dict, Optional

import pytest

from tartiflette import Directive, Resolver


def create_person(id, name, nickname=None, hobby=None):
    return {"id": id, "name": name, "nickname": nickname, "hobby": hobby}


def bakery(schema_name):
    @Directive("alwaysSkip", schema_name=schema_name)
    class AlwaysSkipDirective:
        async def on_field_collection(
            self,
            directive_args: Dict[str, Any],
            next_directive: Callable,
            field_node: "FieldNode",
            ctx: Optional[Any],
        ) -> "FieldNode":
            raise Exception("Oopsie")

    @Resolver("Query.person", schema_name=schema_name)
    async def resolve_query_person(*_, **__):
        return create_person(1, "Person #1", "Huh", "Sport")

    @Resolver("Person.parents", schema_name=schema_name)
    async def resolve_person_parents(*_, **__):
        return [create_person(2, "Parent #1")]


# TODO: we should fix that when `on_***_collection` unexpected errors will
# be properly handled.
@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    directive @alwaysSkip on FIELD | FRAGMENT_SPREAD | INLINE_FRAGMENT

    type Person {
      id: Int!
      name: String!
      nickname: String
      hobby: String
      parents: [Person!]
    }

    type Query {
      person(id: Int!): Person
    }
    """,
    bakery=bakery,
)
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            {
              person(id: 1) @alwaysSkip {
                id
                name
                nickname
              }
            }
            """,
            {"data": {}},
        ),
        (
            """
            {
              person(id: 1) {
                id @alwaysSkip
                name
                nickname
              }
            }
            """,
            {"data": {"person": {"name": "Person #1", "nickname": "Huh"}}},
        ),
        (
            """
            {
              person(id: 1) {
                id @alwaysSkip
                name @alwaysSkip
                nickname
              }
            }
            """,
            {"data": {"person": {"nickname": "Huh"}}},
        ),
        (
            """
            {
              person(id: 1) {
                id
                name
                nickname @alwaysSkip
              }
            }
            """,
            {"data": {"person": {"id": 1, "name": "Person #1"}}},
        ),
        (
            """
            {
              person(id: 1) {
                id
                name
                nickname
                parents {
                  id @alwaysSkip
                  name @alwaysSkip
                }
              }
            }
            """,
            {
                "data": {
                    "person": {
                        "id": 1,
                        "name": "Person #1",
                        "nickname": "Huh",
                        "parents": [{}],
                    }
                }
            },
        ),
        (
            """
            {
              person(id: 1) {
                id
                name
                nickname
                parents {
                  id
                  name
                  nickname @alwaysSkip
                }
              }
            }
            """,
            {
                "data": {
                    "person": {
                        "id": 1,
                        "name": "Person #1",
                        "nickname": "Huh",
                        "parents": [{"id": 2, "name": "Parent #1"}],
                    }
                }
            },
        ),
        (
            """
            {
              person(id: 1) {
                id
                name
                nickname @alwaysSkip
                parents {
                  id
                  name
                  nickname @alwaysSkip
                }
              }
            }
            """,
            {
                "data": {
                    "person": {
                        "id": 1,
                        "name": "Person #1",
                        "parents": [{"id": 2, "name": "Parent #1"}],
                    }
                }
            },
        ),
        (
            """
            {
              person(id: 1) {
                id
                name @alwaysSkip
                nickname @alwaysSkip
                parents {
                  id
                  name
                  nickname @alwaysSkip
                }
              }
            }
            """,
            {
                "data": {
                    "person": {
                        "id": 1,
                        "parents": [{"id": 2, "name": "Parent #1"}],
                    }
                }
            },
        ),
    ],
)
async def test_directives_on_collection_error(schema_stack, query, expected):
    assert await schema_stack.execute(query) == expected
