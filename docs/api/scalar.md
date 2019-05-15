---
id: scalar
title: Scalar
sidebar_label: Scalar
---

Tartiflette allows you to use your own `scalar` and even redefine the behavior of the built-in ones.
Your `scalar` will have to declare 2 methods `coerce_input` and `coerce_output`.

- **coerce_input(val:Any)->Any**
- **coerce_output(val:Any)->Any**

This 2 methods are what we call `coercers`.

### coerce_input

This method will be used to translate the resolver inputs.

This method should return something that will be usefull to your resolver.

> called when the `scalar` is used as type for an `argument` (or is inside an `input object`).

### coerce_output

This method will be used to translate resolver outputs.

This method shoud return something that is JSON serializable.

> called when the `scalar` is used as a type for `field`.

## How to declare a new scalar

In this example we will declare a new scalar that will transform "anystring" into "Anystring" and back.

```graphql
scalar CapitalizedString

type Query {
  hello: CapitalizedString
}
```

```python
from typing import Any, Callable, Dict, Optional

from tartiflette import Scalar


@Scalar("CapitalizedString")
class CapitalizedString:
    @staticmethod
    def coerce_input(val):
        # Argument value from the query are passed here in the `val` parameter.
        # This method is expected to return the value transformed into something usable by your code
        return val.capitalized()

    @staticmethod
    def coerce_output(val):
        # Here `val` is what is returned by the resolver of a field having for type this scalar.
        # This method is expected to return a value that serializable, that will be returned to the caller.
        return val.lower()
```

## Built-in Scalars

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

from tartiflette import Scalar

@Scalar("Int")
class ScalarInt:
    @staticmethod
    def coerce_input(val):
        # Do what you want
        return val

    @staticmethod
    def coerce_output(val):
        # Do what you want
        return val


engine = Engine(the_sdl, exclude_builtins_scalars=["Int"])
```

Then the engine will use your own version of the `Integer Scalar`.
