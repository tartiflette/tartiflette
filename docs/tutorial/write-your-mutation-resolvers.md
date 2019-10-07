---
id: write-your-mutation-resolvers
title: Write your mutation resolvers
sidebar_label: 7. Write your mutation resolvers
---

If you plan to build an application, most of the time you will need to provide a way to create, update and delete data over your API. In the REST-full world, this operations are available through some exposed endpoints available on the different `POST`, `PUT`, `PATCH` and `DELETE` HTTP methods. In the GraphQL world, all the actions which mutate the data are available behind the `mutation` operation.

The `mutation` operation type looks like the `query` one but with a major difference in the way of being executed. While root fields of a `query` operation are executed and resolved in parallel, in a `mutation` operation, root fields are executed in serial order.

## Write code

In our case, we would like to be able to update a recipe. Thus, we will expose a field to update a recipe, either its name or/and cooking time.

First, we will start to define the `Mutation` schema part:

### `recipes_manager/sdl/Mutation.graphql`

```graphql
input RecipeInput {
  id: Int!
  name: String
  cookingTime: Int
}

type Mutation {
  updateRecipe(input: RecipeInput!): Recipe!
}
```

### `recipes_manager/mutation_resolvers.py`

And now the resolver which is in charge of updating the recipe metadata:
```python
from typing import Any, Dict, Optional

from tartiflette import Resolver

from recipes_manager.data import RECIPES


@Resolver("Mutation.updateRecipe")
async def resolve_mutation_update_recipe(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: "ResolveInfo",
) -> Dict[str, Any]:
    """
    Resolver in charge of the mutation of a recipe.
    :param parent: initial value filled in to the engine `execute` method
    :param args: computed arguments related to the mutation
    :param ctx: context filled in at engine initialization
    :param info: information related to the execution and field resolution
    :type parent: Optional[Any]
    :type args: Dict[str, Any]
    :type ctx: Dict[str, Any]
    :type info: ResolveInfo
    :return: the mutated recipe
    :rtype: Dict[str, Any]
    :raises Exception: if the recipe id doesn't exist
    """
    recipe_id = args["input"]["id"]
    name = args["input"].get("name")
    cooking_time = args["input"].get("cookingTime")

    if not (name or cooking_time):
        raise Exception(
            "You should provide at least one value for either name or "
            "cookingTime."
        )

    for index, recipe in enumerate(RECIPES):
        if recipe["id"] == recipe_id:
            if name:
                RECIPES[index]["name"] = name
            if cooking_time:
                RECIPES[index]["cookingTime"] = cooking_time
            return RECIPES[index]

    raise Exception(f"The recipe < {recipe_id} > does not exist.")
```

## Launch the app

Your **Tartiflette recipes manager** is now able to mutate data. Launch it with the following command and go to the next step to find out how to execute a mutation request to your GraphQL API:

```bash
python -m recipes_manager
```
