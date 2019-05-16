import pytest

from tartiflette import Directive, create_engine

_SDL = """
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

"""


@Directive("lol", schema_name="test_issue143")
class Lol:
    pass


@Directive("ninja", schema_name="test_issue143")
class Ninja:
    pass


@pytest.fixture(scope="module")
async def ttftt_engine():
    return await create_engine(sdl=_SDL, schema_name="test_issue143")


@pytest.mark.asyncio
async def test_issue143(ttftt_engine):
    query = """query Test{
        __type(name: "R") {
            fields(includeDeprecated: true) {
                name
                isDeprecated
                deprecationReason
            }
        }
    }"""

    assert await ttftt_engine.execute(query) == {
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
