---
id: subscription
title: Subscription
sidebar_label: Subscription
---

Subscription is the third operation available in GraphQL. It brings the [event-based subscriptions](https://graphql.org/blog/subscriptions-in-graphql-and-relay/#event-based-subscriptions) mindset to the Engine.

It's up to you to implement the Event technology you want, like Google Pub/Sub, Nats, Redis ... in our example, we decided to focus purely on the Engine part of the feature.

## `Engine`: How to execute a subscription?

The Engine is responsible for executing both the `Query`/`Mutation`s and the `Subscription`'s. The first ones are executed by the `execute` method, where the `Subscription`, is executed by the method named `subscribe`.

The parameters that are available on the `subscribe` method of `Engine`.
* `query`: the GraphQL request / query as UTF8-encoded string
* `operation_name`: the operation name to execute
* `context`: a dict containing anything you need
* `variables`: the variables used in the GraphQL request
* `initial_value`: an initial value given to the resolver of the root type

```python
from tartiflette import create_engine

engine = await create_engine(
    "myDsl.graphql"
)

result = engine.subscribe(
    query="subscription MyLiveVideo($id: String) { videoLive(id: $id) { id viewsNumber } }",
    operation_name="MyLiveVideo",
    context={
        "mysql_client": MySQLClient(),
        "auth_info": AuthInfo()
    },
    variables: {
        "id": "1234"
    },
    initial_value: {}
)

# `result` will yield with this kind of values
# {
#     "data": {
#         "videoLive": {
#             "id": "1234",
#             "viewsNumber": 87564
#         }
#     }
# }
```

## `@Subscription`: How to subscribe to a field?

In the Tartiflette Engine to subscribe to a field, you simply use the decorator _(@Subscription)_ over a function which returns an async generator. That's all there is to it. For advanced use-cases, take a look at putting a `Resolver` on top of a `Subscription` (see below).

```python
import asyncio

from tartiflette import Subscription

from recipes_manager.data import RECIPES

@Subscription("Subscription.launchAndWaitCookingTimer")
async def subscription_cooking_time(
    parent_result, args, ctx, info
):
  recipe = [r for r in RECIPES if r["id"] == int(args["id"])]

  if not recipe:
    raise Exception(f"The recipe with the id '{args['d']}' doesn't exist.")

  for index in range(0, recipe[0]["cookingTime"]):
    await asyncio.sleep(1)

    yield {
      "remainingTime": recipe[0]["cookingTime"] - index,
      "status": "COOKING"
    }

  yield {
    "remainingTime": 0,
    "status": "COOKED"
  }
```

## `@Resolver`: Manipulating and shaping the result of a `@Subscription` function

In some cases, especially when you use tools like Redis, Google Pub/Sub etc ... the value which will be `yield`ed won't be structured as expected by the Schema. In addition to the `@Subscription` decorator, you can implement a wrapper `@Resolver` to shape the data accordingly to the return type.

```python
import asyncio

from tartiflette import Resolver, Subscription

from recipes_manager.data import RECIPES

@Resolver("Subscription.launchAndWaitCookingTimer")
async def resolver_cooking_time(
    parent_result, args, ctx, info
):
  if parent_result > 0:
    return {
      "remainingTime": parent_result,
      "status": "COOKING"
    }
  
  return {
    "remainingTime": 0,
    "status": "COOKED"
  }


@Subscription("Subscription.launchAndWaitCookingTimer")
async def subscription_cooking_time(
    parent_result, args, ctx, info
):
  recipe = [r for r in RECIPES if r["id"] == int(args["id"])]

  if not recipe:
    raise Exception(f"The recipe with the id '{args['d']}' doesn't exist.")

  for index in range(0, recipe[0]["cookingTime"]):
    await asyncio.sleep(1)
    yield recipe[0]["cookingTime"] - index

```