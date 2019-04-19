import pytest

from tartiflette import Engine, Resolver


@pytest.mark.asyncio
async def test_tartiflette_execute_interface_type_output(clean_registry):
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

    @Resolver("Query.test")
    async def func_field_resolver(parent, arguments, request_ctx, info):
        return {"field2": 42}

    ttftt = Engine(schema_sdl)

    result = await ttftt.execute(
        """
    query Test{
        test {
            field2
        }
    }
    """,
        operation_name="Test",
    )

    assert {"data": {"test": {"field2": 42}}} == result
