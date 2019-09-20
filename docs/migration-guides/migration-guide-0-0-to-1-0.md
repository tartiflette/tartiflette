---
id: migration-guide-0-0-to-1-0
title: Moving from v0.x.x to v1.0.x
sidebar_label: Moving from v0.x.x to v1.0.x
---

# Migration Guide: Moving from v0.x.x to v1.0.x

## Miscellaneous

### `engine_coercer` has to be asynchronous

The [`error_coercer`](../api/error-handling.md#advanced-add-a-global-error-coercer) parameter now expects an asynchronous function instead of a synchronous function.

If you are using this advanced feature in your project you have to convert your synchronous function into an asynchronous one in order to make your project compliant with Tartiflette `v1.x.x`.

Taking in example the following error coercer:
```python
from typing import Dict, Any


class MyCustomException(Exception):
    pass


def my_error_coercer(
    exception: Exception, error: Dict[str, Any]
) -> Dict[str, Any]:
    if isinstance(exception, MyCustomException):
        error["extensions"]["type"] = "custom_exception"
    return error
```

You just have to convert the function as an asynchronous one:
```patch
-def my_error_coercer(
+async def my_error_coercer(
```

### Strong distinction between non-supplied values and `null` values

We now make a strong distinction between non-supplied values and `null` values. This is to avoid passing `null` value when a value has not been supplied (especially for arguments). This modification can have an impact on your resolvers and directives hooks implementations.

Taking in example the following SDL:
```graphql
type News {
  id: Int!
  title: String!
  resume: String
  content: String!
}

input AddNewsInput {
  title: String!
  resume: String
  content: String!
}

type Mutation {
  addNews(input: AddNewsInput!): News!
}
```

With the following resolver implementation:
```python
from tartiflette import Resolver


def insert_news_to_db(args):
    # Write your business logic here
    return 1


@Resolver("Mutation.addNews")
async def resolve_mutation_add_news(parent, args, ctx, info):
    news_id = insert_news_to_db(args)
    return {
        "id": news_id,
        "title": args["input"]["title"],
        "resume": args["input"]["resume"],
        "content": args["input"]["content"],
    }
```

With the following GraphQL request:
```graphql
mutation {
  addNews(input: {title: "Title", content: "Content"}) {
    id
    title
    resume
    content
  }
}
```

In Tartiflette `v1.0.0`, a `KeyError` exception will be raised in the `resolve_mutation_add_news` function since `resume` input field hasn't been supplied, meaning the key isn't present in the `args["input"]` dictionnary.

This is the patch of the `args` dictionary content between `v0.x.x` and `v1.x.x` for the previous request:
```patch
-{"input": {"title": "Title", "resume": None, "content": "Content"}}
+{"input": {"title": "Title", "content": "Content"}}
```

This means that if you were used to "hard" access your arguments (especially the nullable ones) you should be careful to your resolvers and directive hooks implementations. The same way, previously you couldn't trust the `None` value you could encouter on your `args` values. Now, you can trust them. If you have a `None` value on one of your arguments, that means it has been filled in by the user as `null` in the request.

For instance, if we make this request:
```graphql
mutation {
  addNews(input: {title: "Title", content: "Content"}) {
    id
    title
    resume
    content
  }
}
```

You'll have `{"input": {"title": "Title", "resume": None, "content": "Content"}}` as `args` value in both `v0.x.x` and `v1.x.x` versions.

This behaviour follow the [June 2018 GraphQL specification](https://graphql.github.io/graphql-spec/June2018/) as describe in the **Input Coercion** part of **[Scalars](https://graphql.github.io/graphql-spec/June2018/#sec-Scalars)** specification:
> For all types below, with the exception of Non‐Null, if the explicit value null is provided, then the result of input coercion is null.

### Subscriptions no longer have a specific default resolver

The `@Subscription` decorator no longer has its specific default resolver. This means that the messages returned by `@Subscription` will no longer be wrapped with the field name as before (when the field doesn't have a dedicated `@Resolver`).

On older versions, subscriptions had a specific default resolver aimaing to automatically wrap the result of each message comming from the subscription in a dictionnary such as: `{field_name: message}`. This behaviour wasn't compliant with the GraphQL specification and has been removed.

However, this occurs only of subscriptions which hasn't a dedicated `@Resolver`. If you have some subscriptions implemented which have also a `@Resolver` this will not have any impact for you. If not, follow the following steps.

Taking in example the following SDL:
```graphql
enum CookingStatus {
  COOKING
  COOKED
}

type CookingTimer {
  remainingTime: Int!
  status: CookingStatus!
}

type Subscription {
  launchAndWaitCookingTimer(id: Int!): CookingTimer
}
```

With the following subscription implementation:
```python
from tartiflette import Subscription


@Subscription("Subscription.launchAndWaitCookingTimer")
async def subscribe_subscription_launch_and_wait_cooking_timer(
    parent, args, ctx, info
):
    yield {"remainingTime": 0, "status": "COOKED"}
```

You just have to wrap the returned messages into the field name by yourself:
```patch
-   yield {"remainingTime": 0, "status": "COOKED"}
+   yield {"launchAndWaitCookingTimer": {"remainingTime": 0, "status": "COOKED"}}
```

This modification has been made to be compliant with the [June 2018 GraphQL specification](https://graphql.github.io/graphql-spec/June2018/) and the [`Subscribe`](https://graphql.github.io/graphql-spec/June2018/#Subscribe()) algorithm.

### The shape of the `info` parameter has changed

The shape of the [`info`](../api/resolver.md#resolver-info-argument) parameter accessible in particular in the resolvers and some hooks of directives has been completely changed:

```python
class Info:
    def __init__(
        self,
        query_field: "NodeField",
        schema_field: "GraphQLField",
        schema: "GraphQLSchema",
        path: List[str],
        location: "Location",
        execution_ctx: ExecutionContext,
    ) -> None:
        self.query_field = query_field
        self.schema_field = schema_field
        self.schema = schema
        self.path = path
        self.location = location
        self.execution_ctx = execution_ctx
```

```patch
-class Info:
+class ResolveInfo:
    def __init__(
        self,
-       query_field: "NodeField",
-       schema_field: "GraphQLField",
-       schema: "GraphQLSchema",
-       path: List[str],
-       location: "Location",
-       execution_ctx: ExecutionContext,
+       field_name: str,
+       field_nodes: List["FieldNodes"],
+       return_type: "GraphQLOutputType",
+       parent_type: "GraphQLObjectType",
+       path: "Path",
+       schema: "GraphQLSchema",
+       fragments: Dict[str, "FragmentDefinitionNode"],
+       root_value: Optional[Any],
+       operation: "OperationDefinitionNode",
+       variable_values: Optional[Dict[str, Any]],
+       is_introspection_context: bool,
    ) -> None:
```

## Directives

The signature of some directive hooks has been changed:
* [`on_argument_execution`](#on_argument_execution)
* [`on_post_input_coercion`](#on_argument_execution)
* [`on_pre_output_coercion`](#on_pre_output_coercion)

### `on_argument_execution`

Taking in example the following directive implementing the `on_argument_execution` hook directive:
```python
from typing import Dict, Any, Callable, Optional

from tartiflette import Directive


@Directive("MyDirective")
class MyDirective:
    async def on_argument_execution(
        self,
        directive_args: Dict[str, Any],
        next_directive: Callable,
        argument_definition: "GraphQLArgument",
        args: Dict[str, Any],
        ctx: Optional[Any],
        info: "Info",
    ) -> Any:
        # Write your business logic here
        return next_directive(argument_definition, args, ctx, info)
```

In order to make this hook directive implementation compatible with Tartiflette `v1.x.x`, please follow the following `patch`:
```patch
@Directive("MyDirective")
class MyDirective:
    async def on_argument_execution(
        self,
        directive_args: Dict[str, Any],
        next_directive: Callable,
-       argument_definition: "GraphQLArgument",
-       args: Dict[str, Any],
-       ctx: Optional[Any],
-       info: "Info",
+       parent_node: Union["FieldNode", "DirectiveNode"],
+       argument_node: "ArgumentNode",
+       value: Any,
+       ctx: Optional[Any],
    ) -> Any:
        # Write your business logic here
-       return next_directive(argument_definition, args, ctx, info)
+       return next_directive(parent_node, argument_node, value, ctx)
```

### `on_post_input_coercion`

Taking in example the following directive implementing the `on_post_input_coercion` hook directive:
```python
from typing import Dict, Any, Callable, Optional

from tartiflette import Directive


@Directive("MyDirective")
class MyDirective:
    async def on_post_input_coercion(
        self,
        directive_args: Dict[str, Any],
        next_directive: Callable,
        value: Any,
        argument_definition: "GraphQLArgument",
        ctx: Optional[Any],
        info: "Info",
    ) -> Any:
        # Write your business logic here
        return next_directive(value, argument_definition, ctx, info)
```

In order to make this hook directive implementation compatible with Tartiflette `v1.x.x`, please follow the following `patch`:
```patch
@Directive("MyDirective")
class MyDirective:
    async def on_post_input_coercion(
        self,
        directive_args: Dict[str, Any],
        next_directive: Callable,
-       value: Any,
-       argument_definition: "GraphQLArgument",
-       ctx: Optional[Any],
-       info: "Info",
+       parent_node: Union["VariableDefinitionNode", "InputValueDefinitionNode"],
+       value: Any,
+       ctx: Optional[Any],
    ) -> Any:
        # Write your business logic here
-       return next_directive(value, argument_definition, ctx, info)
+       return next_directive(parent_node, value, ctx)
```

### `on_pre_output_coercion`

Taking in example the following directive implementing the `on_pre_output_coercion` hook directive:
```python
from typing import Dict, Any, Callable, Optional

from tartiflette import Directive


@Directive("MyDirective")
class MyDirective:
    async def on_pre_output_coercion(
        self,
        directive_args: Dict[str, Any],
        next_directive: Callable,
        value: Any,
        field_definition: "GraphQLField",
        ctx: Optional[Any],
        info: "Info",
    ) -> Any:
        # Write your business logic here
        return next_directive(value, field_definition, ctx, info)

```

In order to make this hook directive implementation compatible with Tartiflette `v1.x.x`, please follow the following `patch`:
```patch
@Directive("MyDirective")
class MyDirective:
    async def on_pre_output_coercion(
        self,
        directive_args: Dict[str, Any],
        next_directive: Callable,
        value: Any,
-       field_definition: "GraphQLField",
        ctx: Optional[Any],
-       info: "Info",
+       info: "ResolveInfo",
    ) -> Any:
        # Write your business logic here
-       return next_directive(value, field_definition, ctx, info)
+       return next_directive(value, ctx, info)
```

## Scalar definitions

Scalar definition now requires the implementation of a third `parse_literal` method.

Taking in example the following scalar definition:
```python
from typing import Any, Union

from tartiflette import Scalar
from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import StringValueNode


@Scalar("String")
class ScalarString:
    def coerce_output(self, value: Any) -> str:
        return str(value)

    def coerce_input(self, value: Any) -> str:
        if not isinstance(value, str):
            raise TypeError(
                f"String cannot represent a non string value: < {value} >."
            )
        return value
```

From Tartiflette `v1.x.x`, we have split the input coercion in two methods. Variables values are coerced through the `coerce_input` method, while literal values (value from the query itself) are coerced through the new `parse_literal` method.

So, the aim of the `parse_literal` method is to coerce an `ast` node into a Python value.

In order to make this hook directive implementation compatible with Tartiflette `v1.x.x`, you have to implements a third `parse_literal` method which follow this method signature:
```python
def parse_literal(self, ast: "Node") -> Union[str, "UNDEFINED_VALUE"]:
```

In our example, the `parse_literal` method would look like this:
```python
def parse_literal(self, ast: "Node") -> Union[str, "UNDEFINED_VALUE"]:
    if isinstance(ast, StringValueNode)
        return ast.value
    return UNDEFINED_VALUE
```
