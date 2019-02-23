---
id: schema-registry
title: Schema registry
sidebar_label: Schema Registry
---

By default, all the resolvers created thanks to the `@Resolver` decorator, are registered to the "default" schema in the `Schema Registry`.

#### What is aim of the Schema Registry?

The `Schema Registry` is an advanced use-case of Tartiflette, used by the developers who want to expose more than one Engine from the same codebase.

The Schema Registry will help you to assign a `Resolver` to a specific Schema, then, during the initialization process of the Engine, you will be able to choose a specific Schema to use.

By default, every `Resolver` are assigned to the `default` schema. Moreover, every Engine are attached to the `default` schema.

#### How to use multiple Schema and Engine from the same codebase?

This following code sample will create 2 schemas in the `Schema Registry`.

- "default"
- "proof_of_concept"

```python
import asyncio

from tartiflette import Engine, Resolver

@Resolver("Query.hello") # Will be assigned to the 'default' Schema
async def resolver_hello(parent, args, ctx, info):
    return "hello " + args["name"]


@Resolver("Query.hello", "proof_of_concept") # Will be assigned to the 'proof_of_concept' Schema
async def resolver_hello(parent, args, ctx, info):
    return "Hey " + args["name"]


async def run():
    tftt_engine = Engine("""
    type Query {
        hello(name: String): String
    }
    """) # This Engine will attached the SDL to the 'default' Schema.

    result = await tftt_engine.execute(
        query='query { hello(name: "Chuck") }'
    )

    # result will be equals to
    # {
    #     "data": {
    #         "hello": "Hello Chuck"
    #     }
    # }

    tftt_proof_of_concept = Engine("""
    type Query {
        hello(name: String): String
    }
    """,
    schema_name="proof_of_concept") # This Engine will attached the SDL to the 'proof_of_concept' Schema.

    result_poc = await tftt_proof_of_concept.execute(
        query='query { hello(name: "Chuck") }'
    )

    # result_poc will be equals to
    # {
    #     "data": {
    #         "hello": "Hey Chuck"
    #     }
    # }
```