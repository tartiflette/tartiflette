from unittest.mock import Mock

import pytest

from tartiflette import Resolver
from tartiflette.tartiflette import Tartiflette


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

    ttftt = Tartiflette(schema_sdl)

    @Resolver("Query.objectTest", schema=ttftt.schema)
    async def func_field_resolver(*args, **kwargs):
        return {"field1": "Test"}

    result = await ttftt.execute("""
    query Test{
        objectTest {
            field1
        }
    }
    """)

    assert """{"data":{"objectTest":{"field1":"Test"}}}""" == result


@pytest.mark.asyncio
@pytest.mark.parametrize("input_sdl,resolver_response,expected", [
    (
        "Test",
        {"field1": "Test"},
        '{"data":{"testField":{"field1":"Test"}}}',
    ),
    (
        "Test!",
        None,
        '{"data":{"testField":null},"errors":[{"message":"Invalid value (value: None) for field `testField` of type `Test!`","path":["testField"],"locations":[{"line":1,"column":26}]}]}',
    ),
])
async def test_tartiflette_execute_object_type_advanced(input_sdl, resolver_response, expected):
    schema_sdl = """
    type Test {{
        field1: String
    }}

    type Query {{
        testField: {}
    }}
    """.format(input_sdl)

    ttftt = Tartiflette(schema_sdl)

    @Resolver("Query.testField", schema=ttftt.schema)
    async def func_field_resolver(*args, **kwargs):
        return resolver_response

    result = await ttftt.execute("""
    query Test{
        testField
    }
    """)

    # TODO: Fix the test once the collect_value on object works.
    # assert expected == result


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

    ttftt = Tartiflette(schema_sdl)

    mock_call = Mock()

    @Resolver("Content.title", schema=ttftt.schema)
    async def func_field_resolver(*args, **kwargs):
        mock_call()
        return "Test"

    @Resolver("Post.content", schema=ttftt.schema)
    async def func_field_resolver(*args, **kwargs):
        return {"title": "Stuff"}

    result = await ttftt.execute("""
    query Test{
        posts {
            content {
                title
            }
        }
    }
    """)

    # TODO: There is an issue here: the `Query.posts` resolver doesn't exist
    # so the fallback kicks-in. The issue is that the fallback returns a default
    # value of None or {} and that's not a valid return value.
    # Also the None value interrupts the execution and value "bubble up"
    # assert result == """{"data":{"posts":[{"content":{"title":"Test"}}]}}"""
    # assert mock_call.assert_called_once()
