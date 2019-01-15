from collections import namedtuple
from typing import Any
from unittest.mock import Mock, call

import pytest

from tartiflette import Resolver
from tartiflette.engine import Engine
from tartiflette.executors.types import Info
from tartiflette.types.location import Location


@pytest.mark.asyncio
async def test_full_query_with_alias(clean_registry):
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
        query TestQueriesFromEnd2End{
            libraries {
                anAlias: books {
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
                    "anAlias": [
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
                    "anAlias": [
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


@pytest.mark.asyncio
async def test_full_mutation_execute_alias(clean_registry):
    schema_sdl = """
    enum Status {
        SUCCESS
    }

    schema {
        query: CustomRootQuery
        mutation: CustomRootMutation
    }

    type CustomRootQuery {
        books: [Book]
    }

    type Book {
        title: String
        price: Float
    }

    type CustomRootMutation {
        addBook(input: AddBookInput!): AddBookPayload
    }

    input AddBookInput {
        clientMutationId: String
        title: String!
        price: Float!
    }

    type AddBookPayload {
        status: Status
        clientMutationId: String
        book: Book
    }
    """

    Book = namedtuple("Book", ("title", "price"))

    data_store = [Book(title="The Jungle Book", price=14.99)]

    @Resolver("CustomRootMutation.addBook")
    async def add_book_resolver(_, args, *__):
        added_book = Book(
            title=args["input"]["title"], price=args["input"]["price"]
        )
        data_store.append(added_book)
        return {
            "clientMutationId": args["input"].get("clientMutationId"),
            "status": "SUCCESS",
            "book": added_book,
        }

    assert len(data_store) == 1

    ttftt = Engine(schema_sdl)

    result = await ttftt.execute(
        """
        mutation AddBook($input: AddBookInput!) {
          lol: addBook(input: $input) {
            status
            clientMutationId
            booooook: book {
                title
                price
            }
          }
        }
        """,
        variables={
            "input": {"clientMutationId": 1, "title": "My Book", "price": 9.99}
        },
    )

    assert len(data_store) == 2

    assert {
        "data": {
            "lol": {
                "clientMutationId": "1",
                "status": "SUCCESS",
                "booooook": {"title": "My Book", "price": 9.99},
            }
        }
    } == result
