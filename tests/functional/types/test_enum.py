import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_tartiflette_execute_enum_type_output():
    schema_sdl = """
    enum Test {
        Value1
        Value2
        Value3
    }

    type Query {
        enumTest: Test
    }
    """

    @Resolver(
        "Query.enumTest",
        schema_name="test_tartiflette_execute_enum_type_output",
    )
    async def func_field_resolver(*args, **kwargs):
        return "Value1"

    ttftt = await create_engine(
        schema_sdl, schema_name="test_tartiflette_execute_enum_type_output"
    )

    result = await ttftt.execute(
        """
    query Test{
        enumTest
    }
    """,
        operation_name="Test",
    )

    assert {"data": {"enumTest": "Value1"}} == result


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
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
                    },
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
                    },
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
                    },
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
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
                        "locations": [{"line": 3, "column": 13}],
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
    schema_sdl = """
    enum MyEnum {{ ENUM_1, ENUM_2 }}

    type Query {{
        testField: {}
    }}
    """.format(
        input_sdl
    )

    @Resolver("Query.testField", schema_name=random_schema_name)
    async def func_field_resolver(*args, **kwargs):
        return resolver_response

    ttftt = await create_engine(schema_sdl, schema_name=random_schema_name)

    result = await ttftt.execute(
        """
        query Test{
            testField
        }
        """,
        operation_name="Test",
    )

    assert expected == result
