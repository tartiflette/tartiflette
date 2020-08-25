from collections import namedtuple

import pytest

from tartiflette import Resolver


def tartiflette_execute_simple_coercion_bakery(schema_name):
    @Resolver("Query.fieldScalar", schema_name=schema_name)
    async def resolve_query_field_scalar(*args, **kwargs):
        return "Test"

    @Resolver("Query.fieldEnum", schema_name=schema_name)
    async def resolve_query_field_enum(*args, **kwargs):
        return "Val2"

    @Resolver("Query.fieldObject", schema_name=schema_name)
    async def resolve_query_field_object(*args, **kwargs):
        return {"data": "DataString"}

    @Resolver("Query.fieldNotNull", schema_name=schema_name)
    async def resolve_query_field_not_null(*args, **kwargs):
        return "Test"

    @Resolver("Query.fieldList", schema_name=schema_name)
    async def resolve_query_field_list(*args, **kwargs):
        return ["A", "List", "Of", "Strings"]

    @Resolver("Query.fieldAdvanced1", schema_name=schema_name)
    async def resolve_query_field_advanced_A(*args, **kwargs):
        return [{"data": "DataString1A"}, {"data": "DataString1B"}]

    @Resolver("Query.fieldAdvanced2", schema_name=schema_name)
    async def resolve_query_field_advanced_2(*args, **kwargs):
        return [{"data": "DataString2A"}, {"data": "DataString2B"}]

    @Resolver("Query.fieldAdvanced3", schema_name=schema_name)
    async def resolve_query_field_advanced_3(*args, **kwargs):
        return [{"data": "DataString3A"}, {"data": "DataString3B"}]

    @Resolver("Query.fieldAdvanced4", schema_name=schema_name)
    async def resolve_query_field_advanced_4(*args, **kwargs):
        return [{"data": "DataString4A"}, {"data": "DataString4B"}]


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
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
    bakery=tartiflette_execute_simple_coercion_bakery,
)
async def test_tartiflette_execute_simple_coercion(schema_stack):
    assert (
        await schema_stack.execute(
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
        == {
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
        }
    )


def tartiflette_execute_nested_coercion_bakery(schema_name):
    Book = namedtuple("Book", "title,authors")
    Author = namedtuple("Author", "name")

    @Resolver("Query.library", schema_name=schema_name)
    async def func_field_library_resolver(*args, **kwargs):
        return [Book("A new beginning", [Author("Lemony Snicket")])]


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
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
    bakery=tartiflette_execute_nested_coercion_bakery,
)
async def test_tartiflette_execute_nested_coercion(schema_stack):
    assert (
        await schema_stack.execute(
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
        == {
            "data": {
                "library": [
                    {
                        "title": "A new beginning",
                        "authors": [{"name": "Lemony Snicket"}],
                    }
                ]
            }
        }
    )
