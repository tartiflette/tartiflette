import pytest

from tartiflette import Directive, Engine
from tartiflette.directive import CommonDirective

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
class Lol(CommonDirective):
    pass


@Directive("ninja", schema_name="test_issue143")
class Ninja(CommonDirective):
    pass


_ENGINE = Engine(sdl=_SDL, schema_name="test_issue143")


@pytest.mark.asyncio
async def test_issue143():
    query = """query Test{
        __type(name: "R") {
            fields {
                name
                isDeprecated
                deprecationReason
            }
        }
    }"""

    assert await _ENGINE.execute(query) == {
        "data": {
            "__type": {
                "fields": [
                    {
                        "name": "a",
                        "deprecationReason": "NTM",
                        "isDeprecated": True,
                    },
                    {
                        "isDeprecated": False,
                        "name": "b",
                        "deprecationReason": None,
                    },
                    {
                        "isDeprecated": False,
                        "name": "c",
                        "deprecationReason": None,
                    },
                ]
            }
        }
    }
