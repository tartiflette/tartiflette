import pytest

from tartiflette import Resolver


def bakery(schema_name):
    @Resolver("Query.test", schema_name=schema_name)
    async def resolve_query_test(parent, args, ctx, info):
        chosen = args.get("choose", 0)
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
                        aField
                        bField
                    }
                    ... on Two {
                        cField
                        dField
                    }
                    ... on Three {
                        eField
                        fField
                    }
                }
            }
            """,
            {"data": {"test": {"aField": "aValue", "bField": 1}}},
        ),
        (
            """
            query aquery {
                test(choose:2){
                    ... on One {
                        aField
                        bField
                    }
                    ... on Two {
                        cField
                        dField
                    }
                    ... on Three {
                        eField
                        fField
                    }
                }
            }
            """,
            {"data": {"test": {"cField": 2, "dField": "dValue"}}},
        ),
        (
            """
            query aquery {
                test(choose:3){
                    ... on One {
                        aField
                        bField
                    }
                    ... on Two {
                        cField
                        dField
                    }
                    ... on Three {
                        eField
                        fField
                    }
                }
            }
            """,
            {"data": {"test": {"eField": 3.6, "fField": "fValue"}}},
        ),
        (
            """
            fragment bob on One {
                __typename
                aField
                bField
            }

            fragment ninja on Two {
                __typename
                cField
                dField
            }

            fragment lol on Three {
                __typename
                eField
                fField
            }

            query aquery {
                test(choose:3){
                    ... bob
                    ... ninja
                    ... lol
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
async def test_tartiflette_execute_union_type_output(
    schema_stack, query, expected
):
    assert (
        await schema_stack.execute(query, operation_name="aquery") == expected
    )
