from collections import namedtuple

import pytest

from tartiflette import Resolver

Book = namedtuple("Book", ("title", "price"))

_DATA_STORE = [Book(title="The Jungle Book", price=14.99)]


def bakery(schema_name):
    @Resolver("CustomRootMutation.addBook", schema_name=schema_name)
    async def add_book_resolver(_, args, *__):
        added_book = Book(
            title=args["input"]["title"], price=args["input"]["price"]
        )
        _DATA_STORE.append(added_book)
        return {
            "clientMutationId": args["input"].get("clientMutationId"),
            "status": "SUCCESS",
            "book": added_book,
        }


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
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
    """,
    bakery=bakery,
)
async def test_full_mutation_execute(schema_stack):
    assert len(_DATA_STORE) == 1

    assert (
        await schema_stack.execute(
            """
            mutation AddBook($input: AddBookInput!) {
              addBook(input: $input) {
                status
                clientMutationId
                book {
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
        == {
            "data": {
                "addBook": {
                    "clientMutationId": "1",
                    "status": "SUCCESS",
                    "book": {"title": "My Book", "price": 9.99},
                }
            }
        }
    )

    assert len(_DATA_STORE) == 2
