from unittest.mock import Mock

import pytest

from tartiflette import Resolver, create_schema, executor_factory
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.types.exceptions.tartiflette import (
    ImproperlyConfigured,
    NonCallable,
    NonCoroutine,
)


@pytest.mark.asyncio
@pytest.mark.parametrize("sdl", [None, ""])
async def test_create_schema_without_sdl(sdl, random_schema_name):
    with pytest.raises(ImproperlyConfigured, match="Please provide a SDL."):
        await create_schema(sdl, name=random_schema_name)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "modules",
    [
        "tests.unit.schema.modules",
        ["tests.unit.schema.modules"],
    ],
)
async def test_create_schema_with_modules(random_schema_name, modules):
    schema = await create_schema(
        """
        scalar String
        type Query {
          hello(name: String!): String!
        }
        """,
        name=f"{random_schema_name}{hash(str(modules))}",
        modules=modules,
    )
    execute = executor_factory(schema)
    assert await execute(
        """
            {
              hello(name: "John")
            }
            """
    ) == {
        "data": {
            "hello": "Hello John!",
        },
    }


@pytest.mark.asyncio
async def test_create_schema_with_invalid_default_resolver(random_schema_name):
    def my_default_resolver(*_, **__):
        return "DefaultResolverValue"

    with pytest.raises(
        NonCoroutine,
        match="Given < default_resolver > is not a coroutine callable.",
    ):
        await create_schema(
            """
            type Query {
              hello(name: String!): String!
            }
            """,
            name=random_schema_name,
            default_resolver=my_default_resolver,
        )


@pytest.mark.asyncio
async def test_create_schema_with_default_resolver(random_schema_name):
    async def my_default_resolver(*_, **__):
        return "DefaultResolverValue"

    @Resolver("Query.hello", schema_name=random_schema_name)
    async def resolve_query_hello(parent, args, ctx, info):
        return f"Hello {args['name']}!"

    schema = await create_schema(
        """
        type Query {
          hello(name: String!): String!
          bye(name: String!): String!
        }
        """,
        name=random_schema_name,
        default_resolver=my_default_resolver,
    )
    execute = executor_factory(schema)
    assert await execute(
        """
            {
              hello(name: "John")
              bye(name: "John")
            }
            """
    ) == {
        "data": {
            "hello": "Hello John!",
            "bye": "DefaultResolverValue",
        },
    }


@pytest.mark.asyncio
async def test_create_schema_with_invalid_default_type_resolver(
    random_schema_name,
):
    with pytest.raises(
        NonCallable,
        match="Given < default_type_resolver > is not a coroutine callable.",
    ):
        await create_schema(
            """
            type Query {
              hello(name: String!): String!
            }
            """,
            name=random_schema_name,
            default_type_resolver="not_a_callable",
        )


@pytest.mark.asyncio
async def test_create_schema_with_default_type_resolver(random_schema_name):
    def my_default_type_resolver(result, *args, **kwargs):
        return getattr(result, "kind", None)

    @Resolver("Query.named", schema_name=random_schema_name)
    async def resolve_query_named(parent, args, ctx, info):
        class Person(dict):
            pass

        result = Person({"name": "John"})
        setattr(result, "kind", "Person")
        return result

    schema = await create_schema(
        """
        interface Named {
          name: String!
        }

        type Person implements Named {
          name: String!
        }

        type Query {
          named(id: Int!): Named
        }
        """,
        name=random_schema_name,
        default_type_resolver=my_default_type_resolver,
    )
    execute = executor_factory(schema)
    assert await execute(
        """
            {
              named(id: 1) {
                __typename
                name
              }
            }
            """
    ) == {
        "data": {
            "named": {
                "__typename": "Person",
                "name": "John",
            },
        },
    }


@pytest.mark.asyncio
async def test_create_schema_with_invalid_default_arguments_coercer(
    random_schema_name,
):
    def my_default_arguments_coercer(*coroutines):
        return [str(i) for i in range(len(coroutines))]

    with pytest.raises(
        NonCoroutine,
        match="Given < default_arguments_coercer > is not a coroutine callable.",
    ):
        await create_schema(
            """
            type Query {
              hello(name: String!): String!
            }
            """,
            name=random_schema_name,
            default_arguments_coercer=my_default_arguments_coercer,
        )


@pytest.mark.asyncio
async def test_create_schema_with_default_arguments_coercer(
    random_schema_name,
):
    async def my_default_arguments_coercer(*coroutines):
        return [str(i) for i in range(len(coroutines))]

    @Resolver("Query.hello", schema_name=random_schema_name)
    async def resolve_query_hello(parent, args, ctx, info):
        return f"Hello {args['firstname']} {args['lastname']}!"

    schema = await create_schema(
        """
        type Query {
          hello(firstname: String!, lastname: String!): String!
        }
        """,
        name=random_schema_name,
        default_arguments_coercer=my_default_arguments_coercer,
    )
    execute = executor_factory(schema)
    assert await execute(
        """
            {
              hello(firstname: "John", lastname: "Doe")
            }
            """
    ) == {
        "data": {
            "hello": "Hello 0 1!",
        },
    }


@pytest.mark.asyncio
async def test_create_schema_with_parser(random_schema_name):
    mocked_parser = Mock(wraps=parse_to_document)

    mocked_parser.assert_not_called()
    await create_schema(
        """
        type Query {
          hello(name: String!): String!
        }
        """,
        name=random_schema_name,
        parser=mocked_parser,
    )
    mocked_parser.assert_called_once()
