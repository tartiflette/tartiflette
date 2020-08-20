from collections import namedtuple

import pytest

from tartiflette import Resolver

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


def full_query_with_alias_bakery(schema_name):
    @Resolver("Query.libraries", schema_name=schema_name)
    async def resolve_query_libraries(*_args, **_kwargs):
        return [LibraryOne, LibraryTwo]


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    preset="libraries", bakery=full_query_with_alias_bakery
)
async def test_full_query_with_alias(schema_stack):
    # TODO: Add Union and Interface and NonNull, All scalars Fields.
    result = await schema_stack.execute(
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


BookLight = namedtuple("BookLight", ("title", "price"))

data_store = [BookLight(title="The Jungle Book", price=14.99)]


def full_mutation_execute_alias_bakery(schema_name):
    @Resolver("CustomRootMutation.addBook", schema_name=schema_name)
    async def resolve_custom_root_mutation_add_book(_, args, *__):
        added_book = BookLight(
            title=args["input"]["title"], price=args["input"]["price"]
        )
        data_store.append(added_book)
        return {
            "clientMutationId": args["input"].get("clientMutationId"),
            "status": "SUCCESS",
            "book": added_book,
        }


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    preset="libraries", bakery=full_mutation_execute_alias_bakery,
)
async def test_full_mutation_execute_alias(schema_stack):
    assert len(data_store) == 1

    result = await schema_stack.execute(
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
