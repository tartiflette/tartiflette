import pytest

from tartiflette import Resolver
from tartiflette.engine import Engine


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl_type, returnval, expected",
    [
        pytest.param(
            "String",
            "Something",
            {"data": {"obj": {"field": "Something"}}},
            id="String",
        ),
        pytest.param(
            "String!",
            None,
            {
                "data": {"obj": None},
                "errors": [
                    {
                        "locations": [{"column": 64, "line": 1}],
                        "message": "Invalid value (value: None) for field `field` of type `String!`",
                        "path": ["obj", "field"],
                    }
                ],
            },
            id="String!",
        ),
        pytest.param(
            "[String]",
            ["Before", None, "After"],
            {"data": {"obj": {"field": ["Before", None, "After"]}}},
            id="[String]",
        ),
        pytest.param(
            "[String!]",
            ["Before", None, "After"],
            {
                "data": {"obj": {"field": None}},
                "errors": [
                    {
                        "locations": [{"column": 64, "line": 1}],
                        "message": "Invalid value (value: None) for field `field` of type `[String!]`",
                        "path": ["obj", "field"],
                    }
                ],
            },
            id="[String!]",
        ),
        pytest.param(
            "[String]!",
            None,
            {
                "data": {"obj": None},
                "errors": [
                    {
                        "locations": [{"column": 64, "line": 1}],
                        "message": "Invalid value (value: None) for field `field` of type `[String]!`",
                        "path": ["obj", "field"],
                    }
                ],
            },
            id="[String]!",
        ),
        pytest.param(
            "[String!]!",
            ["Before", None, "After"],
            {
                "data": {"obj": None},
                "errors": [
                    {
                        "locations": [{"column": 64, "line": 1}],
                        "message": "Invalid value (value: None) for field `field` of type `[String!]!`",
                        "path": ["obj", "field"],
                    }
                ],
            },
            id="[String!]!",
        ),
        pytest.param(
            "[String!]!",
            None,
            {
                "data": {"obj": None},
                "errors": [
                    {
                        "locations": [{"column": 64, "line": 1}],
                        "message": "Invalid value (value: None) for field `field` of type `[String!]!`",
                        "path": ["obj", "field"],
                    }
                ],
            },
            id="[String!]!",
        ),
        pytest.param(
            "[[String]]",
            [["Nobody", "Expects"], ["The", "Spanish", "Inquisition"]],
            {
                "data": {
                    "obj": {
                        "field": [
                            ["Nobody", "Expects"],
                            ["The", "Spanish", "Inquisition"],
                        ]
                    }
                }
            },
            id="[[String]]",
        ),
        # TODO: move below test to a coercion test
        # (it doesn't really test empty values)
        pytest.param(
            "[[String]]",
            [42, None, ["The", "Spanish", "Inquisition"]],
            {
                "data": {
                    "obj": {
                        "field": [
                            ["42"],
                            None,
                            ["The", "Spanish", "Inquisition"],
                        ]
                    }
                }
            },
            id="[[String]]",
        ),
        pytest.param(
            "[[String!]]",
            [["Nobody", "Expects"], ["The", "Spanish"], [None, "Inquisition"]],
            {
                "data": {"obj": {"field": None}},
                "errors": [
                    {
                        "locations": [{"column": 64, "line": 1}],
                        "message": "Invalid value (value: None) for field `field` of type `[[String!]]`",
                        "path": ["obj", "field"],
                    }
                ],
            },
            id="[[String!]]",
        ),
        pytest.param(  # Test #10
            "[[String!]!]",
            [["Nobody", "Expects"], ["The", "Spanish"], [None, "Inquisition"]],
            {
                "data": {"obj": {"field": None}},
                "errors": [
                    {
                        "locations": [{"column": 64, "line": 1}],
                        "message": "Invalid value (value: None) for field `field` of type `[[String!]!]`",
                        "path": ["obj", "field"],
                    }
                ],
            },
            id="[[String!]!]",
        ),
        pytest.param(
            "[[String!]!]!",
            [["Nobody", "Expects"], ["The", "Spanish"], [None, "Inquisition"]],
            {
                "data": {"obj": None},
                "errors": [
                    {
                        "locations": [{"column": 64, "line": 1}],
                        "message": "Invalid value (value: None) for field `field` of type `[[String!]!]!`",
                        "path": ["obj", "field"],
                    }
                ],
            },
            id="[[String!]!]!",
        ),
    ],
)
async def test_tartiflette_execute_simple_empty_value(
    sdl_type, returnval, expected, clean_registry
):
    schema_sdl = (
        """
    type Obj {
        field: %s
    }

    type Query {
        obj: Obj
    }
    """
        % sdl_type
    )

    @Resolver("Obj.field")
    async def func_field_scalar_resolver(*args, **kwargs):
        return returnval

    ttftt = Engine(schema_sdl)

    result = await ttftt.execute(
        """
    query TestExecutionEmptyValues{
        obj {
            field
        }
    }
    """
    )

    assert expected == result


@pytest.mark.asyncio
async def test_tartiflette_execute_bubble_up_empty_value(clean_registry):
    schema_sdl = """
        type SubObj {
            fieldAgain: Int!
        }

        type Obj {
            field: SubObj!
        }

        type Query {
            obj: Obj!
        }
        """

    @Resolver("SubObj.fieldAgain")
    async def func_field_scalar_resolver(*args, **kwargs):
        return None

    @Resolver("Query.obj")
    async def func_field_obj_resolver(*args, **kwargs):
        return {}

    @Resolver("Obj.field")
    async def func_field_field_resolver(*args, **kwargs):
        return {}

    ttftt = Engine(schema_sdl)

    result = await ttftt.execute(
        """
        query TestExecutionEmptyValues{
            obj {
                field {
                    fieldAgain
                }
            }
        }
        """
    )

    assert result == {
        "data": None,
        "errors": [
            {
                "locations": [{"column": 104, "line": 1}],
                "message": "Invalid value (value: None) for field `fieldAgain` of type `Int!`",
                "path": ["obj", "field", "fieldAgain"],
            }
        ],
    }
