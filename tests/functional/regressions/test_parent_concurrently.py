import asyncio
import random

import pytest

from tartiflette import Resolver, create_engine
from tartiflette.resolver.default import default_field_resolver

_AUTHORS = [
    {"id": i, "firstName": f"First #{i}", "lastName": f"Last #{i}"}
    for i in range(1, 3)
]
_BOOKS = [
    {
        "id": i,
        "title": f"Book #{i}",
        "comments": [f"Comment #{i}" for j in range(1, 3)],
        "rating": 4,
        "author_ids": [1, 2],
    }
    for i in range(1, 3)
]

_SDL = """
type Author {
  id: Int!
  firstName: String!
  lastName: String!
}

type Book {
  id: Int!
  title: String!
  comments: [String!]
  rating: Int!
  authors: [Author!]
}

type Query {
  books: [Book!]
}
"""

_QUERY = """
{
  books {
    id
    title
    comments
    rating
    authors {
      id
      firstName
      lastName
    }
  }
}
"""

_EXPECTED = {
    "data": {
        "books": [
            {
                "id": 1,
                "title": "Book #1",
                "comments": ["Comment #1", "Comment #1"],
                "rating": 4,
                "authors": [
                    {"id": 1, "firstName": "First #1", "lastName": "Last #1"},
                    {"id": 2, "firstName": "First #2", "lastName": "Last #2"},
                ],
            },
            {
                "id": 2,
                "title": "Book #2",
                "comments": ["Comment #2", "Comment #2"],
                "rating": 4,
                "authors": [
                    {"id": 1, "firstName": "First #1", "lastName": "Last #1"},
                    {"id": 2, "firstName": "First #2", "lastName": "Last #2"},
                ],
            },
        ]
    }
}


@pytest.mark.asyncio
async def test_issue_xxx_sequentially(random_schema_name):
    parsed_fields = []

    async def custom_default_field_resolver(parent, args, ctx, info):
        parsed_fields.append(f"{info.parent_type}.{info.field_name}")
        return await default_field_resolver(parent, args, ctx, info)

    @Resolver(
        "Query.books", list_concurrently=False, schema_name=random_schema_name
    )
    async def resolve_query_books(parent, args, ctx, info):
        return _BOOKS

    @Resolver(
        "Book.authors", list_concurrently=False, schema_name=random_schema_name
    )
    async def resolve_book_authors(parent, args, ctx, info):
        return [
            author
            for author in _AUTHORS
            if author["id"] in parent["author_ids"]
        ]

    @Resolver(
        "Book.id", parent_concurrently=False, schema_name=random_schema_name
    )
    @Resolver(
        "Book.title", parent_concurrently=False, schema_name=random_schema_name
    )
    @Resolver(
        "Book.comments",
        parent_concurrently=False,
        schema_name=random_schema_name,
    )
    @Resolver(
        "Book.rating",
        parent_concurrently=False,
        schema_name=random_schema_name,
    )
    @Resolver(
        "Author.id", parent_concurrently=False, schema_name=random_schema_name
    )
    @Resolver(
        "Author.firstName",
        parent_concurrently=False,
        schema_name=random_schema_name,
    )
    @Resolver(
        "Author.lastName",
        parent_concurrently=False,
        schema_name=random_schema_name,
    )
    async def resolve_default_with_random_sleep(parent, args, ctx, info):
        await asyncio.sleep(random.randint(0, 10) / 100)
        return await custom_default_field_resolver(parent, args, ctx, info)

    engine = await create_engine(
        _SDL,
        custom_default_resolver=custom_default_field_resolver,
        schema_name=random_schema_name,
    )

    assert await engine.execute(_QUERY) == _EXPECTED
    assert parsed_fields == [
        "Book.id",
        "Book.title",
        "Book.comments",
        "Book.rating",
        "Author.id",
        "Author.firstName",
        "Author.lastName",
        "Author.id",
        "Author.firstName",
        "Author.lastName",
        "Book.id",
        "Book.title",
        "Book.comments",
        "Book.rating",
        "Author.id",
        "Author.firstName",
        "Author.lastName",
        "Author.id",
        "Author.firstName",
        "Author.lastName",
    ]


@pytest.mark.asyncio
async def test_issue_xxx_concurrently(random_schema_name):
    parsed_fields = []

    async def custom_default_field_resolver(parent, args, ctx, info):
        parsed_fields.append(f"{info.parent_type}.{info.field_name}")
        return await default_field_resolver(parent, args, ctx, info)

    @Resolver(
        "Query.books", list_concurrently=False, schema_name=random_schema_name
    )
    async def resolve_query_books(parent, args, ctx, info):
        return _BOOKS

    @Resolver(
        "Book.authors", list_concurrently=False, schema_name=random_schema_name
    )
    async def resolve_book_authors(parent, args, ctx, info):
        return [
            author
            for author in _AUTHORS
            if author["id"] in parent["author_ids"]
        ]

    @Resolver(
        "Book.id", parent_concurrently=True, schema_name=random_schema_name
    )
    @Resolver(
        "Book.title", parent_concurrently=True, schema_name=random_schema_name
    )
    @Resolver(
        "Book.comments",
        parent_concurrently=True,
        schema_name=random_schema_name,
    )
    @Resolver(
        "Book.rating", parent_concurrently=True, schema_name=random_schema_name
    )
    @Resolver(
        "Author.id", parent_concurrently=True, schema_name=random_schema_name
    )
    @Resolver(
        "Author.firstName",
        parent_concurrently=True,
        schema_name=random_schema_name,
    )
    @Resolver(
        "Author.lastName",
        parent_concurrently=True,
        schema_name=random_schema_name,
    )
    async def resolve_default_with_random_sleep(parent, args, ctx, info):
        await asyncio.sleep(random.randint(0, 10) / 100)
        return await custom_default_field_resolver(parent, args, ctx, info)

    engine = await create_engine(
        _SDL,
        custom_default_resolver=custom_default_field_resolver,
        schema_name=random_schema_name,
    )

    assert await engine.execute(_QUERY) == _EXPECTED
    assert parsed_fields != [
        "Book.id",
        "Book.title",
        "Book.comments",
        "Book.rating",
        "Author.id",
        "Author.firstName",
        "Author.lastName",
        "Author.id",
        "Author.firstName",
        "Author.lastName",
        "Book.id",
        "Book.title",
        "Book.comments",
        "Book.rating",
        "Author.id",
        "Author.firstName",
        "Author.lastName",
        "Author.id",
        "Author.firstName",
        "Author.lastName",
    ]


@pytest.mark.asyncio
async def test_issue_xxx_mixed(random_schema_name):
    async def custom_default_field_resolver(
        parent, args, ctx, info, parsed_fields
    ):
        parsed_fields.append(f"{info.parent_type}.{info.field_name}")
        await asyncio.sleep(random.randint(0, 10) / 100)
        return await default_field_resolver(parent, args, ctx, info)

    @Resolver(
        "Query.books",
        list_concurrently=False,
        schema_name=random_schema_name,
    )
    async def resolve_query_books(parent, args, ctx, info):
        return _BOOKS

    @Resolver(
        "Book.authors",
        list_concurrently=False,
        schema_name=random_schema_name,
    )
    async def resolve_book_authors(parent, args, ctx, info):
        return [
            author
            for author in _AUTHORS
            if author["id"] in parent["author_ids"]
        ]

    parsed_book_fields = []

    @Resolver(
        "Book.id", parent_concurrently=False, schema_name=random_schema_name
    )
    @Resolver(
        "Book.title", parent_concurrently=True, schema_name=random_schema_name
    )
    @Resolver(
        "Book.comments",
        parent_concurrently=True,
        schema_name=random_schema_name,
    )
    @Resolver(
        "Book.rating",
        parent_concurrently=False,
        schema_name=random_schema_name,
    )
    async def resolve_default_with_random_sleep(parent, args, ctx, info):
        return await custom_default_field_resolver(
            parent, args, ctx, info, parsed_book_fields
        )

    parsed_author_fields = []

    @Resolver(
        "Author.id", parent_concurrently=True, schema_name=random_schema_name
    )
    @Resolver(
        "Author.firstName",
        parent_concurrently=True,
        schema_name=random_schema_name,
    )
    @Resolver(
        "Author.lastName",
        parent_concurrently=False,
        schema_name=random_schema_name,
    )
    async def resolve_default_with_random_sleep(parent, args, ctx, info):
        return await custom_default_field_resolver(
            parent, args, ctx, info, parsed_author_fields
        )

    engine = await create_engine(
        _SDL,
        custom_default_resolver=custom_default_field_resolver,
        schema_name=random_schema_name,
    )

    assert await engine.execute(_QUERY) == _EXPECTED
    assert len(parsed_book_fields) == 8
    assert len(parsed_author_fields) == 12
    assert parsed_book_fields[:2] == ["Book.id", "Book.rating"]
    assert parsed_author_fields[:1] == ["Author.lastName"]


@pytest.mark.asyncio
async def test_issue_xxx_sequentially_schema_level(random_schema_name):
    fields_parsing_order = []

    async def custom_default_field_resolver(parent, args, ctx, info):
        fields_parsing_order.append(f"{info.parent_type}.{info.field_name}")
        return await default_field_resolver(parent, args, ctx, info)

    engine = await create_engine(
        _SDL,
        custom_default_resolver=custom_default_field_resolver,
        coerce_list_concurrently=False,
        coerce_parent_concurrently=False,
        schema_name=random_schema_name,
    )
    assert await engine.execute(
        "{ books { id title } }", initial_value={"books": _BOOKS}
    ) == {
        "data": {
            "books": [
                {"id": book["id"], "title": book["title"]} for book in _BOOKS
            ]
        }
    }
    assert fields_parsing_order == [
        "Query.books",
        "Book.id",
        "Book.title",
        "Book.id",
        "Book.title",
    ]


@pytest.mark.asyncio
async def test_issue_xxx_concurrently_schema_level(random_schema_name):
    fields_parsing_order = []

    async def custom_default_field_resolver(parent, args, ctx, info):
        await asyncio.sleep(random.randint(0, 10) / 100)
        fields_parsing_order.append(f"{info.parent_type}.{info.field_name}")
        return await default_field_resolver(parent, args, ctx, info)

    engine = await create_engine(
        _SDL,
        custom_default_resolver=custom_default_field_resolver,
        coerce_list_concurrently=False,
        coerce_parent_concurrently=True,
        schema_name=random_schema_name,
    )
    assert await engine.execute(
        "{ books { id title rating } }", initial_value={"books": _BOOKS}
    ) == {
        "data": {
            "books": [
                {
                    "id": book["id"],
                    "title": book["title"],
                    "rating": book["rating"],
                }
                for book in _BOOKS
            ]
        }
    }
    assert fields_parsing_order != [
        "Query.books",
        "Book.id",
        "Book.title",
        "Book.rating",
        "Book.id",
        "Book.title",
        "Book.rating",
    ]
