# API

Before going deeply into the Tartiflette API, don't forget to take a look of the [getting started](./getting-started.md) section.

## Engine initialization

The way to generate the engine is pretty simple.

The engine accepts at least one parameter, called "sdl", the other [are documented in the advanced part](#advanced-constructor).

```python
from tartiflette import Engine
Engine(sdl [, resolver_middlewares, resolvers, directive_resolvers])
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

The filepath specified have to contain the full schema definition language.

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
    resolver_middlewares=[],
    resolvers={},
    directive_resolvers={},
)
```

1. **sdl:** Schema Definition Language, detailed above.
2. **resolver_middlewares:** Middlewares list which are applied **only** to resolvers.
3. **resolvers:** By default, [the resolvers should be decorated with `@Resolver`](#with-decorators). It is possible to specify a list of resolvers
```python
def my_hello_resolver(parent, args, ctx, info):
    return "Hey"

resolvers = {
    "Query.hello": my_hello_resolver
}
```
4. **directive_resolvers:** Resolver list which is used as the directive resolvers.

## Resolver

### Declare resolvers

Tartiflette provides 2 different ways to declare a resolver for a Field.

#### With decorators

The most common way to assign specific resolver to a Field, is to decorate your resolver function with the `@Resolver` decorator. Your function [MUST BE compliant with the function signature](#function-signature).

```python
from tartiflette import Resolver

@Resolver("Query.hello")
def my_hello_resolver(parent, args, context, info):
    return "Chuck"
```

#### During Engine initialization

The second way is to use the [advanced Engine initialization](#advanced-constructor) to specify a map of resolvers associated to Fields.

```python
import tartiflette

def my_hello_resolver(parent, args, ctx, info):
    return "Chuck"

engine = tartiflette.Engine(
    sdl,
    resolvers={
        "Query.hello": my_hello_resolver
    }
)
```

### Function signature

Every resolver in Tartiflette accepts four positional arguments:

_(This signature has been highly inspired by the GraphQL.js implementation)_

```python
def my_hello_resolver(parent, args, context, info):
    pass
```

1. **parent:** The result returned by the resolver of the parent field. The `root_value` is passed in the case of a top-level Query field.
2. **args:** A dict which contains the arguments passed for the field. _(in the query)_. e.g. if the field was called with `hello(name: "Chuck")`, the args dict will be equals to `{ "name": "Chuck" }`.
3. **context:** Dict shared by all resolvers, could be different for each query. It acts as a container or a state for a specific request.
4. **info:** This argument CAN BE be used only in advanced cases, but it contains information about the execution state of the query.

#### Resolver `info` argument

`info` argument contains the query AST and other execution details, which could be useful for middleware and advanced use-cases.

Here are the properties:

* `field_name` string - Describes the field name.
* `field_node` tartiflette.parser.NodeField - Describes the field from the parser point of view.
* `field_sdl` tartiflette.types.field.GraphQLField - Describes the field from the SDL point of view _(Metadata, directives, Type...)_.
* `schema` tartiflette.Schema - Describes the entire Schema.
* `path` list[string] - Describes the path in the Query.
