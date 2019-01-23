import pytest

from tartiflette import Resolver


@Resolver("Query.dog")
async def _query_dog_resolver(*_args, **__kwargs):
    return {"name": "Doggy"}


@Resolver("Dog.doesKnowCommand")
async def _dog_does_know_command_resolver(
    _parent_result, args, *__args, **___kwargs
):
    return args["dogCommand"] == "SIT"


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    resolvers={
        "Query.dog": _query_dog_resolver,
        "Dog.doesKnowCommand": _dog_does_know_command_resolver,
    }
)
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            query {
              dog {
                name
                doesKnowCommand(dogCommand: SIT)
              }
            }
            """,
            {"data": {"dog": {"name": "Doggy", "doesKnowCommand": True}}},
        ),
        (
            """
            query {
              dog {
                name
                doesKnowCommand(dogCommand: DOWN)
              }
            }
            """,
            {"data": {"dog": {"name": "Doggy", "doesKnowCommand": False}}},
        ),
    ],
)
async def test_issue103(engine, query, expected):
    assert await engine.execute(query) == expected
