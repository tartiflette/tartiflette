![Tartiflette](docs/github-landing.png)

**Tartiflette** is a GraphQL Server implementation built with **Python 3.5+**.

**Tartiflette is under heavy development. [Feel free to join us to build Tartiflette](./docs/CONTRIBUTING.md).**

The engine **IS NOT** ready to use, feel free to take a look at **[our roadmap for v1](#roadmap---road-to-v1)**.

**DNA**

* Define the **GraphQL schema** with the brand new [SDL _(Schema Definition Language)_](https://github.com/facebook/graphql/blob/master/spec/Section%203%20--%20Type%20System.md).
* **Performance oriented:** Performance is the core of our work.
* **Simple is better than complex:** Built with [the Zen of Python](https://www.python.org/dev/peps/pep-0020/#id3) in mind. No over-engineering.

This lib depends on libgraphqlparser (in submodule in this repository).

You need to build and install this libgraphqlparser binary on your system before using this.
See [here](https://github.com/graphql/libgraphqlparser) for more details.

## Roadmap - Road to v1

Following on our experience in managing GraphQL APIs in production **for more than a year**, we've decided to build a brand new GraphQL Engine.

[Know more about the API.](docs/API.md)

Here are the subjects we are working on:

### Communication and documentation

* [x] Define Open Source guidelines (Contributing, Code of conduct, Issue Template, PR Template).
* [ ] (API) Describe the API that will be used by the Tartiflette users.
  * [x] (API) [Engine constructor](https://github.com/dailymotion/tartiflette/blob/master/docs/API.md#engine-initialization) - _[#19](https://github.com/dailymotion/tartiflette/issues/19)_.
  * [ ] (API) How to declare custom directives in the Engine Constructor.
  * [ ] (API) How to declare middleware on a resolver.
  * [ ] (API) Executor.
  * [x] (API) Resolver - _[#19](https://github.com/dailymotion/tartiflette/issues/19)_.
  * [x] (API) Resolver - `Info` parameter - _[#19](https://github.com/dailymotion/tartiflette/issues/19)_.
* [ ] (Website) Landing page for https://tartiflette.io
* [ ] (Website) Expose documentation on https://tartiflette.io
### Query Parser

* [x] Build communication interface between [libgraphqlparser](https://github.com/graphql/libgraphqlparser) & Tartiflette through [CFFI](https://cffi.readthedocs.io).
* [x] Build a `Parser` which parses a GraphQL Query and creates a list of Asynchronous Tasks.
* [x] Build an `Executor` which executes the Asynchronous Tasks list created by the `Parser`.

### Executor

* [x] Bind the Types specified in the SDL to the `Executor`.
* [x] Typing [resolver outputs](https://github.com/dailymotion/tartiflette/blob/master/tartiflette/parser/visitor.py#L191) - _[#17 - In progress](https://github.com/dailymotion/tartiflette/issues/17)_
* [x] Error management
* [ ] Abstract and Compound Types: Unions, Interfaces, …
* [ ] NodeDefinition: Check that the [Type exists](https://github.com/dailymotion/tartiflette/blob/master/tartiflette/parser/nodes/definition.py#L26)
* [x] (Resolver) Think how to apply [a default resolver](https://github.com/dailymotion/tartiflette/blob/master/tartiflette/parser/visitor.py#L18) to a field.
* [ ] (Directive) Integrate the directive's execution in the Executor.
* [ ] Integrate the middleware in the Executor.

### SDL - Schema Definition Language

* [x] Build a `Parser` which parse the [Schema Definition Language](https://github.com/facebook/graphql/blob/master/spec/Section%202%20--%20Language.md) and created the associated schema and types as Python objects.
* [ ] Think about custom Scalar API
* [x] (Introspection) Implement the `__type` Field. - [_[#15 - In progress](https://github.com/dailymotion/tartiflette/issues/15)_
* [x] (Introspection) Implement the `__schema`Field. - [_[#16 - In progress](https://github.com/dailymotion/tartiflette/issues/16)_
* [ ] (Directive) Append directive informations _(from SDL)_ as metadata on Fields / Types.
* [ ] (Directive) Implement the declaration of the custom directives into the Engine constructor.
* [ ] (Directive) Implement @deprecated

### Continuous integration

* [ ] Run Code Quality checks + Tests
* [ ] Automatize the integration of `libgraphqlparser`
* [ ] Build & Publish artifact to pypi

## Roadmap - Milestone #2

* [ ] Implement **[Apollo Cache Control](https://github.com/apollographql/apollo-cache-control)**
* [ ] Implement dynamic introspection based on directive
* [ ] Think about `subscriptions`
