from datetime import datetime

import pytest

from tartiflette import Resolver
from tartiflette.tartiflette import Tartiflette


@pytest.mark.asyncio
async def test_tartiflette_execute_scalar_type_output():
    schema_sdl = """
    scalar Date

    type Query {
        lastUpdate: Date
    }
    """

    def from_date_to_str(datetime):
        return datetime.isoformat()

    def from_str_to_date(datetime_str):
        return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")

    ttftt = Tartiflette(schema_sdl)

    ttftt.schema.types["Date"].coerce_output = from_date_to_str
    ttftt.schema.types["Date"].coerce_input = from_str_to_date

    @Resolver("Query.lastUpdate", schema=ttftt.schema)
    async def func_field_resolver(*args, **kwargs):
        return datetime(year=2018, month=4, day=19,
                        hour=14, minute=57, second=38)

    ttftt.schema.bake()
    result = await ttftt.execute("""
    query Test{
        lastUpdate
    }
    """)

    assert {"data":{"lastUpdate":"2018-04-19T14:57:38"}} == result


@pytest.mark.asyncio
@pytest.mark.parametrize("input_sdl,resolver_response,expected", [
    (
        "String",
        "test",
        {"data":{"testField":"test"}},
    ),
    (
        "String!",
        None,
        {"data":{"testField":None},"errors":[{"message":"Invalid value (value: None) for field `testField` of type `String!`","path":["testField"],"locations":[{"line":1,"column":26}]}]},
    ),
    (
        "Int",
        45,
        {"data":{"testField":45}},
    ),
    (
        "Float",
        45.0,
        {"data":{"testField":45.0}},
    ),
    (
        "Boolean",
        True,
        {"data":{"testField":True}},
    ),
    (
        "Boolean",
        False,
        {"data":{"testField":False}},
    ),
    (
        "[Date]",
        [datetime(year=2018, month=4, day=19, hour=14, minute=57, second=38)],
        {"data":{"testField":["2018-04-19T14:57:38"]}},
    ),
    (
        "[[Date!]!]!",
        [[
            datetime(year=2017, month=3, day=18, hour=13, minute=56, second=37),
            datetime(year=2018, month=4, day=19, hour=14, minute=57, second=38),
          ]],
        {"data":{"testField":[["2017-03-18T13:56:37","2018-04-19T14:57:38"]]}},
    ),
    (
        "[Date]",
        [
            datetime(year=2017, month=3, day=18, hour=13, minute=56, second=37),
            None,
            datetime(year=2018, month=4, day=19, hour=14, minute=57, second=38),
        ],
        {"data":{"testField":["2017-03-18T13:56:37",None,"2018-04-19T14:57:38"]}},
    ),
    # TODO: Test temporarily disabled (needs a fix on error resolving etc.)
    (
        "[Date!]",
        [
            datetime(year=2017, month=3, day=18, hour=13, minute=56, second=37),
            None,
            datetime(year=2018, month=4, day=19, hour=14, minute=57, second=38),
        ],
        {"data":{"testField": None},"errors":[{"message":"Invalid value (value: None) for field `testField` of type `[Date!]`","path":["testField",1],"locations":[{"line":1,"column":26}]}]},
    ),
])
async def test_tartiflette_execute_scalar_type_advanced(input_sdl, resolver_response, expected):
    schema_sdl = """
    scalar Date

    type Query {{
        testField: {}
    }}
    """.format(input_sdl)

    def from_date_to_str(datetime):
        try:
            return datetime.isoformat()
        except AttributeError:
            return None

    ttftt = Tartiflette(schema_sdl)

    ttftt.schema.types["Date"].coerce_input = lambda x: x
    ttftt.schema.types["Date"].coerce_output = from_date_to_str

    @Resolver("Query.testField", schema=ttftt.schema)
    async def func_field_resolver(*args, **kwargs):
        return resolver_response

    ttftt.schema.bake()
    result = await ttftt.execute("""
    query Test{
        testField
    }
    """)

    assert expected == result
