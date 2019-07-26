---
id: add-subscription
title: Add subscription
sidebar_label: 9. Add subscription (advanced)
---

We discovered how to query and mutate data, now, we are going to discover a more advanced part of GraphQL, the [event-based subscriptions](https://graphql.org/blog/subscriptions-in-graphql-and-relay/#event-based-subscriptions), known as the `subscription` operation in the specification.

In this tutorial, we will implement a subscription field which will wait for the end of the cooking process of a given recipe.

During the cooking process, we will notify the client each second about the remaining time, and at the end, we will notify it that the cooking is over.

This feature will allow the client of our GraphQL API to update its UI in real time.

For development purposes, we will consider that the cooking duration is in seconds instead of minutes _(our oven is really powerful!)_.

## Write code

### `recipes_manager/sdl/Subscription.graphql`

First, as usual, we start by defining the `Subscription` schema part.

```graphql
enum CookingStatus {
  COOKING
  COOKED
}

type CookingTimer {
  remainingTime: Int!
  status: CookingStatus!
}

type Subscription {
  launchAndWaitCookingTimer(id: Int!): CookingTimer
}
```

The client will subscribe to the `launchAndWaitCookingTimer` field _(with the recipe ID as an argument)_, and will receive a response each second which will follow the `CookingTimer` type.

### `recipes_manager/subscription_resolvers.py`

In order to make your subscriptions work properly, Tartiflette needs to know for each subscription fields which event stream to listen to. Like for queries and mutations, there is a built-in `@Subscription` decorator which will bind a callable to the specified subscription field. Unlike the `@Resolver` decorator the `@Subscription` decorator can be applied only on a subscription field and have to returns an asynchronous generator. For advanced use-cases, we suggest you using pub/sub mechanisms like Redis, Nats, Google Pub/Sub, Amazon EQS...

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

In case the data `yield`ed is not compliant with the schema's return type, you can apply a resolver to apply a transformation. See more on the [subscription API page](/docs/api/subscription).

## How can we use it?

As mentioned previously, for this tutorial, we decided to use the simplest form of a subscription in Tartiflette, and we did not cover the transport layer.

Do you remember that the **Tartiflette recipes manager** is based on `tartiflette-aiohttp`? Aside from the HTTP layer, it also provides a way to expose subscription operation through a WebSocket.

Remember the **recipes_manager/app.py** file? Let's update it to:
```python
web.run_app(
    register_graphql_handlers(
        app=web.Application(),
        engine_sdl=os.path.dirname(os.path.abspath(__file__)) + "/sdl",
        engine_modules=[
            "recipes_manager.query_resolvers",
            "recipes_manager.mutation_resolvers",
            "recipes_manager.subscription_resolvers",
            "recipes_manager.directives.rate_limiting",
            "recipes_manager.directives.auth",
        ],
        executor_http_endpoint="/graphql",
        executor_http_methods=["POST"],
        graphiql_enabled=True,
        subscription_ws_endpoint="/ws",
    )
)
```

By defining the `subscription_ws_endpoint` parameter, a WebSocket endpoint is created to handle the subscription. This is what we are going to use in the next step.

## Launch the app

Your **Tartiflette recipes manager** is now able to provide subscriptions to your clients. Launch it with this following command and go to the next step to know how to deal with subscriptions in your GraphQL API:

```bash
python -m recipes_manager
```

> Note: WebSockets are only available on `GET` HTTP requests so the `/ws` endpoint is created on a `GET` HTTP endpoint and ignores the `executor_http_methods` which only apply to query and mutation requests on `/graphql`.
