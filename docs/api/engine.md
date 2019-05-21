---
id: engine
title: Engine
sidebar_label: Engine
---

The way to generate an engine is pretty simple.

The engine accepts at least one parameter, called "sdl", the others are [documented in the advanced usage](#advanced-constructor) part of the documents.

```python
from tartiflette import Engine
Engine(
    sdl,
    schema_name,              # Optional
    error_coercer,            # Optional
    custom_default_resolver,  # Optional
    modules,                  # Optional
)
```

## Using the SDL _(Schema Definition Language)_ parameter with different types

### When the `sdl` parameter contains the raw schema

```python
import tartiflette

engine = tartiflette.Engine(
    """
    type Query {
        hello: String
    }
    """
)
```

### When the `sdl` parameter targets a file

The file path specified has to contain the full schema definition language.

```python
import tartiflette

engine = tartiflette.Engine(
    "/User/chuck/workspace/mytartiflette/schema.graphql"
)
```

### When the `sdl` parameter targets a file list

Every file will be concatenated, in the order of the provided list.

```python
import tartiflette

engine = tartiflette.Engine(
    [
        "/User/chuck/workspace/mytartiflette/schema_query.graphql",
        "/User/chuck/workspace/mytartiflette/schema_mutation.graphql"
    ]
)
```

### When the `sdl` parameter targets a folder

Every file which ends by `.graphql` _(or `.sdl`)_ will be concatenated in lexicographical order.

```python
import tartiflette

engine = tartiflette.Engine(
    "/User/chuck/workspace/mytartiflette"
)
```

## Advanced constructor

The engine provides an advanced interface for initialization. It accepts optional and named parameters.

```python
import tartiflette

engine = tartiflette.Engine(
    sdl,
    schema_name="default",
)
```

1. **sdl:** Schema Definition Language, detailed above.
2. **schema_name:** Schema used from the **[Schema Registry](/docs/api/schema-registry/)**. _(default: "default")_
3. **[error_coercer](#parameter-error-coercer):** Coercer used when an error is raised.
4. **[custom_default_resolver](#parameter-custom-default-resolver):** Use another default resolver. (Useful if you want to override the behavior for resolving a property, e.g. from snake_case to camelCase and vice versa).
5. **[modules](#parameter-modules):** list of modules containing your decorated code such as `@Resolver`, `@Subscription`, `@Mutation`, `@Scalar` and `@Directive`.

### Parameter: `error_coercer`

The main objective of the `error_coercer` is to provide you a way to extend the behavior when an exception is raised into tartiflette.

For instance:
* Add a log entry when a third-party exceptions is raised _(e.g pymsql, redis)_.
* Hide technical message's exception for production environment _(don't expose your internal stack from outside)_

`error_coercer` SHOULDN'T be used for custom functional exception, for this common use-case, please take a look of the [`TartifletteError` and its documentation's page](/docs/api/error-handling/).

```python
import logging


class CustomException(Exception):
    def __init__(self, type_name, message):
        self.type = type_name
        self.message = message


def my_error_coercer(exception, error) -> dict:
    if isinstance(exception, CustomException):
        logging.error("Unable to reach the Storage host.")
        error["extensions"]["type"] = exception.type

    return error


e = Engine(
    "my_sdl.graphql",
    error_coercer=my_error_coercer
)
```

### Parameter: `custom_default_resolver`

Use another default resolver. It can be useful to override the behavior for resolving a property, from `snake_case` to `camelCase` and vice versa.

```python
async def my_default_resolver(parent_result, arguments, context, info):
    do_ing_some_thin_gs = 42
    return a_value

e = Engine(
    "my_sdl.graphql",
    custom_default_resolver=my_default_resolver
)
```

### Parameter: `modules`

list of modules containing your decorated code such as:

* `@Resolver`
* `@Subscription`
* `@Scalar`
* `@Directive`

Simplify your code by writing this
```python
engine = Engine(
    os.path.dirname(os.path.abspath(__file__)) + "/sdl",
    modules=[
        "recipes_manager.query_resolvers",
        "recipes_manager.mutation_resolvers",
        "recipes_manager.subscription_resolvers",
        "recipes_manager.directives.rate_limiting",
        "recipes_manager.directives.non_introspectable",
    ]
)
```

instead of
```python
import recipes_manager.query_resolvers
import recipes_manager.mutation_resolvers
import recipes_manager.subscription_resolvers
import recipes_manager.directives.rate_limiting
import recipes_manager.directives.non_introspectable

engine = Engine(
    os.path.dirname(os.path.abspath(__file__)) + "/sdl"
)
```
