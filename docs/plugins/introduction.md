---
id: introduction
title: Introduction
sidebar_label: Introduction
---

![Tartiflette Plugins](/docs/assets/tartiflette-plugin.png)

## Plugins approach

The idea behind the plugin approach of Tartiflette is to bring extensibility, community and reusability to your SDL using [directives](/docs/api/directive), [custom scalars](/docs/api/scalar) and [resolvers](/docs/api/resolver) as plugins.

## What is a Tartiflette plugin?

A Tartiflette plugin is a python package that will provide a bit of SDL defining `Directives`, `Scalar`, `Types`, etc... and code implementation of those objects.

This is not mandatory, but we would like to have plugins name prefixed by `tartiflette-plugins-***`, E.g. for a plugin named `oauth`, its pypi package will be `tartiflette-plugin-oauth` and its python package will be `tartiflette_plugin_oauth`.

## How can I create one?

Have a look at the "[Create a plugin](/docs/plugins/create-a-plugin)" page for a detailled way on how to create a plugin.
You can also have a look at the [time-it plugin repository](https://github.com/tartiflette/tartiflette-plugin-time-it).

## How can I use plugins?

Have a look at the "[Use a Plugin](/docs/plugins/use-a-plugin)" page for a detailled way on how to use a plugin.
