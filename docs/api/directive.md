---
id: directive
title: Directive
sidebar_label: Directive
---

Tartiflette bases most of its extensibility on Directives. A directive will allow you to execute a behavior at 6 different stages.

* `on_build`: To wrap your directive around the build process of the SDL
* `on_field_execution`: Allows you to wrap the field execution. _(e.g. Access Rights on a specific field, apply a specific rate limit on a field.)_
* `on_argument_execution`: Allows you to wrap the argument execution. _(e.g Check the format of an input.)_.
* `on_pre_output_coercion`: Allows you to hook the execution flow right before a field result value is being coerced (Appears in version `0.10.0`)
* `on_post_input_coercion`: Allows you to hook the execution flow right after an argument value has beed coerced (Appears in version `0.10.0`)
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

from tartiflette import Directive


@Directive("myDirective")
class MyDirective:
    async def on_field_execution(
        self,
        directive_args: Dict[str, Any],
        next_resolver: Callable,
        parent: Optional[Any],
        args: Dict[str, Any],
        ctx: Optional[Dict[str, Any]],
        info: "Info",
    ) -> Any:
        ######################
        # Add your code here #
        ######################
        return await next_resolver(parent, args, ctx, info)


    async def on_argument_execution(
        self,
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


    async def on_post_input_coercion(
        self,
        directive_args: Dict[str, Any],
        next_directive: Callable,
        value: Any,
        argument_definition: "GraphQLArgument",
        ctx: Optional[Dict[str, Any]],
        info: "Info",
    ) -> Any:
        ######################
        # Add your code here #
        ######################
        return await next_directive(value, argument_definition, ctx, info)


    async def on_pre_output_coercion(
        self,
        directive_args: Dict[str, Any],
        next_directive: Callable,
        value: Any,
        field_definition: "GraphQLField",
        ctx: Optional[Dict[str, Any]],
        info: "Info",
    ) -> Any:
        ######################
        # Add your code here #
        ######################
        return await next_directive(value, field_definition, ctx, info)


    async def on_introspection(
        self,
        directive_args: Dict[str, Any],
        next_directive: Callable,
        introspected_element: Any,
        ctx: Optional[Dict[str, Any]],
        info: "Info",
    ) -> Any:
        ######################
        # Add your code here #
        ######################
        return await next_directive(introspected_element, ctx, info)
```

## Execution Flow

>Warning: This is valid since 0.10.0

Directive Hook Execution flow is like:

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
async def query_field1_resolver(pr, args, ctx, info):
    return {"aField": "aValue", "anEnumField":"ONE"}

@Resolver("Query.field2")
async def query_field2_resolver(pr, args, ctx, info):
    return {"aField": "aValue", "anEnumField":"TWO"}

@Resolver("Query.field3")
async def query_field3_resolver(pr, args, ctx, info):
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

  1. `Query.field1` Resolver
  2. `on_pre_output_coercion` of directive `directiveObject` of type `aType`
  3. `output_coercer` for ObjectType

Then the resolution of `aType.aField` will ran: (Parrallely ran with `aType.anEnumField`)

  1. `on_field_execution` of directive `directiveField` on `aType.aField`
  2. `aType.aField` Resolver
  3. `on_pre_output_coercion` of directive `directiveScalar` on `aScalar`
  4. `output_coercer` of the scalar `aScalar`.

The resolution of `aType.anEnumField` will ran: (Parrallely ran with `aType.aField`)

  1. `on_field_execution` of directive `directiveField` on `aType.anEnumField`
  2. `aType.anEnumField` Resolver
  3. `on_pre_output_coercion` of directive `directiveEnumValue` cause `ONE` has a directive
  4. `on_pre_output_coercion` of directive `directiveEnum` of enum `anEnum`
  5. `output_coercer` for enum.

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

  1. `input_coercer` for InputObjectType
  2. `input_coercer` for argument `anInputField` of type `aScalar`
  3. `on_post_input_coercion` of directive `directiveScalar` of scalar `aScalar`
  4. `on_post_input_coercion` of directive `directiveInputObject` of type `anInputType`
  5. `on_argument_execution` of directive `directiveArgument` for argument `anArgument`
  6. `Query.field2` Resolver
  7. `on_pre_output_coercion` of directive `directiveObject` of type `aType`
  8. `output_coercer` for ObjectType

Then the resolution of `aType.aField` will ran: (Parrallely ran with `aType.anEnumField`)

  1. `on_field_execution` of directive `directiveField` on `aType.aField`
  2. `aType.aField` Resolver
  3. `on_pre_output_coercion` of directive `directiveScalar` on `aScalar`
  4. `output_coercer` of the scalar `aScalar`.

The resolution of `aType.anEnumField` will ran: (Parrallely ran with `aType.aField`)

  1. `on_field_execution` of directive `directiveField` on `aType.anEnumField`
  2. `aType.anEnumField` Resolver (method `atype_anenumfield_resolver` returned "ONE")
  3. `on_pre_output_coercion` of directive `directiveEnumValue` cause `ONE` has a directive
  4. `on_pre_output_coercion` of directive `directiveEnum` of enum `anEnum`
  5. `output_coercer` for enum.

#### Query 3

```
query aQuery {
    field3
}
```

The resolution of `Query.field3` will ran:

  1. `Query.field3` Resolver
  2. `on_pre_output_coercion` of directive `directiveEnum` of enum `anEnum`
  3. `output_coercer` for EnumType
