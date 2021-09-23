![Tartiflette](docs/github-landing.png)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=tartiflette_tartiflette&metric=alert_status)](https://sonarcloud.io/dashboard?id=tartiflette_tartiflette)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/tartiflette/tartiflette.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/tartiflette/tartiflette/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/tartiflette/tartiflette.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/tartiflette/tartiflette/context:python)


**Tartiflette** is a GraphQL Server implementation built with **Python 3.6+**.

**Summary**

- [Motivation](#motivation)
- [Status](#status)
- [Usage](#usage)
- [Installation](#installation)
  - [Installation dependencies](#installation-dependencies)
- [Tartiflette over HTTP](#tartiflette-over-http)
- [Roadmaps](#roadmaps)
- [How to contribute to the documentation?](#how-to-contribute-to-the-documentation)
  - [How to run the website locally?](#how-to-run-the-website-locally)
- [Known issues](#known-issues)

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

## Usage

```python
import asyncio

from tartiflette import Resolver, create_engine

@Resolver("Query.hello")
async def resolver_hello(parent, args, ctx, info):
    return "hello " + args["name"]


async def run():
    engine = await create_engine(
        """
        type Query {
            hello(name: String): String
        }
        """
    )

    result = await engine.execute(
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

#### 1.2.0+

As Tartiflette based its Executor engine on *[libgraphqlparser](https://github.com/graphql/libgraphqlparser)*. You'll need these following commands on your environment to use the library. `cmake`

*MacOSX*
```bash
brew install cmake
```

*Ubuntu*
```bash
apt-get install cmake
```

#### Before 1.2.0

As Tartiflette based its Executor engine on *[libgraphqlparser](https://github.com/graphql/libgraphqlparser)*. You'll need these following commands on your environment to use the library. `cmake`, `bison` and `flex`.

*MacOSX*
```bash
brew install cmake flex bison
```

*Ubuntu*
```bash
apt-get install cmake flex bison
```

Make sure you have `bison` in version 3
>Note to Mac OS users: Make sure bison in your path is really Bison 3, look [here](https://stackoverflow.com/questions/10778905/why-does-my-mac-os-x-10-7-3-have-an-old-version-2-3-of-gnu-bison/30844621#30844621) for details.
The `LIBGRAPHQLPARSER_DIR` environmental variable is available to specify where the `libgraphqlparser.so` file is located.

## Tartiflette over HTTP

Discover our implementation of tartiflette over HTTP called [tartiflette-aiohttp](https://github.com/tartiflette/tartiflette-aiohttp).

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

We built a docker image for the documentation _(tartiflette/tartiflette.io on docker hub)_, which allow us to provide you an easy way to launch the documentation locally, without installing a specific version of node.

**prerequisite**:
- Docker
- Docker Compose
- Make

```bash
make run-docs
```

Every change you will make in the `/docs` folder will be automatically hot reloaded. :tada:

## Known issues

* [Schema directives aren't executed](https://github.com/tartiflette/tartiflette/issues/134)
