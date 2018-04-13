import pytest

from tartiflette import Resolver
from tartiflette.tartiflette import Tartiflette


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

    ttftt = Tartiflette(schema_sdl)

    @Resolver("Query.enumTest", schema=ttftt.schema_definition)
    async def func_field_resolver(*args, **kwargs):
        return "Value1"

    result = await ttftt.execute("""
    query Test{
        enumTest
    }
    """)

    assert """{"data":{"enumTest":"Value1"}}""" == result


# @pytest.mark.asyncio
# @pytest.mark.parametrize("input_sdl,resolver_response,expected", [
#     (
#         "Test",
#         "Value1",
#         '{"data":{"testField":"Value1"}}',
#     ),
#     (
#         "Test",
#         "UnknownValue",
#         '{"data":{"testField":null},"errors":[]}',
#     ),
#
# ])
# async def test_tartiflette_execute_enum_type_advanced(input_sdl, resolver_response, expected):
#     schema_sdl = """
#     enum Test {{
#         Value1
#         Value2
#         Value3
#     }}
#
#     type Query {{
#         testField: {}
#     }}
#     """.format(input_sdl)
#
#     ttftt = Tartiflette(schema_sdl)
#
#     @Resolver("Query.testField", schema=ttftt.schema_definition)
#     async def func_field_resolver(*args, **kwargs):
#         return resolver_response
#
#     result = await ttftt.execute("""
#     query Test{
#         testField
#     }
#     """)
#
#     assert expected == result
