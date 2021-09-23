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
  - [Building from source](#building-from-source)
- [HTTP server implementations](#http-server-implementations)
- [Roadmaps](#roadmaps)
- [How to contribute to the documentation?](#how-to-contribute-to-the-documentation)
  - [How to run the website locally?](#how-to-run-the-website-locally)

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

While the project depends on *[libgraphqlparser](https://github.com/graphql/libgraphqlparser)*,
wheels are provided since version 1.4.0, ensuring that no system dependency is required.

To install the library:

```bash
pip install tartiflette
```

### Building from source

If you use a platform incompatible with the provided wheels, you'll need to install `cmake` to build `libgraphqlparser`
in order to install the library.

*macOS*
```bash
brew install cmake
```

*Debian/Ubuntu*
```bash
apt-get install cmake
```

## HTTP server implementations

`tartiflette` library itself is transport agnostic, but to simplify integration with existing HTTP servers, two
different libraries are available:

- [tartiflette-aiohttp](https://github.com/tartiflette/tartiflette-aiohttp): integration with `aiohttp`
- [tartiflette-asgi](https://github.com/tartiflette/tartiflette-asgi): integration with ASGI compatible HTTP servers

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
