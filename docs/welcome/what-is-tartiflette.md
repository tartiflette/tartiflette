---
id: what-is-tartiflette
title: What is Tartiflette?
sidebar_label: What is Tartiflette?
---

Welcome, glad to see you here.

**Tartiflette** is a GraphQL engine, built on top of Python 3.6 and above. Focused on building GraphQL APIs using the awesome **Schema Definition Language**.

## What is GraphQL?

> GraphQL is a query language for APIs and a runtime for fulfilling those queries with your existing data. GraphQL provides a complete and understandable description of the data in your API, gives clients the power to ask for exactly what they need and nothing more, makes it easier to evolve APIs over time, and enables powerful developer tools.

Source: [https://graphql.org/](https://graphql.org/)

## Can I use a standalone Tartiflette for my project?

Our engine follows the [June 2018 GraphQL Specification](https://graphql.github.io/graphql-spec/June2018/), which doesn't specify any transport layer. You can integrate the Tartiflette engine wherever you need and use whatever transport layer you want: JSON RPC, gRPC or, obviously, HTTP.

However, in addition to the Tartiflette engine, and based on common integrations of GraphQL, we developed an HTTP integration of the Tartiflette engine over the awesome `aiohttp` library.

![HTTP Tartiflette integration into tartiflette-aiohttp](/docs/assets/tartiflette-aiohttp.png)

If you are new in the GraphQL world, or if you don't want to deal with the integration of Tartiflette behind an HTTP layer, we suggest the use of `tartiflette-aiohttp`.

For advanced use-cases, you should jump to [the API documentation](/docs/api/engine) of Tartiflette.

In any case, this is the perfect moment to start [the tutorial](/docs/tutorial) which is based on `tartiflette-aiohttp`.
