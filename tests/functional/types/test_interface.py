import pytest

from tartiflette import Resolver
from tartiflette.engine import Engine


@pytest.mark.asyncio
async def test_tartiflette_execute_interface_type_output():
    schema_sdl = """
    type Obj1 implements Iface {
        field1: String
        field2: Int
    }

    type Obj2 implements Iface {
        field2: Int
        field3: String
    }

    interface Iface {
        field2: Int
    }

    type Query {
        test: Iface
    }
    """

    ttftt = Engine(schema_sdl)

    @Resolver("Query.test", schema=ttftt.schema)
    async def func_field_resolver(parent, arguments, request_ctx, info):
        return {"field2": 42}


    result = await ttftt.execute("""
    query Test{
        test
    }
    """)

    # TODO: This should return an error (there is no sub-field selection)
    # assert {"data":None,"errors":["...the test field should select sub-fields error..."]} == result

    result = await ttftt.execute("""
    query Test{
        test {
            field2
        }
    }
    """)

    assert {"data":{"test":{"field2":42}}} == result
