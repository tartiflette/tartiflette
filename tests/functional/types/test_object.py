from collections import namedtuple
from unittest.mock import Mock

import pytest

from tartiflette import Resolver, create_schema_with_operators


def tartiflette_execute_object_type_output_bakery(schema_name):
    @Resolver("Query.objectTest", schema_name=schema_name)
    async def resolve_query_object_test(*args, **kwargs):
        return {"field1": "Test"}


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    type Test {
      field1: String
    }

    type Query {
      objectTest: Test
    }
    """,
    bakery=tartiflette_execute_object_type_output_bakery,
)
async def test_tartiflette_execute_object_type_output(schema_stack):
    assert (
        await schema_stack.execute(
            """
            query Test{
              objectTest {
                field1
              }
            }
            """,
            operation_name="Test",
        )
        == {"data": {"objectTest": {"field1": "Test"}}}
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_sdl,resolver_response,expected",
    [
        (
            "Test",
            {"field1": "Test"},
            {"data": {"testField": {"field1": "Test"}}},
        ),
        (
            "Test!",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 15}],
                    }
                ],
            },
        ),
    ],
)
async def test_tartiflette_execute_object_type_advanced(
    input_sdl, resolver_response, expected, random_schema_name
):
    schema_sdl = """
    type Test {{
      field1: String
    }}

    type Query {{
      testField: {}
    }}
    """.format(
        input_sdl
    )

    @Resolver("Query.testField", schema_name=random_schema_name)
    async def resolve_query_test_field(*args, **kwargs):
        return resolver_response

    _, execute, __ = await create_schema_with_operators(
        schema_sdl, name=random_schema_name
    )

    assert (
        await execute(
            """
            query Test{
              testField {
                field1
              }
            }
            """,
            operation_name="Test",
        )
        == expected
    )


@pytest.mark.asyncio
async def test_tartiflette_execute_object_type_unknown_field():
    schema_sdl = """
    type Post {
      content: Content
      meta_creator: String
    }

    type Content {
      title: String
    }

    type Query {
      posts: [Post!]
    }
    """

    mock_call = Mock()

    @Resolver(
        "Content.title",
        schema_name="test_tartiflette_execute_object_type_unknown_field",
    )
    async def func_field_resolver(*args, **kwargs):
        mock_call()
        return "Test"

    @Resolver(
        "Post.content",
        schema_name="test_tartiflette_execute_object_type_unknown_field",
    )
    async def func_field_resolver_2(*args, **kwargs):
        return {"title": "Stuff"}

    Post = namedtuple("Post", ["content", "meta_creator"])
    Content = namedtuple("Content", ["title"])

    @Resolver(
        "Query.posts",
        schema_name="test_tartiflette_execute_object_type_unknown_field",
    )
    async def func_field_resolver_3(*args, **kwargs):
        return [
            Post(content=Content(title="Test"), meta_creator="Dailymotion")
        ]

    _, execute, __ = await create_schema_with_operators(
        schema_sdl, name="test_tartiflette_execute_object_type_unknown_field",
    )

    assert (
        await execute(
            """
            query Test{
              posts {
                content {
                  title
                }
              }
            }
            """,
            operation_name="Test",
        )
        == {"data": {"posts": [{"content": {"title": "Test"}}]}}
    )

    assert mock_call.called is True


@pytest.mark.asyncio
async def test_ttftt_object_with_interfaces():
    sdl = """
    interface Identifiable {
      id: String!
    }

    interface Nameable {
      name: String!
    }

    interface Titleable {
      title: String!
    }

    interface Subscribeable {
      subscribers: [User!]!
    }

    interface Starrable {
      nbOfStars: Int!
    }

    interface UniformResourceLocatable {
      url: String!
    }

    type User implements Identifiable & Nameable & Subscribeable {
      id: String!
      name: String!
      subscribers: [User!]!
      repositories: [Repository!]!
    }

    type Repository implements Identifiable & Titleable & Subscribeable & Starrable {
      id: String!
      title: String!
      subscribers: [User!]!
      nbOfStars: Int!
    }

    type Query {
      user(id: Int!): User!
      repository(id: Int!): Repository!
      users: [User!]!
      repositories: [Repository!]!
    }
    """

    @Resolver("Query.user", schema_name="test_ttftt_object_with_interfaces")
    async def _query_user_resolver(*_args, **_kwargs):
        return {
            "id": 1,
            "name": "Hooman",
            "subscribers": [],
            "repositories": [
                {"id": 1, "title": "Repoo", "subscribers": [], "nbOfStars": 2}
            ],
        }

    schema, execute, __ = await create_schema_with_operators(
        sdl, name="test_ttftt_object_with_interfaces"
    )

    user_type = schema.find_type("User")
    repository_type = schema.find_type("Repository")

    user_interfaces = ["Identifiable", "Nameable", "Subscribeable"]
    for user_interface in user_interfaces:
        interface = schema.find_type(user_interface)
        assert user_interface in user_type.interfaces_names
        assert interface in user_type.interfaces
        assert user_type in interface.possibleTypes
    assert len(user_interfaces) == len(user_type.interfaces_names)

    repository_interfaces = [
        "Identifiable",
        "Titleable",
        "Subscribeable",
        "Starrable",
    ]
    for repository_interface in repository_interfaces:
        interface = schema.find_type(repository_interface)
        assert repository_interface in repository_type.interfaces_names
        assert interface in repository_type.interfaces
        assert repository_type in interface.possibleTypes
    assert len(repository_interfaces) == len(repository_type.interfaces_names)

    url_interface = schema.find_type("UniformResourceLocatable")
    assert url_interface.possibleTypes == []

    assert (
        await execute(
            """
            query {
              user(id: 1) {
                id
                name
                subscribers {
                  id
                  name
                }
                repositories {
                  id
                  title
                  nbOfStars
                }
              }
            }
            """
        )
        == {
            "data": {
                "user": {
                    "id": "1",
                    "name": "Hooman",
                    "subscribers": [],
                    "repositories": [
                        {"id": "1", "title": "Repoo", "nbOfStars": 2}
                    ],
                }
            }
        }
    )
