from collections import namedtuple

import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_full_mutation_execute(clean_registry):
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

    ttftt = await create_engine(schema_sdl)

    result = await ttftt.execute(
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

    assert len(data_store) == 2

    assert {
        "data": {
            "addBook": {
                "clientMutationId": "1",
                "status": "SUCCESS",
                "book": {"title": "My Book", "price": 9.99},
            }
        }
    } == result
