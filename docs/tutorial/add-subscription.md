---
id: add-subscription
title: Add subscription
sidebar_label: 9. Add subscription (advanced)
---

We discovered how to Query and Mutate data, now, we are going to discover a more advanced part of GraphQL, the [event-based subscriptions](https://graphql.org/blog/subscriptions-in-graphql-and-relay/#event-based-subscriptions), known as the `subscription` operation in the specification.

In this tutorial, we'll implement a subscription which will wait for the end of the cooking process for a given recipe.

During the cooking process, we'll notify the client each second about the remaining time, and at the end, we'll notify that the cooking is over.

This feature will allow the client of our GraphQL API to update its UI in real time.

For development purposes, we'll consider that the cooking duration is in seconds instead of minutes _(Our oven is really powerful !)_.

## **recipes_manager/sdl/Subscription.graphql**

First, as usual, we define the SDL.

* `launchAndWaitCookingTimer`: The client will subscribe to this field _(with the recipe id as a parameter)_, and will receive a message each second which will follow the `CookingTimer` type.

```graphql
type Subscription {
    launchAndWaitCookingTimer(id: Int!): CookingTimer
}

enum CookingStatus {
    COOKING
    COOKED
}

type CookingTimer {
    remainingTime: Int!
    status: CookingStatus!
}
```

## **recipes_manager/subscription_resolvers.py**

In the Tartiflette Engine, we allow you to link a subscription resolver to your schema simply by using the corresponding decorator _(@Subscription)_ over a function which returns an async generator, that it. For advanced use-cases, we suggest using pub/sub mechanisms like Redis, Nats, Google Pub/Sub, Amazon EQS etc...

```python
import asyncio

from tartiflette import Subscription

from recipes_manager.data import RECIPES


@Subscription("Subscription.launchAndWaitCookingTimer")
async def on_cooking_time(
    parent, args, ctx, info
):
    recipe = [r for r in RECIPES if r["id"] == int(args["id"])]

    if not recipe:
        raise Exception(f"The recipe with the id '{args['id']}' doesn't exist.")

    for index in range(0, recipe[0]["cookingTime"]):
        yield {
            "remainingTime": recipe[0]["cookingTime"] - index,
            "status": "COOKING"
        }

        await asyncio.sleep(1)

    yield {
        "remainingTime": 0,
        "status": "COOKED"
    }
```

In case the data `yield`ed is not compliant with the Schema's return type, you can apply a resolver to apply a transformation. See more on the [subscription API page](../api/subscription.md).

## How can we use it?

As mentioned previously, for this tutorial, we decided to use the simplest form of a Subscription in Tartiflette, and we didn't cover the transport layer.

Do you remember that the Recipes Manager GraphQL API is based on the `tartiflette-aiohttp`? Aside from the HTTP layer, it also provides a way to expose Subscription operations through a Web Socket.

Remember the **recipes_manager/app.py** file?
```python
    web.run_app(
        register_graphql_handlers(
            app=app,
            engine_sdl="sdl ...",
            subscription_ws_endpoint="/ws",
            executor_http_endpoint='/graphql',
            executor_http_methods=['POST'],
            graphiql_enabled=True
        )
    )
```

By defining the `subscription_ws_endpoint` parameter, a WebSocket endpoint is created to handle the subscription. This is what we are going to use in the next step.

## Launch the app

Your Recipes Manager GraphQL API is now able to provide subscriptions to your clients. Launch it with this following command and go to the next step to know how to deal with subscriptions in your GraphQL API.

> Note: WebSockets are only available on `GET` HTTP requests so the `/ws` endpoint is created on a `GET` HTTP endpoint and ignores the `executor_http_methods` which only apply to query and mutation requests on `/graphql`.

```bash
$ python -m recipes_manager
======== Running on http://0.0.0.0:8080 ========
(Press CTRL+C to quit)

```
