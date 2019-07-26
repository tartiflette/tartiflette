---
id: schema-registry
title: Schema registry
sidebar_label: Schema Registry
---

By default, all the resolvers created using the `@Resolver` decorator, are registered to the "default" schema in the `Schema Registry`.

#### What is the aim of the Schema Registry?

The `Schema Registry` is an advanced use-case of Tartiflette, used by the developers who want to expose multiple schema from the same codebase.

The Schema Registry will allow you to assign a `Resolver` to a specific schema, which you can then choose during the initialization process of the engine.

By default, every `Resolver` is assigned to the `default` schema. Moreover, every engine is attached to the `default` schema by default.

#### How to use multiple schemas and engines from the same codebase?

The following code sample will create 2 schemas in the `Schema Registry`:
- default
- proof_of_concept

```python
from tartiflette import Resolver, create_engine


@Resolver("Query.hello")  # Will be assigned to the "default" schema
async def resolve_default_query_hello(parent, args, ctx, info):
    return "Hello " + args["name"]


@Resolver("Query.hello", schema_name="proof_of_concept")  # Will be assigned to the "proof_of_concept" schema
async def resolve_proof_of_concept_query_hello(parent, args, ctx, info):
    return "Hey " + args["name"]


async def run():
    tftt_engine = await create_engine(
        """
        type Query {
            hello(name: String): String
        }
        """
    )  # The engine created will be attached to the SDL of the "default" schema

    result = await tftt_engine.execute("""{ hello(name: "Chuck") }""")
    # the result will be:
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
        schema_name="proof_of_concept",
    )  # This engine will be attached to the SDL of the "proof_of_concept" schema

    result_poc = await tftt_proof_of_concept.execute(
        """{ hello(name: "Chuck") }"""
    )
    # the `result_poc` will be:
    # {
    #     "data": {
    #         "hello": "Hey Chuck"
    #     }
    # }
```
