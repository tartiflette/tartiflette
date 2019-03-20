import pytest

from tartiflette import Engine
from tartiflette.types.exceptions.tartiflette import GraphQLSchemaError


def test_issue160():
    with pytest.raises(
        GraphQLSchemaError,
        match="""

0: Field < F.a > is Invalid: the given Type < G > does not exist!
1: Field < C.a > is missing as defined in the < Bob > Interface.
2: Type < D > implements < Richard > which does not exist!
3: Type < J > implements < F > which is not an interface!
4: Field < K.a > should be of Type < String > as defined in the < Bob > Interface.
5: Missing Query Type < Query >.
6: Missing Mutation Type < MutationType >.
7: Missing Subscription Type < SubscriptionType >.
8: Type < R > has no fields.
9: Union Type < H > contains itself.
10: Scalar < E > is missing an implementation
11: Enum < I > has a value of < J > which is a Type
12: Argument < arg > of Field < L.aField > is of type < LL > which is not a Scalar, an Enum or an InputObject
13: Argument < arg > of Directive < m > is of type < LL > which is not a Scalar, an Enum or an InputObject
14: Field < N.b > is of type < L > which is not a Scalar, an Enum or an InputObject""",
    ):
        Engine(
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
            schema_name="test_issue160",
        )
