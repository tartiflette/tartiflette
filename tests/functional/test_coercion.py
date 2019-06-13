from collections import namedtuple

import pytest

from tartiflette import Resolver, create_engine


@Resolver(
    "Query.fieldScalar", schema_name="test_tartiflette_execute_simple_coercion"
)
async def func_field_scalar_resolver(*args, **kwargs):
    return "Test"


@Resolver(
    "Query.fieldEnum", schema_name="test_tartiflette_execute_simple_coercion"
)
async def func_field_enum_resolver(*args, **kwargs):
    return "Val2"


@Resolver(
    "Query.fieldObject", schema_name="test_tartiflette_execute_simple_coercion"
)
async def func_field_object_resolver(*args, **kwargs):
    return {"data": "DataString"}


@Resolver(
    "Query.fieldNotNull",
    schema_name="test_tartiflette_execute_simple_coercion",
)
async def func_field_not_null_resolver(*args, **kwargs):
    return "Test"


@Resolver(
    "Query.fieldList", schema_name="test_tartiflette_execute_simple_coercion"
)
async def func_field_list_resolver(*args, **kwargs):
    return ["A", "List", "Of", "Strings"]


@Resolver(
    "Query.fieldAdvanced1",
    schema_name="test_tartiflette_execute_simple_coercion",
)
async def func_field_advanced1_resolver(*args, **kwargs):
    return [{"data": "DataString1A"}, {"data": "DataString1B"}]


@Resolver(
    "Query.fieldAdvanced2",
    schema_name="test_tartiflette_execute_simple_coercion",
)
async def func_field_advanced2_resolver(*args, **kwargs):
    return [{"data": "DataString2A"}, {"data": "DataString2B"}]


@Resolver(
    "Query.fieldAdvanced3",
    schema_name="test_tartiflette_execute_simple_coercion",
)
async def func_field_advanced3_resolver(*args, **kwargs):
    return [{"data": "DataString3A"}, {"data": "DataString3B"}]


@Resolver(
    "Query.fieldAdvanced4",
    schema_name="test_tartiflette_execute_simple_coercion",
)
async def func_field_advanced4_resolver(*args, **kwargs):
    return [{"data": "DataString4A"}, {"data": "DataString4B"}]


@pytest.fixture(scope="module")
async def ttftt_engine_1():
    return await create_engine(
        sdl="""
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
                fieldEnum: EnumType
                fieldObject: Obj
                fieldNotNull: String!
                fieldList: [String]
                fieldAdvanced1: [Obj]
                fieldAdvanced2: [Obj]!
                fieldAdvanced3: [Obj!]
                fieldAdvanced4: [Obj!]!
            }
        """,
        schema_name="test_tartiflette_execute_simple_coercion",
    )


Book = namedtuple("Book", "title,authors")
Author = namedtuple("Author", "name")


@Resolver(
    "Query.library", schema_name="test_tartiflette_execute_nested_coercion"
)
async def func_field_library_resolver(*args, **kwargs):
    return [Book("A new beginning", [Author("Lemony Snicket")])]


@pytest.fixture(scope="module")
async def ttftt_engine_2():
    return await create_engine(
        sdl="""
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
            """,
        schema_name="test_tartiflette_execute_nested_coercion",
    )


@pytest.mark.asyncio
async def test_tartiflette_execute_simple_coercion(ttftt_engine_1):
    result = await ttftt_engine_1.execute(
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
    """,
        operation_name="TestExecutionCoercion",
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
async def test_tartiflette_execute_nested_coercion(ttftt_engine_2):
    result = await ttftt_engine_2.execute(
        """
    query TestExecutionCoercion{
        library {
            title
            authors {
                name
            }
        }
    }
    """,
        operation_name="TestExecutionCoercion",
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
