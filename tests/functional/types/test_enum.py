import pytest

from tartiflette import Resolver
from tartiflette.engine import Engine


@pytest.mark.asyncio
async def test_tartiflette_execute_enum_type_output(clean_registry):
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

    @Resolver("Query.enumTest")
    async def func_field_resolver(*args, **kwargs):
        return "Value1"

    ttftt = Engine(schema_sdl)

    result = await ttftt.execute(
        """
    query Test{
        enumTest
    }
    """
    )

    assert {"data": {"enumTest": "Value1"}} == result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_sdl,resolver_response,expected",
    [
        ("Test", "Value1", {"data": {"testField": "Value1"}}),
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
        (
            "[Test]",
            ["Value3", "Value1"],
            {"data": {"testField": ["Value3", "Value1"]}},
        ),
        (
            "[Test]",
            ["Value3", "UnknownValue"],
            {
                "data": {"testField": None},
                "errors": [
                    {
                        "message": "Invalid value (value: 'UnknownValue') for field `testField` of type `[Test]`",
                        "path": ["testField"],
                        "locations": [{"line": 1, "column": 26}],
                    }
                ],
            },
        ),
    ],
)
async def test_tartiflette_execute_enum_type_advanced(
    input_sdl, resolver_response, expected, clean_registry
):
    schema_sdl = """
    enum Test {{
        Value1
        Value2
        Value3
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
        testField
    }
    """
    )

    assert expected == result
