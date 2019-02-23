---
id: write-your-mutation-resolvers
title: Write your mutation resolvers
sidebar_label: 6. Write your mutation resolvers
---

If you plan to build an application, most of the time, you want to expose mutation endpoints, well known as "PUT", "DELETE", "POST" in the REST full world. In the GraphQL world, all the actions which mutate the data are available behind the operation `mutation`. 

The `mutation` type looks like the Query one, with some less features _(no union, interface, arguments)_. 

Thus, we will expose a field to update a recipe, either its name or cooking time.

First, here is the SDL

## **recipes_manager/sdl/Mutation.graphql**

Compare to the Query types, the mutation types are less complex, you have to named them `input` instead of `type`.

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

Below the resolver which is in charge of updating the recipe metadata.

```python
import collections

from tartiflette import Resolver

from recipes_manager.data import INGREDIENTS_QUANTITY, RECIPES


@Resolver("Mutation.updateRecipe")
async def resolver_recipe(parent, args, ctx, info):
    recipe_input = args["input"]
    
    for index, recipe in enumerate(RECIPES):
        if recipe["id"] == recipe_input["id"]:
            if "name" in recipe_input:
                RECIPES[index]["name"] = recipe_input["name"]

            if "cookingTime" in recipe_input:
                RECIPES[index]["cookingTime"] = recipe_input["cookingTime"]

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
