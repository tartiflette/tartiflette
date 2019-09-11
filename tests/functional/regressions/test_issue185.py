from typing import Union

import pytest

from tartiflette import Resolver, create_engine
from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import StringValueNode
from tartiflette.scalar.scalar import Scalar

_SDL = """
scalar CapitalizedString

type Person {
    name: CapitalizedString
}

type ComplexPerson {
    name: CapitalizedString
    father: Person
    mother: Person
}

input PersonInput {
    name: CapitalizedString
}

input ComplexInput {
    name: CapitalizedString
    father: PersonInput
    mother: PersonInput
}

type Query {
    person(name: CapitalizedString): Person
    complexPerson(details: ComplexInput): ComplexPerson
}
"""


@pytest.fixture(scope="module")
async def ttftt_engine():
    @Scalar("CapitalizedString", schema_name="test_issue185")
    class CapitalizedString:
        @staticmethod
        def coerce_output(val) -> str:
            return str(val)

        @staticmethod
        def coerce_input(val: str) -> str:
            return val.capitalize()

        @staticmethod
        def parse_literal(ast: "Node") -> Union[str, "UNDEFINED_VALUE"]:
            return (
                ast.value.capitalize()
                if isinstance(ast, StringValueNode)
                else UNDEFINED_VALUE
            )

    @Resolver("Query.person", schema_name="test_issue185")
    async def the_query_person_resolver(_parents, args, _ctx, _info):
        return args

    @Resolver("Query.complexPerson", schema_name="test_issue185")
    async def the_query_complexPerson_resolver(_parents, args, _ctx, _info):
        return args["details"]

    return await create_engine(sdl=_SDL, schema_name="test_issue185")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            'query { person(name: "jack") { name } }',
            {"data": {"person": {"name": "Jack"}}},
        ),
        (
            'query { complexPerson(details: { name: "roger", father: { name: "jean"}, mother: {name: "regina"}}){ name father {name} mother {name}}}',
            {
                "data": {
                    "complexPerson": {
                        "name": "Roger",
                        "father": {"name": "Jean"},
                        "mother": {"name": "Regina"},
                    }
                }
            },
        ),
    ],
)
async def test_issue185(query, expected, ttftt_engine):
    assert await ttftt_engine.execute(query) == expected
