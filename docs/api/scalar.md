---
id: scalar
title: Scalar
sidebar_label: Scalar
---

Tartiflette allows you to use your own `scalar` and even redefine the behavior of the built-in ones.
Your `scalar` will have to declare 3 methods `parse_literal`, `coerce_input` and `coerce_output`.

Signatures of those methods should follow:
* `parse_literal`:
    ```python
    def parse_literal(self, ast: "ValueNode") -> Union[Any, UNDEFINED_VALUE]:
    ```
* `coerce_input`:
    ```python
    def coerce_input(self, value: Any) -> str:
    ```
* `coerce_output`:
    ```python
    def coerce_output(self, value: Any) -> Any
    ```

### parse_literal

This method will be used to translate a literal value provided in the query/SDL into its Python representation.

> Notes: literal values are all values which are "hard coded" into a query/SDL such as argument value, default values...

### coerce_input

This method will be used to translate a variable value provided by the client into its Python representation.

### coerce_output

This method will be used to translate a resolved field value into its final response result.

This method should returns a JSON serializable value.

## How to declare a new scalar

In this example we will declare a new scalar that will transform "anystring" into "Anystring" and back.

```graphql
scalar CapitalizedString

type Query {
  hello: CapitalizedString
}
```

```python
from typing import Any, Union

from tartiflette import Scalar
from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import StringValueNode


@Scalar("CapitalizedString")
class ScalarCapitalizedString:
    def coerce_output(self, value: Any) -> str:
        # Here `val` is what is returned by the resolver of a field having for type this scalar.
        # This method is expected to return a value that serializable, that will be returned to the caller.
        return str(value).lower()

    def coerce_input(self, value: Any) -> str:
        # Argument value from the query are passed here in the `val` parameter.
        # This method is expected to return the value transformed into something usable by your code
        if not isinstance(value, str):
            raise TypeError(
                f"String cannot represent a non string value: < {value} >"
            )
        return value.capitalized()

    def parse_literal(self, ast: "valueNode") -> Union[str, "UNDEFINED_VALUE"]:
        if isinstance(ast, StringValueNode):
            return ast.value.capitalized()
        return UNDEFINED_VALUE
```

## Built-in scalars

- **ID**
- **Int**
- **String**
- **Float**
- **Boolean**
- **Date**
- **Time**
- **DateTime**

You can redefine them at engine initialization time like:

```graphql
scalar Int

type Query {
  hello: Int
}
```

```python
from typing import Any, Callable, Dict, Optional

from tartiflette import Scalar, create_engine


@Scalar("Int")
class ScalarInt:
    def coerce_output(self, value: Any) -> int:
        # Do what you want here
        pass

    def coerce_input(self, value: Any) -> int:
        # Do what you want here
        pass

    def parse_literal(self, ast: "valueNode") -> Union[int, "UNDEFINED_VALUE"]:
        # Do what you want here
        pass

engine = await create_engine("Your SDL...")
```

During the build process of the engine, Tartiflette will automaticaly detect that your code has its own implementation of a built-in scalar. It will replace its own implementation by yours.
