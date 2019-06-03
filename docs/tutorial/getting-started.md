---
id: getting-started
title: Getting started with Tartiflette
sidebar_label: 1. Getting started
---

Welcome! Whether you are a GraphQL newbie or experienced veteran, Tartiflette will help you to build a powerful GraphQL API.

This tutorial will explain to you the main features of Tartiflette as well as some more advanced ones _(dynamic introspection, SDL Directives & more)_

## What are we doing?

Nothing is better than coding to understand a library. Let's develop your own **Tartiflette recipes manager served through an awesome GraphQL API**.

Here are the topics we will cover during this _Getting Started Tutorial_.

* Install the Tartiflette library _(and sub-dependencies)_.
* Declare your schema using the SDL _(Schema Definition Language)_.
* Create a Tartiflette _(Server)_ instance.
* Write Query, Mutation, and Subscription resolvers.
* Run Query, Mutation and Subscription requests on your **Engine**.
* Declare and use custom directives _(Advanced)_.
* Secure nodes with directives _(Advanced)_.
* Expose different portions of the schema in the introspection based on context (Dynamic introspection) _(Advanced)_.

The tutorial's end result is available on GitHub at [tartiflette-aiohttp-tutorial](https://github.com/tartiflette/tartiflette-aiohttp-tutorial).

## Prerequisites

We assume that you're familiar with Python 3.6+, asyncio and more generally with asynchronous development. We do not plan to link this tutorial with other technologies like RDBMS _(MySQL, Postgres etc ...)_. We'll keep this tutorial focused on `tartiflette` usage.

Moreover, we will intensively use the command line to manipulate files or launch commands.

### System requirements

Make sure that your setup contains:
* Python 3.6+ via Pipenv
* git
* Package manager (e.g: homebrew on Macosx or apt on Ubuntu)

## Do you need help?

If you're ever feeling lost or don't understand a concept, [join the Tartiflette community on Slack](http://slack-tartiflette-io.herokuapp.com/) _(with luck, some of the tartiflette maintainers will be there)_.
