# Tartiflette Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- [PR-155](https://github.com/dailymotion/tartiflette/pull/155): Add support for `extensions` field in GraphQLError exceptions and allow importing exceptions more easily.

## [Released]

## [0.6.5] - 2019-03-12

### Changed

- It is no more possible to pass an instance of GraphQLSchema to the Engine Constructor.
- Introspection code moved into the schema submodule.
- Introspection no longer return __ starting fields data

## [0.6.4] - 2019-03-11

### Fixed

- Apply directives on sub-levels arguments.


## [0.6.3] - 2019-03-07

### Fixed

- [ISSUE-143](https://github.com/dailymotion/tartiflette/issues/143): Fix regression in on_introspection directive method call

## [0.6.2] - 2019-03-07

### Added

- [ISSUE-140](https://github.com/dailymotion/tartiflette/issues/140): A new parameter in Engine() constructor, you can now specify a list of modules containing your decorated code such as:

  1. Resolver
  2. Subscription
  3. Mutation
  4. Scalar
  5. Directive

  IE:

  ```python
  Engine = Engine(a_sdl, modules=["some.module", "another.module", "oh.another.module"])
  ```

## [0.6.1] - 2019-03-05

### Changed

- Add docstring and remove `_` prefix on unused parameter on public API.
- Clean some unused stuff.

## [0.6.0] - 2019-03-04

### Added

- [ISSUE-133](https://github.com/dailymotion/tartiflette/issues/133): Add an `on_argument_execution` directive method to handle argument directive hook.

### Changed

- Rename `on_execution` directive method name to `on_execution_field`.

### Fixed

- Properly set `directives` to `GraphQLArgument` at bake time.

## [0.5.1] - 2019-03-04

### Fixed

- [ISSUE-127](https://github.com/dailymotion/tartiflette/issues/127): Now Object and List are supported as input values for arguments

>Note: This patch doesn't include validation of theses Values (yet), this will be done in a more global PR about Document Validation that is coming soon [ISSUE-121](https://github.com/dailymotion/tartiflette/issues/121)

## [0.5.0] - 2019-03-01

### Added

- Pass `ctx` & `info` as argument to `on_introspection` directive's method.

## [0.4.2] - 2019-03-01

### Fixed

- [ISSUE-126](https://github.com/dailymotion/tartiflette/issues/126): Now, child of a None result are no more executed

## [0.4.1] - 2019-02-27

### Fixed

- [ISSUE-128](https://github.com/dailymotion/tartiflette/issues/128): Use a specific default resolver for subscription which doesn't implement a dedicated resolver.

## [0.4.0] - 2019-02-25

### Added

- [ISSUE-113](https://github.com/dailymotion/tartiflette/issues/113) Handle subscriptions as async generator.

### Fixed

- [ISSUE-119](https://github.com/dailymotion/tartiflette/issues/119): Add an `initial_value` parameter on the `execute`'s engine method.

## [0.3.7] - 2019-02-06

### Fixed

- [ISSUE-99](https://github.com/dailymotion/tartiflette/issues/99): Raise errors on non unique arguments on fields or directives.
- [ISSUE-114](https://github.com/dailymotion/tartiflette/issues/114): Execute only the specified operation or throw on error if not exists.
- [ISSUE-117](https://github.com/dailymotion/tartiflette/issues/117): Execute top-level mutation selection set serially.

## [0.3.6] - 2019-01-30

### Fixed

- [ISSUE-109](https://github.com/dailymotion/tartiflette/issues/109): Manage SelectionSet errors on leaf/non-leaf field.

## [0.3.5] - 2019-01-30

### Changed

- Add type hints & some refactoring / code cleaning.

### Fixed

- [ISSUE-108](https://github.com/dailymotion/tartiflette/issues/108): Understand .graphql files as SDL ones

### [0.3.4] - 2019-01-25

### Fixed

- [ISSUE-97](https://github.com/dailymotion/tartiflette/issues/97): Raise errors on undefined arguments on nodes or directives.
- [ISSUE-103](https://github.com/dailymotion/tartiflette/issues/103): Process enum values.
- [ISSUE-105](https://github.com/dailymotion/tartiflette/issues/105): Process fragment spreading properly.
- [ISSUE-101](https://github.com/dailymotion/tartiflette/issues/101): Raise errors on missing required argument on field / directive.

### [0.3.3] - 2019-01-21

#### Added

- Add import sorting on style rule.
- Add formating on tests.
- Add link to tartiflette-aiohttp in readme.
- Add a `ttftt_engine` pytest marker to improve the way we handle functional tests.

### Fixed

- [ISSUE-85](https://github.com/dailymotion/tartiflette/issues/85): Raise errors on non-unique named operation definition.
- [ISSUE-86](https://github.com/dailymotion/tartiflette/issues/86): Raise errors on not alone anonymous operation.
- [ISSUE-87](https://github.com/dailymotion/tartiflette/issues/87): Raise errors on subscription operations with multiple root field.
- [ISSUE-94](https://github.com/dailymotion/tartiflette/issues/94): Raise errors when redefining directives, scalars or resolvers multiple times.
- [ISSUE-92](https://github.com/dailymotion/tartiflette/issues/92): Official Introspection Query support.
  - Unordered Fragments support
  - Don't fail on type that doesn't have fields
  - Support `possibleTypes` on Union
  - Support `interfaces` on Object
  - Support `inputFields` on InputValue

#### Removed

- Remove aiohttp example files

### [0.3.2] - 2019-01-15

#### Fixed

- [ISSUE-79](https://github.com/dailymotion/tartiflette/issues/79): Raise errors when fragment target unknown type.
- [ISSUE-80](https://github.com/dailymotion/tartiflette/issues/80): Raise errors when defined fragment isn't used.
- [ISSUE-82](https://github.com/dailymotion/tartiflette/issues/82): Raise errors when undefined fragment is used.
- [ISSUE-76](https://github.com/dailymotion/tartiflette/issues/76): Path is correctly set on "Unknow field" errors.

### [0.3.1] - 2019-01-15

#### Fixed

- Really fixes Issue-70, previous 0.3.0 was 'too permissive' in fragment execution code.

### [0.3.0] - 2019-01-14

#### Added

- Allows to handle custom exception errors.
- Coerce exception raised during query parsing instead of throwing them:

```python
class BadRequestError(Exception):
    def coerce_value(self, *_args, path=None, locations=None, **_kwargs):
        return your_coerced_error


@Resolver("Query.hello")
async def resolver_hello(parent, args, ctx, info):
    if args["name"] == "":
        raise BadRequestError("`name` argument shouldn't by empty.")
    return "hello " + args["name"]
```

- Enable you to override the `default_error_coercer` at Engine initialization time:

```python
def my_error_coercer(exception) -> dict:
    do_ing_some_thin_gs = 42
    return a_value

e = Engine("my_sdl.sdl", error_coercer=my_error_coercer)
```

- Adds manually path & locations attributes to the `UnknownSchemaFieldResolver` raised exception.
- Returns all encountered errors during query parsing instead of only the last one.
- _typename tartiflette attribute is now automatically set by coercion except inside union type where it is deduce at execution time.

#### Changed

- Makes raised exceptions inherits from `GraphQLError`.

#### Fixed

- Parse raw GraphQL query in order to have the correct locations on raised errors.
- Avoid `TypeError` by re-raising `UnknownSchemaFieldResolver` or casting `_inline_fragment_type` to string.
- Raise `GraphQLError` instead of builtin exceptions.
- [ISSUE-70](https://github.com/dailymotion/tartiflette/issues/70): Now Typecondition is correctly unset for nested fields inside a fragment.
- [ISSUE-71](https://github.com/dailymotion/tartiflette/issues/71): Now libgraphqlparser parsing errors only lives for the duration of the request.

### [0.2.2] - 2019-01-04

#### Added

- Enable you to exclude builtins scalars at Engine initialization time with `exclude_builtins_scalars` parameter.
- Publish package to Test PyPi on each working branch.

```python
e = Engine("my_sdl.sdl", exclude_builtins_scalars=["Date", "DateTime"])
```

### [0.2.1] - 2018-12-27

#### Added

- Enable you to override the `default_resolver` at Engine initialization time.

```python

async def my_default_resolver(parent_result, arguments, context, info):
    do_ing_some_thin_gs = 42
    return a_value

e = Engine("my_sdl.sdl", custom_default_resolver=my_default_resolver)

```

#### Removed

- Dependancy to `python-rapidjson`, `uvloop`, `cython`.

#### Fixed

- Default values for arguments setted in SDL where ignored, now they aren't anymore.

### [0.2.0] - 2018-12-06

#### Changed

- Drop plural of `Engine` `sdls` constructor parameter.
  Went from :

  ```python
  class Engine():
      def __init__(sdls, ....):
  ```

  to

  ```python
  class Engine():
      def __init__(sdl, ...):
  ```

### [0.1.9] - 2018-11-16

#### Added

- Support for `__typename` meta field

### [0.1.8] - 2018-11-15

#### Added

- Support for Union and TypeCondition filtering

#### Changed

Now a resolver of a union type should explicitly define the value of `_typename` on it's return value.

- If the resolver wants to return a `dict` a `_typename` key must be present.
- If the resolver wants to return an `object` (a class instance), a `_typename` attribute should be present.
- If none of the above are present the execution engine infer `_typename` from the class name of the object returned by the resolver.

I.E.

```python
def get_typename(resolver_result):
    try:
        return resolver_result["_typename"]
    except (KeyError, TypeError):
        pass

    try:
        return resolver_result._typename
    except AttributeError:
        pass

    return resolver_result.__class__.__name__
```

#### Fixed

- Change the way README.md is read in setup.py for long_description, now file is closed after reading.

### [0.1.7] - 2018-11-12

#### Added

- (Query) Support Alias in Query and Mutation

### [0.1.6] - 2018-10-31

#### Added

- (CI) Integrate missing Grammar

#### Fixed

- Retrieve the appropriate operation type with operation definition.
- (SDL) Remove useless type and add Line/Col info propagation
- Add missing "UnknownDirectiveDefinition" imports

### [0.1.5] - 2018-10-11

#### Added

- (CI) Integrate missing Grammar

### [0.1.4] - 2018-10-09

#### Added

- (SDL / Executor) Implement declaration and execution of custom directives
- (SDL) Implement Interfaces
- (SDL) Implement Scalar Types
- (SDL) Implement directive `@Deprecated`
- (Executor) Implement Introspection and Dynamic intropection _(Documentation needed)_

#### Changed

- Executor engine

## [Unreleased]

### [0.1.0] - 2018-01-26

#### Added

- README.md & LICENSE
