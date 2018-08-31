from collections import namedtuple

import pytest

from tartiflette import Resolver
from tartiflette.engine import Engine


@pytest.mark.asyncio
async def test_tartiflette_execute_simple_coercion():
    schema_sdl = """
    enum EnumType {
        Val1
        Val2
        Val3
    }

    type Obj {
        data: String
    }

    type Query {
        fieldScalar: String
        fieldEnum: String
        fieldObject: Obj
        fieldNotNull: String!
        fieldList: [String]
        fieldAdvanced1: [Obj]
        fieldAdvanced2: [Obj]!
        fieldAdvanced3: [Obj!]
        fieldAdvanced4: [Obj!]!
    }
    """

    #    fieldAdvanced5: [[Obj!]!]!
    #    fieldAdvanced6: [[[Obj!]!]!]!  add this to the thing, but, maybe we could enforce relay here ?

    ttftt = Engine(schema_sdl)

    @Resolver("Query.fieldScalar", schema=ttftt.schema)
    async def func_field_scalar_resolver(*args, **kwargs):
        return "Test"

    @Resolver("Query.fieldEnum", schema=ttftt.schema)
    async def func_field_enum_resolver(*args, **kwargs):
        return "Val2"

    @Resolver("Query.fieldObject", schema=ttftt.schema)
    async def func_field_object_resolver(*args, **kwargs):
        return {"data": "DataString"}

    @Resolver("Query.fieldNotNull", schema=ttftt.schema)
    async def func_field_not_null_resolver(*args, **kwargs):
        return "Test"

    @Resolver("Query.fieldList", schema=ttftt.schema)
    async def func_field_list_resolver(*args, **kwargs):
        return ["A", "List", "Of", "Strings"]

    @Resolver("Query.fieldAdvanced1", schema=ttftt.schema)
    async def func_field_advanced1_resolver(*args, **kwargs):
        return [{"data": "DataString1A"}, {"data": "DataString1B"}]

    @Resolver("Query.fieldAdvanced2", schema=ttftt.schema)
    async def func_field_advanced2_resolver(*args, **kwargs):
        return [{"data": "DataString2A"}, {"data": "DataString2B"}]

    @Resolver("Query.fieldAdvanced3", schema=ttftt.schema)
    async def func_field_advanced3_resolver(*args, **kwargs):
        return [{"data": "DataString3A"}, {"data": "DataString3B"}]

    @Resolver("Query.fieldAdvanced4", schema=ttftt.schema)
    async def func_field_advanced4_resolver(*args, **kwargs):
        return [{"data": "DataString4A"}, {"data": "DataString4B"}]

    # @Resolver("Query.fieldAdvanced5", schema=ttftt.schema)
    # async def func_field_advanced5_resolver(*args, **kwargs):
    #     return [
    #         [{"data": "DataString5A"}, {"data": "DataString5B"}],
    #         [{"data": "DataString5C"}, {"data": "DataString5D"}],
    #     ]

    # @Resolver("Query.fieldAdvanced6", schema=ttftt.schema)
    # async def func_field_advanced6_resolver(*args, **kwargs):
    #     return [
    #         [
    #             [{"data": "DataString6A"}, {"data": "DataString6B"}],
    #             [{"data": "DataString6C"}, {"data": "DataString6D"}],
    #         ],
    #         [
    #             [{"data": "DataString6E"}, {"data": "DataString6F"}],
    #             [{"data": "DataString6G"}, {"data": "DataString6H"}],
    #         ],
    #     ]

    result = await ttftt.execute(
        """
    query TestExecutionCoercion{
        fieldScalar
        fieldEnum
        fieldObject{
            data
        }
        fieldNotNull
        fieldList
        fieldAdvanced1 {
            data
        }
        fieldAdvanced2 {
            data
        }
        fieldAdvanced3 {
            data
        }
        fieldAdvanced4 {
            data
        }
    }
    """
    )

    assert {
        "data": {
            "fieldScalar": "Test",
            "fieldEnum": "Val2",
            "fieldObject": {"data": "DataString"},
            "fieldNotNull": "Test",
            "fieldList": ["A", "List", "Of", "Strings"],
            "fieldAdvanced1": [
                {"data": "DataString1A"},
                {"data": "DataString1B"},
            ],
            "fieldAdvanced2": [
                {"data": "DataString2A"},
                {"data": "DataString2B"},
            ],
            "fieldAdvanced3": [
                {"data": "DataString3A"},
                {"data": "DataString3B"},
            ],
            "fieldAdvanced4": [
                {"data": "DataString4A"},
                {"data": "DataString4B"},
            ],
        }
    } == result


@pytest.mark.asyncio
async def test_tartiflette_execute_nested_coercion():
    schema_sdl = """
    type Book {
        title: String!
        authors: [Author]
    }

    type Author {
        name: String!
    }

    type Query {
        library: [Book!]
    }
    """

    ttftt = Engine(schema_sdl)

    Book = namedtuple("Book", "title,authors")
    Author = namedtuple("Author", "name")

    @Resolver("Query.library", schema=ttftt.schema)
    async def func_field_library_resolver(*args, **kwargs):
        return [Book("A new beginning", [Author("Lemony Snicket")])]

    result = await ttftt.execute(
        """
    query TestExecutionCoercion{
        library {
            title
            authors {
                name
            }
        }
    }
    """
    )

    assert {
        "data": {
            "library": [
                {
                    "title": "A new beginning",
                    "authors": [{"name": "Lemony Snicket"}],
                }
            ]
        }
    } == result
