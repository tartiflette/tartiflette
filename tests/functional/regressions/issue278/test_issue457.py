import asyncio
import random

import pytest

from tartiflette import Resolver, create_engine

_BOOKS = [{"id": i, "title": f"Book #{i}"} for i in range(25)]

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
        await asyncio.sleep(random.randint(0, 10) / 100)
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
        await asyncio.sleep(random.randint(0, 10) / 100)
        books_parsing_order.append(parent["id"])
        return parent["id"]

    engine = await create_engine(_SDL, schema_name=random_schema_name)
    assert await engine.execute("{ books { id title } }") == {
        "data": {"books": _BOOKS}
    }
    assert books_parsing_order != [book["id"] for book in _BOOKS]


@pytest.mark.asyncio
async def test_issue_457_sequentially_schema_level(random_schema_name):
    books_parsing_order = []

    @Resolver("Book.id", schema_name=random_schema_name)
    async def test_book_id(parent, args, ctx, info):
        await asyncio.sleep(random.randint(0, 10) / 100)
        books_parsing_order.append(parent["id"])
        return parent["id"]

    engine = await create_engine(
        _SDL, coerce_list_concurrently=False, schema_name=random_schema_name
    )
    assert await engine.execute(
        "{ books { id title } }", initial_value={"books": _BOOKS}
    ) == {"data": {"books": _BOOKS}}
    assert books_parsing_order == [book["id"] for book in _BOOKS]


@pytest.mark.asyncio
async def test_issue_457_concurrently_schema_level(random_schema_name):
    books_parsing_order = []

    @Resolver("Book.id", schema_name=random_schema_name)
    async def test_book_id(parent, args, ctx, info):
        await asyncio.sleep(random.randint(0, 10) / 100)
        books_parsing_order.append(parent["id"])
        return parent["id"]

    engine = await create_engine(
        _SDL, coerce_list_concurrently=True, schema_name=random_schema_name
    )
    assert await engine.execute(
        "{ books { id title } }", initial_value={"books": _BOOKS}
    ) == {"data": {"books": _BOOKS}}
    assert books_parsing_order != [book["id"] for book in _BOOKS]
