---
id: create-server
title: Create a Tartiflette server
sidebar_label: 4. Create a Tartiflette server
---

Make sure you followed the [Project initialization](./install-tartiflette.md) steps.

To help you with the code to build the "Tartiflette recipes manager" application, we will provide some code blocks. Simply copy/paste the code into the appropriate file (which has been created at the previous step and which should be empty for now).

## Write code

### `recipes_manager/sdl/Query.graphql`

As explained on the homepage, Tartiflette use the official [Schema Definition Language](https://graphql.org/learn/schema/) to define the GraphQL API schema.

We will start to define the `Query` schema part, first:
```graphql
enum UnitMeasurement {
  GRAM
  LITER
  UNIT
}

type Ingredient {
  name: String!
  quantity: Float!
  unitMeasurement: UnitMeasurement!
}

type Recipe {
  id: Int!
  name: String!
  ingredients: [Ingredient!]!
  cookingTime: Int!
}

type Query {
  recipes: [Recipe!]
  recipe(id: Int!): Recipe
}
```

### `recipes_manager/app.py`

The following file will be in charge of running the HTTP server _(`web.run_app` function)_.

* `register_graphql_handlers` will attach HTTP handlers to the `aiohttp` application
  * `app`: the `aiohttp` application (created with `web.Application()`)
  * `engine_sdl`: the Tartiflette engine which will be used by the HTTP handlers
  * `engine_modules`: the modules list which will be loaded by Tartiflette at cooking time _(building process)_
  * `executor_http_endpoint`: endpoint path where the GraphQL API will be exposed
  * `executor_http_methods`: HTTP methods on which the GraphQL API will be exposed _(we recommend to expose it only on `POST`)_
  * `graphiql_enabled`: a [GraphiQL](https://github.com/graphql/graphiql) client to browse the GraphQL, used mostly for development

```python
import os

from aiohttp import web

from tartiflette_aiohttp import register_graphql_handlers


def run():
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
        )
    )
```

### `recipes_manager/__main__.py`

This is the entrypoint of our application, we will not go into more details here.

```python
#!/usr/bin/env python
import sys

from recipes_manager.app import run


if __name__ == "__main__":
    sys.exit(run())
```

## Launch the app

We are now ready to launch our GraphQL API. _(make sure that your shell is inside the virtual environment with the `pipenv shell` command)_.

```bash
python -m recipes_manager
```

Your **Tartiflette recipes manager** is now live.

But there is nothing in it... yet. We are now going to implement our first resolver.
