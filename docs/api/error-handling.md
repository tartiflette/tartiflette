---
id: error-handling
title: Error handling
sidebar_label: Error handling
---

Tartiflette Engine provides an unique `TartifletteError` class, which is designed to format errors accordingly to the GraphQL specification.

When an error occurs from both tartiflette engine and your resolvers, it is formated to respect the regular GraphQL Error shape.

```json
{
    "data": {
        "myField": {}
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

Commonly, each exception is wrapped into a `TartifletteError` exception, the message is copied, and the original exception is stored into theinstance is put into the `original_error` property.

In that use-case, there is no way to specify custom properties.

e.g

```python
from tartiflette import Resolver

@Resolver("Query.myField")
async def resolve_my_field(parent, args, ctx, info):
    # bla bla bla
    raise Exception("There is an error with your storage")

```

Will return this response payload.


```json
{
    "data": {
        "myField": {}
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

## Add custom properties to the response payload

In some use-cases, like form's validation, functional error, you want to expose more fine-grained details to your API's clients. These details allow them to adapt their UI on your custom attributes. 

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
async def resolve_my_field(parent, args, ctx, info):
    raise DomainException("invalid_request", "Your request is not valid.")

```

The response payload will be.

```json
{
    "data": {
        "myField": {}
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

**Warning**: This is an advanced feature, for common error handling behaviors, please take a look of the `TartifletteError` above.

Every errors are coerced with a default behavior _(the exception message is put in the "messages" response property)_. 

This behavior fit the common use-cases, sometimes, you want to override some behavior when a specific error occured, like:

* Add a log entry when a third-party exceptions is raised _(e.g pymsql, redis)_.
* Hide technical message's exception for production environment _(don't expose your internal stack to the outside world)_

To implement this, Tartiflette Engine allows you to override the default coercer by yours. It should be passed at the Engine instanciation in the `error_coercer`property, and respect this following signature `my_error_coercer(exception, error) -> dict`.


Here is an example of a custom error coercer.

```python
import logging


class CustomException(Exception):
    def __init__(self, type_name, message):
        self.type = type_name
        self.message = message


def my_error_coercer(exception, error) -> dict:
    if isinstance(exception, CustomException):
        logging.error("Unable to reach the Storage host.")
        error["extensions"]["type"] = exception.type

    return error


e = Engine(
    "my_sdl.graphql",
    error_coercer=my_error_coercer
)
```