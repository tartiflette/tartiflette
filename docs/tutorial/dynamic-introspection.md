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
from urllib.parse import urlparse

from tartiflette import Directive


def _is_expected_domain(req: "yarl.URL", expected_domain: str) -> bool:
    """
    Determines whether or not the user come from the expected domain.
    :param req: incoming aiohttp request
    :param expected_domain: expected domain from which the user should come
    from
    :type req: yarl.URL
    :type expected_domain: str
    :return: whether or not the user come from the expected domain
    :rtype: bool
    """
    parsed_url = urlparse(str(req.url))
    return parsed_url.hostname == expected_domain


@Directive("auth")
class AuthDirective:
    """
    Directive to limit access to field and introspection if the user doesn't
    come from the expected domain.
    """

    async def on_introspection(
        self,
        directive_args: Dict[str, Any],
        next_directive: Callable,
        introspected_element: Any,
        ctx: Dict[str, Any],
        info: "ResolveInfo",
    ) -> Optional[Any]:
        """
        Blocks the introspection if the user doesn't come from the expected
        domain.
        :param directive_args: computed arguments related to the directive
        :param next_directive: next directive to call
        :param introspected_element: current introspected element
        :param ctx: context filled in at engine initialization
        :param info: information related to the execution and field resolution
        :type directive_args: Dict[str, Any]
        :type next_directive: Callable
        :type introspected_element: Any
        :type ctx: Dict[str, Any]
        :type info: ResolveInfo
        :return: the introspected element
        :rtype: Any
        """
        # This piece of code is built ONLY for tutorial purpose.
        # Do NOT use this in real application.
        if not _is_expected_domain(ctx["req"], directive_args["domain"]):
            return None
        return await next_directive(introspected_element, ctx, info)

    async def on_field_execution(
        self,
        directive_args: Dict[str, Any],
        next_resolver: Callable,
        parent: Optional[Any],
        args: Dict[str, Any],
        ctx: Dict[str, Any],
        info: "ResolveInfo",
    ) -> Any:
        """
        Blocks the field access if the user doesn't come from the expected
        domain.
        :param directive_args: computed arguments related to the directive
        :param next_resolver: next resolver to call
        :param parent: initial value filled in to the engine `execute` or
        `subscribe` method or field parent value
        :param args: computed arguments related to the field
        :param ctx: context filled in at engine initialization
        :param info: information related to the execution and field resolution
        :type directive_args: Dict[str, Any]
        :type next_resolver: Callable
        :type parent: Optional[Any]
        :type args: Dict[str, Any]
        :type ctx: Dict[str, Any]
        :type info: ResolveInfo
        :return: result of the field resolution
        :rtype: Any
        :raises Exception: if the user doesn't come from the expected domain
        """
        # This piece of code is built ONLY for tutorial purpose.
        # Do NOT use this in real application.
        if not _is_expected_domain(ctx["req"], directive_args["domain"]):
            raise Exception(
                "You are not allowed to execute this action. Please retry "
                f"from '{directive_args['domain']}'."
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

directive @auth(domain: String!) on FIELD_DEFINITION

input RecipeInput {
  id: Int!
  name: String
  cookingTime: Int
}

type Mutation {
  updateRecipe(input: RecipeInput!): Recipe! @auth(domain: "localhost") @rateLimiting(name: "update_recipe")
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
    }
  }
}
```

* without the `@auth(domain: "localhost")` you **will** see the `updateRecipe` field
* with the `@auth(domain: "localhost")` in your schema you **will not** see the `updateRecipe` field if your are not using the `localhost` domain

![Auth Directive on introspection](/docs/assets/auth-directive-introspection-v1.gif)

This is the behavior implemented by the `on_introspection` method of our `AuthDirective`.

If you want, you can also test the behavior from the `on_field_execution` method by executing a mutation request on the `updateRecipe` field:

```graphql
mutation {
  updateRecipe(input: {
    id: 1
    name: "The best Tartiflette by Eric Guelpa"
    cookingTime: 12
  }) {
    id
    name
    cookingTime
  }
}
```

![Auth Directive on mutation](/docs/assets/auth-directive-mutation-v1.gif)
