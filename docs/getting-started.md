# Getting Started With Tartiflette

## Prerequisites

Before getting started, you should have installed the `tartfilette` package through Pypi.

[Follow the instructions details in the README](../README.md#installation).

## Your first Tartiflette!

The smallest recipe to make a tartiflette is pretty easy. Let's start with a hello world.

* Define a **Schema** _(with the Schema Definition Language)_ that defines the **`Query`** type.
* Implement a simple resolver which resolves the `hello` field.

```python
import asyncio

from tartiflette import Engine, Resolver

@Resolver("Query.hello")
async def resolver_hello(parent, args, ctx, info):
    return "hello " + args["name"]

async def run():
    tftt_engine = Engine("""
    type Query {
        hello(name: String): String
    }
    """)

    result = await tftt_engine.execute(
        query='query { hello(name: "Chuck") }'
    )

    print(result)
    # {'data': {'hello': 'hello Chuck'}}

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
```
