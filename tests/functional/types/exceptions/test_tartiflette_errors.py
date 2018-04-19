from datetime import datetime

import pytest

from tartiflette import Resolver
from tartiflette.tartiflette import Tartiflette


@pytest.mark.asyncio
async def test_tartiflette_execute_scalar_type_output():
    schema_sdl = """
    scalar Date
    
    type Obj {
        deep: Nested  # Try [Nested!] later
    }
    
    type Nested {
        lastUpdate: [Date!]
    }

    type Query {
        test: Obj
    }
    """

    def from_date_to_str(datetime):
        return datetime.isoformat()

    def from_str_to_date(datetime_str):
        return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")

    ttftt = Tartiflette(schema_sdl)

    ttftt.schema_definition.types["Date"].coerce_output = from_date_to_str
    ttftt.schema_definition.types["Date"].coerce_input = from_str_to_date

    @Resolver("Nested.lastUpdate", schema=ttftt.schema_definition)
    async def func_field_resolver(*args, **kwargs):
        return [datetime(year=2018, month=4, day=19,
                        hour=14, minute=57, second=38), None]

    # @Resolver("Obj.deep", schema=ttftt.schema_definition)
    # async def func_deep_resolver(*args, **kwargs):
    #     return []

    result = await ttftt.execute("""
    query Test{
        test {
            deep {
                lastUpdate
            }
        }
    }
    """)

    assert """{"data":{"test":{"deep":{"lastUpdate":["2018-04-19T14:57:38"]}}},"errors":[{"message":"Invalid value (value: None) for field `lastUpdate` of type `[Date!]`","path":["test","deep","lastUpdate",1],"locations":[]}]}""" == result
