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
async def test_full_query_with_alias(engine):
    # TODO: Add Union and Interface and NonNull, All scalars Fields.
    result = await engine.execute(
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
        """,
        operation_name="TestQueriesFromEnd2End",
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


data_store = [{"title": "The Jungle Book", "price": 14.99}]


async def add_book_resolver(_, args, *__):
    added_book = {
        "title": args["input"]["title"],
        "price": args["input"]["price"],
    }
    data_store.append(added_book)
    return {
        "clientMutationId": args["input"].get("clientMutationId"),
        "status": "SUCCESS",
        "book": added_book,
    }


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="libraries",
    resolvers={"CustomRootMutation.addBook": add_book_resolver},
)
async def test_full_mutation_execute_alias(engine):
    assert len(data_store) == 1

    result = await engine.execute(
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
            "input": {
                "clientMutationId": "1",
                "title": "My Book",
                "price": 9.99,
            }
        },
        operation_name="AddBook",
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
