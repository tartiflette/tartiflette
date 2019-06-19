---
id: introduction
title: Plugins
sidebar_label: Plugins
---

![tartiflette Plugins](/docs/assets/tartiflette-plugin.png)

## Plugins approach

The idea behind the plugin approach of tartiflette is to bring extensibility, community and reusability to your sdl using [Directive](/docs/api/directive.md), [Custom Scalar](/docs/api/scalar.md) and [Resolver](/docs/api/resolver.md) as plugins.

## What is a tartiflette plugin ?

A tartiflette plugin is a python package that will prodive a bit of SDL defining Directives, Scalar, Types, etc and code implementation of those objects.

It's name should be prefixed by `tartiflette-plugins-`, I.E. for a plugin named `oauth`, its pypi package will be `tartiflette-plugin-oauth` and its python package will be `tartiflette_plugin_oauth`.

## How can I create one ?

Have a look at the [Create a plugin](/docs/plugins/create-a-plugin.md) page for a detailled way on how to create a plugin.
You can also have a look at the [Time-it plugin Repositry](https://github.com/tartiflette/tartiflette-plugin-time-it).

## How can I use plugins ?

Have a look at the [Use a Plugin](/docs/plugins/use-a-plugin.md) page for a detailled way on how to use a plugin.


