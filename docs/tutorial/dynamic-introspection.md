---
id: dynamic-introspection
title: Dynamic introspection
sidebar_label: 13. Dynamic introspection
---

One of the most powerful feature of GraphQL is to provide an introspection on its own Schema, which gives the ability to the developer to build some interesting tools based on this introspection. [The best example is graphiql, the GraphQL Explorer.](https://github.com/graphql/graphiql).

## Introspection caveats

Most of the time, those who build GraphQL APIs, don't restrict the introspection use based on the access rights.

### What are the impacts?

If you restrict some fields for your administration panel, or for some premium users. Those who will query your GraphQL API with an introspection Query, will get the whole shape of Schema, with the fields, types etc ... They will be able to know how your products are built, which data you have ...

This is what we want to solve with **the dynamic introspection**. You will be able to update the result of the introspection query, based on your business rules.

You will be able to:
* Provide differents introspection schema based on your business rules (unlogged user, logged user, administrator)
* Remove completely some fields from the introspection
* Append some metadata to the introspection result

## **recipes_manager/directives/non_introspectable.py**

The idea of this following code is to create a new directive called "@nonIntrospectable" which allow you to hide some fields/types from the introspection query.

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
        # based it on:
        # - the directive arguments (directive_args)
        # - the context (ctx)
        # - the information Query (Schema, Query ...)
        return None

```

## **recipes_manager/sdl/Mutation.graphql**

We will update a little bit the Mutation SDL by declaring and adding the `@nonIntrospectable` directive.

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

Execute this following query to retrieve the list of mutation fields.

* Without the `@nonIntrospectable` you **will** see the `updateRecipe` field.
* With the `@nonIntrospectable` you **won't** see the `updateRecipe` field.

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