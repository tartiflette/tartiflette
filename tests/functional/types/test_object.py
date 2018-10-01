from collections import namedtuple
from unittest.mock import Mock

import pytest

from tartiflette import Resolver
from tartiflette.engine import Engine


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
    """
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
                        "locations": [{"line": 1, "column": 26}],
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
    """
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
    """
    )

    assert result == {"data": {"posts": [{"content": {"title": "Test"}}]}}
    assert mock_call.called is True
