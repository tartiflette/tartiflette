import json

import pytest

from tartiflette import Resolver
from tartiflette.tartiflette import Tartiflette


@pytest.mark.asyncio
async def test_tartiflette_execute_basic_type_introspection_output():
    schema_sdl = """
    \"\"\"This is the description\"\"\"
    type Test {
        field1: String
        field2: Int
    }

    type Query {
        objectTest: Test
    }
    """

    ttftt = Tartiflette(schema_sdl)

    @Resolver("Query.objectTest", schema=ttftt.schema)
    async def func_field_resolver(*args, **kwargs):
        return {"field1": "Test", "field2": 42}

    ttftt.schema.bake()
    result = await ttftt.execute("""
    query Test{
        __type(name: "Test") {
            name
            kind
            description
            fields {
                name
            }
        } 
    }
    """)

    dic = json.loads(result)
    assert {
        "data": {
            "__type": {
                "name": "Test",
                "kind": "OBJECT",
                "description": "This is the description",
                "fields": [
                    {"name": "field1"},
                    {"name": "field2"},
                ],
            },
        }
    } == dic


@pytest.mark.asyncio
async def test_tartiflette_execute_schema_introspection_output():
    schema_sdl = """
    schema {
        query: CustomRootQuery
        mutation: CustomRootMutation
        subscription: CustomRootSubscription
    }
    
    type CustomRootQuery {
        test: String
    }
    
    type CustomRootMutation {
        test: Int
    }
    
    type CustomRootSubscription {
        test: String
    }
    """

    ttftt = Tartiflette(schema_sdl)
    ttftt.schema.bake()
    result = await ttftt.execute("""
    query Test{
        __schema {
            queryType { name }
            mutationType { name }
            subscriptionType { name }
        } 
    }
    """)

    dic = json.loads(result)
    assert {
        "data": {
            "__schema": {
                "queryType": {
                    "name": "CustomRootQuery",
                },
                "mutationType": {
                    "name": "CustomRootMutation",
                },
                "subscriptionType": {
                    "name": "CustomRootSubscription",
                }
            },
        }
    } == dic