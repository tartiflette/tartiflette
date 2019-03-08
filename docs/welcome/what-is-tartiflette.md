---
id: what-is-tartiflette
title: What is Tartiflette
sidebar_label: What is Tartiflette?
---

Welcome, glad to see you here.

**Tartiflette** is a GraphQL Engine, built on top of Python 3.6 and above. Focused on building GraphQL APIs using the awesome **Schema Definition Language**.

## What is GraphQL?

> GraphQL is a query language for APIs and a runtime for fulfilling those queries with your existing data. GraphQL provides a complete and understandable description of the data in your API, gives clients the power to ask for exactly what they need and nothing more, makes it easier to evolve APIs over time, and enables powerful developer tools.

Source: [https://graphql.org/](https://graphql.org/)

## Can I use a standalone Tartiflette for my project?

Our engine follows the [GraphQL Specification](https://facebook.github.io/graphql/), which doesn't specify any transport layer. You can integrate the Tartiflette Engine wherever you need and use whatever transport layer you want: JSON RPC, gRPC or, obviously, HTTP.

In addition to the Tartiflette Engine, and based on common integrations of GraphQL, we developed a GraphQL HTTP Library, which uses the awesome `aiohttp` library to expose the Tartiflette Engine through HTTP.

![tartiflette integration into tartiflette-aiohttp](/docs/assets/tartiflette-aiohttp.png)

If you just landed in the GraphQL world, or if you don't want to deal with the integration of Tartiflette behind an HTTP layer, we suggest the use of `tartiflette-aiohttp`.

For advanced use-cases, you should jump to the API documentation of Tartiflette.

In any case, this is the perfect moment to start [the tutorial](/docs/tutorial) which is based on `tartiflette-aiohttp`.
