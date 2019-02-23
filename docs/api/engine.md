---
id: engine
title: Engine
sidebar_label: Engine
---

The way to generate the engine is pretty simple.

The engine accepts at least one parameter, called "sdl", the other [are documented in the advanced part](#advanced-constructor).

```python
from tartiflette import Engine
Engine(
    sdl,
    schema_name,              # Optional
    error_coercer,            # Optional
    custom_default_resolver,  # Optional
    exclude_builtins_scalars  # Optional
)
```

## Use the SDL parameter as different types 

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

The filepath specified has to contain the full schema definition language.

```python
import tartiflette

engine = tartiflette.Engine(
    "/User/chuck/workspace/mytartiflette/schema.sdl"
)
```

### When the `sdl` parameter targets a file list

Every file will be concatenated, in the order of the provided list.

```python
import tartiflette

engine = tartiflette.Engine(
    [
        "/User/chuck/workspace/mytartiflette/schema_query.sdl",
        "/User/chuck/workspace/mytartiflette/schema_mutation.sdl"
    ]
)
```

### When the `sdl` parameter targets a folder

Every file which ends by `.sdl` will be concatenated, in lexicographical order.

```python
import tartiflette

engine = tartiflette.Engine(
    "/User/chuck/workspace/mytartiflette"
)
```

### When the `sdl` parameter is a Schema object

```python
import tartiflette

sdl = """
type Query {
    hello: String
}
"""

schema = tartiflette.Schema(sdl)
engine = tartiflette.Engine(schema)
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
4. **[custom_default_resolver](#parameter-custom-default-resolver):** Use another default resolver. (useful to override the behavior for resolving a property, snakecase -> camelcase and vice versa).
5. **[exclude_builtins_scalars](#parameter-exclude-builtins-scalars):** List of scalars you want to exclude from the default list.

### Parameter: `error_coercer`

Override the default coercer when an exception is raised.

```python
def my_error_coercer(exception) -> dict:
    do_ing_some_thin_gs = 42
    return a_value

e = Engine(
    "my_sdl.sdl",
    error_coercer=my_error_coercer
)
```

### Parameter: `custom_default_resolver`

Use another default resolver. Could be useful to override the behavior for resolving a property, snakecase -> camelcase and vice versa.

```python
async def my_default_resolver(parent_result, arguments, context, info):
    do_ing_some_thin_gs = 42
    return a_value

e = Engine(
    "my_sdl.sdl",
    custom_default_resolver=my_default_resolver
)
```

### Parameter: `exclude_builtins_scalars`

List of scalars you want to exclude [from the default list](https://github.com/dailymotion/tartiflette/blob/master/tartiflette/scalar/__init__.py). Useful if you define by yourself the default scalar in the SDL.

```python
e = Engine(
    "my_sdl.sdl",
    exclude_builtins_scalars=["Date", "DateTime"]
)
```
