---
id: subscription
title: Subscription
sidebar_label: Subscription
---

Subscription is the third operation type available in GraphQL. It brings the [event-based subscriptions](https://graphql.org/blog/subscriptions-in-graphql-and-relay/#event-based-subscriptions) mindset to the engine.

It's up to you to implement the event technology you want, like Google Pub/Sub, Nats, Redis... in our example, we decided to focus purely on the engine part of the feature.

## `Engine`: How to execute a subscription?

The engine is responsible for executing both the `Query`/`Mutation`s and the `Subscription`'s. The first ones are executed by the `execute` method, where `Subscription`, is executed by the `subscribe` method.

The parameters that are available on the `subscribe` method are:
* `query` _(Union[str, bytes])_: the GraphQL request/query as UTF8-encoded string
* `operation_name` _(Optional[str])_: the operation name to execute
* `context` _(Optional[Any])_: value containing anything you could need and which will be available during all the execution process
* `variables` _(Optional[Dict[str, Any]])_: the variables provided in the GraphQL request
* `initial_value` _(Optional[Any])_: an initial value which will be forwarded to the resolver of root type (Query/Mutation/Subscription) fields

```python
from tartiflette import create_engine


engine = await create_engine(
    "myDsl.graphql"
)

async for result in engine.subscribe(
    query="subscription MyLiveVideo($id: String!) { videoLive(id: $id) { id viewsNumber } }",
    operation_name="MyLiveVideo",
    context={
        "mysql_client": MySQLClient(),
        "auth_info": AuthInfo(),
    },
    variables={
        "id": "1234",
    },
    initial_value={},
):
    pass

# each yield `result` will contains something like
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

In the Tartiflette engine, to subscribe to a field, you simply use the decorator `@Subscription` over a callable which returns an `async generator`. That's all there is to it. For advanced use-cases, take a look at putting a `@Resolver` on top of a `Subscription` ([see below](#resolver-manipulating-and-shaping-the-result-of-a-subscription-function)).

```python
import asyncio

from tartiflette import Subscription

from recipes_manager.data import RECIPES


@Subscription("Subscription.launchAndWaitCookingTimer")
async def subscribe_subscription_launch_and_wait_cooking_timer(
    parent, args, ctx, info
):
    recipe = None
    for recipe_item in RECIPES:
      if recipe_item["id"] == args["id"]:
        recipe = recipe_item

    if not recipe:
        raise Exception(f"The recipe < {args['id']} > does not exist.")

    for i in range(recipe["cookingTime"]):
        yield {
            "remainingTime": recipe["cookingTime"] - i,
            "status": "COOKING",
        }
        await asyncio.sleep(1)

    yield {
        "launchAndWaitCookingTimer": {
            "remainingTime": 0,
            "status": "COOKED",
        },
    }
```

## Decorator signature

* `name` _(str)_: fully qualified field name to resolve
* `schema_name` _(str = "default")_: name of the schema to which link the subscription
* `arguments_coercer` _(Optional[Callable] = None)_: callable to use to coerce field arguments

The `arguments_coercer` parameter is here to provide an easy way to override the default callable used internaly by Tartiflette to coerce the arguments of the field. It has the same behaviour as the `custom_default_arguments_coercer` parameter at engine initialisation but impact only the field.

## `@Resolver`: Manipulating and shaping the result of a `@Subscription` function

In some cases, especially when you use tools like Redis, Google Pub/Sub etc... the value which will be `yield`ed won't be structured as expected by the schema. In addition to the `@Subscription` decorator, you can implement a `@Resolver` wrapper to shape the data accordingly to the return type.

```python
import asyncio

from tartiflette import Resolver, Subscription

from recipes_manager.data import RECIPES


@Resolver("Subscription.launchAndWaitCookingTimer")
async def resolve_subscription_launch_and_wait_cooking_timer(
    parent, args, ctx, info
):
    if parent > 0:
        return {
            "remainingTime": parent,
            "status": "COOKING",
        }
    return {
        "remainingTime": 0,
        "status": "COOKED",
    }


@Subscription("Subscription.launchAndWaitCookingTimer")
async def subscribe_subscription_launch_and_wait_cooking_timer(
    parent, args, ctx, info
):
    recipe = None
    for recipe_item in RECIPES:
      if recipe_item["id"] == args["id"]:
        recipe = recipe_item

    if not recipe:
        raise Exception(f"The recipe < {args['id']} > does not exist.")

    for i in range(recipe["cookingTime"]):
        yield recipe["cookingTime"] - i
        await asyncio.sleep(1)
```
