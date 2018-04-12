from datetime import datetime

import pytest

from tartiflette import Resolver
from tartiflette.tartiflette import Tartiflette
from tartiflette.types.exceptions.tartiflette import \
    TartifletteUnexpectedNullValue, TartifletteNonListValue


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

    ttftt.schema_definition.types["Date"].serializer = from_date_to_str
    ttftt.schema_definition.types["Date"].deserializer = from_str_to_date

    @Resolver("Query.lastUpdate", schema=ttftt.schema_definition)
    async def func_field_resolver(*args, **kwargs):
        return datetime(year=2018, month=4, day=19,
                        hour=14, minute=57, second=38)

    result = await ttftt.execute("""
    query Test{
        lastUpdate
    }
    """)

    assert """{"lastUpdate":"2018-04-19T14:57:38"}""" == result


@pytest.mark.asyncio
@pytest.mark.parametrize("input_sdl,resolver_response,expects_error,expected", [
    (
        "[Date]",
        [datetime(year=2018, month=4, day=19, hour=14, minute=57, second=38)],
        False,
        '["2018-04-19T14:57:38"]',
    ),
    (
        "[[Date!]!]!",
        [[
            datetime(year=2017, month=3, day=18, hour=13, minute=56, second=37),
            datetime(year=2018, month=4, day=19, hour=14, minute=57, second=38),
          ]],
        False,
        '[["2017-03-18T13:56:37","2018-04-19T14:57:38"]]',
    ),
    (
        "[Date]",
        [
            datetime(year=2017, month=3, day=18, hour=13, minute=56, second=37),
            None,
            datetime(year=2018, month=4, day=19, hour=14, minute=57, second=38),
        ],
        False,
        '["2017-03-18T13:56:37",null,"2018-04-19T14:57:38"]',
    ),
    (
        "[Date!]",
        [
            datetime(year=2017, month=3, day=18, hour=13, minute=56, second=37),
            None,
            datetime(year=2018, month=4, day=19, hour=14, minute=57, second=38),
        ],
        True,  # We expect the "None" in the response to raise an error
        '',
    ),
    (
        "[Date!]",
        datetime(year=2017, month=3, day=18, hour=13, minute=56, second=37),
        True,  # We expect the wrong type (not a list) to raise an error
        '',
    ),
    (
        "String",
        "test",
        False,
        '"test"',
    ),
    (
        "String!",
        None,
        True,
        '',
    ),
])
async def test_tartiflette_execute_scalar_type_nested(input_sdl,resolver_response,expects_error,expected):
    schema_sdl = """
    scalar Date

    type Query {{
        testField: {}
    }}
    """.format(input_sdl)

    def from_date_to_str(datetime_str):
        try:
            return datetime_str.isoformat()
        except AttributeError:
            return None

    ttftt = Tartiflette(schema_sdl)

    ttftt.schema_definition.types["Date"].serializer = from_date_to_str

    @Resolver("Query.testField", schema=ttftt.schema_definition)
    async def func_field_resolver(*args, **kwargs):
        return resolver_response

    if expects_error:
        with pytest.raises((TartifletteUnexpectedNullValue, TartifletteNonListValue)):
            await ttftt.execute("""
            query Test{
                testField
            }
            """)
    else:
        result = await ttftt.execute("""
                    query Test{
                        testField
                    }
                    """)
        assert """{{"testField":{}}}""".format(expected) == result
