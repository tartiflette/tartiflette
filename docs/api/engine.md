---
id: engine
title: Engine
sidebar_label: Engine
---

The way to generate an engine is pretty simple, most of the time, you will use the `create_engine` method, expose in `tartiflette` package. This method has all the necessary to build your engine.

## `create_engine` prepares and cooks your engine

`create_engine` is the easiest and quickiest method to instanciate and build an Engine(). Behind the scene, this factory will implement the regular [cooking process](#cook-your-tartiflette).

### Using the SDL _(Schema Definition Language)_ parameter with different types

#### When the `sdl` parameter contains the raw schema

```python
from tartiflette import create_engine 

engine = await create_engine(
    """
    type Query {
        hello: String
    }
    """
)
```

#### When the `sdl` parameter targets a file

The file path specified has to contain the full schema definition language.

```python
from tartiflette import create_engine 

engine = await create_engine(
    "/User/chuck/workspace/mytartiflette/schema.graphql"
)
```

#### When the `sdl` parameter targets a file list

Every file will be concatenated, in the order of the provided list.

```python
from tartiflette import create_engine 

engine = await create_engine(
    [
        "/User/chuck/workspace/mytartiflette/schema_query.graphql",
        "/User/chuck/workspace/mytartiflette/schema_mutation.graphql"
    ]
)
```

#### When the `sdl` parameter targets a folder

Every file which ends by `.graphql` _(or `.sdl`)_ will be concatenated in lexicographical order.

```python
from tartiflette import create_engine 

engine = await create_engine(
    "/User/chuck/workspace/mytartiflette"
)
```

### Advanced constructor

The `create_engine` method provides an advanced interface for initialization. It accepts optional and named parameters.

```python
from tartiflette import create_engine 

engine = await create_engine(
    sdl,
    schema_name="default",
)
```

1. **sdl:** Schema Definition Language, detailed above.
2. **schema_name:** Schema used from the **[Schema Registry](/docs/api/schema-registry/)**. _(default: "default")_
3. **[error_coercer](#parameter-error-coercer):** Coercer used when an error is raised.
4. **[custom_default_resolver](#parameter-custom-default-resolver):** Use another default resolver. (Useful if you want to override the behavior for resolving a property, e.g. from snake_case to camelCase and vice versa).
5. **[modules](#parameter-modules):** list of modules containing your decorated code such as `@Resolver`, `@Subscription`, `@Scalar` and `@Directive`.

#### Parameter: `error_coercer`

The main objective of the `error_coercer` is to provide you a way to extend the behavior when an exception is raised into tartiflette.

For instance:
* Add a log entry when a third-party exceptions is raised _(e.g pymsql, redis)_.
* Hide technical message's exception for production environment _(don't expose your internal stack from outside)_

`error_coercer` SHOULDN'T be used for custom functional exception, for this common use-case, please take a look of the [`TartifletteError` and its documentation's page](/docs/api/error-handling/).

```python
import logging
from tartiflette import create_engine 


class CustomException(Exception):
    def __init__(self, type_name, message):
        self.type = type_name
        self.message = message


def my_error_coercer(exception, error) -> dict:
    if isinstance(exception, CustomException):
        logging.error("Unable to reach the Storage host.")
        error["extensions"]["type"] = exception.type

    return error


e = await create_engine(
    "my_sdl.graphql",
    error_coercer=my_error_coercer
)
```

#### Parameter: `custom_default_resolver`

Use another default resolver. It can be useful to override the behavior for resolving a property, from `snake_case` to `camelCase` and vice versa.

```python
from tartiflette import create_engine 

async def my_default_resolver(parent_result, arguments, context, info):
    do_ing_some_thin_gs = 42
    return a_value

e = await create_engine(
    "my_sdl.graphql",
    custom_default_resolver=my_default_resolver
)
```

#### Parameter: `modules`

Prior creating the `Engine()`, all your code must be decoratored by these following ones to be taken into account.

* `@Resolver`
* `@Subscription`
* `@Scalar`
* `@Directive`

Doing it by yourself could be verbose and generate a lot of imports.

Both for your internal code and the plugins management, tartiflette provides a parameters called `modules` which give you the ability to specify all the internal and external code you want to import. In addition to the module, you will be able to specify a configuration, which will be mostly used by the [tartiflette plugin approach](/docs/plugin/introduction).

```python
from tartiflette import create_engine

engine = await create_engine(
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

engine = await create_engine(
    os.path.dirname(os.path.abspath(__file__)) + "/sdl"
)
```

##### Giving configuration to a module

```python
from tartiflette import create_engine

engine = create_engine(
    os.path.dirname(os.path.abspath(__file__)) + "/sdl",
    modules=[
        "recipes_manager.query_resolvers",
        "recipes_manager.mutation_resolvers",
        { "name": "a.module.that.needs.config", "config": {"key": "value"} },
        { "name": "another.module.that.needs.config", "config": {"key": "value"} }
    ]
)
```

## Advanced instanciation

For those who want to integrate tartiflette in advanced use-cases. You could be interested by owning the process of building an `Engine()`.

### Why owning the cooking (building) process of tartiflette?

The cooking process of tartiflette is equals to a `build` process on another librairies, it will prepare your engine to be executed. Thus, useless to say that an engine instance can't be executed without beeing cooked. The parrallele with a tartiflette meal is so close, you can't eat a tartiflette without cooking it. That's it. 

Customise the cooking process is interesting to integrate tartiflette into another librairies, like `aiohttp`, `starlette, `django` and so one.

_For your information_: `tartiflette-aiohttp` has its own flow to manage the cooking process of the Engine. 

### `cook()` your tartiflette

As specified above, the Engine() needs to be cook() before being executed. here are the sequence to execute a query on an `Engine()` instance.

```python
from tartiflette import Engine

# 1. Create an instance of the Engine
engine = Engine()

# 2. Cook (build) the engine to prepare it to be executed
await engine.cook(
    """
    type Query {
        hello: String
    }
    """
)

# 3. Execute a GraphQL Query
engine.execute(
    query="query { hello )"
)
```

#### `cook()` interface

The `cook()` method is asynchronous, this *strong choice* will allow us to execute asynchronous tasks during the building process, like:

* Fetching SDL from another API.
* Fetch third-parties services _(Database structure, Cloud provider objects ...)_
* Fetch Schema from a Schema Manager.

```python
async def cook(
        self,
        sdl: Union[str, List[str]],
        error_coercer: Callable[[Exception], dict] = None,
        custom_default_resolver: Optional[Callable] = None,
        modules: Optional[Union[str, List[str]]] = None,
        schema_name: str = "default",
    ):
    pass
```

1. **sdl:** Schema Definition Language, detailed above.
2. **[error_coercer](#parameter-error-coercer):** Coercer used when an error is raised.
3. **[custom_default_resolver](#parameter-custom-default-resolver):** Use another default resolver. (Useful if you want to override the behavior for resolving a property, e.g. from snake_case to camelCase and vice versa).
4. **[modules](#parameter-modules):** list of modules containing your decorated code such as `@Resolver`, `@Subscription`, `@Scalar` and `@Directive`.
5. **schema_name:** Schema used from the **[Schema Registry](/docs/api/schema-registry/)**. _(default: "default")_
