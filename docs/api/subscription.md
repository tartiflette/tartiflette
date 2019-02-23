---
id: subscription
title: Subscription
sidebar_label: Subscription
---

Subscription is the third operation available on GraphQL. It bring the [event-based subscriptions](https://graphql.org/blog/subscriptions-in-graphql-and-relay/#event-based-subscriptions) mindset to the Engine.

Up to you to implement the Event technology you want, like Google Pub/Sub, Nats, Redis ... in our example, we decided to focus on the feature.

## `Engine`: How to execute the subscription?

The Engine is responsible of executing both the Query/Mutation and the Subscription. The first ones are executed by the `execute` method, and the last one, Subscription, is executed by the method named `subscribe`.

Here are the parameters available on the `subscribe` method of `Engine`.
* `query`: the GraphQL request / query as UTF8-encoded string
* `operation_name`: the operation name to execute
* `context`: a dict containing anything you need
* `variables`: the variables used in the GraphQL request
* `initial_value`: an initial value corresponding to the root type being executed

```python

import tartiflette

engine = tartiflette.Engine(
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

# `result` will yield with that kind of values
# {
#     "data": {
#         "videoLive": {
#             "id": "1234",
#             "viewsNumber": 87564
#         }
#     }
# }
```

## `@Subscription` How to subscribe to a field?

In the tartiflette engine, we implemented subscription simply by implementing a specific decorator _(@Subscription)_ over a function which returns an async generators, that it. For advanced use-cases, take a look of putting a Resolver on top of a `Resolver`.

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

## `@Resolver`: Manipulation and shape the result of a `@Subscription` function

In some cases, especially when you use tools like Redis, Google Pub/Sub etc ... the value which will be yield won't be structured as expected by the Schema. In addition to the `@Subscription`, you can implement the `@Resolver` to shape the data accordingly to the return type.

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