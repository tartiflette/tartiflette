import pytest

from tartiflette import Resolver, create_schema_with_operators


def bakery(schema_name):
    @Resolver("Query.enumTest", schema_name=schema_name)
    async def resolve_query_enum_test(*args, **kwargs):
        return "Value1"


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    enum Test {
        Value1
        Value2
        Value3
    }

    type Query {
        enumTest: Test
    }
    """,
    bakery=bakery,
)
async def test_tartiflette_execute_enum_type_output(schema_stack):
    assert (
        await schema_stack.execute(
            """
            query Test{
                enumTest
            }
            """,
            operation_name="Test",
        )
        == {"data": {"enumTest": "Value1"}}
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_sdl,resolver_response,expected",
    [
        ("MyEnum", None, {"data": {"testField": None}}),
        (
            "MyEnum",
            "UNKNOWN_VALUE",
            {
                "data": {"testField": None},
                "errors": [
                    {
                        "message": "Expected value of type MyEnum but received <class 'str'>.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 15}],
                    }
                ],
            },
        ),
        ("MyEnum", "ENUM_1", {"data": {"testField": "ENUM_1"}}),
        (
            "MyEnum!",
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
        (
            "MyEnum!",
            "UNKNOWN_VALUE",
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type MyEnum but received <class 'str'>.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 15}],
                    }
                ],
            },
        ),
        ("MyEnum!", "ENUM_1", {"data": {"testField": "ENUM_1"}}),
        ("[MyEnum]", None, {"data": {"testField": None}}),
        ("[MyEnum]", [None], {"data": {"testField": [None]}}),
        (
            "[MyEnum]",
            "UNKNOWN_VALUE",
            {
                "data": {"testField": None},
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 15}],
                    }
                ],
            },
        ),
        (
            "[MyEnum]",
            ["UNKNOWN_VALUE"],
            {
                "data": {"testField": [None]},
                "errors": [
                    {
                        "message": "Expected value of type MyEnum but received <class 'str'>.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 15}],
                    }
                ],
            },
        ),
        (
            "[MyEnum]",
            "ENUM_1",
            {
                "data": {"testField": None},
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 15}],
                    }
                ],
            },
        ),
        ("[MyEnum]", ["ENUM_1"], {"data": {"testField": ["ENUM_1"]}}),
        (
            "[MyEnum]",
            ["ENUM_1", None],
            {"data": {"testField": ["ENUM_1", None]}},
        ),
        (
            "[MyEnum]",
            ["ENUM_1", "UNKNOWN_VALUE"],
            {
                "data": {"testField": ["ENUM_1", None]},
                "errors": [
                    {
                        "message": "Expected value of type MyEnum but received <class 'str'>.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 15}],
                    }
                ],
            },
        ),
        (
            "[MyEnum]",
            ["ENUM_1", "ENUM_2"],
            {"data": {"testField": ["ENUM_1", "ENUM_2"]}},
        ),
        (
            "[MyEnum]!",
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
        ("[MyEnum]!", [None], {"data": {"testField": [None]}}),
        (
            "[MyEnum]!",
            "UNKNOWN_VALUE",
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 15}],
                    }
                ],
            },
        ),
        (
            "[MyEnum]!",
            ["UNKNOWN_VALUE"],
            {
                "data": {"testField": [None]},
                "errors": [
                    {
                        "message": "Expected value of type MyEnum but received <class 'str'>.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 15}],
                    }
                ],
            },
        ),
        (
            "[MyEnum]!",
            "ENUM_1",
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 15}],
                    }
                ],
            },
        ),
        ("[MyEnum]!", ["ENUM_1"], {"data": {"testField": ["ENUM_1"]}}),
        (
            "[MyEnum]!",
            ["ENUM_1", None],
            {"data": {"testField": ["ENUM_1", None]}},
        ),
        (
            "[MyEnum]!",
            ["ENUM_1", "UNKNOWN_VALUE"],
            {
                "data": {"testField": ["ENUM_1", None]},
                "errors": [
                    {
                        "message": "Expected value of type MyEnum but received <class 'str'>.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 15}],
                    }
                ],
            },
        ),
        (
            "[MyEnum]!",
            ["ENUM_1", "ENUM_2"],
            {"data": {"testField": ["ENUM_1", "ENUM_2"]}},
        ),
        ("[MyEnum!]", None, {"data": {"testField": None}}),
        (
            "[MyEnum!]",
            [None],
            {
                "data": {"testField": None},
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 15}],
                    }
                ],
            },
        ),
        (
            "[MyEnum!]",
            "UNKNOWN_VALUE",
            {
                "data": {"testField": None},
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 15}],
                    }
                ],
            },
        ),
        (
            "[MyEnum!]",
            ["UNKNOWN_VALUE"],
            {
                "data": {"testField": None},
                "errors": [
                    {
                        "message": "Expected value of type MyEnum but received <class 'str'>.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 15}],
                    }
                ],
            },
        ),
        (
            "[MyEnum!]",
            "ENUM_1",
            {
                "data": {"testField": None},
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 15}],
                    }
                ],
            },
        ),
        ("[MyEnum!]", ["ENUM_1"], {"data": {"testField": ["ENUM_1"]}}),
        (
            "[MyEnum!]",
            ["ENUM_1", None],
            {
                "data": {"testField": None},
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 15}],
                    }
                ],
            },
        ),
        (
            "[MyEnum!]",
            ["ENUM_1", "UNKNOWN_VALUE"],
            {
                "data": {"testField": None},
                "errors": [
                    {
                        "message": "Expected value of type MyEnum but received <class 'str'>.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 15}],
                    }
                ],
            },
        ),
        (
            "[MyEnum!]",
            ["ENUM_1", "ENUM_2"],
            {"data": {"testField": ["ENUM_1", "ENUM_2"]}},
        ),
        (
            "[MyEnum!]!",
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
        (
            "[MyEnum!]!",
            [None],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 15}],
                    }
                ],
            },
        ),
        (
            "[MyEnum!]!",
            "UNKNOWN_VALUE",
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 15}],
                    }
                ],
            },
        ),
        (
            "[MyEnum!]!",
            ["UNKNOWN_VALUE"],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type MyEnum but received <class 'str'>.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 15}],
                    }
                ],
            },
        ),
        (
            "[MyEnum!]!",
            "ENUM_1",
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 15}],
                    }
                ],
            },
        ),
        ("[MyEnum!]!", ["ENUM_1"], {"data": {"testField": ["ENUM_1"]}}),
        (
            "[MyEnum!]!",
            ["ENUM_1", None],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 15}],
                    }
                ],
            },
        ),
        (
            "[MyEnum!]!",
            ["ENUM_1", "UNKNOWN_VALUE"],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type MyEnum but received <class 'str'>.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 15}],
                    }
                ],
            },
        ),
        (
            "[MyEnum!]!",
            ["ENUM_1", "ENUM_2"],
            {"data": {"testField": ["ENUM_1", "ENUM_2"]}},
        ),
        (
            "[[MyEnum!]!]!",
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
        (
            "[[MyEnum!]!]!",
            [None],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 15}],
                    }
                ],
            },
        ),
        (
            "[[MyEnum!]!]!",
            "UNKNOWN_VALUE",
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 15}],
                    }
                ],
            },
        ),
        (
            "[[MyEnum!]!]!",
            ["UNKNOWN_VALUE"],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 15}],
                    }
                ],
            },
        ),
        (
            "[[MyEnum!]!]!",
            "ENUM_1",
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 15}],
                    }
                ],
            },
        ),
        (
            "[[MyEnum!]!]!",
            ["ENUM_1"],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 15}],
                    }
                ],
            },
        ),
        (
            "[[MyEnum!]!]!",
            ["ENUM_1", None],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 15}],
                    },
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 15}],
                    },
                ],
            },
        ),
        (
            "[[MyEnum!]!]!",
            ["ENUM_1", "UNKNOWN_VALUE"],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 15}],
                    },
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 15}],
                    },
                ],
            },
        ),
        (
            "[[MyEnum!]!]!",
            ["ENUM_1", "ENUM_2"],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 15}],
                    },
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 15}],
                    },
                ],
            },
        ),
        (
            "[[MyEnum!]!]!",
            [[None]],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 0, 0],
                        "locations": [{"line": 3, "column": 15}],
                    }
                ],
            },
        ),
        (
            "[[MyEnum!]!]!",
            [["UNKNOWN_VALUE"]],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type MyEnum but received <class 'str'>.",
                        "path": ["testField", 0, 0],
                        "locations": [{"line": 3, "column": 15}],
                    }
                ],
            },
        ),
        ("[[MyEnum!]!]!", [["ENUM_1"]], {"data": {"testField": [["ENUM_1"]]}}),
        (
            "[[MyEnum!]!]!",
            [["ENUM_1", None]],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 0, 1],
                        "locations": [{"line": 3, "column": 15}],
                    }
                ],
            },
        ),
        (
            "[[MyEnum!]!]!",
            [["ENUM_1", "UNKNOWN_VALUE"]],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected value of type MyEnum but received <class 'str'>.",
                        "path": ["testField", 0, 1],
                        "locations": [{"line": 3, "column": 15}],
                    }
                ],
            },
        ),
        (
            "[[MyEnum!]!]!",
            [["ENUM_1", "ENUM_2"]],
            {"data": {"testField": [["ENUM_1", "ENUM_2"]]}},
        ),
    ],
)
async def test_tartiflette_execute_enum_type_advanced(
    input_sdl, resolver_response, expected, random_schema_name
):
    @Resolver("Query.testField", schema_name=random_schema_name)
    async def resolve_query_test_field(*args, **kwargs):
        return resolver_response

    _, execute, __ = await create_schema_with_operators(
        """
        enum MyEnum {{ ENUM_1, ENUM_2 }}

        type Query {{
            testField: {}
        }}
        """.format(
            input_sdl
        ),
        name=random_schema_name,
    )

    assert (
        await execute(
            """
            query Test {
              testField
            }
            """,
            operation_name="Test",
        )
        == expected
    )
