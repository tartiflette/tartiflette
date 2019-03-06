---
id: directive
title: Directive
sidebar_label: Directive
---

Tartiflette bases most of its extensibility on Directives. A directive will allow you to execute a behavior at 4 different stages.

* `on_build`: To wrap your directive around the build process of the SDL.
* `on_field_execution`: Allows you to wrap the field execution _(e.g. Access Rights on a specific field, apply a specific rate limit on a field.)_.
* `on_argument_execution`: Allows you to wrap the argument execution _(e.g. Check the format of an input.)_.
* `on_introspection`: During an introspection query, allows you to wrap the schema fields to add metadata _(e.g. add deprecated information)_ to fields or even to remove objects _(e.g. dynamic introspection based on access rights)_.

## How to declare a new directive?

```graphql
directive @myDirective(
  name: String = "Chuck"
) on FIELD_DEFINITION

type Query {
  hello: String @myDirective(name: "Norris")
}
```

```python
from typing import Any, Callable, Dict, Optional

from tartiflette.directive import Directive, CommonDirective


@Directive("myDirective")
class MyDirective(CommonDirective):
    @staticmethod
    def on_build(schema: "GraphQLSchema") -> None:
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
