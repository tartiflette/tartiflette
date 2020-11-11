import asyncio
import random

import pytest

from tartiflette import Resolver, create_engine

_BOOKS = [
    {"id": 1, "title": "Book #1"},
    {"id": 2, "title": "Book #2"},
    {"id": 3, "title": "Book #3"},
    {"id": 4, "title": "Book #4"},
    {"id": 5, "title": "Book #5"},
    {"id": 6, "title": "Book #6"},
    {"id": 7, "title": "Book #7"},
    {"id": 8, "title": "Book #8"},
]

_SDL = """
type Book {
  id: Int!
  title: String!
}

type Query {
  books: [Book!]
}
"""


@pytest.mark.asyncio
async def test_issue_457_sequentially(random_schema_name):
    @Resolver(
        "Query.books", concurrently=False, schema_name=random_schema_name
    )
    async def test_query_books(parent, args, ctx, info):
        return _BOOKS

    books_parsing_order = []

    @Resolver("Book.id", schema_name=random_schema_name)
    async def test_book_id(parent, args, ctx, info):
        await asyncio.sleep(random.randint(1, 10) / 10)
        books_parsing_order.append(parent["id"])
        return parent["id"]

    engine = await create_engine(_SDL, schema_name=random_schema_name)
    assert await engine.execute("{ books { id title } }") == {
        "data": {"books": _BOOKS}
    }
    assert books_parsing_order == [book["id"] for book in _BOOKS]


@pytest.mark.asyncio
async def test_issue_457_concurrently(random_schema_name):
    @Resolver("Query.books", concurrently=True, schema_name=random_schema_name)
    async def test_query_books(parent, args, ctx, info):
        return _BOOKS

    books_parsing_order = []

    @Resolver("Book.id", schema_name=random_schema_name)
    async def test_book_id(parent, args, ctx, info):
        await asyncio.sleep(random.randint(1, 10) / 10)
        books_parsing_order.append(parent["id"])
        return parent["id"]

    engine = await create_engine(_SDL, schema_name=random_schema_name)
    assert await engine.execute("{ books { id title } }") == {
        "data": {"books": _BOOKS}
    }
    assert books_parsing_order != [book["id"] for book in _BOOKS]
