# [Next]

## Added

- [ISSUE-363](https://github.com/dailymotion/tartiflette/issues/363) - Add an optional `query_cache_decorator` argument at engine initialisation allowing to forward a custom decorator to use to cache query parsing.
- [ISSUE-362](https://github.com/dailymotion/tartiflette/issues/362) - Add an optional `json_loader` argument to engine creation APIs so json loader can be customized.
- [ISSUE-361](https://github.com/dailymotion/tartiflette/issues/361) - Add an optional `custom_default_arguments_coercer` argument at engine initialisation to override the callable used to coerce arguments.
- [ISSUE-361](https://github.com/dailymotion/tartiflette/issues/361) - Add an optional `arguments_coercer` to `@Directive`, `@Subscription` & `@Resolver` decorator to override the callable used to coerce arguments on the decorated directive/field.

## Changed

- [ISSUE-356](https://github.com/dailymotion/tartiflette/issues/362) - Removed dependancies on `flex` and `bison` for installing Tartiflette. `cmake` is still necessary.
- [ISSUE-361](https://github.com/dailymotion/tartiflette/issues/361) - Coerce lists (input, literal, output) synchronously to avoid creation of too many `asyncio` tasks.

## Fixed
