from collections import namedtuple
from unittest.mock import Mock

import pytest

from tartiflette import Resolver
from tartiflette.engine import Engine


@pytest.mark.asyncio
async def test_tartiflette_execute_object_type_output():
    schema_sdl = """
    type Test {
        field1: String
    }

    type Query {
        objectTest: Test
    }
    """

    ttftt = Engine(schema_sdl)

    @Resolver("Query.objectTest", schema=ttftt.schema)
    async def func_field_resolver(*args, **kwargs):
        return {"field1": "Test"}

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
                        "message": "Shouldn't be null - testField is not nullable",
                        "path": ["testField"],
                        "locations": [{"line": 1, "column": 26}],
                    }
                ],
            },
        ),
    ],
)
async def test_tartiflette_execute_object_type_advanced(
    input_sdl, resolver_response, expected
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

    ttftt = Engine(schema_sdl)

    @Resolver("Query.testField", schema=ttftt.schema)
    async def func_field_resolver(*args, **kwargs):
        return resolver_response

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

    ttftt = Engine(schema_sdl)

    mock_call = Mock()

    @Resolver("Content.title", schema=ttftt.schema)
    async def func_field_resolver(*args, **kwargs):
        mock_call()
        return "Test"

    @Resolver("Post.content", schema=ttftt.schema)
    async def func_field_resolver(*args, **kwargs):
        return {"title": "Stuff"}

    Post = namedtuple("Post", ["content", "meta_creator"])
    Content = namedtuple("Content", ["title"])

    @Resolver("Query.posts", schema=ttftt.schema)
    async def func_field_resolver(*args, **kwargs):
        return [
            Post(content=Content(title="Test"), meta_creator="Dailymotion")
        ]

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
