---
id: getting-started
title: Getting started with Tartiflette
sidebar_label: 1. Getting started
---

Welcome! Whether you are a GraphQL newbie or experienced veteran, Tartiflette will help you to build a powerful GraphQL API.

This tutorial will explain to you the main features of Tartiflette as well as some more advanced ones _(dynamic introspection, SDL directives & more)_.

## What are we doing?

Nothing is better than coding to understand a library. In this tutorial, we will develop our own **Tartiflette recipes manager served by an awesome GraphQL API**.

Here are the topics we will cover during this tutorial:
* install the Tartiflette library _(and sub-dependencies)_
* declare your schema using the SDL _(Schema Definition Language)_
* create a Tartiflette _(Server)_ instance
* write Query, Mutation, and Subscription resolvers
* run Query, Mutation and Subscription requests
* declare and use custom directives _(Advanced)_
* secure nodes with directives _(Advanced)_
* expose different portions of the schema in the introspection based on context (dynamic introspection) _(Advanced)_

The tutorial's end result is available on GitHub at [tartiflette-aiohttp-tutorial](https://github.com/tartiflette/tartiflette-aiohttp-tutorial).

## Prerequisites

We assume that you are familiar with Python 3.6+, `asyncio` and more generally with asynchronous development. We do not plan to link this tutorial with other technologies like RDBMS _(MySQL, Postgres etc ...)_. We will keep this tutorial focused on `tartiflette` usage.

Moreover, we will intensively use the command line to manipulate files or launch commands.

### System requirements

Make sure that your setup contains:
* Python 3.6+ via Pipenv
* git
* a package manager (e.g: `homebrew` on macOS or `apt` on Ubuntu)

## Do you need help?

If you are ever feeling lost or do not understand a concept, [join the Tartiflette community on Slack](http://slack-tartiflette-io.herokuapp.com/) _(with luck, some of the Tartiflette maintainers will be there)_.
