# Roadmap: Version 1

- [Roadmap: Version 1](#roadmap-version-1)
  - [Communication and documentation](#communication-and-documentation)
  - [Query Parser](#query-parser)
  - [Executor](#executor)
  - [SDL - Schema Definition Language](#sdl---schema-definition-language)
  - [Continuous integration](#continuous-integration)

Following on our experience in managing GraphQL APIs in production **for more than a year**, we've decided to build a brand new GraphQL Engine.

Here are the subjects we were working during 2018 and early 2019:

## Communication and documentation

* [x] Define Open Source guidelines (contributing, code of conduct, issue template, PR template).
* [X] (API) Describe the API that will be used by the Tartiflette users.
  * [x] (API) [Engine constructor](../api.md#engine-initialization)
  * [X] (API) How to declare custom directives in the Engine Constructor.
  * [X] (API) How to declare middlewares on a resolver.
  * [X] (API) Executor implementation.
  * [x] (API) Resolver implementation.
  * [x] (API) Resolver - `Info` parameter.
* [x] (Website) Landing page for https://tartiflette.io
* [x] (Website) Publish documentation on https://tartiflette.io

## Query Parser

* [x] Build communication interface between [libgraphqlparser](https://github.com/graphql/libgraphqlparser) & Tartiflette through [CFFI](https://cffi.readthedocs.io).
* [x] Build a `Parser` which parses a GraphQL Query and creates a list of Asynchronous Tasks.
* [x] Build an `Executor` which executes the Asynchronous Tasks list created by the `Parser`.

## Executor

* [x] Bind the Types specified in the SDL to the `Executor`.
* [x] Typing resolver outputs
* [x] Error management
* [X] Abstract and Compound Types: Interfaces
* [x] Abstract and Compound Types: Unions
* [X] NodeDefinition: Check that the Type exists.
* [X] (Directive) Integrate the directive's execution in the Executor.
* [X] (Directive) introspection based on directives
* [X] Subscription Support

## SDL - Schema Definition Language

* [x] Build a `Parser` which parse the [Schema Definition Language](https://github.com/facebook/graphql/blob/master/spec/Section%202%20--%20Language.md) and creates the associated schema and types as Python objects.
* [X] Think about custom Scalar API
* [x] (Introspection) Implement the `__type` Field.
* [x] (Introspection) Implement the `__schema`Field.
* [X] (Directive) Append directive information _(from SDL)_ as metadata on Fields / Types.
* [X] (Directive) Implement the declaration of the custom directives into the Engine constructor.
* [X] (Directive) Implement @deprecated

## Continuous integration

* [x] Run Code Quality checks + Tests
* [x] Automatize the integration of `libgraphqlparser`
* [X] Build & Publish artifact to pypi
