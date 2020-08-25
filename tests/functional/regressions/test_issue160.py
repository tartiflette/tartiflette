import pytest

from tartiflette import create_schema
from tartiflette.types.exceptions.tartiflette import GraphQLSchemaError
from tests.functional.utils import match_schema_errors


@pytest.mark.asyncio
async def test_issue160():
    with pytest.raises(GraphQLSchemaError) as excinfo:
        await create_schema(
            """
        type R

        interface Bob {
            a: String
        }

        type C implements Bob {
            b: Int
        }

        type D implements Richard {
            e: String
        }

        type F {
            a: G
        }

        union H = H | F | G

        type J implements F {
            g: F
        }

        type K implements Bob {
            a: Int
        }

        schema {
            query: Query
            mutation: MutationType
            subscription: SubscriptionType
        }

        scalar E

        enum I {
            TATA
            TITI
            TOTO
            J
        }

        type LL {
            a: String
        }

        type L {
            aField(arg: LL!): Int
        }

        directive @m(arg: LL!) on SCHEMA

        input N {
            a: String
            b: L
        }
        """,
            name="test_issue160",
        )

    match_schema_errors(
        excinfo.value,
        [
            "Type < D > must only implement Interface types, it cannot implement < Richard >.",
            "Unknown type < Richard >.",
            "The type of < F.a > must be Output type but got: G.",
            "Unknown type < G >.",
            "Unknown type < G >.",
            "Type < J > must only implement Interface types, it cannot implement < F >.",
            "Unknown type < Query >.",
            "Unknown type < MutationType >.",
            "Unknown type < SubscriptionType >.",
            "The type of L.aField(arg:) must be Input type but got: LL!.",
            "The type of @m(arg:) must be Input type but got: LL!.",
            "The type of N.b must be Input type but got: L.",
            "Query root type must be Object type.",
            "Mutation root type must be Object type.",
            "Subscription root type must be Object type.",
            "Type < R > must define one or more fields.",
            "Union type < H > can only include Object types, it cannot include < H >.",
            "Union type < H > can only include Object types, it cannot include < G >.",
            "Interface field < Bob.a > expected but < C > does not provide it.",
            "Interface field < Bob.a > expects type < String > but < K.a > is type < Int >.",
        ],
    )
