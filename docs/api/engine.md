---
id: engine
title: Engine
sidebar_label: Engine
---

The way to generate a Tartiflette engine is pretty simple, most of the time, you will use the `create_engine` function, exposed in the `tartiflette` package. This function performs all the necessary tasks needed to build your engine.

## `create_engine` prepares and cooks your engine

`create_engine` is the easiest and quickiest way to instanciate and build a Tartiflette engine. Behind the scene, this factory will implements the regular [cooking process](#cook-your-tartiflette).

### Using the SDL _(Schema Definition Language)_ parameter with different types

#### When the `sdl` parameter contains the SDL as a raw string

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

#### When the `sdl` parameter contains a path to a file

The file path specified has to contain the full Schema Definition Language.

```python
from tartiflette import create_engine


engine = await create_engine(
    "/User/chuck/workspace/mytartiflette/schema.graphql"
)
```

#### When the `sdl` parameter contains a list of file path

Every file will be concatenated, in the order of the provided list.

```python
from tartiflette import create_engine


engine = await create_engine(
    [
        "/User/chuck/workspace/mytartiflette/schema_query.graphql",
        "/User/chuck/workspace/mytartiflette/schema_mutation.graphql",
    ]
)
```

#### When the `sdl` parameter contains a path to a directory

Every file which ends with `.graphql` _(or `.sdl`)_ will be concatenated in lexicographical order.

```python
from tartiflette import create_engine


engine = await create_engine("/User/chuck/workspace/mytartiflette")
```

### Advanced constructor

The `create_engine` function provides an advanced interface for initialization. It accepts multiple parameters:

* `sdl` _(Union[str, List[str]])_: raw SDL, path or list of file path/directory from which retrieve the SDL (more detail above)
* `schema_name` _(str = "default")_: name of the schema represented by the provided SDL ([more detail here](./schema-registry.md))
* `error_coercer` _(Callable[[Exception, Dict[str, Any]], Dict[str, Any]])_: callable used to coerced an exception into a GraphQL valid output format ([more detail here](#parameter-error_coercer))
* `custom_default_resolver` _(Optional[Callable])_: callable used to resolve fields which doesn't implements a dedicated resolver (useful if you want to override the behavior for resolving a field, e.g. from `snake_case` to `camelCase` and vice versa) ([more detail here](#parameter-custom_default_resolver))
* `custom_default_type_resolver` _(Optional[Callable])_: callable that will replace the tartiflette `default_type_resolver` (will be called on abstract types to deduct the type of a result) ([more detail here](#parameter-custom_default_type_resolver))
* `modules` _(Optional[Union[str, List[str], List[Dict[str, Any]]]])_: list of string containing the name of the modules you want the engine to import, usually this modules contains your `@Resolvers`, `@Directives`, `@Scalar` or `@Subscription` code ([more detail here](#parameter-modules))
* `query_cache_decorator` _(Optional[Callable])_: callable that will replace the tartiflette default lru_cache decorator to cache query parsing
* `json_loader` _(Optional[Callable[[str], Dict[str, Any]]])_: a Callable that will replace python built-in `json.loads` when Tartiflette will transform the json-ast of the query into a dict useable by the execution algorithm. ([more detail here](#parameter-json_loader))
* `custom_default_arguments_coercer` _(Optional[Callable])_: callable that will replace the tartiflette `default_arguments_coercer`
* `coerce_list_concurrently` _(Optional[bool])_: determine whether or not output list are coerced concurrently by default

#### Parameter: `error_coercer`

The main objective of the `error_coercer` is to provide you a way to extend the behavior when an exception is raised into Tartiflette.

For instance:
* add a log entry when a third-party exceptions is raised _(e.g `pymsql`, `redis`)_.
* hide technical message's exception for production environment _(don't expose your internal stack to the outside world)_

`error_coercer` **SHOULDN'T** be used for custom functional exception, for this common use-case, please take a look of the [`TartifletteError` and its documentation's page](./error-handling.md).

```python
import logging

from typing import Any, Dict

from tartiflette import create_engine

logger = logging.getLogger(__name__)


class CustomException(Exception):
    def __init__(self, type_name: str, message: str) -> None:
        self.type = type_name
        self.message = message


async def my_error_coercer(
    exception: Exception, error: Dict[str, Any]
) -> Dict[str, Any]:
    if isinstance(exception, CustomException):
        logger.error("Unable to reach the Storage host.")
        error["extensions"]["type"] = exception.type
    return error


engine = await create_engine(
    "my_sdl.graphql",
    error_coercer=my_error_coercer,
)
```

#### Parameter: `custom_default_resolver`

The `custom_default_resolver` parameter is here to provide an easy way to override the default resolver used internaly by Tartiflette during the execution. The default resolver is the resolver which is used for each field which doesn't implements a dedicated resolver (meaning a field which doesn't implement a callable decorated with `@Resolver`). It can be useful to override the behavior for resolving a field, for instance from `snake_case` to `camelCase` and vice versa.

```python
from tartiflette import create_engine


async def my_default_resolver(parent, arguments, context, info):
    do_ing_some_thin_gs = 42
    return a_value


engine = await create_engine(
    "my_sdl.graphql",
    custom_default_resolver=my_default_resolver,
)
```

#### Parameter: `custom_default_type_resolver`

The `custom_default_type_resolver` parameter is here to provide an easy way to override the default type resolver used internaly by Tartiflette during the execution. The default type resolver is the resolver which is used for each abstract field which doesn't implements a dedicated type resolver. It can be useful to override the behavior for resolving the `__typename` of a field.

```python
from tartiflette import create_engine


async def my_default_type_resolver(result, ctx, info, abstract_type):
    return parent["__typename"]


engine = await create_engine(
    "my_sdl.graphql",
    custom_default_type_resolver=my_default_type_resolver,
)
```

#### Parameter: `modules`

Prior creating the Tartiflette engine, all your code must be decoratored by these following ones to be taken into account:
* `@Resolver`
* `@TypeResolver`
* `@Subscription`
* `@Scalar`
* `@Directive`

Doing it by yourself could be verbose and generate a lot of imports.

Both for your internal code and the plugins management, Tartiflette provides a `modules` parameter which give you the ability to specify all the internal and external modules you want to import. In addition to the module, you will be able to specify a configuration, which will be mostly used by the [Tartiflette plugin approach](../plugins/introduction.md).

This allow you to have a cleaner code by doing this:
```python
from tartiflette import create_engine


engine = await create_engine(
    os.path.dirname(os.path.abspath(__file__)) + "/sdl",
    modules=[
        "recipes_manager.query_resolvers",
        "recipes_manager.mutation_resolvers",
        "recipes_manager.subscription_resolvers",
        "recipes_manager.directives.auth",
        "recipes_manager.directives.rate_limiting",
    ],
)
```

instead of:
```python
import recipes_manager.query_resolvers
import recipes_manager.mutation_resolvers
import recipes_manager.subscription_resolvers
import recipes_manager.directives.auth
import recipes_manager.directives.rate_limiting


engine = await create_engine(
    os.path.dirname(os.path.abspath(__file__)) + "/sdl"
)
```

##### Giving configuration to a module

As explain above, the `modules` parameter can be used to provide a list of modules to import but sometimes you will need to provide some configuration to some modules. In order to do that, instead of providing a simple string which target to the module, you will have to fill in a dictionnary with a `name` parameter which target to the module and a `config` key which will contains the configuration needed by the module:
```python
from tartiflette import create_engine


engine = await create_engine(
    os.path.dirname(os.path.abspath(__file__)) + "/sdl",
    modules=[
        "recipes_manager.query_resolvers",
        "recipes_manager.mutation_resolvers",
        {"name": "a.module.that.needs.config", "config": {"key": "value"}},
        {"name": "b.module.that.needs.config", "config": {"key": "value"}},
    ],
)
```

#### Parameter: `query_cache_decorator`

The `query_cache_decorator` parameter is here to provide an easy way to override the default cache decorated used internaly by Tartiflette over the parsing of queries.

The default cache decorator use the `functools.lru_cache` function with a `maxsize` to `512`.

If necessary, you can change this behavior by providing your own decorator to cache query parsing or disable the cache by providing the `None` value to this parameter.

Here is an example of a custom decorator using `lru_cache` with a `maxsize` of `1024` instead of the default `512`:
```python
from functools import lru_cache
from typing import Callable

from tartiflette import create_engine


def my_cache_decorator(func: Callable) -> Callable:
    return lru_cache(maxsize=1024)(func)


engine = await create_engine(
    "my_sdl.graphql",
    query_cache_decorator=my_cache_decorator,
)
```

#### Parameter: `json_loader`

This parameter enables you to use another json lib for ast-json loading (happens around [here](https://github.com/tartiflette/tartiflette/blob/master/tartiflette/language/parsers/libgraphqlparser/parser.py#L155)).

Example usage could be to change the json lib:
```python
import rapidjson

engine = await create_engine(*
    os.path.dirname(os.path.abspath(__file__)) + "/sdl",
    modules=[
        "recipes_manager.query_resolvers",
        "recipes_manager.mutation_resolvers",
        {"name": "a.module.that.needs.config", "config": {"key": "value"}},
        {"name": "b.module.that.needs.config", "config": {"key": "value"}},
    ],
    json_loader=rapidjson.loads
)
```

or to give more arguments to the built-in python loader.

```python
from functools import partial
import json

engine = await create_engine(
    os.path.dirname(os.path.abspath(__file__)) + "/sdl",
    modules=[
        "recipes_manager.query_resolvers",
        "recipes_manager.mutation_resolvers",
        {"name": "a.module.that.needs.config", "config": {"key": "value"}},
        {"name": "b.module.that.needs.config", "config": {"key": "value"}},
    ],
    json_loader=partial(json.loads, parse_float=..., object_hook=...)
)
```

#### Parameter: `custom_default_arguments_coercer`

The `custom_default_arguments_coercer` parameter is here to provide an easy way to override the default callable used internaly by Tartiflette to coerce arguments. The default arguments coercer use the `asyncio.gather` function to coerce asynchronously the arguments. It can be useful to override this behavior to change this behavior. For instance, you could use the `sync_arguments_coercer` in order to coerce your arguments synchronously and avoid the creation of too many asyncio tasks.

```python
from typing import Any, List

from tartiflette import create_engine


async def my_default_arguments_coercer(*coroutines) -> List[Exception, Any]:
    results = []
    for coroutine in coroutines:
        try:
            result = await coroutine
        except Exception as e:  # pylint: disable=broad-except
            result = e
        results.append(result)
    return results


engine = await create_engine(
    "my_sdl.graphql",
    custom_default_arguments_coercer=my_default_arguments_coercer,
)
```

## Advanced instanciation

For those who want to integrate Tartiflette in advanced use-cases. You could be interested by owning the process of building an `Engine`.

### Why owning the cooking (building) process of Tartiflette?

The cooking process of Tartiflette is equals to a `build` process on another library, it will prepare your engine to be executed. Thus, it's useless to say that an engine instance can not be executed without beeing cooked. Like the meal, you can not eat a tartiflette without cooking it first. That's it.

Customize the cooking process is interesting to integrate Tartiflette into another library, like `aiohttp`, `starlette`, `django` and so one.

> Note: `tartiflette-aiohttp` has its own flow to manage the cooking process of the engine.

### `cook()` your Tartiflette

As specified above, the `Engine` needs to be `cook()` before being executed. Here are the sequence to execute a query on an `Engine` instance.

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
await engine.execute("query { hello )")
```

#### `cook()` interface

The `cook` method is asynchronous, this *strong choice* will allow us to execute asynchronous tasks during the building process, like:
* fetching SDL from another API
* fetch third-parties services _(database structure, cloud provider objects ...)_
* fetch schema from a schema manager

```python
async def cook(
    self,
    sdl: Union[str, List[str]] = None,
    error_coercer: Callable[[Exception, Dict[str, Any]], Dict[str, Any]] = None,
    custom_default_resolver: Optional[Callable] = None,
    modules: Optional[Union[str, List[str], List[Dict[str, Any]]]] = None,
    query_cache_decorator: Optional[Callable] = UNDEFINED_VALUE,
    json_loader: Optional[Callable[[str], Dict[str, Any]]] = None,
    custom_default_arguments_coercer: Optional[Callable] = None,
    coerce_list_concurrently: Optional[bool] = None,
    schema_name: str = None,
) -> None:
    pass
```

* `sdl` _(Union[str, List[str]])_: raw SDL, path or list of file path/directory from which retrieve the SDL (more detail above)
* `error_coercer` _(Callable[[Exception, Dict[str, Any]], Dict[str, Any]])_: callable used to coerced an exception into a GraphQL valid output format ([more detail here](#parameter-error_coercer))
* `custom_default_resolver` _(Optional[Callable])_: callable used to resolve fields which doesn't implements a dedicated resolver (useful if you want to override the behavior for resolving a field, e.g. from `snake_case` to `camelCase` and vice versa) ([more detail here](#parameter-custom_default_resolver))
* `custom_default_type_resolver` _(Optional[Callable])_: callable that will replace the tartiflette `default_type_resolver` (will be called on abstract types to deduct the type of a result) ([more detail here](#parameter-custom_default_type_resolver))
* `modules` _(Optional[Union[str, List[str], List[Dict[str, Any]]]])_: list of string containing the name of the modules you want the engine to import, usually this modules contains your `@Resolvers`, `@Directives`, `@Scalar` or `@Subscription` code ([more detail here](#parameter-modules))
* `query_cache_decorator` _(Optional[Callable])_: callable that will replace the tartiflette default lru_cache decorator to cache query parsing
* `json_loader` _(Optional[Callable[[str], Dict[str, Any]]])_: a Callable that will replace python built-in `json.loads` when Tartiflette will transform the json-ast of the query into a dict useable by the execution algorithm. ([more detail here](#parameter-json_loader))
* `custom_default_arguments_coercer` _(Optional[Callable])_: callable that will replace the tartiflette `default_arguments_coercer`
* `coerce_list_concurrently` _(Optional[bool])_: determine whether or not output list are coerced concurrently by default
* `schema_name` _(str = "default")_: name of the schema represented by the provided SDL ([more detail here](./schema-registry.md))
