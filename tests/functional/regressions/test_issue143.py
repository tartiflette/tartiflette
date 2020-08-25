import pytest

from tartiflette import Directive


def bakery(schema_name):
    @Directive("lol", schema_name=schema_name)
    class Lol:
        pass

    @Directive("ninja", schema_name=schema_name)
    class Ninja:
        pass


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    directive @lol on FIELD_DEFINITION

    directive @ninja on FIELD_DEFINITION

    type R {
        a:String @lol @ninja @deprecated(reason: "NTM")
        b:String @lol @deprecated(reason: "NTM3") @ninja
        c:String @deprecated(reason: "jjjjjjjjjjjjjj") @lol @ninja
    }

    type Query {
        l: R
    }
    """,
    bakery=bakery,
)
async def test_issue143(schema_stack):
    assert (
        await schema_stack.execute(
            """
            query Test{
              __type(name: "R") {
                fields(includeDeprecated: true) {
                  name
                  isDeprecated
                  deprecationReason
                }
              }
            }
            """
        )
        == {
            "data": {
                "__type": {
                    "fields": [
                        {
                            "name": "a",
                            "deprecationReason": "NTM",
                            "isDeprecated": True,
                        },
                        {
                            "isDeprecated": True,
                            "name": "b",
                            "deprecationReason": "NTM3",
                        },
                        {
                            "isDeprecated": True,
                            "name": "c",
                            "deprecationReason": "jjjjjjjjjjjjjj",
                        },
                    ]
                }
            }
        }
    )
