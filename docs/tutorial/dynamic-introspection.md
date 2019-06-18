---
id: dynamic-introspection
title: Dynamic introspection
sidebar_label: 13. Dynamic introspection
---

One of the most powerful features of GraphQL is to provide an introspection of its Schema, which gives the developer the ability to build tools based on the result of the introspection. [The best example is GraphiQL, the GraphQL Explorer.](https://github.com/graphql/graphiql).

## Introspection caveats

### What are the consequences?

Most of the time, people building GraphQL APIs don't restrict the introspection which allows everyone to have detailed information about the schema. This potentially exposes fields, like administration or internal company fields, you would prefer to keep private.

To solve this, we will use **dynamic introspection**. You will be able to update the result of the introspection query, based on your business rules and access control.

You will be able to:
* Provide different introspection schemas based on your business rules (unlogged user, logged user, administrator)
* Completely remove some fields from the introspection
* Append some metadata to the introspection result

## **recipes_manager/directives/auth.py**

The idea of the following code is to create a new directive called "@auth" which allow you to:
* hide fields and/or types from the introspection query.
* restrict the access to fields and/or types

In this following code, we check that the user uses the API endpoint `localhost:8080`, if the user doesn't use this one, like `127.0.0.1:8080` or another, an error will be thrown.

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
        ctx: Optional[Dict[str, Any]],
        info: "Info",
    ) -> Any:
        # We limit the introspection only if the user comes from `localhost:8080`
        # This piece of code is built ONLY for tutorial purpose. Do not use this
        # in real application.
        if ctx["req"].host != "localhost:8080":
            return None

        return await next_directive(introspected_element, ctx, info)


    async def on_field_execution(
        self,
        directive_args: Dict[str, Any],
        next_resolver: Callable,
        parent_result: Optional[Any],
        args: Dict[str, Any],
        ctx: Optional[Dict[str, Any]],
        info: "Info",
    ) -> Any:
        # We limit the introspection only if the user comes from `localhost:8080`
        # This piece of code is built ONLY for tutorial purpose. Do not use this
        # in real application.
        if ctx["req"].host != "localhost:8080":
            raise Exception("You are not allowed to execute this action. Please retry from 'localhost:8080'")

        return await next_resolver(parent_result, args, ctx, info)

```

## **recipes_manager/sdl/Mutation.graphql**

We will update the Mutation SDL by declaring and adding the `@nonIntrospectable` directive.

```python
directive @rateLimiting(
    name: String
    max_attempts: Int = 5
    duration: Int = 60
) on FIELD_DEFINITION

directive @auth(role: String!) on FIELD_DEFINITION

type Mutation {
    updateRecipe(input: RecipeInput!): Recipe @auth(role: "admin") @rateLimiting(name: "update_recipe")
}

input RecipeInput {
    id: Int!
    name: String
    cookingTime: Int
}
```

## How can we test it?

To simulate the non-introspectable feature, make sure that your application is running.

```bash
$ python -m recipes_manager
======== Running on http://0.0.0.0:8080 ========
(Press CTRL+C to quit)

```

### GraphQL Query

Execute the following query to retrieve the list of mutation fields.

* Without the `@auth(role: "admin")` you **will** see the `updateRecipe` field.
* With the `@auth(role: "admin") in your schema you **won't** see the `updateRecipe` if your aren't using the `localhost:8080` endpoint.

```graphql
query IntrospectionQuery {
  __type(name: "Mutation") {
    kind
    name
    fields{
      name
      description
    }
  }
}
```

![Auth Directive](/docs/assets/auth-directive.gif)
