---
id: resolver
title: Resolver
sidebar_label: Resolver
---

The most common way to assign a specific resolver to a Field, is to decorate your resolver function with the `@Resolver` decorator. Your function [MUST BE compliant with the function signature](#function-signature) and be `async`.

```python
from tartiflette import Resolver

@Resolver("Query.hello")
async def my_hello_resolver(parent, args, context, info):
    return "Chuck"
```

## Function signature

Every resolver in Tartiflette accepts four positional arguments:

_(This signature has been highly inspired by the GraphQL.js implementation)_

```python
async def my_hello_resolver(parent, args, context, info):
    pass
```

1. **parent:** The result returned by the resolver of the parent field. The `initial_value` of the execution is passed in the case of a top-level Query field.
2. **args:** A dict which contains the arguments passed for the field. _(in the query)_. e.g. if the field was called with `hello(name: "Chuck")`, the args dict will be equals to `{ "name": "Chuck" }`.
3. **context:** Dict shared by all resolvers, that can be different for each query. It acts as a container or a state for a specific request.
4. **info:** This argument CAN BE used for advanced use-cases; but it contains information about the execution state of the query.

### Resolver `info` argument

The `info` argument contains the query's AST _(Abstract Syntax Tree)_ and other execution details, which can be useful for middlewares and advanced use-cases.

Here are the available properties:

- `query_field` tartiflette.parser.NodeField - Contains the information of the field from the query's perspective.
- `schema_field` tartiflette.types.field.GraphQLField - Contains the information of the field from the schema's perspective (type, default values, and more.)
- `schema` tartiflette.schema.GraphQLSchema - Contains the GraphQL's server complete schema instance.
- `path` List[string] - Describes the path in the current query
- `location` tartiflette.types.location.Location - Describes the location in the query
- `execution_ctx` tartiflette.executor.types.ExecutionContext - Contains execution values (like `errors`).
