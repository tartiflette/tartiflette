---
id: introduction
title: Introduction
sidebar_label: Introduction
---

![tartiflette Plugins](/docs/assets/tartiflette-plugin.png)

## Plugins approach

The idea behind the plugin approach of tartiflette is to bring extensibility, community and reusability to your SDL using [Directive](/docs/api/directive), [Custom Scalar](/docs/api/scalar) and [Resolver](/docs/api/resolver) as plugins.

## What is a tartiflette plugin ?

A tartiflette plugin is a python package that will provide a bit of SDL defining Directives, Scalar, Types, etc and code implementation of those objects.

This is not mandatory, but we would like to have plugins name prefixed by `tartiflette-plugins-`, I.E. for a plugin named `oauth`, its pypi package will be `tartiflette-plugin-oauth` and its python package will be `tartiflette_plugin_oauth`.

## How can I create one ?

Have a look at the "[Create a plugin](/docs/plugins/create-a-plugin)" page for a detailled way on how to create a plugin.
You can also have a look at the [Time-it plugin Repository](https://github.com/tartiflette/tartiflette-plugin-time-it).

## How can I use plugins ?

Have a look at the "[Use a Plugin](/docs/plugins/use-a-plugin)" page for a detailled way on how to use a plugin.
