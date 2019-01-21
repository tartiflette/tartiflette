from collections import namedtuple

import pytest

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


async def func_field_libraries_resolver(*_args, **_kwargs):
    return [LibraryOne, LibraryTwo]


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="libraries",
    resolvers={"Query.libraries": func_field_libraries_resolver},
)
async def test_full_query_execute(engine):
    result = await engine.execute(
        """
        fragment boby on Author {
            name
        }

        query TestQueriesFromEnd2End{
            libraries {
                books(title: "Book") {
                    title
                    price
                    category
                    author {
                        name
                    }
                }
                authors(name: "Author") {
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
