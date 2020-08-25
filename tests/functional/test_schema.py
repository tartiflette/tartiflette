import os

import pytest

from tartiflette import create_schema
from tartiflette.schema.registry import SchemaRegistry
from tests.data.utils import get_path_to_sdl

_curr_path = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.asyncio
async def test_tartiflette_schema_initialization_with_sdl_file_list():
    await create_schema(
        [
            get_path_to_sdl("splitted_sdl/directives.sdl"),
            get_path_to_sdl("splitted_sdl/author.sdl"),
            get_path_to_sdl("splitted_sdl/blog.sdl"),
            get_path_to_sdl("splitted_sdl/post.sdl"),
            get_path_to_sdl("splitted_sdl/query.sdl"),
        ],
        name="test_tartiflette_schema_initialization_with_sdl_file_list",
    )

    assert (
        SchemaRegistry.find_schema(
            "test_tartiflette_schema_initialization_with_sdl_file_list"
        ).find_type("Author")
        is not None
    )
    assert (
        SchemaRegistry.find_schema(
            "test_tartiflette_schema_initialization_with_sdl_file_list"
        ).find_type("Blog")
        is not None
    )
    assert (
        SchemaRegistry.find_schema(
            "test_tartiflette_schema_initialization_with_sdl_file_list"
        ).find_type("Post")
        is not None
    )
    assert (
        SchemaRegistry.find_schema(
            "test_tartiflette_schema_initialization_with_sdl_file_list"
        )
        .find_type("Query")
        .find_field("blogs")
        is not None
    )


@pytest.mark.parametrize(
    "path",
    [
        get_path_to_sdl("splitted_sdl"),
        get_path_to_sdl("splitted_graphql"),
        get_path_to_sdl("splitted_mixed"),
        get_path_to_sdl("splitted_mixed_sub_dir"),
    ],
)
@pytest.mark.asyncio
async def test_tartiflette_schema_initialization_with_sdl_folder(path):
    schema_name = (
        f"{path}_test_tartiflette_schema_initialization_with_sdl_folder"
    )

    await create_schema(path, name=schema_name)

    assert (
        SchemaRegistry.find_schema(schema_name).find_type("Author") is not None
    )
    assert (
        SchemaRegistry.find_schema(schema_name).find_type("Blog") is not None
    )
    assert (
        SchemaRegistry.find_schema(schema_name).find_type("Post") is not None
    )
    assert (
        SchemaRegistry.find_schema(schema_name)
        .find_type("Query")
        .find_field("blogs")
        is not None
    )


@pytest.mark.asyncio
async def test_tartiflette_schema_initialization_with_single_sdl_file():
    await create_schema(
        get_path_to_sdl("simple_full_sdl/simple_full.sdl"),
        name="test_tartiflette_schema_initialization_with_single_sdl_file",
    )

    assert (
        SchemaRegistry.find_schema(
            "test_tartiflette_schema_initialization_with_single_sdl_file"
        ).find_type("Author")
        is not None
    )
    assert (
        SchemaRegistry.find_schema(
            "test_tartiflette_schema_initialization_with_single_sdl_file"
        ).find_type("Blog")
        is not None
    )
    assert (
        SchemaRegistry.find_schema(
            "test_tartiflette_schema_initialization_with_single_sdl_file"
        ).find_type("Post")
        is not None
    )
    assert (
        SchemaRegistry.find_schema(
            "test_tartiflette_schema_initialization_with_single_sdl_file"
        )
        .find_type("Query")
        .find_field("blogs")
        is not None
    )


@pytest.mark.asyncio
async def test_tartiflette_schema_initialization_with_string_schema():
    await create_schema(
        """
        directive @relation(name: String!) on FIELD_DEFINITION
        directive @default(value: Int!) on FIELD_DEFINITION

        type Post {
            id: ID!
            title: String!
            publishedAt: Int!
            likes: Int! @default(value: 0)
            author: Author! @relation(name: "Posts")
            blog: Blog @relation(name: "Posts")
        }

        type Author {
            id: ID!
            name: String!
            posts: [Post!]! @relation(name: "Author")
        }

        type Blog {
            id: ID!
            name: String!
            description: String,
            authors: [Author!]!
            posts: [Post!]! @relation(name: "Posts")
        }

        type Query {
            authors: [Author!]!
            blogs: [Blog!]!
        }
        """,
        name="test_tartiflette_schema_initialization_with_string_schema",
    )

    assert (
        SchemaRegistry.find_schema(
            "test_tartiflette_schema_initialization_with_string_schema"
        ).find_type("Author")
        is not None
    )
    assert (
        SchemaRegistry.find_schema(
            "test_tartiflette_schema_initialization_with_string_schema"
        ).find_type("Blog")
        is not None
    )
    assert (
        SchemaRegistry.find_schema(
            "test_tartiflette_schema_initialization_with_string_schema"
        ).find_type("Post")
        is not None
    )
    assert (
        SchemaRegistry.find_schema(
            "test_tartiflette_schema_initialization_with_string_schema"
        )
        .find_type("Query")
        .find_field("blogs")
        is not None
    )
