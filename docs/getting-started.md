# Getting Started With Tartiflette

## Prerequisites

Before getting started, you should have Python 3.5+ installed _(at least)_. As we are using ["libgraphqlparser"](https://github.com/graphql/libgraphqlparser), the C++ query parser, you should have the necessary to compile that library. **We suggest to use the docker image, which contains the necessary to work**.

To create a new project with Tartiflette, just execute that command.

```bash
pip install tartiflette
```

## Your first Tartiflette!

The smallest recipe to make a tartiflette is pretty easy. Let's start with a hello world.

* Define a **Schema** _(with Schema Definition Language)_ that defines the **"Query"** type.
* Implement a simple resolver which resolve the hello field.

```python
import asyncio
from tartiflette import Engine, Resolver

engine = Engine(
    """
    type Query {
        hello: String
        whoami: Kevin
    }
    """
)

@Resolver("hello")
async def hello_resolver():
    return "World"

def run():
    result = await engine.execute(
        """
        query {
            hello
        }
        """
    )
    print(result["data"]["hello"])

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
loop.close()
```
