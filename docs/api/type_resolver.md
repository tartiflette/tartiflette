---
id: type-resolver
title: Type resolver
sidebar_label: Type resolver
---

When resolving a field implementing an abstract type (either an Union or an Interface) the engine need to have a way of determining which object a given result corresponds to. This logic is handled by the type resolver.

There is multiple option to define a type resolver

A type resolver can be defined at several levels, from the most precise to the most generic:
* on the `@Resolver` of a field by fill in the `type_resolver` argument
* by decorating a dedicated callable with the `@TypeResolver` decorator
* by replacing the default type resolver of the engine with a custom one

## `@Resolver`

The `@Resolver` accepts a `type_resolver` optional parameter which expect a callable which must be compliant with [the function signature](#function-signature).

```python
from tartiflette import Resolver


@Resolver(
    "Query.pet",
    type_resolver=lambda: result, context, info, abstract_type: (
        "Cat" if "meowVolume" in result else "Dog"
    )
)
async def resolve_query_pet(parent, args, context, info):
    return {"id": 1, "name": "Cat", "meowVolume": 10}
```

## `@TypeResolver`

A more generic way to define a type resolver is to provide a dedicated type resolver for an abstract type with the `@TypeResolver` decorator.

```python
from tartiflette import TypeResolver


@TypeResolver("Pet")
def resolve_pet_type(result, context, info, abstract_type):
    return "Cat" if "meowVolume" in result else "Dog"
```

> Notes: the `@TypeResolver` can only be applied to an abstract type.

## Overriding the default type resolver

By default, Tartiflette provide a type resolver which will be called when resolving any field which implements an abstract type.

Its default behavior is to get the `_typename` key, then the `_typename` attribute and if both failed, it'll return the `__class__.__name__` of the `result` parameter.

This default type resolver can be override by providing a custom one at the engine initialization with the `custom_default_type_resolver` parameter ([more detail here](/docs/api/engine/#parameter-custom_default_type_resolver))

## Function signature

Every type resolver in Tartiflette accepts four positional arguments:

```python
async def my_type_resolver(
    result: Any,
    ctx: Optional[Any],
    info: "ResolverInfo",
    abstract_type: Union["GraphQLInterfaceType", "GraphQLUnionType"],
) -> Any:
    pass
```

* `result` _(Any)_: resolved field result
* `ctx` _(Optional[Any])_: will be the value of the `context` argument provided when calling the `execute` or `subscribe`'s `Engine` method
* `info` _(ResolverInfo)_: informationinternal Tartiflette object containing information related to the execution and the resolved field. It *CAN BE* used for advanced use-cases ([more detail here](#resolver-info-argument))
* `abstract_type` _(Union[GraphQLInterfaceType, GraphQLUnionType])_: the GraphQLAbstractType instance to resolve

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
