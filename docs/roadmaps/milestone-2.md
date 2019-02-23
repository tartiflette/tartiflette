# Roadmap: Version 2

- [Roadmap: Version 2](#roadmap-version-2)
  - [Communication and documentation](#communication-and-documentation)
  - [Directives](#directives)
  - [Executor](#executor)
  - [Continuous integration](#continuous-integration)

These topics list is not frozen, we will iterate on them to improve Tartiflette to be more and more performant and compliant with the specification.

## Communication and documentation

* [ ] Provide code samples about the Subscription over Redis, Nats, Google Pub/Sub.
* [ ] Provide code samples about advanced use-cases of Directives (introspection, on build etc ...)

## Directives

* [ ] Provide built-ins or externals directives to extend the capabilities of Tartiflette (e.g @maxLength)
* [ ] Provide built-in directives to handle the Relay specification.

## Executor

* [ ] [Improve and simplify query parsing and validation](https://github.com/dailymotion/tartiflette/issues/121)
* [ ] [Improve type resolving #122](https://github.com/dailymotion/tartiflette/issues/122)

## Continuous integration

* [ ] Provide official docker images for tartiflette-aiohttp