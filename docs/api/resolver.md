---
id: resolver
title: Resolver
sidebar_label: Resolver
---

The most common way to assign a specific resolver to a field is to decorate your resolver callable with the `@Resolver` decorator. Your resolver [MUST BE compliant with the resolver signature](#resolver-signature) and be `async`.

```python
from tartiflette import Resolver


@Resolver("Query.hello")
async def my_hello_resolver(parent, args, context, info):
    return "Chuck"
```

## Decorator signature

* `name` _(str)_: fully qualified field name to resolve
* `schema_name` _(str = "default")_: name of the schema to which link the resolver
* `type_resolver` _(Optional[Callable] = None)_: the callable to use to resolve the type of an abstract type
* `arguments_coercer` _(Optional[Callable] = None)_: callable to use to coerce field arguments
* `concurrently` _(Optional[bool] = None)_: determine whether or not the output list of the decorated field should be coerced concurrently

The `arguments_coercer` parameter is here to provide an easy way to override the default callable used internaly by Tartiflette to coerce the arguments of the field. It has the same behaviour as the `custom_default_arguments_coercer` parameter at engine initialisation but impact only the field.

## Resolver signature

Every resolver in Tartiflette accepts four positional arguments:

_(This signature is highly inspired by the GraphQL.js implementation)_

```python
async def my_hello_resolver(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Optional[Any],
    info: "ResolveInfo",
) -> Any:
    pass
```

* `parent` _(Optional[Any])_: resolved value returned by the parent resolver field, if the parent is a root type (Query/Mutation/Subscription) the value passed will be the `initial_value` of the execution
* `args` _(Dict[str, Any])_: a dictionary containing the arguments passed for the field. _(in the query)_. e.g. if the field was called with `hello(name: "Chuck")`, the `args` dictionary will be equals to `{"name": "Chuck"}`
* `ctx` _(Optional[Any])_: will be the value of the `context` argument provided when calling the `execute` or `subscribe`'s `Engine` method
* `info` _("ResolveInfo")_: internal Tartiflette object containing information related to the execution and the resolved field. It *CAN BE* used for advanced use-cases ([more detail here](#resolver-info-argument))

### Resolver `info` argument

The `info` argument contains information related to the execution and the resolved field which can be useful for middlewares and advanced use-cases.

Here are the available properties:
* `field_name` _(str)_: name of the resolved field
* `field_nodes` _(List["FieldNodes"])_: AST nodes related to the resolved field
* `return_type` _("GraphQLOutputType")_: GraphQLOutputType instance of the resolved field
* `parent_type` _("GraphQLObjectType")_: GraphQLObjectType of the field's parent
* `path` _("Path")_: the path traveled until this field
* `schema` _("GraphQLSchema")_: the GraphQLSchema instance linked to resolved field
* `fragments` _(Dict[str, "FragmentDefinitionNode"])_: a dictionary of fragment definition AST nodes contained in the request
* `root_value` _(Optional[Any])_: the initial value corresponding to provided value at `execute` or `subscribe` method call
* `operation` _("OperationDefinitionNode")_: the AST operation definition node to execute
* `variable_values` _(Optional[Dict[str, Any]])_: the variables provided in the GraphQL request
* `is_introspection` _(bool)_: determines whether or not the resolved field is in a context of an introspection query
