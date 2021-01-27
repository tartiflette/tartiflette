# [Next]

## Added

- Built-in introspection directive `@nonIntrospectable` now supports SCHEMA object decoration.
```
schema @nonIntrospectable {
    ...
}
```

## Fixed

- [ISSUE-453](https://github.com/tartiflette/tartiflette/issues/453) - Exceptions in schema directive are now handled
