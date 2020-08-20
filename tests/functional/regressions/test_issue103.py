import pytest

from tartiflette import Resolver


def bakery(schema_name):
    @Resolver("Query.dog", schema_name=schema_name)
    async def resolve_query_dog(*_args, **__kwargs):
        return {"name": "Doggy"}

    @Resolver("Dog.doesKnowCommand", schema_name=schema_name)
    async def resolve_dog_does_know_command(_parent, args, *_args, **__kwargs):
        return args["dogCommand"] == "SIT"


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="animals", bakery=bakery)
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
async def test_issue103(schema_stack, query, expected):
    assert await schema_stack.execute(query) == expected
