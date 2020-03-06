import pytest

from tartiflette import Scalar, create_engine
from tartiflette.scalar.builtins.string import ScalarString
from tartiflette.types.exceptions.tartiflette import GraphQLSchemaError


@pytest.mark.asyncio
async def test_issue370_double_values():

    with pytest.raises(
        GraphQLSchemaError,
        match="""

0: Enum < Invalid > is invalid, Value < VALUE_3 > is not unique
1: Enum < Invalid > is invalid, Value < VALUE_2 > is not unique""",
    ):
        await create_engine(
            """
            enum Invalid {
                VALUE_1
                VALUE_2
                VALUE_3
                VALUE_3
                VALUE_2
            }

            type Query {
                field1: Invalid
            }
        """,
            schema_name="test_issue370_uniqueness",
        )


@pytest.mark.asyncio
async def test_issue370_type_name_enum_value_mismatch():
    @Scalar("aType", schema_name="test_issue370_type_name_enum_value_mismatch")
    class _(ScalarString):
        pass

    assert (
        await create_engine(
            """
            scalar aType
            enum Valid {
                VALUE_1
                VALUE_2
                VALUE_3
                aType
            }

            type Query {
                field1: Valid
            }
        """,
            schema_name="test_issue370_type_name_enum_value_mismatch",
        )
        is not None
    )
