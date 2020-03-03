---
id: directive
title: Directive
sidebar_label: Directive
---

Tartiflette bases most of its extensibility on directives. A directive will allow you to execute a behavior at different stages:

* `on_argument_execution`: allows you to wrap the argument execution. _(e.g. access rights, validate the input format...)_
* `on_field_execution`: allows you to wrap the field execution. _(e.g. resolve the field remotly, apply a specific rate limit on a field...)_
* `on_introspection`: during an introspection query, allows you to wrap the schema fields to add metadata to fields or even to remove objects _(e.g. dynamic introspection based on access rights)_

New in `0.10.0`:
* `on_post_input_coercion`: allows you to hook the execution flow right after an input value/variable has beed coerced
* `on_pre_output_coercion`: allows you to mutate the result of the resolved value of a field before returning it

New in `1.1.0`:
* `on_schema_execution`: allows you to wrap the execution of a request (`QUERY` or `MUTATION`) in order to manipulate the `initial_value` or add extensions to the global result dict.
* `on_schema_subscription`: allows you to wrap the async generator of a `SUBSCRIPTION` in order to manipulate the `initial_value` or add extensions to the gobal result dict.


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
from typing import Any, Callable, Dict, Optional, Union

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
        self,
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

    async def on_schema_execution(
        self,
        directive_args: Dict[str, Any],
        next_directive: Callable,
        schema: "GraphQLSchema",
        document: "DocumentNode",
        parsing_errors: Optional[List["TartifletteError"]],
        operation_name: Optional[str],
        context: Optional[Dict[str, Any]],
        variables: Optional[Dict[str, Any]],
        initial_value: Optional[Any],
    ):
        ######################
        # Add your code here #
        ######################
        results = await next_directive(
            schema,
            document,
            parsing_errors,
            operation_name,
            context,
            variables,
            initial_value,
        )
        ###############
        # Or/And here #
        ###############
        return results

    async def on_schema_subscription(
        self,
        directive_args: Dict[str, Any],
        next_directive: Callable,
        schema: "GraphQLSchema",
        document: "DocumentNode",
        parsing_errors: Optional[List["TartifletteError"]],
        operation_name: Optional[str],
        context: Optional[Dict[str, Any]],
        variables: Optional[Dict[str, Any]],
        initial_value: Optional[Any],
    ):
        ######################
        # Add your code here #
        ######################
        async for result in next_directive(
            schema,
            document,
            parsing_errors,
            operation_name,
            context,
            variables,
            initial_value,
        ):
            ###############
            # Or/And here #
            ###############
            yield result
            ###############
            # Or/And here #
            ###############
```

## Decorator signature

* `name` _(str)_: name of the directive
* `schema_name` _(str = "default")_: name of the schema to which link the directive
* `arguments_coercer` _(Optional[Callable] = None)_: callable to use to coerce directive arguments

The `arguments_coercer` parameter is here to provide an easy way to override the default callable used internaly by Tartiflette to coerce the arguments of the directive. It has the same behaviour as the `custom_default_arguments_coercer` parameter at engine initialisation but impact only the directive.

## Execution flow

> Warning: This is valid since `1.1.0`.

Directive hook execution flow is like:

![ExecutionOrder](/docs/assets/execution-order-v1-1-0.png)

### Example

```graphql
directive @directiveField on FIELD
directive @directiveScalar on SCALAR
directive @directiveEnum on ENUM
directive @directiveEnumValue on ENUM_VALUE
directive @directiveObject on OBJECT
directive @directiveInputObject on INPUT_OBJECT
directive @directiveArgument on ARGUMENT
directive @directiveSchema on SCHEMA

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

schema @directiveSchema {
    query: Query
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
1. `on_schema_execution` of directive `directiveSchema`.
2. `Query.field1` resolver
3. `on_pre_output_coercion` of directive `directiveObject` of type `aType`
4. `output_coercer` for `ObjectType`

Then the resolution of `aType.aField` will ran (parrallely ran with `aType.anEnumField`):
1. `on_schema_execution` of directive `directiveSchema`.
2. `on_field_execution` of directive `directiveField` on `aType.aField`
3. `aType.aField` resolver
4. `on_pre_output_coercion` of directive `directiveScalar` on `aScalar`
5. `output_coercer` of the scalar `aScalar`

The resolution of `aType.anEnumField` will ran (parrallely ran with `aType.aField`):
1. `on_schema_execution` of directive `directiveSchema`.
2. `on_field_execution` of directive `directiveField` on `aType.anEnumField`
3. `aType.anEnumField` resolver
4. `on_pre_output_coercion` of directive `directiveEnumValue` cause `ONE` has a directive
5. `on_pre_output_coercion` of directive `directiveEnum` of enum `anEnum`
6. `output_coercer` for enum

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
1. `on_schema_execution` of directive `directiveSchema`
2. `input_coercer` for `InputObjectType`
3. `input_coercer` for argument `anInputField` of type `aScalar`
4. `on_post_input_coercion` of directive `directiveScalar` of scalar `aScalar`
5. `on_post_input_coercion` of directive `directiveInputObject` of type `anInputType`
6. `on_argument_execution` of directive `directiveArgument` for argument `anArgument`
7. `Query.field2` resolver
8. `on_pre_output_coercion` of directive `directiveObject` of type `aType`
9.  `output_coercer` for `ObjectType`

Then the resolution of `aType.aField` will ran (parrallely ran with `aType.anEnumField`):
1. `on_schema_execution` of directive `directiveSchema`.
2. `on_field_execution` of directive `directiveField` on `aType.aField`
3. `aType.aField` resolver
4. `on_pre_output_coercion` of directive `directiveScalar` on `aScalar`
5. `output_coercer` of the scalar `aScalar`

The resolution of `aType.anEnumField` will ran (parrallely ran with `aType.aField`):
1. `on_schema_execution` of directive `directiveSchema`.
2. `on_field_execution` of directive `directiveField` on `aType.anEnumField`
3. `aType.anEnumField` resolver (method `atype_anenumfield_resolver` returned "ONE")
4. `on_pre_output_coercion` of directive `directiveEnumValue` cause `ONE` has a directive
5. `on_pre_output_coercion` of directive `directiveEnum` of enum `anEnum`
6. `output_coercer` for enum

#### Query 3

```
query aQuery {
  field3
}
```

The resolution of `Query.field3` will ran:
1. `on_schema_execution` of directive `directiveSchema`.
2. `Query.field3` resolver
3. `on_pre_output_coercion` of directive `directiveEnum` of enum `anEnum`
4. `output_coercer` for `EnumType`
