import os

import pytest

from tartiflette import create_engine
from tartiflette.schema.registry import SchemaRegistry

_curr_path = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.asyncio
async def test_tartiflette_engine_initialization_with_sdl_file_list():
    engine = await create_engine(
        [
            _curr_path + "/data/splitted_sdl/directives.sdl",
            _curr_path + "/data/splitted_sdl/author.sdl",
            _curr_path + "/data/splitted_sdl/blog.sdl",
            _curr_path + "/data/splitted_sdl/post.sdl",
            _curr_path + "/data/splitted_sdl/query.sdl",
        ],
        schema_name="test_tartiflette_engine_initialization_with_sdl_file_list",
    )

    assert (
        SchemaRegistry.find_schema(
            "test_tartiflette_engine_initialization_with_sdl_file_list"
        ).find_type("Author")
        is not None
    )
    assert (
        SchemaRegistry.find_schema(
            "test_tartiflette_engine_initialization_with_sdl_file_list"
        ).find_type("Blog")
        is not None
    )
    assert (
        SchemaRegistry.find_schema(
            "test_tartiflette_engine_initialization_with_sdl_file_list"
        ).find_type("Post")
        is not None
    )
    assert (
        SchemaRegistry.find_schema(
            "test_tartiflette_engine_initialization_with_sdl_file_list"
        )
        .find_type("Query")
        .find_field("blogs")
        is not None
    )


@pytest.mark.parametrize(
    "path",
    [
        _curr_path + "/data/splitted_sdl",
        _curr_path + "/data/splitted_graphql",
        _curr_path + "/data/splitted_mixed",
        _curr_path + "/data/splitted_mixed_sub_dir",
    ],
)
@pytest.mark.asyncio
async def test_tartiflette_engine_initialization_with_sdl_folder(path,):
    schema_name = (
        f"{path}_test_tartiflette_engine_initialization_with_sdl_folder"
    )

    engine = await create_engine(path, schema_name=schema_name)

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
async def test_tartiflette_engine_initialization_with_single_sdl_file():
    engine = await create_engine(
        _curr_path + "/data/simple_full_sdl/simple_full.sdl",
        schema_name="test_tartiflette_engine_initialization_with_single_sdl_file",
    )

    assert (
        SchemaRegistry.find_schema(
            "test_tartiflette_engine_initialization_with_single_sdl_file"
        ).find_type("Author")
        is not None
    )
    assert (
        SchemaRegistry.find_schema(
            "test_tartiflette_engine_initialization_with_single_sdl_file"
        ).find_type("Blog")
        is not None
    )
    assert (
        SchemaRegistry.find_schema(
            "test_tartiflette_engine_initialization_with_single_sdl_file"
        ).find_type("Post")
        is not None
    )
    assert (
        SchemaRegistry.find_schema(
            "test_tartiflette_engine_initialization_with_single_sdl_file"
        )
        .find_type("Query")
        .find_field("blogs")
        is not None
    )


@pytest.mark.asyncio
async def test_tartiflette_engine_initialization_with_string_schema():
    engine = await create_engine(
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
        schema_name="test_tartiflette_engine_initialization_with_string_schema",
    )

    assert (
        SchemaRegistry.find_schema(
            "test_tartiflette_engine_initialization_with_string_schema"
        ).find_type("Author")
        is not None
    )
    assert (
        SchemaRegistry.find_schema(
            "test_tartiflette_engine_initialization_with_string_schema"
        ).find_type("Blog")
        is not None
    )
    assert (
        SchemaRegistry.find_schema(
            "test_tartiflette_engine_initialization_with_string_schema"
        ).find_type("Post")
        is not None
    )
    assert (
        SchemaRegistry.find_schema(
            "test_tartiflette_engine_initialization_with_string_schema"
        )
        .find_type("Query")
        .find_field("blogs")
        is not None
    )
