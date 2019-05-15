from datetime import datetime

import pytest

from tartiflette import Engine, Resolver


@pytest.mark.asyncio
async def test_tartiflette_execute_scalar_type_output(clean_registry):
    schema_sdl = """
    type Query {
        lastUpdate: DateTime
    }
    """

    @Resolver("Query.lastUpdate")
    async def func_field_resolver(*args, **kwargs):
        return datetime(
            year=2018, month=4, day=19, hour=14, minute=57, second=38
        )

    ttftt = Engine(schema_sdl)

    result = await ttftt.execute(
        """
    query Test{
        lastUpdate
    }
    """,
        operation_name="Test",
    )

    assert {"data": {"lastUpdate": "2018-04-19T14:57:38"}} == result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_sdl,resolver_response,expected",
    [
        ("String", "test", {"data": {"testField": "test"}}),
        (
            "String!",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Invalid value (value: None) for field `testField` of type `String!`",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 9}],
                    }
                ],
            },
        ),
        ("Int", 45, {"data": {"testField": 45}}),
        ("Float", 45.0, {"data": {"testField": 45.0}}),
        ("Boolean", True, {"data": {"testField": True}}),
        ("Boolean", False, {"data": {"testField": False}}),
        (
            "[DateTime]",
            [
                datetime(
                    year=2018, month=4, day=19, hour=14, minute=57, second=38
                )
            ],
            {"data": {"testField": ["2018-04-19T14:57:38"]}},
        ),
        (
            "[[DateTime!]!]!",
            [
                [
                    datetime(
                        year=2017,
                        month=3,
                        day=18,
                        hour=13,
                        minute=56,
                        second=37,
                    ),
                    datetime(
                        year=2018,
                        month=4,
                        day=19,
                        hour=14,
                        minute=57,
                        second=38,
                    ),
                ]
            ],
            {
                "data": {
                    "testField": [
                        ["2017-03-18T13:56:37", "2018-04-19T14:57:38"]
                    ]
                }
            },
        ),
        (
            "[DateTime]",
            [
                datetime(
                    year=2017, month=3, day=18, hour=13, minute=56, second=37
                ),
                None,
                datetime(
                    year=2018, month=4, day=19, hour=14, minute=57, second=38
                ),
            ],
            {
                "data": {
                    "testField": [
                        "2017-03-18T13:56:37",
                        None,
                        "2018-04-19T14:57:38",
                    ]
                }
            },
        ),
        # TODO: Test temporarily disabled (needs a fix on error resolving etc.)
        (
            "[DateTime!]",
            [
                datetime(
                    year=2017, month=3, day=18, hour=13, minute=56, second=37
                ),
                None,
                datetime(
                    year=2018, month=4, day=19, hour=14, minute=57, second=38
                ),
            ],
            {
                "data": {"testField": None},
                "errors": [
                    {
                        "message": "Invalid value (value: None) for field `testField` of type `[DateTime!]`",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 9}],
                    }
                ],
            },
        ),
    ],
)
async def test_tartiflette_execute_scalar_type_advanced(
    input_sdl, resolver_response, expected, clean_registry
):
    schema_sdl = """

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
    """,
        operation_name="Test",
    )

    assert expected == result


@pytest.mark.asyncio
async def test_tartiflette_declare_custom_scalar(clean_registry):
    from tartiflette import Scalar

    sdl = """
        scalar Ntm

        type Lol {
            joey: Ntm
        }

        type Query {
            alol: Lol
        }
    """

    @Resolver("Query.alol")
    async def alol_resolver(*_, **__):
        class customobject:
            def __init__(self, p1):
                self.p1 = p1

        return {"joey": customobject("OL")}

    @Scalar(name="Ntm")
    class Ntm:
        def coerce_output(self, val):
            return "I'am a val %s " % val.p1

        def coerce_input(self, val):
            return val

    ttftt = Engine(sdl)

    result = await ttftt.execute(
        query="""
        query {
            alol {
                joey
            }
        }
        """
    )

    assert {"data": {"alol": {"joey": "I'am a val OL "}}} == result
