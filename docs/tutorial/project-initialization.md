---
id: project-initialization
title: Initialization of your Tartiflette recipes manager GraphQL API
sidebar_label: 2. Project initialization
---

We are going to create a Tartiflette recipes manager served by a GraphQL API, an exciting application which will allow you to manage efficiently all your recipes.

Here is a list of some features we are going to implement:
* list recipes _(`Query` operation)_
* update a recipe _(`Mutation` operation)_
* launch and wait for the end of the cooking process _(`Subscription` operation)_
* adding rate limiting on updating recipes _(How to implement `directives`)_
* do not expose all your GraphQL API for everyone, limit the administration features, `Mutation`, to administrators


## Initialization of the recipes manager project

Prepare your favorite editor and your terminal, we will switch back and forth between them.

First, create the project's directory called `ttftt-recipes-manager`:
```bash
mkdir ttftt-recipes-manager/

# Move to the directory we just created
cd ttftt-recipes-manager
```

We will put all our python files into the `recipes_manager` Python module:
```bash
mkdir -p recipes_manager
```

Moreover, we are going to create multiple files which will contain our application code:
* `recipes_manager/app.py`: entrypoint of our application. In charge of the initialization of the `tartiflette-aiohttp` server
* `recipes_manager/sdl`: directory which will contain our SDL _(Schema Definition Language)_ files
  * `recipes_manager/sdl/Query.graphql`: schema with our **Query** type
  * `recipes_manager/sdl/Mutation.graphql`: schema with our **Mutation** type
  * `recipes_manager/sdl/Subscription.graphql`: schema with our **Subscription** type
* `recipes_manager/query_resolvers.py`: will contain the **Query** resolvers
* `recipes_manager/mutation_resolvers.py`: will contain the **Mutation** resolvers
* `recipes_manager/subscription_resolvers.py`: will contain the **Subscription** resolvers
* `recipes_manager/data.py`: will contain the data used by the resolvers
* `recipes_manager/directives/auth.py`: will contain the logic of the `@auth` directive
* `recipes_manager/directives/rate_limiting.py`: will contain the logic of the `@rateLimit` directive

```bash
mkdir -p recipes_manager/sdl recipes_manager/directives

touch recipes_manager/__init__.py
touch recipes_manager/__main__.py
touch recipes_manager/directives/__init__.py

touch recipes_manager/app.py
touch recipes_manager/sdl/Query.graphql
touch recipes_manager/sdl/Mutation.graphql
touch recipes_manager/sdl/Subscription.graphql
touch recipes_manager/query_resolvers.py
touch recipes_manager/mutation_resolvers.py
touch recipes_manager/subscription_resolvers.py
touch recipes_manager/data.py
touch recipes_manager/directives/auth.py
touch recipes_manager/directives/rate_limiting.py
```

Your tree should look something like this:
```bash
.
└── recipes_manager
    ├── __init__.py
    ├── __main__.py
    ├── app.py
    ├── data.py
    ├── directives
    │   ├── __init__.py
    │   ├── auth.py
    │   └── rate_limiting.py
    ├── mutation_resolvers.py
    ├── query_resolvers.py
    ├── sdl
    │   ├── Mutation.graphql
    │   ├── Query.graphql
    │   └── Subscription.graphql
    └── subscription_resolvers.py
```

## Our data

We will need some data to execute `query`, `mutation` and `subscription`.

Fill the file **recipes_manager/data.py** with this data:
```python
# Dictionnary which contains the ingredients based on the recipe ID as key.
INGREDIENTS = {
    1: [
        {"name": "potato", "quantity": 10, "type": "UNIT"},
        {"name": "onion", "quantity": 2, "type": "UNIT"},
        {"name": "bacon", "quantity": 100, "type": "GRAM"},
        {"name": "white wine", "quantity": 0.05, "type": "LITER"},
        {"name": "reblochon AOP", "quantity": 1, "type": "UNIT"},
    ],
    2: [
        {"name": "potato", "quantity": 1000, "type": "GRAM"},
        {"name": "bacon", "quantity": 200, "type": "GRAM"},
        {"name": "onion", "quantity": 200, "type": "GRAM"},
        {"name": "reblochon AOP", "quantity": 1, "type": "UNIT"},
        {"name": "tablespoon of oil", "quantity": 2, "type": "UNIT"},
        {"name": "clove of garlic", "quantity": 1, "type": "UNIT"},
    ],
    3: [
        {"name": "potato", "quantity": 1000, "type": "GRAM"},
        {"name": "smoked bacon", "quantity": 200, "type": "GRAM"},
        {"name": "onion", "quantity": 2, "type": "UNIT"},
        {"name": "reblochon AOP", "quantity": 1, "type": "UNIT"},
        {"name": "fresh cream", "quantity": 0.100, "type": "LITER"},
        {"name": "butter", "quantity": 40, "type": "GRAM"},
        {"name": "tablespoon of pepper", "quantity": 1, "type": "UNIT"},
    ],
}

RECIPES = [
    {
        "id": 1,
        "name": "Tartiflette by Eric Guelpa",
        "cookingTime": 15,
    },
    {
        "id": 2,
        "name": "La 'vraie' Tartiflette",
        "cookingTime": 20,
    },
    {
        "id": 3,
        "name": "Tartiflette by Alain Ducasse",
        "cookingTime": 25,
    },
]
```

Let's start coding :tada:
