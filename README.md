![Tartiflette](docs/github-landing.png)

**Tartiflette** is a GraphQL Server implementation built with **Python 3.5+**.

**Tartiflette is not production ready, we are working on it heavily. [Feel free to join us to build Tartiflette](./docs/CONTRIBUTING.md).**

**[Take a look of our roadmap for v1](#roadmap---road-to-v1)**.

**DNA**

* Define the **GraphQL schema** with the brand new [SDL _(Schema Definition Language)_](https://github.com/facebook/graphql/blob/master/spec/Section%203%20--%20Type%20System.md).
* **Performance oriented:** Performance is the core of our work.
* **Simple is better than complex:** Built with [the Zen of Python](https://www.python.org/dev/peps/pep-0020/#id3) in mind. No over-engineering.

**Summary**

* [Usage](#usage)
* [Installation](#installation)
  * [installation dependencies](#installation-dependencies)
* [Getting Started](./docs/getting-started.md)
* [API](./docs/API.md)
* [Roadmap - Road to v1](#roadmap---road-to-v1)
* [Roadmap - Milestone 2](#roadmap---milestone-2)

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

## Roadmap - Road to v1

Following on our experience in managing GraphQL APIs in production **for more than a year**, we've decided to build a brand new GraphQL Engine.

[Know more about the API.](docs/API.md)

Here are the subjects we are working on:

### Communication and documentation

* [x] Define Open Source guidelines (Contributing, Code of conduct, Issue Template, PR Template).
* [X] (API) Describe the API that will be used by the Tartiflette users.
  * [x] (API) [Engine constructor](https://github.com/dailymotion/tartiflette/blob/master/docs/API.md#engine-initialization)
  * [X] (API) How to declare custom directives in the Engine Constructor.
  * [X] (API) How to declare middleware on a resolver.
  * [X] (API) Executor.
  * [x] (API) Resolver.
  * [x] (API) Resolver - `Info` parameter.
* [ ] (Website) Landing page for https://tartiflette.io
* [ ] (Website) Expose documentation on https://tartiflette.io

### Query Parser

* [x] Build communication interface between [libgraphqlparser](https://github.com/graphql/libgraphqlparser) & Tartiflette through [CFFI](https://cffi.readthedocs.io).
* [x] Build a `Parser` which parses a GraphQL Query and creates a list of Asynchronous Tasks.
* [x] Build an `Executor` which executes the Asynchronous Tasks list created by the `Parser`.

### Executor

* [x] Bind the Types specified in the SDL to the `Executor`.
* [x] Typing resolver outputs
* [x] Error management
* [X] Abstract and Compound Types: Interfaces
* [x] Abstract and Compound Types: Unions
* [X] NodeDefinition: Check that the Type exists.
* [X] (Directive) Integrate the directive's execution in the Executor.
* [X] (Directive) introspection based on directive

### SDL - Schema Definition Language

* [x] Build a `Parser` which parse the [Schema Definition Language](https://github.com/facebook/graphql/blob/master/spec/Section%202%20--%20Language.md) and created the associated schema and types as Python objects.
* [X] Think about custom Scalar API
* [x] (Introspection) Implement the `__type` Field.
* [x] (Introspection) Implement the `__schema`Field.
* [X] (Directive) Append directive informations _(from SDL)_ as metadata on Fields / Types.
* [X] (Directive) Implement the declaration of the custom directives into the Engine constructor.
* [X] (Directive) Implement @deprecated

### Continuous integration

* [x] Run Code Quality checks + Tests
* [x] Automatize the integration of `libgraphqlparser`
* [X] Build & Publish artifact to pypi

## Roadmap - Milestone 2

* [ ] Implement **[Apollo Cache Control](https://github.com/apollographql/apollo-cache-control)**
* [ ] Think about `subscriptions`

## Integration Example

An integration example can be found on the [tartiflette-aiohttp](https://github.com/dailymotion/tartiflette-aiohttp) github repository
