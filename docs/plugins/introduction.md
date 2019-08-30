---
id: introduction
title: Introduction
sidebar_label: Introduction
---

![tartiflette Plugins](/docs/assets/tartiflette-plugin.png)

## Plugins approach

The idea behind the plugin approach of tartiflette is to bring extensibility, community and reusability to your SDL using [Directive](../api/directive.md), [Custom Scalar](../api/scalar.md) and [Resolver](../api/resolver.md) as plugins.

## What is a tartiflette plugin ?

A tartiflette plugin is a python package that will provide a bit of SDL defining Directives, Scalar, Types, etc and code implementation of those objects.

This is not mandatory, but we would like to have plugins name prefixed by `tartiflette-plugins-`, I.E. for a plugin named `oauth`, its pypi package will be `tartiflette-plugin-oauth` and its python package will be `tartiflette_plugin_oauth`.

## How can I craete one ?

Have a look at the "[Create a plugin](./create-a-plugin.md)" page for a detailled way on how to create a plugin.
You can also have a look at the [Time-it plugin Repository](https://github.com/tartiflette/tartiflette-plugin-time-it).

## How can I use plugins ?

Have a look at the "[Use a Plugin](./use-a-plugin.md)" page for a detailled way on how to use a plugin.
