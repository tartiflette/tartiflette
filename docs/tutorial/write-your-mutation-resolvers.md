---
id: write-your-mutation-resolvers
title: Write your mutation resolvers
sidebar_label: 7. Write your mutation resolvers
---

If you plan to build an application, most of the time, you want to expose mutation endpoints, well known as "PUT", "DELETE" and "POST" in the REST-full world. In the GraphQL world though, all the actions which mutate the data are available behind the `mutation` operation.

The `mutation` operation type looks like the `query` one but with some features less _(no unions, interfaces, arguments)_.

Thus, we will expose a field to update a recipe, either its name or cooking time.

First, here is the SDL

## **recipes_manager/sdl/Mutation.graphql**

Compared to the `query` types, the `mutation` types are less complex, you have to name them `input` instead of `type`.

```graphql
type Mutation {
    updateRecipe(input: RecipeInput!): Recipe
}

input RecipeInput {
    id: Int!
    name: String
    cookingTime: Int
}
```

## **recipes_manager/mutation_resolvers.py**

And now the resolver which is in charge of updating the recipe metadata.

```python
import collections

from tartiflette import Resolver

from recipes_manager.data import INGREDIENTS, RECIPES


@Resolver("Mutation.updateRecipe")
async def update_recipe(parent, args, ctx, info):
    if not args.get("input"):
        raise Exception("'input' parameter is mandatory")

    for index, recipe in enumerate(RECIPES):
        if recipe["id"] == args["input"].get("id"):
            if "name" in args["input"]:
                RECIPES[index]["name"] = args["input"]["name"]

            if "cookingTime" in args["input"]:
                RECIPES[index]["cookingTime"] = args["input"]["cookingTime"]

            return RECIPES[index]

    raise Exception("The recipe specified is not found.")

```

## Launch the app

Your Recipes Manager GraphQL API is now able to mutate data. Launch it with this following command and go to the next step to know how to execute a mutation your GraphQL API.

```bash
$ python -m recipes_manager
======== Running on http://0.0.0.0:8080 ========
(Press CTRL+C to quit)

```
