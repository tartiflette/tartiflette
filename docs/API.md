- [Engine initialization](#engine-initialization)
  - [Advanced constructor](#advanced-constructor)
    - [Engine parameter: error_coercer](#engine-parameter-errorcoercer)
    - [Engine parameter: custom_default_resolver](#engine-parameter-customdefaultresolver)
    - [Engine parameter: exclude_builtins_scalars](#engine-parameter-excludebuiltinsscalars)
- [Resolver](#resolver)
  - [@Resolver decorator](#resolver-decorator)
  - [Schema Registry](#schema-registry)
    - [What is aim of the Schema Registry?](#what-is-aim-of-the-schema-registry)
    - [How to use multiple Schema and Engine from the same codebase?](#how-to-use-multiple-schema-and-engine-from-the-same-codebase)
  - [Function signature](#function-signature)
    - [Resolver `info` argument](#resolver-info-argument)
- [Types](#types)
  - [Scalars](#scalars)

Before going deeply into the Tartiflette API, don't forget to take a look of the [getting started](./getting-started.md) section.

## Engine initialization

The way to generate the engine is pretty simple.

The engine accepts at least one parameter, called "sdl", the other [are documented in the advanced part](#advanced-constructor).

```python
from tartiflette import Engine
Engine(sdl [, schema_name, error_coercer, custom_default_resolver, exclude_builtins_scalars])
```

**When the `sdl` parameter contains the raw schema.**

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

**When the `sdl` parameter targets a file.**

The filepath specified has to contain the full schema definition language.

```python
import tartiflette

engine = tartiflette.Engine(
    "/User/chuck/workspace/mytartiflette/schema.sdl"
)
```

**When the `sdl` parameter targets a file list.**

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

**When the `sdl` parameter targets a folder.**

Every file which ends by `.sdl` will be concatenated, in lexicographical order.

```python
import tartiflette

engine = tartiflette.Engine(
    "/User/chuck/workspace/mytartiflette"
)
```

**When the `sdl` parameter is a Schema object.**

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

### Advanced constructor

The engine provides an advanced interface for initialization. It accepts optional and named parameters.

```python
import tartiflette

engine = tartiflette.Engine(
    sdl,
    schema_name="default",
)
```

1. **sdl:** Schema Definition Language, detailed above.
2. **schema_name:** Schema used from the [Schema Registry](schema-registry). _(default: "default")_
3. **[error_coercer](#engine-parameter-errorcoercer):** Coercer used when an error is raised.
4. **[custom_default_resolver](#engine-parameter-customdefaultresolver):** Used another default resolver. (useful to override the behavior for resolving a property, snakecase -> camelcase and vice versa).
5. **[exclude_builtins_scalars](#engine-parameter-excludebuiltinsscalars):** List of scalars you want to exclude from the default list.

#### Engine parameter: error_coercer

Override the default coercer when an exception is raised.

```python
def my_error_coercer(exception) -> dict:
    do_ing_some_thin_gs = 42
    return a_value

e = Engine("my_sdl.sdl", error_coercer=my_error_coercer)
```

#### Engine parameter: custom_default_resolver

Used another default resolver. Could be useful to override the behavior for resolving a property, snakecase -> camelcase and vice versa.

```python

async def my_default_resolver(parent_result, arguments, context, info):
    do_ing_some_thin_gs = 42
    return a_value

e = Engine("my_sdl.sdl", custom_default_resolver=my_default_resolver)
```

#### Engine parameter: exclude_builtins_scalars

List of scalars you want to exclude [from the default list](#scalars). Useful if you define by yourself the default scalar in the SDL.

```python
e = Engine("my_sdl.sdl", exclude_builtins_scalars=["Date", "DateTime"])
```

## Resolver

### @Resolver decorator

The most common way to assign specific resolver to a Field, is to decorate your resolver function with the `@Resolver` decorator. Your function [MUST BE compliant with the function signature](#function-signature).

```python
from tartiflette import Resolver

@Resolver("Query.hello")
async def my_hello_resolver(parent, args, context, info):
    return "Chuck"
```

### Schema Registry

By default, all the resolvers created thanks to the `@Resolver` decorator, are registered to the "default" schema in the `Schema Registry`.

#### What is aim of the Schema Registry?

The `Schema Registry` is an advanced use-case of Tartiflette, used by the developers who want to expose more than one Engine from the same codebase.

The Schema Registry will help you to assign a `Resolver` to a specific Schema, then, during the initialization process of the Engine, you will be able to choose a specific Schema to use.

By default, every `Resolver` are assigned to the `default` schema. Moreover, every Engine are attached to the `default` schema.

#### How to use multiple Schema and Engine from the same codebase?

This following code sample will create 2 schemas in the `Schema Registry`.

- "default"
- "proof_of_concept"

```python
import asyncio

from tartiflette import Engine, Resolver

@Resolver("Query.hello") # Will be assigned to the 'default' Schema
async def resolver_hello(parent, args, ctx, info):
    return "hello " + args["name"]


@Resolver("Query.hello", "proof_of_concept") # Will be assigned to the 'proof_of_concept' Schema
async def resolver_hello(parent, args, ctx, info):
    return "Hey " + args["name"]


async def run():
    tftt_engine = Engine("""
    type Query {
        hello(name: String): String
    }
    """) # This Engine will attached the SDL to the 'default' Schema.

    result = await tftt_engine.execute(
        query='query { hello(name: "Chuck") }'
    )

    # result will be equals to
    # {
    #     "data": {
    #         "hello": "Hello Chuck"
    #     }
    # }

    tftt_proof_of_concept = Engine("""
    type Query {
        hello(name: String): String
    }
    """,
    schema_name="proof_of_concept") # This Engine will attached the SDL to the 'proof_of_concept' Schema.

    result_poc = await tftt_proof_of_concept.execute(
        query='query { hello(name: "Chuck") }'
    )

    # result_poc will be equals to
    # {
    #     "data": {
    #         "hello": "Hey Chuck"
    #     }
    # }
```

### Function signature

Every resolver in Tartiflette accepts four positional arguments:

_(This signature has been highly inspired by the GraphQL.js implementation)_

```python
async def my_hello_resolver(parent, args, context, info):
    pass
```

1. **parent:** The result returned by the resolver of the parent field. The `root_value` is passed in the case of a top-level Query field.
2. **args:** A dict which contains the arguments passed for the field. _(in the query)_. e.g. if the field was called with `hello(name: "Chuck")`, the args dict will be equals to `{ "name": "Chuck" }`.
3. **context:** Dict shared by all resolvers, could be different for each query. It acts as a container or a state for a specific request.
4. **info:** This argument CAN BE be used only in advanced cases, but it contains information about the execution state of the query.

#### Resolver `info` argument

`info` argument contains the query AST and other execution details, which could be useful for middleware and advanced use-cases.

Here are the properties:

- `query_field` tartiflette.parser.NodeField - Contains the information of the field from the query's perspective.
- `schema_field` tartiflette.types.field.GraphQLField - Contains the information of the field from the schema's perspective (type, default values, and more.)
- `schema` tartiflette.schema.GraphQLSchema - Contains the GraphQL's server schema.
- `path` List[string] - Describes the path in the current query
- `location` tartiflette.types.location.Location - Describes the location in the query
- `execution_ctx` tartiflette.executor.types.ExecutionContext - Contains execution values (like `errors`).

## Types

### Scalars

The built-ins Scalars list used by tartiflette is available in the directory [`./tartiflette/builtins`](https://github.com/dailymotion/tartiflette/tree/master/tartiflette/schema/builtins/scalars)

- Boolean
- Date
- DateTime
- Float
- ID
- Int
- String
- Time
