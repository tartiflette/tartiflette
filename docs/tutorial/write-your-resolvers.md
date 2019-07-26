---
id: write-your-resolvers
title: Write your resolvers
sidebar_label: 5. Write your resolvers
---

[Previously](/docs/tutorial/create-server), we created our application instance with a [first iteration of our schema](/docs/tutorial/create-server#recipes-manager-sdl-querygraphql) using the SDL. Now, we are going to bind our **Query** type fields to some data. This is done using resolvers which are in charge of your application logic.

## What is a resolver?

A resolver is a callable _(which has to be asynchronous)_ that is attached to a field of your schema. It will be in charge of returning data accordingly to the field it is bind to.

### How to attach a resolver to a field with Tartiflette?

With Tartiflette, it is very straightforward to bind a resolver to a field.

There is a built-in `@Resolver` decorator which will bind your callable to the specified field:
```python
from tartiflette import Resolver


@Resolver("Query.hello")
async def resolve_query_hello(parent, args, ctx, info):
    return "Hello"
```

In this example, the function `resolve_query_hello` will be executed each time the root field `hello` is called.

> Note: by default, the root type name for query operations is `Query` so the full name of the field is `Query.hello`.

If you want to know more about the `@Resolver` decorator, we suggest you taking a look at [the `@Resolver` API documentation](/docs/api/resolver).

## Write code

In our example, we will have 3 different resolvers:
* one which will resolve the recipes list: `@Resolver("Query.recipes")`
* another which will resolve only one recipe: `@Resolver("Query.recipe")`
* a last one which will resolve a subfield of the `Recipe` type, the ingredients: `@Resolver("Recipe.ingredients")`

### `recipes_manager/query_resolvers.py`

```python
import collections

from tartiflette import Resolver

from recipes_manager.data import INGREDIENTS, RECIPES


@Resolver("Query.recipes")
async def resolve_query_recipes(parent, args, ctx, info):
    return RECIPES


@Resolver("Query.recipe")
async def resolve_query_recipe(parent, args, ctx, info):
    for recipe in RECIPES:
        if recipe["id"] == args["id"]:
            return recipe
    return None


@Resolver("Recipe.ingredients")
async def resolve_recipe_ingredients(parent, args, ctx, info):
    if parent and parent["id"] in INGREDIENTS:
        return INGREDIENTS[parent["id"]]
    return None
```

## Launch the app

Your **Tartiflette recipes manager** is now able to return data. Launch it with the following command and go to the next step to find out how to execute a query request to your GraphQL API:

```bash
python -m recipes_manager
```
