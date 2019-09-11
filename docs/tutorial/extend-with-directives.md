---
id: extend-with-directives
title: Extend with directives
sidebar_label: 11. Extend with directives
---

A directive is a way of describing a behavior you can apply to different objects in your SDL. It looks like a decorator in our favorite language, Python. The possible applications are numerous, access permissions, limiting the introspection, rate limiting, auto-generating resolver function etc... the only limit is your imagination.

Tartiflette provides a bunch of built-ins directives:
* `@deprecated`: allows you to mark a field or an enum value as deprecated _(this introspection will flag them as deprecated)_
* `@skip`: allows for conditional exclusion of fields, fragment spreads, and inline fragments during execution as described by the if argument
* `@include`: allows for conditional inclusion of fields, fragment spreads, and inline fragments during execution as described by the if argument
* `@nonIntrospectable`: allows you to hide elements of your SDL from the introspection query

## How to use a directive?

As explain above, directive looks like a decorator in Python and are used the same way. For instance, in the following SDL, we will define a `Recipe` type with a deprecated `title` field:
```graphql
directive @deprecated(
  reason: String = "No longer supported"
) on FIELD_DEFINITION | ENUM_VALUE

type Recipe {
  id: Int!
  name: String!
  ingredients: [Ingredient!]!
  cookingTime: Int!
  title: String! @deprecated(reason: "Use `name` instead.")
}
```

## How to implement?

Tartiflette gets most of its extensibility by directives. A directive will allow you to execute some logic at any of the following stages:

* `on_argument_execution`: allows you to wrap the argument execution. _(e.g. access rights, validate the input format...)_
* `on_post_input_coercion`: allows you to hook the execution flow right after an input value/variable has beed coerced (appears in version `0.10.0`)
* `on_field_execution`: allows you to wrap the field execution. _(e.g. resolve the field remotly, apply a specific rate limit on a field...)_
* `on_pre_output_coercion`: allows you to mutate the result of the resolved value of a field before returning it
* `on_introspection`: during an introspection query, allows you to wrap the schema fields to add metadata to fields or even to remove objects _(e.g. dynamic introspection based on access rights)_

### How to declare a new directive?

```python
from typing import Any, Callable, Dict, Optional, Union

from tartiflette import Directive


@Directive("rateLimiting")
class RateLimiting:
    async def on_argument_execution(
        self,
        directive_args: Dict[str, Any],
        next_directive: Callable,
        parent_node: Union["FieldNode", "DirectiveNode"],
        argument_node: "ArgumentNode",
        value: Any,
        ctx: Optional[Any],
    ) -> Any:
        ######################
        # Add your code here #
        ######################
        return await next_directive(parent_node, argument_node, value, ctx)

    async def on_post_input_coercion(
        self,
        directive_args: Dict[str, Any],
        next_directive: Callable,
        parent_node: Union["VariableDefinitionNode", "InputValueDefinitionNode"],
        value: Any,
        ctx: Optional[Any],
    ) -> Any:
        ######################
        # Add your code here #
        ######################
        return await next_directive(parent_node, value, ctx)

    async def on_field_execution(
        self,
        directive_args: Dict[str, Any],
        next_resolver: Callable,
        parent: Optional[Any],
        args: Dict[str, Any],
        ctx: Optional[Any],
        info: "ResolveInfo",
    ) -> Any:
        ######################
        # Add your code here #
        ######################
        return await next_resolver(parent, args, ctx, info)

    async def on_pre_output_coercion(
        directive_args: Dict[str, Any],
        next_directive: Callable,
        value: Any,
        ctx: Optional[Any],
        info: "ResolveInfo",
    ) -> Any:
        ######################
        # Add your code here #
        ######################
        return await next_directive(value, ctx, info)

    async def on_introspection(
        self,
        directive_args: Dict[str, Any],
        next_directive: Callable,
        introspected_element: Any,
        ctx: Optional[Any],
        info: "ResolveInfo",
    ) -> Any:
        ######################
        # Add your code here #
        ######################
        return await next_directive(introspected_element, ctx, info)
```

In the next steps, we will implement some specific behavior in this directive.
