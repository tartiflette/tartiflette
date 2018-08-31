from collections import namedtuple
from typing import Any

import pytest
from unittest.mock import Mock, call

from tartiflette import Resolver
from tartiflette.executors.types import Info
from tartiflette.engine import Engine
from tartiflette.types.location import Location


@pytest.mark.asyncio
async def test_full_query_execute():
    # TODO: Add Union and Interface and NonNull, All scalars Fields.
    schema_sdl = """
    enum BookCategory {
        Action
        Adventure
        Romance
        Fiction
        History
    }

    type Query {
        libraries: [Library]
    }

    type Library {
        books: [Book]
        authors: [Author]
    }

    type Author {
        name: String
    }

    type Book {
        title: String
        author: Author
        price: Float
        category: String
    }
    """

    # Support of enum is broken, TODO, find why

    ttftt = Engine(schema_sdl)

    Library = namedtuple("Library", "books,authors")
    Author = namedtuple("Author", "name")
    Book = namedtuple("Book", "title,author,price,category")

    AuthorRudyardKipling = Author("Rudyard Kipling")
    AuthorHarperLee = Author("Harper Lee")
    AuthorLeoTolstoy = Author("Leo Tolstoy")
    AuthorJaneAustin = Author("Jane Austin")
    BookJungleBook = Book(
        title="The Jungle Book",
        author=AuthorRudyardKipling,
        price=14.99,
        category="Adventure",
    )
    BookToKillAMockingbird = Book(
        title="To Kill a Mockingbird",
        author=AuthorHarperLee,
        price=12.99,
        category="Fiction",
    )
    BookAnnaKarenina = Book(
        title="Anna Karenina",
        author=AuthorLeoTolstoy,
        price=19.99,
        category="Fiction",
    )
    BookPrideAndPrejudice = Book(
        title="Pride and Prejudice",
        author=AuthorJaneAustin,
        price=11.99,
        category="Romance",
    )
    LibraryOne = Library(
        books=[BookAnnaKarenina, BookJungleBook, BookToKillAMockingbird],
        authors=[AuthorLeoTolstoy, AuthorHarperLee, AuthorRudyardKipling],
    )
    LibraryTwo = Library(
        books=[BookPrideAndPrejudice, BookJungleBook],
        authors=[AuthorJaneAustin, AuthorRudyardKipling],
    )

    @Resolver("Query.libraries", schema=ttftt.schema)
    async def func_field_libraries_resolver(
        parent, arguments, request_ctx, info: Info
    ):
        return [LibraryOne, LibraryTwo]

    result = await ttftt.execute(
        """
        query TestQueriesFromEnd2End{
            libraries {
                books {
                    title
                    price
                    category
                    author {
                        name
                    }
                }
                authors {
                    name
                }
            }
        }
        """
    )

    assert {
        "data": {
            "libraries": [
                {
                    "books": [
                        {
                            "title": "Anna Karenina",
                            "author": {"name": "Leo Tolstoy"},
                            "price": 19.99,
                            "category": "Fiction",
                        },
                        {
                            "title": "The Jungle Book",
                            "author": {"name": "Rudyard Kipling"},
                            "price": 14.99,
                            "category": "Adventure",
                        },
                        {
                            "title": "To Kill a Mockingbird",
                            "author": {"name": "Harper Lee"},
                            "price": 12.99,
                            "category": "Fiction",
                        },
                    ],
                    "authors": [
                        {"name": "Leo Tolstoy"},
                        {"name": "Harper Lee"},
                        {"name": "Rudyard Kipling"},
                    ],
                },
                {
                    "books": [
                        {
                            "title": "Pride and Prejudice",
                            "author": {"name": "Jane Austin"},
                            "price": 11.99,
                            "category": "Romance",
                        },
                        {
                            "title": "The Jungle Book",
                            "author": {"name": "Rudyard Kipling"},
                            "price": 14.99,
                            "category": "Adventure",
                        },
                    ],
                    "authors": [
                        {"name": "Jane Austin"},
                        {"name": "Rudyard Kipling"},
                    ],
                },
            ]
        }
    } == result
