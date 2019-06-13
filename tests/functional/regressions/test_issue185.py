import pytest

from tartiflette import Resolver, create_engine
from tartiflette.scalar.custom_scalar import Scalar

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

    @Resolver("Query.person", schema_name="test_issue185")
    async def the_query_person_resolver(_parent_results, args, _ctx, _info):
        return args

    @Resolver("Query.complexPerson", schema_name="test_issue185")
    async def the_query_complexPerson_resolver(
        _parent_results, args, _ctx, _info
    ):
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
