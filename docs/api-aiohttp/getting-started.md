---
id: getting-started
title: Getting started with tartiflette-aiohttp
sidebar_label: Getting started
---

**tartiflette-aiohttp** is a wrapper of aiohttp which includes the Tartiflette GraphQL Engine, do not hesitate to take a look of the [Tartiflette API documentation](/docs/api/engine/).

## Usage

```python
# main.py
from aiohttp import web
from tartiflette import Resolver
from tartiflette_aiohttp import register_graphql_handlers

@Resolver("Query.hello")
async def resolver_hello(parent, args, ctx, info):
    return "hello " + args["name"]

sdl = """
    type Query {
        hello(name: String): String
    }
"""

web.run_app(
    register_graphql_handlers(
        web.Application(),
        engine_sdl=sdl
    )
)
```

Save the file and start the server.

```bash
$ python main.py
======== Running on http://0.0.0.0:8080 ========
(Press CTRL+C to quit)
```

Execute a request to your server
```
curl -v -d '{"query": "query { hello(name: "Chuck") }"}' -H "Content-Type: application/json" http://localhost:8080/graphql
```

## Installation

`tartiflette-aiohttp` is available on [pypi.org](https://pypi.org/project/tartiflette-aiohttp/).

```bash
pip install tartiflette-aiohttp
```

Do not forget to install the [tartiflette dependencies as explained in the tutorial](/docs/tutorial/install-tartiflette/).

## How to use

### Use with built-in Tartiflette Engine

The basic and common way to use Tartiflette with aiohttp, is to create an aiohttp `web.Application` and use the `register_graphql_handlers` helper to bind Tartiflette and aiohttp together. `engine_*` parameters will be forwarded to the built-in [tartiflette](https://github.com/dailymotion/tartiflette) engine instance.

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

**Parameters**:

* **engine_sdl**: Contains the [Schema Definition Language](https://graphql.org/learn/schema/)
  - Could be a string which contains the SDL
  - Could be an array of string, which contain the SDLs
  - Could be a path of an SDL
  - Could be an array of paths which contain the SDLs
* **engine_schema_name**: Name of the schema used the built-in engine.
* **executor_context**: Context which will be passed to each resolver. Be default, the context passed to each resolvers, will contain these properties.
  - **req**: Request object from aiohttp
  - **app**: Application object from aiohttp
* **executor_http_endpoint**: Endpoint where the GraphQL Engine will be attached, by default on `/graphql`
* **executor_http_methods**: HTTP Method where the GraphQL Engine will be attached, by default on **POST** and **GET**.

### Use with custom Tartiflette engine

In the case you already have a Tartiflette Engine instance, or, you do not want to use the built-in instance. You can pass an existing instance to the `register_graphql_handlers` helper.

```python
# main.py
from aiohttp import web
from tartiflette import Resolver, Engine
from tartiflette_aiohttp import register_graphql_handlers

@Resolver("Query.hello")
async def resolver_hello(parent, args, ctx, info):
    return "hello " + args["name"]

sdl = """
    type Query {
        hello(name: String): String
    }
"""

engine = Engine(sdl)

ctx = {
    'user_service': user_service
}

web.run_app(
    register_graphql_handlers(
        app=web.Application(),
        engine=engine,
        executor_context=ctx,
        executor_http_endpoint='/graphql',
        executor_http_methods=['POST', 'GET']
    )
)
```

**Parameters**:

* **engine**: Tartiflette Engine instance
* **executor_context**: Context which will be passed to each resolver. Be default, the context passed to each resolvers, will contain these properties
  - **req**: Request object from aiohttp
  - **app**: Application object from aiohttp
* **executor_http_endpoint**: Endpoint where the GraphQL Engine will be attached, by default on `/graphql`
* **executor_http_methods**: HTTP Method where the GraphQL Engine will be attached, by default on **POST** and **GET**

### Tartiflette with subscriptions

Tartiflette embeds an easy way to deal with subscription. The only thing to do is
to fill in the `subscription_ws_endpoint` parameter and everything will work out
of the box with `aiohttp` WebSockets. You can see a full example
[here](examples/aiohttp/dogs).

### Enable GraphiQL handler

Tartiflette allows you to set up an instance of GraphiQL easily to quickly test
your queries. The easiest way to do that is to set the `graphiql_enabled`
parameter to `True`. Then, you can customize your GraphiQL instance by filling
the `graphiql_options` parameter as bellow:

```python
from aiohttp import web

from tartiflette_aiohttp import register_graphql_handlers


_SDL = """
    type Query {
        hello(name: String): String
    }
"""

web.run_app(
    register_graphql_handlers(
        app=web.Application(),
        engine_sdl=_SDL,
        graphiql_enabled=True,
        graphiql_options={  # This is optional
            "endpoint": "/explorer",  # Default: `/graphiql`,
            "default_query": """
                query Hello($name: String) {
                  hello(name: $name)
                }
            """,
            "default_variables": {
                "name": "Bob",
            },
            "default_headers": {
                "Authorization": "Bearer <default_token>",
            },
        },
    )
)
```

**Parameters**:

* **engine_sdl**: Contains the [Schema Definition Language](https://graphql.org/learn/schema/)
  - Could be a string which contains the SDL
  - Could be an array of string, which contain the SDLs
  - Could be a path of an SDL
  - Could be an array of paths which contain the SDLs
* **graphiql_enabled** *(Optional[bool] = False)*: Determines whether or not we should handle a GraphiQL endpoint
* **graphiql_options** *(Optional[dict] = None)*: Customization options for the GraphiQL instance:
  - **endpoint** *(Optional[str] = "/graphiql")*: allows to customize the GraphiQL endpoint
  - **default_query** *(Optional[str] = None)*: allows you to pre-fill the GraphiQL interface with a default query
  - **default_variables** *(Optional[dict] = None)*: allows you to pre-fill the GraphiQL interface with default variables
  - **default_headers** *(Optional[dict] = None)*: allows you to add default headers to each request sent through the GraphiQL instance