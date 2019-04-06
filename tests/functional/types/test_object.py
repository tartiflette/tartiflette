from collections import namedtuple
from unittest.mock import Mock

import pytest

from tartiflette import Engine, Resolver


@pytest.mark.asyncio
async def test_tartiflette_execute_object_type_output(clean_registry):
    schema_sdl = """
    type Test {
        field1: String
    }

    type Query {
        objectTest: Test
    }
    """

    @Resolver("Query.objectTest")
    async def func_field_resolver(*args, **kwargs):
        return {"field1": "Test"}

    ttftt = Engine(schema_sdl)

    result = await ttftt.execute(
        """
    query Test{
        objectTest {
            field1
        }
    }
    """,
        operation_name="Test",
    )

    assert {"data": {"objectTest": {"field1": "Test"}}} == result


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
                        "message": "Invalid value (value: None) for field `testField` of type `Test!`",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 9}],
                    }
                ],
            },
        ),
    ],
)
async def test_tartiflette_execute_object_type_advanced(
    input_sdl, resolver_response, expected, clean_registry
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

    @Resolver("Query.testField")
    async def func_field_resolver(*args, **kwargs):
        return resolver_response

    ttftt = Engine(schema_sdl)

    result = await ttftt.execute(
        """
    query Test{
        testField {
            field1
        }
    }
    """,
        operation_name="Test",
    )

    assert expected == result


@pytest.mark.asyncio
async def test_tartiflette_execute_object_type_unknown_field(clean_registry):
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

    @Resolver("Content.title")
    async def func_field_resolver(*args, **kwargs):
        mock_call()
        return "Test"

    @Resolver("Post.content")
    async def func_field_resolver(*args, **kwargs):
        return {"title": "Stuff"}

    Post = namedtuple("Post", ["content", "meta_creator"])
    Content = namedtuple("Content", ["title"])

    @Resolver("Query.posts")
    async def func_field_resolver(*args, **kwargs):
        return [
            Post(content=Content(title="Test"), meta_creator="Dailymotion")
        ]

    ttftt = Engine(schema_sdl)

    result = await ttftt.execute(
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

    assert result == {"data": {"posts": [{"content": {"title": "Test"}}]}}
    assert mock_call.called is True


@pytest.mark.asyncio
async def test_ttftt_object_with_interfaces(clean_registry):
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

    ttftt_engine = Engine(sdl, schema_name="test_ttftt_object_with_interfaces")

    user_type = ttftt_engine._schema.find_type("User")
    repository_type = ttftt_engine._schema.find_type("Repository")

    user_interfaces = ["Identifiable", "Nameable", "Subscribeable"]
    for user_interface in user_interfaces:
        interface = ttftt_engine._schema.find_type(user_interface)
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
        interface = ttftt_engine._schema.find_type(repository_interface)
        assert repository_interface in repository_type.interfaces_names
        assert interface in repository_type.interfaces
        assert repository_type in interface.possibleTypes
    assert len(repository_interfaces) == len(repository_type.interfaces_names)

    url_interface = ttftt_engine._schema.find_type("UniformResourceLocatable")
    assert url_interface.possibleTypes == []

    result = await ttftt_engine.execute(
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

    assert result == {
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
