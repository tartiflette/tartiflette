---
id: create-server
title: Create Tartiflette instance
sidebar_label: 4. Create Tartiflette instance
---

Be sure that you followed the [Project initialization](/docs/tutorial/install-tartiflette) step.

We will help you to build the "Recipes Manager" application, we are going to provide some code block. You will have to put all the code block into the `app.py` previously created, which should be empty at this step.

## Write code

### **recipes_manager/sdl/Query.graphql**

As explained on the homepage, our Engine based the schema definition on the [official Schema Definition Language](https://graphql.org/learn/schema/).

We will start to define the `Query` Schema, first.

```graphql
type Query {
  recipes: [Recipe]
  recipe(id: Int!): Recipe
}

enum IngredientType {
    GRAM
    LITER
    UNIT
}

type IngredientQuantity {
    name: String!
    quantity: Float!
    type: IngredientType!
}

type Recipe {
  id: Int
  name: String
  ingredientsQuantity: [IngredientQuantity]
  cookingTime: Int
}
```

### **recipes_manager/app.py**

This following file will be in charge of starting the HTTP Server _(`web.run_app` function)_.

* `register_graphql_handlers` will attach HTTP handlers to the aiohttp application
  * `app`: The aiohttp application (create with `app = web.Application()`)
  * `engine`: Tartiflette engine which will be used by the HTTP Handlers
  * `executor_http_endpoint`: Endpoint where the GraphQL API will be exposed
  * `executor_http_methods`: HTTP methods where the GraphQL API will be exposed _(Only `POST` is advisable)_
  * `graphiql_enabled`: [GraphiQL](https://github.com/graphql/graphiql) client to browse the GraphQL, used mostly in development flow.

```python
import os
from aiohttp import web

from tartiflette import Engine
from tartiflette_aiohttp import register_graphql_handlers

import recipes_manager.query_resolvers
import recipes_manager.mutation_resolvers
import recipes_manager.subscription_resolvers
import recipes_manager.directives.rate_limiting

# Tartiflette Engine, the only one :)
# Will load the SDL files from the ./sdl folder
engine = Engine(
    os.path.dirname(os.path.abspath(__file__)) + "/sdl"
)


def run():
    app = web.Application()

    web.run_app(
        register_graphql_handlers(
            app=app,
            engine=engine,
            executor_http_endpoint='/graphql',
            executor_http_methods=['POST'],
            graphiql_enabled=True
        )
    )
```

### **recipes_manager/__main__.py**

This is the entrypoint of our application, we won't develop more on it.

```python
#!/usr/bin/env python
import sys

from open_data_orleans.app import run

if __name__ == "__main__":
    sys.exit(run())

```

## Launch the app

We are now ready to launch our API. _(Be sure that your shell is inside the virtualenv with the `pipenv shell` command)_.

```bash
$ python -m recipes_manager
======== Running on http://0.0.0.0:8080 ========
(Press CTRL+C to quit)

```

Your **Recipes Manager GraphQL API** is now live. 

But ... there is nothing into it, we are now going to implement our first resolver.