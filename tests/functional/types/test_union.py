import pytest

from tartiflette import Resolver
from tartiflette.executors.types import Info
from tartiflette.engine import Engine


@pytest.mark.skip
@pytest.mark.asyncio
async def test_tartiflette_execute_union_type_output():
    schema_sdl = """
    enum Test {
        Value1
        Value2
        Value3
    }

    type SomethingElse {
        field: Int!
    }

    union Mixed = Test | SomethingElse

    type Query {
        test(choose: Int = 1): Mixed
    }
    """

    ttftt = Engine(schema_sdl)

    @Resolver("Query.test", schema=ttftt.schema)
    async def func_field_resolver(parent, arguments, request_ctx, info: Info):
        if arguments.get("choose", 0) == 1:
            return "Value1"  # First Union type
        elif arguments.get("choose", 0) == 2:
            return {"field": 42}  # Second Union type
        elif arguments.get("choose", 0) == 3:
            return "Unknown Value"  # Unknown value => error
        else:
            return None

    result = await ttftt.execute(
        """
    query Test{
        test(choose: 1)
    }
    """
    )

    assert {"data": {"test": "Value1"}} == result

    # TODO: Fix this.
    # result = await ttftt.execute("""
    # query Test{
    #     test(choose: 2)
    # }
    # """)
    #
    # # TODO: This is not possible: unions can only work on same type unions
    # assert {"data":{"test":{"field":42}}} == result

    # TODO: Fix this test. See comment below.
    # result = await ttftt.execute("""
    # query Test{
    #     test(choose: 3)
    # }
    # """)
    #
    # # This should fail but succeeds because we don't check fields on object types.
    # # We currently use the resolver logic to validate a field exists that's
    # # why this works and doesn't fail. See the GraphQLObjectType coerce_value
    # # to understand.
    # assert {"data":{"test": None},"errors":["... add the true error here..."]} == result
