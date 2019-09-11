---
id: dynamic-introspection
title: Dynamic introspection
sidebar_label: 13. Dynamic introspection
---

One of the most powerful features of GraphQL is to provide an introspection of its schema, which gives the developer the ability to build tools based on the result of the introspection. [The best example is GraphiQL, the GraphQL Explorer](https://github.com/graphql/graphiql).

## Introspection caveats

### What are the consequences?

Most of the time, people building GraphQL APIs do not restrict the introspection which allows everyone to have detailed information about the schema. This potentially exposes fields, like administration or internal company fields, you would prefer to keep private.

To solve this, we will use **dynamic introspection**. You will be able to update the result of the introspection query, based on your business rules and access control.

You will be able to:
* provide different introspection schemas based on your business rules (unlogged user, logged user, administrator)
* completely remove some fields from the introspection
* append some metadata to the introspection result

## Write code

### `recipes_manager/directives/auth.py`

The idea of the following code is to create a new directive called `@auth` which allow you to:
* hide fields and/or types from the introspection query
* restrict the access to fields and/or types

In this following code, we check that the user uses the API through the domain `localhost`, if the user does not use this one, like `127.0.0.1` or another, an error will be thrown.

Useless to say that this example is suited for this tutorial and must not be put in a real application.

```python
from typing import Any, Callable, Dict, Optional

from tartiflette import Directive


@Directive("auth")
class Auth:
    async def on_introspection(
        self,
        directive_args: Dict[str, Any],
        next_directive: Callable,
        introspected_element: Any,
        ctx: Optional[Any],
        info: "ResolveInfo",
    ) -> Any:
        # We limit the introspection only if the user comes from `localhost`.
        # This piece of code is built ONLY for tutorial purpose.
        # Do not use this in real application.
        if not ctx["req"].host.startswith("localhost"):
            return None
        return await next_directive(introspected_element, ctx, info)

    async def on_field_execution(
        self,
        directive_args: Dict[str, Any],
        next_resolver: Callable,
        parent: Optional[Any],
        args: Dict[str, Any],
        ctx: Optional[Any],
        info: "ResolveInfo",
    ) -> Any:
        # We limit the introspection only if the user comes from `localhost`.
        # This piece of code is built ONLY for tutorial purpose.
        # Do not use this in real application.
        if not ctx["req"].host.startswith("localhost"):
            raise Exception(
                "You are not allowed to execute this action. Please retry "
                "from 'localhost'"
            )
        return await next_resolver(parent, args, ctx, info)
```

### `recipes_manager/sdl/Mutation.graphql`

We will update the Mutation SDL by declaring and adding the `@auth` directive.

```graphql
directive @rateLimiting(
  name: String!
  maxAttempts: Int! = 5
  duration: Int! = 60
) on FIELD_DEFINITION

directive @auth(role: String!) on FIELD_DEFINITION

input RecipeInput {
  id: Int!
  name: String
  cookingTime: Int
}

type Mutation {
  updateRecipe(input: RecipeInput!): Recipe! @auth(role: "admin") @rateLimiting(name: "update_recipe")
}
```

## How can we test it?

To simulate the `@auth` feature, make sure that your application is running:

```bash
python -m recipes_manager
```

### GraphQL request

Execute the following request to retrieve the list of mutation fields:

```graphql
query IntrospectionQuery {
  __type(name: "Mutation") {
    kind
    name
    fields {
      name
      description
    }
  }
}
```

* without the `@auth(role: "admin")` you **will** see the `updateRecipe` field
* with the `@auth(role: "admin")` in your schema you **will not** see the `updateRecipe` field if your are not using the `localhost` domain

![Auth Directive](/docs/assets/auth-directive.gif)
