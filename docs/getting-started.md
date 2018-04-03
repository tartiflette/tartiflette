# Getting Started With Tartiflette

## Prerequisites

Before getting started, you should have Python 3.5+ installed. As we are using [libgraphqlparser](https://github.com/graphql/libgraphqlparser), a C++ query parser, you should have the necessary to compile that library (Cmake etc.). **We suggest you use the provided docker image, which contains everything needed**.

To create a new project with Tartiflette, just execute this command:

```bash
pip install tartiflette
```

## Your first Tartiflette!

The smallest recipe to make a tartiflette is pretty easy. Let's start with a hello world.

* Define a **Schema** _(with the Schema Definition Language)_ that defines the **`Query`** type.
* Implement a simple resolver which resolves the `hello` field.

```python
import asyncio
from tartiflette import Engine, Resolver

engine = Engine(
    """
    type Query {
        hello: String
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
