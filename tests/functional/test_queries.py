from collections import namedtuple
from typing import Any
from unittest.mock import Mock, call

import pytest

from tartiflette import Resolver
from tartiflette.engine import Engine
from tartiflette.executors.types import Info
from tartiflette.types.location import Location


@pytest.mark.asyncio
async def test_full_query_execute(clean_registry):
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
        category: BookCategory
    }
    """

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

    @Resolver("Query.libraries")
    async def func_field_libraries_resolver(*_args, **_kwargs):
        return [LibraryOne, LibraryTwo]

    ttftt = Engine(schema_sdl)

    result = await ttftt.execute(
        """
        fragment boby on Author {
            name
        }

        query TestQueriesFromEnd2End{
            libraries {
                books {
                    title
                    price(number: 3.6)
                    category
                    author {
                        name(useless: true)
                    }
                }
                authors {
                    ...boby
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
