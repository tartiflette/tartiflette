---
id: install-tartiflette
title: Install Tartiflette package with pipenv
sidebar_label: 3. Install Tartiflette
---

Tartiflette is available on [pypi.org](https://pypi.org/project/tartiflette/) and you can install it with `pip` or `pipenv`. In this tutorial, we will use [`pipenv`](https://docs.pipenv.org/) as it embeds both the package management and the virtual environment.

## Installation dependencies

As Tartiflette based its query parsing on [`libgraphqlparser`](https://github.com/graphql/libgraphqlparser), you will need these following binaries in your environment to use the library: `cmake`

**macOS**:
```bash
brew install cmake
```

**Ubuntu**:
```bash
apt-get install cmake
```

## Installation

Are you ready? We are now going to install Tartiflette!

In this tutorial, we want to expose our GraphQL API through HTTP. To build this API easily and quickly, we are going to use an HTTP integration of Tartiflette called [`tartiflette-aiohttp`](https://github.com/tartiflette/tartiflette-aiohttp).

```bash
# Create the virtual environment
pipenv --python 3.7

# Install tartiflette-aiohttp
pipenv install tartiflette-aiohttp

# Enter into the virtual environment
pipenv shell
```

It is now time to write your first Tartiflette code, the "Tartiflette recipes manager" is coming.
