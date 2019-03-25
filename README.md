![Tartiflette](docs/github-landing.png)

**Tartiflette** is a GraphQL Server implementation built with **Python 3.6+**.

## Motivation

[Read this blogpost about our motivations](https://medium.com/dailymotion/tartiflette-graphql-api-engine-python-open-source-a200c5bbc477)
TL; DR
We reached the limits of Graphene, we wanted to build something which met certain requirements:
* **Offers a better developer experience** that respects the Python mindset
* **Uses SDL** _(Schema Definition Language)_
* Uses **asyncio** as the sole execution engine
* Be 100% open source

## Status

**The [first milestone](/docs/roadmaps/milestone-1.md) is behind us, we are now [on the road to the milestone 2](/docs/roadmaps/milestone-2.md)**.

**DNA**

* Define the **GraphQL schema** with the brand new [SDL _(Schema Definition Language)_](https://github.com/facebook/graphql/blob/master/spec/Section%203%20--%20Type%20System.md).
* **Performance oriented:** Performance is the core of our work.
* **Simple is better than complex:** Built with [the Zen of Python](https://www.python.org/dev/peps/pep-0020/#id3) in mind. No over-engineering.

Discover Tartiflette with our fabulous tutorial on [https://tartiflette.io/docs/tutorial/getting-started](https://tartiflette.io/docs/tutorial/getting-started)

**Summary**

- [Usage](#usage)
- [Installation](#installation)
  - [Installation dependencies](#installation-dependencies)
- [Tartiflette over HTTP](#tartiflette-over-http)
- [Roadmaps](#roadmaps)
- [Known issues](#known-issues)

## Usage

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

More details on the [API Documentation](https://tartiflette.io/docs/api/engine/)

## Installation

Tartiflette is available on [pypi.org](https://pypi.org/project/tartiflette/).

```bash
pip install tartiflette
```

### Installation dependencies

As Tartiflette based its Executor engine on *[libgraphqlparser](https://github.com/graphql/libgraphqlparser)*. You'll need these following commands on your environment to use the library. `cmake`, `bison` and `flex`.

*MacOSX*
```bash
brew install cmake flex bison
```

*Ubuntu*
```bash
apt-get install cmake flex bison
```

## Tartiflette over HTTP

Discover our implementation of tartiflette over HTTP called [tartiflette-aiohttp](https://github.com/dailymotion/tartiflette-aiohttp).

**Overview**
```bash
pip install tartiflette-aiohttp
```

```python
from aiohttp import web
from tartiflette_aiohttp import register_graphql_handlers

sdl = """
    type Query {
        hello(name: String): String
    }
"""

ctx = {
    'user_service': user_service
}

web.run_app(
    register_graphql_handlers(
        app=web.Application(),
        engine_sdl=sdl,
        engine_schema_name="default",
        executor_context=ctx,
        executor_http_endpoint='/graphql',
        executor_http_methods=['POST', 'GET']
    )
)
```

## Roadmaps

* [Milestone 1 _(Released)_](/docs/roadmaps/milestone-1.md) 
* [Milestone 2 - **Work in progress**](/docs/roadmaps/milestone-2.md)

## How to contribute to the documentation?

As you may know, the documentation is hosted on https://tartiflette.io. This _fabulous_ website is built thanks to another amazing tool, [docusaurus](https://docusaurus.io/).

The content of the documentation is hosted in this repository, to be as close as possible to the code. You will find everything you need/want in the folder `/docs`.

### How to run the website locally?

We built a docker image for the documentation _(dailymotion/tartiflette.io on docker hub)_, which allow us to provide you an easy way to launch the documentation locally, without installing a specific version of node.

**prerequisite**:
- Docker
- Docker Compose
- Make

```bash
make run-docs
```

Every change you will make in the `/docs` folder will be automatically hot reloaded. :tada:

## Known issues

* [Schema directives aren't executed](https://github.com/dailymotion/tartiflette/issues/134)
