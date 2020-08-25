import asyncio

import pytest

from tartiflette import Resolver, Subscription


def bakery(schema_name):
    @Subscription("Subscription.newDog", schema_name=schema_name)
    async def subscribe_new_dog(*_args, **_kwargs):
        counter = 0
        while counter < 4:
            counter += 1
            yield counter
            await asyncio.sleep(1)

    @Resolver("Subscription.newDog", schema_name=schema_name)
    async def resolve_subscription_new_dog(counter, *_args, **_kwargs):
        return {
            "name": "Dog #%s" % counter,
            "nickname": "Doggo #%s" % counter,
            "barkVolume": counter,
        }


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="animals", bakery=bakery)
@pytest.mark.parametrize(
    "query",
    [
        """
        subscription {
          newDog {
            name
            nickname
            barkVolume
          }
        }
        """
    ],
)
async def test_issue113(schema_stack, query):
    assert await schema_stack.execute(query)
