---
id: directive
title: Directive
sidebar_label: Directive
---

Tartiflette bases most of its extensibility on directives. A directive will allow you to execute a behavior at different stages:

* `on_argument_execution`: allows you to wrap the argument execution. _(e.g. access rights, validate the input format...)_
* `on_post_input_coercion`: allows you to hook the execution flow right after an input value/variable has beed coerced (appears in version `0.10.0`)
* `on_field_execution`: allows you to wrap the field execution. _(e.g. resolve the field remotly, apply a specific rate limit on a field...)_
* `on_pre_output_coercion`: allows you to mutate the result of the resolved value of a field before returning it (appears in version `0.10.0`)
* `on_introspection`: during an introspection query, allows you to wrap the schema fields to add metadata to fields or even to remove objects _(e.g. dynamic introspection based on access rights)_

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

from tartiflette import Directive


@Directive("myDirective")
class MyDirective:
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
        value: Any,
        ctx: Optional[Any],
    ) -> Any:
        ######################
        # Add your code here #
        ######################
        return await next_directive(value, ctx)

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

## Execution flow

> Warning: This is valid since `0.10.0`.

Directive hook execution flow is like:

![ExecutionOrder](/docs/assets/execution-order.png)

### Example

```graphql
directive @directiveField on FIELD
directive @directiveScalar on SCALAR
directive @directiveEnum on ENUM
directive @directiveEnumValue on ENUM_VALUE
directive @directiveObject on OBJECT
directive @directiveInputObject on INPUT_OBJECT
directive @directiveArgument on ARGUMENT

scalar aScalar @directiveScalar

enum anEnum @directiveEnum {
  ONE @directiveEnumValue
  TWO
}

input anInputObject @directiveInputObject {
  anInputField: aScalar
}

type aType @directiveObject {
  aField: aScalar @directiveField
  anEnumField: anEnum @directiveField
}

type Query {
  field1: aType
  field2(anArgument: anInputObject @directiveArgument): aType
  field3: anEnum
}
```

with Resolvers as:

```python
@Resolver("Query.field1")
async def resolve_query_field1(parent, args, ctx, info):
    return {"aField": "aValue", "anEnumField":"ONE"}

@Resolver("Query.field2")
async def resolve_query_field2(parent, args, ctx, info):
    return {"aField": "aValue", "anEnumField":"TWO"}

@Resolver("Query.field3")
async def resolve_query_field3(parent, args, ctx, info):
    return "TWO"
```

#### Query 1

```
query aQuery {
  field1 {
    aField
    anEnumField
  }
}
```

The resolution of `Query.field1` will ran:
1. `Query.field1` resolver
2. `on_pre_output_coercion` of directive `directiveObject` of type `aType`
3. `output_coercer` for `ObjectType`

Then the resolution of `aType.aField` will ran (parrallely ran with `aType.anEnumField`):
1. `on_field_execution` of directive `directiveField` on `aType.aField`
2. `aType.aField` resolver
3. `on_pre_output_coercion` of directive `directiveScalar` on `aScalar`
4. `output_coercer` of the scalar `aScalar`

The resolution of `aType.anEnumField` will ran (parrallely ran with `aType.aField`):
1. `on_field_execution` of directive `directiveField` on `aType.anEnumField`
2. `aType.anEnumField` resolver
3. `on_pre_output_coercion` of directive `directiveEnumValue` cause `ONE` has a directive
4. `on_pre_output_coercion` of directive `directiveEnum` of enum `anEnum`
5. `output_coercer` for enum

#### Query 2

```
query aQuery {
  field2(anArgument: {anInputField: 3}) {
    aField
    anEnumField
  }
}
```

The resolution of `Query.field2` will ran:
1. `input_coercer` for `InputObjectType`
2. `input_coercer` for argument `anInputField` of type `aScalar`
3. `on_post_input_coercion` of directive `directiveScalar` of scalar `aScalar`
4. `on_post_input_coercion` of directive `directiveInputObject` of type `anInputType`
5. `on_argument_execution` of directive `directiveArgument` for argument `anArgument`
6. `Query.field2` resolver
7. `on_pre_output_coercion` of directive `directiveObject` of type `aType`
8. `output_coercer` for `ObjectType`

Then the resolution of `aType.aField` will ran (parrallely ran with `aType.anEnumField`):
1. `on_field_execution` of directive `directiveField` on `aType.aField`
2. `aType.aField` resolver
3. `on_pre_output_coercion` of directive `directiveScalar` on `aScalar`
4. `output_coercer` of the scalar `aScalar`

The resolution of `aType.anEnumField` will ran (parrallely ran with `aType.aField`):
1. `on_field_execution` of directive `directiveField` on `aType.anEnumField`
2. `aType.anEnumField` resolver (method `atype_anenumfield_resolver` returned "ONE")
3. `on_pre_output_coercion` of directive `directiveEnumValue` cause `ONE` has a directive
4. `on_pre_output_coercion` of directive `directiveEnum` of enum `anEnum`
5. `output_coercer` for enum

#### Query 3

```
query aQuery {
  field3
}
```

The resolution of `Query.field3` will ran:
1. `Query.field3` resolver
2. `on_pre_output_coercion` of directive `directiveEnum` of enum `anEnum`
3. `output_coercer` for `EnumType`
