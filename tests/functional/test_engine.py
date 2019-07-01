import os

import pytest

from tartiflette import create_engine
from tartiflette.schema.schema import GraphQLSchema

_curr_path = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.asyncio
async def test_tartiflette_engine_initialization_with_sdl_file_list(
    clean_registry
):
    engine = await create_engine(
        [
            _curr_path + "/data/splitted_sdl/author.sdl",
            _curr_path + "/data/splitted_sdl/blog.sdl",
            _curr_path + "/data/splitted_sdl/post.sdl",
            _curr_path + "/data/splitted_sdl/query.sdl",
        ]
    )

    assert clean_registry.find_schema().find_type("Author") is not None
    assert clean_registry.find_schema().find_type("Blog") is not None
    assert clean_registry.find_schema().find_type("Post") is not None
    assert (
        clean_registry.find_schema().find_type("Query").find_field("blogs")
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
async def test_tartiflette_engine_initialization_with_sdl_folder(
    path, clean_registry
):
    engine = await create_engine(path)

    assert clean_registry.find_schema().find_type("Author") is not None
    assert clean_registry.find_schema().find_type("Blog") is not None
    assert clean_registry.find_schema().find_type("Post") is not None
    assert (
        clean_registry.find_schema().find_type("Query").find_field("blogs")
        is not None
    )


@pytest.mark.asyncio
async def test_tartiflette_engine_initialization_with_single_sdl_file(
    clean_registry
):
    engine = await create_engine(
        _curr_path + "/data/simple_full_sdl/simple_full.sdl"
    )

    assert clean_registry.find_schema().find_type("Author") is not None
    assert clean_registry.find_schema().find_type("Blog") is not None
    assert clean_registry.find_schema().find_type("Post") is not None
    assert (
        clean_registry.find_schema().find_type("Query").find_field("blogs")
        is not None
    )


@pytest.mark.asyncio
async def test_tartiflette_engine_initialization_with_string_schema(
    clean_registry
):
    engine = await create_engine(
        """
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
    """
    )

    assert clean_registry.find_schema().find_type("Author") is not None
    assert clean_registry.find_schema().find_type("Blog") is not None
    assert clean_registry.find_schema().find_type("Post") is not None
    assert (
        clean_registry.find_schema().find_type("Query").find_field("blogs")
        is not None
    )
