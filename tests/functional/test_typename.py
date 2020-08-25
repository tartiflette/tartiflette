import pytest

from tartiflette import Resolver


def bakery(schema_name):
    @Resolver("Query.test", schema_name=schema_name)
    async def func_field_resolver(parent, arguments, request_ctx, info):
        chosen = arguments.get("choose", 0)
        if chosen == 1:
            return {"aField": "aValue", "bField": 1, "_typename": "One"}
        elif chosen == 2:

            class Lol:
                def __init__(self, *args, **kwargs):
                    self._typename = "Two"
                    self.cField = 2
                    self.dField = "dValue"

            return Lol()
        elif chosen == 3:

            class Three:
                def __init__(self, *args, **kwargs):
                    self.eField = 3.6
                    self.fField = "fValue"

            return Three()

        return None


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    type One {
        aField: String
        bField: Int
    }

    type Two {
        cField: Int
        dField: String
    }

    type Three {
        eField: Float
        fField: String
    }

    union Mixed = One | Two | Three

    type Query {
        test(choose: Int!): Mixed
    }
    """,
    bakery=bakery,
)
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            query aquery {
                test(choose:1){
                    ... on One {
                        __typename
                        aField
                        bField
                    }
                    ... on Two {
                        __typename
                        cField
                        dField
                    }
                    ... on Three {
                        __typename
                        eField
                        fField
                    }
                }
                __typename
            }
            """,
            {
                "data": {
                    "test": {
                        "__typename": "One",
                        "aField": "aValue",
                        "bField": 1,
                    },
                    "__typename": "Query",
                }
            },
        ),
        (
            """
            query aquery {
                test(choose:2){
                    ... on One {
                        __typename
                        aField
                        bField
                    }
                    ... on Two {
                        __typename
                        cField
                        dField
                    }
                    ... on Three {
                        __typename
                        eField
                        fField
                    }
                }
                __typename
            }
            """,
            {
                "data": {
                    "test": {
                        "__typename": "Two",
                        "cField": 2,
                        "dField": "dValue",
                    },
                    "__typename": "Query",
                }
            },
        ),
        (
            """
            query aquery {
                test(choose:3){
                    ... on One {
                        __typename
                        aField
                        bField
                    }
                    ... on Two {
                        __typename
                        cField
                        dField
                    }
                    ... on Three {
                        __typename
                        eField
                        fField
                    }
                }
                __typename
            }
            """,
            {
                "data": {
                    "test": {
                        "__typename": "Three",
                        "eField": 3.6,
                        "fField": "fValue",
                    },
                    "__typename": "Query",
                }
            },
        ),
    ],
)
async def test_tartiflette_typename(schema_stack, query, expected):
    assert (
        await schema_stack.execute(query, operation_name="aquery") == expected
    )
