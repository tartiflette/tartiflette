---
id: write-your-resolvers
title: Write your resolvers
sidebar_label: 5. Write your resolvers
---

[Previsouly](/docs/tutorial/create-server), we created our application instance with a [first iteration of our Schema](/docs/tutorial/create-server#recipes-manager-sdl-querygraphql) using the SDL. Now, we're going to bind some data to our Schema, using resolvers, which are in charge of linking the Schema with your application logic.

## What is a resolver?

A resolver is a function _(which can be asynchronous)_ that is attached to a field of your Schema. It will be in charge of providing data accordingly to the fields or objects it is attached to.

### How to attach a resolver to a Schema field with Tartiflette?

With Tartiflette, it is very straighforward to attach a resolver function to Schema field.

We provide a decorator named `Resolver` which will attach your function to the specified Schema field.

```python
from tartiflette import Resolver

@Resolver("Query.hello")
async def resolver_fieldname(parent, args, ctx, info):
    return {
        "foo": "bar"
    }
```

In this example, the function `resolver_fieldname` will be executed each time the field `hello` is called.

> Note: by default, the root type name for query operations is `Query` so the full name of the field is `Query.hello`.

If you want to know more about the Resolver part, we suggest taking a look at [the Resolver API documentation](/docs/api/resolver).

## Write code

In our example we will have 3 different resolvers.
* One which will resolve the recipes list: `@Resolver("Query.recipes")`
* Another which will resolve only one recipe: `@Resolver("Query.recipe")`
* A last one which will resolve a sub field of the `Recipe` object, the ingredients quantity: `@Resolver("Recipe.ingredientsQuantity")`

**filename: recipes_manager/query_resolvers.py**
```python
import collections

from tartiflette import Resolver

from recipes_manager.data import INGREDIENTS_QUANTITY, RECIPES


@Resolver("Query.recipes")
async def resolver_recipe(parent, args, ctx, info):
    return RECIPES


@Resolver("Query.recipe")
async def resolver_recipe(parent, args, ctx, info):
    recipe = [r for r in RECIPES if r["id"] == int(args["id"])]

    if not recipe:
        return None

    return recipe[0]


@Resolver("Recipe.ingredientsQuantity")
async def resolver_recipe(parent, args, ctx, info):
    if parent and parent["id"] in INGREDIENTS_QUANTITY:
        return INGREDIENTS_QUANTITY[parent["id"]]

    return None

```

## Launch the app

Your Recipes Manager GraphQL API is now able to return data. Launch it with the following command and go to the next step to find out how to query your GraphQL API.

```bash
$ python -m recipes_manager
======== Running on http://0.0.0.0:8080 ========
(Press CTRL+C to quit)

```
