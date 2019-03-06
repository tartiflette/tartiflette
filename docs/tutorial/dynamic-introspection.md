---
id: dynamic-introspection
title: Dynamic introspection
sidebar_label: 13. Dynamic introspection
---

One of the most powerful feature of GraphQL is to provide an introspection of its own Schema, which gives the developer the ability to build tools based on the result of the introspection. [The best example is GraphiQL, the GraphQL Explorer.](https://github.com/graphql/graphiql).

## Introspection caveats

### What are the consequences ?

Most of the time, people building GraphQL APIs don't restrict the introspection which allows everyone to have detailed information about the schema. This potentially exposes fields, like administration or internal company fields, you would prefer to keep private.

To solve this, we will use **dynamic introspection**. You will be able to update the result of the introspection query, based on your business rules and access control.

You will be able to:
* Provide different introspection schemas based on your business rules (unlogged user, logged user, administrator)
* Completely remove some fields from the introspection
* Append some metadata to the introspection result

## **recipes_manager/directives/non_introspectable.py**

The idea of the following code is to create a new directive called "@nonIntrospectable" which allow you to hide some fields and/or types from the introspection query.

```python
from typing import Any, Callable, Dict, Optional

from tartiflette.directive import Directive
from tartiflette.directive import CommonDirective


@Directive("nonIntrospectable")
class NonIntrospectable(CommonDirective):
    @staticmethod
    def on_introspection(
        directive_args: Dict[str, Any],
        next_directive: Callable,
        introspected_element: Any,
        ctx: Optional[Dict[str, Any]],
        info: "Info",
    ) -> Any:
        # Improve the behavior of the introspection and
        # base it on:
        # - the directive arguments (directive_args)
        # - the context (ctx)
        # - the information Query (Schema, Query ...)
        return None

```

## **recipes_manager/sdl/Mutation.graphql**

We will update the Mutation SDL by declaring and adding the `@nonIntrospectable` directive.

```python
directive @rateLimiting(
  name: String
  max_attempts: Int = 5
  duration: Int = 60
) on FIELD_DEFINITION

directive @nonIntrospectable on FIELD_DEFINITION

type Mutation {
  updateRecipe(input: RecipeInput!): Recipe @rateLimiting(name: "update_recipe") @nonIntrospectable
}

input RecipeInput {
  id: Int!
  name: String
  cookingTime: Int
}
```

## How can we test it?

In order to simulate the non introspectable feature. Be sure that your application is running.

```bash
$ python -m recipes_manager
======== Running on http://0.0.0.0:8080 ========
(Press CTRL+C to quit)

```

### GraphQL Query

Execute the following query to retrieve the list of mutation fields.

* Without the `@nonIntrospectable` you **will** see the `updateRecipe` field.
* With the `@nonIntrospectable` in your schema you **won't** see the `updateRecipe` field.

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

![Non introspectable directive](/docs/assets/nonintrospectable-directive.gif)
