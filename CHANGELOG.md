# Tartiflette Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Publish package to Test PyPi on each working branch.

## [Release]

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
