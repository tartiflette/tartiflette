---
id: extend-with-directives
title: Extend with directives
sidebar_label: 11. Extend with directives
---

A directive is a way of describing a behavior you can apply on differents objects in your SDL. It looks like a Decorator in our favorite language, Python. The possible applications are numerous, access permissions, limit the introspection, rate limiting, auto-generating resolver function etc ... the only limit is your imagination.

Tartiflette includes the `@deprecated` directive, which allow you to define a field as deprecated _(The introspection will flag the field as deprecated)_.

```graphql
directive @deprecated(
  reason: String = "No longer supported"
) on FIELD_DEFINITION | ENUM_VALUE

type Recipe {
  id: Int
  name: String
  ingredientsQuantity: [IngredientQuantity]
  cookingTime: Int
  title: String @deprecated(reason: "Use `name` instead.")
}
```

## How to implement?

Tartiflette bases most of its extensibility on Directives. A directive will allow you to execute some behavior at 4 stages.

* `on_build`: Implement some behavior during the build process of the SDL
* `on_field_execution`: Implement a specific behavior during the field execution. _(e.g Access Rights on a specific field, apply a specific rate limit on a field.)_
* `on_argument_execution`: Implement a specific behavior during the argument execution. _(e.g Check the format of an input.)_
* `on_introspection`: During an introspection query, allow you to append some metadata to the fields or even give you the ability to remove objects _(e.g dynamic introspection based on access rights)_

### How to declare a new directive?

```python
from typing import Any, Callable, Dict, Optional

from tartiflette.directive import Directive, CommonDirective


@Directive("rateLimiting")
class RateLimiting(CommonDirective):
    @staticmethod
    def on_build(_schema: "GraphQLSchema") -> None:
        ######################
        # Add your code here #
        ######################

    @staticmethod
    async def on_field_execution(
        directive_args: Dict[str, Any],
        next_resolver: Callable,
        parent_result: Optional[Any],
        args: Dict[str, Any],
        ctx: Optional[Dict[str, Any]],
        info: "Info",
    ) -> Any:
        ######################
        # Add your code here #
        ######################
        return await next_resolver(parent_result, args, ctx, info)
    
    @staticmethod
    async def on_argument_execution(
        directive_args: Dict[str, Any],
        next_directive: Callable,
        argument_definition: "GraphQLArgument",
        args: Dict[str, Any],
        ctx: Optional[Dict[str, Any]],
        info: "Info",
    ) -> Any:
        ######################
        # Add your code here #
        ######################
        return await next_directive(argument_definition, args, ctx, info)

    @staticmethod
    def on_introspection(
        directive_args: Dict[str, Any],
        next_directive: Callable,
        introspected_element: Any,
        ctx: Optional[Dict[str, Any]],
        info: "Info",
    ) -> Any:
        ######################
        # Add your code here #
        ######################
        return next_directive(introspected_element)
```

In the next steps we will implement some specific behavior based on the directives.