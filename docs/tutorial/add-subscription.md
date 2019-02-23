---
id: add-subscription
title: Add subscription
sidebar_label: 9. Add subscription (advanced)
---

We discovered how to Query and Mutate data, now, we are going to discover a most advanced part of GraphQL, the [event-based subscriptions](https://graphql.org/blog/subscriptions-in-graphql-and-relay/#event-based-subscriptions), well-known as `subscription` in the specification.

In this tutorial, we'll implement a subscription which will wait for the end of the cooking process for a given recipe.

During the cooking process, we'll notify the user each second about the remaining time, and in the end, we'll notify that the cooking is over.

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
  COOKING,
  COOKED
}

type CookingTimer {
  remainingTime: Int!
  status: CookingStatus!
}
```

## **recipes_manager/subscription_resolvers.py**

In the tartiflette engine, we implemented subscription simply by implementing a specific decorator _(@Subscription)_ over a function which returns an async generators, that it. For advanced use-cases, we suggest you use pub/sub mecanisms like Redis, Nats, Google Pub/Sub, Amazon EQS etc...

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

In case of the message yield is not compliant with the return type, you can apply a resolver to apply a transformation. See more on the [subscription API page](/docs/api/subscription).

## How can we use it?

As specified previously, for this tutorial, we decided to use the simplest form of a Subscription in Tartiflette, and we don't cover the transport layer.

Do you remember that the Recipes Manager GraphQL API is based on the `tartiflette-aiohttp`? Aside from the HTTP layer, we discovered, thanks to the Query and Mutation part, that this project exposes the Subscription operation through a Web Socket.

Remember the **recipes_manager/app.py** file
```python
    web.run_app(
        register_graphql_handlers(
            app=app,
            engine=engine,
            subscription_ws_endpoint="/ws",
            executor_http_endpoint='/graphql',
            executor_http_methods=['POST'],
            graphiql_enabled=True
        )
    )
```

By defining the `subscription_ws_endpoint` parameter, a WebSocket endpoint is created to handle the subscription, this it what we are going to use in the next step.

## Launch the app

Your Recipes Manager GraphQL API is now able to provide subscriptions to your clients. Launch it with this following command and go to the next step to know how deal with subscription in your GraphQL API.

```bash
$ python -m recipes_manager
======== Running on http://0.0.0.0:8080 ========
(Press CTRL+C to quit)

```
