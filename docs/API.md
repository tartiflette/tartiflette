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
tartiflette.Engine(
    sdl,
    resolver_middlewares=[],
    resolvers={},
    directive_resolvers={},
)
```

1. **sdl:** Schema Definition Language, detailed above.
2. **resolver_middlewares:** Middlewares list which are applied **only** to resolvers.
3. **resolvers:** By default, the resolvers should be decorated with `@Resolver`. It is possible to specify a list of resolvers
```
def my_hello_resolver(parent, args, ctx, info):
    return "Hey"

resolvers = {
    "Query.hello": my_hello_resolver
}
```
4. **directive_resolvers:** Resolver list which is used as the directive resolvers.
