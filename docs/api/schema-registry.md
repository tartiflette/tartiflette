---
id: schema-registry
title: Schema registry
sidebar_label: Schema Registry
---

By default, all the resolvers created using the `@Resolver` decorator, are registered to the "default" schema in the `Schema Registry`.

#### What is the aim of the Schema Registry?

The `Schema Registry` is an advanced use-case of Tartiflette, used by the developers who want to expose multiple Engines from the same codebase.

The Schema Registry will allow you to assign a `Resolver` to a specific Schema, which you can then choose during the initialization process of the Engine.

By default, every `Resolver` is assigned to the `default` schema. Moreover, every Engine is attached to the `default` schema.

#### How to use multiple Schemas and Engines from the same codebase?

The following code sample will create 2 schemas in the `Schema Registry`.

- "default"
- "proof_of_concept"

```python
import asyncio

from tartiflette import Resolver, create_engine

@Resolver("Query.hello") # Will be assigned to the 'default' Schema
async def resolver_hello(parent, args, ctx, info):
    return "hello " + args["name"]


@Resolver("Query.hello", "proof_of_concept") # Will be assigned to the 'proof_of_concept' Schema
async def resolver_hello(parent, args, ctx, info):
    return "Hey " + args["name"]


async def run():
    tftt_engine = await create_engine(
        """
        type Query {
            hello(name: String): String
        }
        """
    ) # The engine created will be attached to the SDL of the 'default' Schema.

    result = await tftt_engine.execute(
        query='query { hello(name: "Chuck") }'
    )

    # the result will be
    # {
    #     "data": {
    #         "hello": "Hello Chuck"
    #     }
    # }

    tftt_proof_of_concept = await create_engine(
        """
        type Query {
            hello(name: String): String
        }
        """,
        schema_name="proof_of_concept"
    ) # This Engine will be attached to the SDL of the 'proof_of_concept' Schema.

    result_poc = await tftt_proof_of_concept.execute(
        query='query { hello(name: "Chuck") }'
    )

    # the `result_poc` will be
    # {
    #     "data": {
    #         "hello": "Hey Chuck"
    #     }
    # }
```
