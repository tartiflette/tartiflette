---
id: error-handling
title: Error handling
sidebar_label: Error handling
---

Tartiflette engine provides an unique `TartifletteError` class, which is designed to format errors accordingly to the GraphQL specification.

When an error occurs from both Tartiflette engine and your resolvers, it is formated to respect the regular [GraphQL error shape](https://graphql.github.io/graphql-spec/June2018/#sec-Errors).

```json
{
  "data": {
    "myField": null
  },
  "errors": [
    {
      "message": "Something wrong happened.",
      "path": ["myField"],
      "locations": [
        {
          "line": 1,
          "column": 2
        }
      ]
    }
  ]
}
```

## Default use-case

Commonly, each exception is wrapped into a `TartifletteError` exception, the message is copied, and the original exception is stored into the `TartifletteError` instance into the `original_error` property.

In that use-case, there is no way to specify custom properties.

E.g:
```python
from tartiflette import Resolver


@Resolver("Query.myField")
async def resolve_query_my_field(parent, args, ctx, info):
    raise Exception("There is an error with your storage.")
```

Will return this response payload:
```json
{
  "data": {
    "myField": null
  },
  "errors": [
    {
      "message": "There is an error with your storage.",
      "path": ["myField"],
      "locations": [
        {
          "line": 1,
          "column": 2
        }
      ]
    }
  ]
}
```

## Add custom properties to the response payload

In some use-cases, like form's validation, functional error, you want to expose more fine-grained details to your API's clients. These details allow them to adapt their UI on your custom properties.

[As explained in the specification](https://graphql.github.io/graphql-spec/June2018/#sec-Errors), this is possible to add extra properties to the response error payload. They have to be included into the `extensions` property of your error.

To enjoy this interesting feature, you have to create your own exception and fullfill the `extensions` property.

```python
from tartiflette import TartifletteError, Resolver


class DomainException(TartifletteError):
    """Base class for Domain exception."""
    def __init__(self, type_name, message):
        super().__init__(message)
        self.extensions = {
            "code": type_name
        }


@Resolver("Query.myField")
async def resolve_query_my_field(parent, args, ctx, info):
    raise DomainException("invalid_request", "Your request is not valid.")
```

The response payload will be:
```json
{
  "data": {
    "myField": null,
  },
  "errors": [
    {
      "message": "Your request is not valid.",
      "path": ["myField"],
      "locations": [
        {
          "line": 1,
          "column": 2
        }
      ],
      "extensions": {
        "code": "invalid_request"
      }
    }
  ]
}
```

## Advanced: add a global error coercer

**Warning**: This is an advanced feature, for common error handling behaviors, please take a look at the `TartifletteError` above.

Every errors are coerced with a default behavior _(the exception message is put in the `message` response property)_.

This behavior fit the common use-cases, sometimes, you want to override some behavior when a specific error occured, like:
* add a log entry when a third-party exceptions is raised _(e.g `pymsql`, `redis`)_.
* hide technical message's exception for production environment _(don't expose your internal stack to the outside world)_

To implement this, Tartiflette engine allows you to override the default coercer by yours. It should be passed at the engine instanciation in the `error_coercer` parameter, and respect this following signature `my_error_coercer(exception: Exception, error: Dict[str, Any]) -> Dict[str, Any]` and should be `async`.


Here is an example of a custom error coercer:
```python
import logging

from typing import Any, Callable, Dict, List, Optional, Union

from tartiflette import create_engine


class CustomException(Exception):
    def __init__(self, type_name, message):
        self.type = type_name
        self.message = message


async def my_error_coercer(
    exception: Exception, error: Dict[str, Any]
) -> Dict[str, Any]:
    if isinstance(exception, CustomException):
        logging.error("Unable to reach the Storage host.")
        error["extensions"]["type"] = exception.type
    return error


engine = await create_engine(
    "my_sdl.graphql",
    error_coercer=my_error_coercer,
)
```
