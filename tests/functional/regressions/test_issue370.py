import pytest

from tartiflette import Scalar, create_engine
from tartiflette.scalar.builtins.string import ScalarString
from tartiflette.types.exceptions.tartiflette import GraphQLSchemaError
from tests.functional.utils import match_schema_errors


@pytest.mark.asyncio
async def test_issue370_double_values():
    with pytest.raises(GraphQLSchemaError) as excinfo:
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

    match_schema_errors(
        excinfo.value,
        [
            "Enum value < Invalid.VALUE_3 > can only be defined once.",
            "Enum value < Invalid.VALUE_2 > can only be defined once.",
        ],
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
