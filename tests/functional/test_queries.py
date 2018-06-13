from collections import namedtuple
from typing import Any

import pytest
from unittest.mock import Mock, call

from tartiflette import Resolver
from tartiflette.executors.types import Info
from tartiflette.tartiflette import Tartiflette
from tartiflette.types.location import Location


GQLTypeMock = namedtuple("GQLTypeMock", ["name", "coerce_value"])


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'query, varis, expected', [
        (
            """
            query a_request {
                A {
                    B {
                        C
                    }
                    D
                    E
                    F {
                        G {
                            H
                        }
                    }
                }
            }
            """, {}, [
                call("Query.A"),
                call("Object.B"),
                call("Object.C"),
                call("Object.D"),
                call("Object.E"),
                call("Object.F"),
                call("Object.G"),
                call("Object.H")
            ]
        )
    ],
    ids=["Simple Order"]
)
async def test_get_field_by_name_call_order(query, varis, expected):
    from tartiflette.tartiflette import Tartiflette

    async def _resolver(_parent_result, _arguments, _request_ctx, _info: Info):
        return {}

    def coerce_value(value: Any, _info: Info) -> Any:
        return value

    field = Mock()
    field.name = "test"
    field.gql_type = GQLTypeMock(name="Object", coerce_value=coerce_value)
    field.resolver = _resolver

    sdm = Mock()
    sdm.query_type = "Query"
    sdm.get_field_by_name = Mock(return_value=field)
    sdm.types = {
        "Query": GQLTypeMock(name="Query", coerce_value=coerce_value),
    }

    ttftt = Tartiflette(schema=sdm)
    await ttftt.execute(query, context={}, variables=varis)

    sdm.get_field_by_name.assert_has_calls(expected, any_order=False)


@pytest.mark.asyncio
async def test_calling_resolver_with_correct_value():
    from tartiflette.tartiflette import Tartiflette

    sdl = '''
        type AType {
            B: BType
            D: String
            E: String
            F: FType
        }

        type BType { C: CType }
        type CType { K: KType }
        type KType { id: String }
        type FType { H: HType }
        type HType { I: String }

        type Query {
            A: [AType]
        }
        '''

    ttftt = Tartiflette(sdl=sdl)

    class resolver_a(Mock):
        async def __call__(self, parent, arguments, request_ctx, info: Info):
            new_info = info.clone(query_field=None, execution_ctx=None)
            super(resolver_a, self).__call__(parent, arguments, request_ctx, new_info)
            return [{"id": 1}, {"id": 2}]

    stuff_a = resolver_a()

    @Resolver("Query.A", schema=ttftt.schema)
    async def wrap_1(parent, arguments, request_ctx, info: Info):
        return await stuff_a(parent, arguments, request_ctx, info)

    class resolver_b(Mock):
        class resolver_b_result:
            def __init__(self):
                self.C = {"id": "b.c"}

            def __repr__(self):
                return "IAmABResults"

        def __init__(self, *args, **kwargs):
            super(resolver_b, self).__init__(*args, **kwargs)
            self.rtrn = resolver_b.resolver_b_result()

        async def __call__(self, parent, arguments, request_ctx, info: Info):
            new_info = info.clone(query_field=None, execution_ctx=None)
            super(resolver_b, self).__call__(parent, arguments, request_ctx, new_info)
            return self.rtrn

    stuff_b = resolver_b()

    @Resolver("AType.B", schema=ttftt.schema)
    async def wrap_2(parent, arguments, request_ctx, info: Info):
        return await stuff_b(parent, arguments, request_ctx, info)

    class resolver_d(Mock):

        async def __call__(self, parent, arguments, request_ctx, info: Info):
            new_info = info.clone(query_field=None, execution_ctx=None)
            super(resolver_d, self).__call__(parent, arguments, request_ctx, new_info)
            return "ValueD"

    stuff_d = resolver_d()

    @Resolver("AType.D", schema=ttftt.schema)
    async def wrap_3(parent, arguments, request_ctx, info: Info):
        return await stuff_d(parent, arguments, request_ctx, info)

    ttftt.schema.bake()
    r = await ttftt.execute(
        """
        query a_request {
            A {
                B {
                    C {
                        K
                    }
                }
                D
                E
                F {
                    H {
                        I
                    }
                }
            }
        }
        """,
        context={},
        variables={}
    )

    stuff_a.assert_has_calls(
        [
            call(
                {},
                {},
                {},
                Info(
                    query_field=None,
                    schema_field=ttftt.schema.types["Query"].fields["A"],
                    schema=ttftt.schema,
                    path=["A"],
                    location=Location(line=1, column=40,
                                      line_end=1, column_end=313, context=''),
                    execution_ctx=None,
                ),
            )
        ],
        any_order=True,
    )

    stuff_b.assert_has_calls(
        [
            call(
                {"id": 1},
                {},
                {},
                Info(
                    query_field=None,
                    schema_field=ttftt.schema.types["AType"].fields["B"],
                    schema=ttftt.schema,
                    path=["A", "B", 0],
                    location=Location(line=1, column=60,
                                      line_end=1, column_end=153, context=''),
                    execution_ctx=None,
                ),
            ),
            call(
                {"id": 2},
                {},
                {},
                Info(
                    query_field=None,
                    schema_field=ttftt.schema.types["AType"].fields["B"],
                    schema=ttftt.schema,
                    path=["A", "B", 1],
                    location=Location(line=1, column=60,
                                      line_end=1, column_end=153, context=''),
                    execution_ctx=None,
                ),
            )
        ],
        any_order=True
    )

    stuff_d.assert_has_calls(
        [
            call(
                {"id": 1},
                {},
                {},
                Info(
                    query_field=None,
                    schema_field=ttftt.schema.types["AType"].fields["D"],
                    schema=ttftt.schema,
                    path=["A", "D", 0],
                    location=Location(line=1, column=170,
                                      line_end=1, column_end=171, context=''),
                    execution_ctx=None,
                ),
            ),
            call(
                {"id": 2},
                {},
                {},
                Info(
                    query_field=None,
                    schema_field=ttftt.schema.types["AType"].fields["D"],
                    schema=ttftt.schema,
                    path=["A", "D", 1],
                    location=Location(line=1, column=170,
                                      line_end=1, column_end=171, context=''),
                    execution_ctx=None,
                ),
            )
        ],
        any_order=True
    )

    # TODO: improve test by replacing / wrapping default resolver
    # class default_resolver(Mock):
    #     async def __call__(self, parent, arguments, request_ctx, info: Info):
    #         super(default_resolver, self).__call__(parent, arguments, request_ctx, info)
    #         try:
    #             return getattr(parent, info.query_field.name)
    #         except:
    #             return {}
    # default_field.resolver.assert_has_calls(
    #     [
    #         call(
    #             {},
    #             Info(
    #                 parent_result={"id": 1},
    #                 path=['A', 'F', 0],
    #                 arguments={},
    #                 name='F',
    #                 field=default_field,
    #                 location=Location(line=1, column=206,
    #                                   line_end=1, column_end=299,
    #                                   context=''),
    #                 schema=ttftt.schema,
    #             )
    #         ),
    #         call(
    #             {},
    #             Info(
    #                 parent_result={"id": 1},
    #                 path=['A', 'E', 0],
    #                 arguments={},
    #                 name='E',
    #                 field=default_field,
    #                 location=Location(line=1, column=188,
    #                                   line_end=1, column_end=189,
    #                                   context=''),
    #                 schema=ttftt.schema,
    #             )
    #         ),
    #         call(
    #             {},
    #             Info(
    #                 parent_result={"id": 2},
    #                 path=['A', 'F', 1],
    #                 arguments={},
    #                 name='F',
    #                 field=default_field,
    #                 location=Location(line=1, column=206,
    #                                   line_end=1, column_end=299,
    #                                   context=''),
    #                 schema=ttftt.schema,
    #             )
    #         ),
    #         call(
    #             {},
    #             Info(
    #                 parent_result={"id": 2},
    #                 path=['A', 'E', 1],
    #                 arguments={},
    #                 name='E',
    #                 field=default_field,
    #                 location=Location(line=1, column=188,
    #                                   line_end=1, column_end=189,
    #                                   context=''),
    #                 schema=ttftt.schema,
    #             )
    #         ),
    #         call(
    #             {},
    #             Info(
    #                 parent_result=field_b.resolver.rtrn,
    #                 path=['A', 'B', 'C', 0],
    #                 arguments={},
    #                 name='C',
    #                 field=default_field,
    #                 location=Location(line=1, column=84,
    #                                   line_end=1, column_end=135,
    #                                   context=''),
    #                 schema=ttftt.schema,
    #             )
    #         ),
    #         call(
    #             {},
    #             Info(
    #                 parent_result=field_b.resolver.rtrn,
    #                 path=['A', 'B', 'C', 1],
    #                 arguments={},
    #                 name='C',
    #                 field=default_field,
    #                 location=Location(line=1, column=84,
    #                                   line_end=1, column_end=135,
    #                                   context=''),
    #                 schema=ttftt.schema,
    #             )
    #         ),
    #         call(
    #             {},
    #             Info(
    #                 parent_result={"id": "b.c"},
    #                 path=['A', 'B', 'C', 'K', 0],
    #                 arguments={},
    #                 name='K',
    #                 field=default_field,
    #                 location=Location(line=1, column=112,
    #                                   line_end=1, column_end=113,
    #                                   context=''),
    #                 schema=ttftt.schema,
    #             )
    #         ),
    #         call(
    #             {},
    #             Info(
    #                 parent_result={"id": "b.c"},
    #                 path=['A', 'B', 'C', 'K', 1],
    #                 arguments={},
    #                 name='K',
    #                 field=default_field,
    #                 location=Location(line=1, column=112,
    #                                   line_end=1, column_end=113,
    #                                   context=''),
    #                 schema=ttftt.schema,
    #             )
    #         ),
    #         call(
    #             {},
    #             Info(
    #                 parent_result={},
    #                 path=['A', 'F', 'H', 1],
    #                 arguments={},
    #                 name='H',
    #                 field=default_field,
    #                 location=Location(line=1, column=230,
    #                                   line_end=1, column_end=281,
    #                                   context=''),
    #                 schema=ttftt.schema,
    #             )
    #         ),
    #         call(
    #             {},
    #             Info(
    #                 parent_result={},
    #                 path=['A', 'F', 'H', 0],
    #                 arguments={},
    #                 name='H',
    #                 field=default_field,
    #                 location=Location(line=1, column=230,
    #                                   line_end=1, column_end=281,
    #                                   context=''),
    #                 schema=ttftt.schema,
    #             )
    #         ),
    #         call(
    #             {},
    #             Info(
    #                 parent_result={},
    #                 path=['A', 'F', 'H', 'I', 1],
    #                 arguments={},
    #                 name='I',
    #                 field=default_field,
    #                 location=Location(line=1, column=258,
    #                                   line_end=1, column_end=259,
    #                                   context=''),
    #                 schema=ttftt.schema,
    #             )
    #         ),
    #         call(
    #             {},
    #             Info(
    #                 parent_result={},
    #                 path=['A', 'F', 'H', 'I', 0],
    #                 arguments={},
    #                 name='I',
    #                 field=default_field,
    #                 location=Location(line=1, column=258,
    #                                   line_end=1, column_end=259,
    #                                   context=''),
    #                 schema=ttftt.schema,
    #             )
    #         ),
    #     ],
    #     any_order=True
    # )


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
        category: BookCategory
    }
    """

    ttftt = Tartiflette(schema_sdl)

    Library = namedtuple("Library", "books,authors")
    Author = namedtuple("Author", "name")
    Book = namedtuple("Book", "title,author,price,category")

    AuthorRudyardKipling = Author("Rudyard Kipling")
    AuthorHarperLee = Author("Harper Lee")
    AuthorLeoTolstoy = Author("Leo Tolstoy")
    AuthorJaneAustin = Author("Jane Austin")
    BookJungleBook = Book(title="The Jungle Book", author=AuthorRudyardKipling,
                          price=14.99, category="Adventure")
    BookToKillAMockingbird = Book(title="To Kill a Mockingbird",
                                  author=AuthorHarperLee, price=12.99,
                                  category="Fiction")
    BookAnnaKarenina = Book(title="Anna Karenina", author=AuthorLeoTolstoy,
                            price=19.99, category="Fiction")
    BookPrideAndPrejudice = Book(title="Pride and Prejudice", author=AuthorJaneAustin,
                            price=11.99, category="Romance")
    LibraryOne = Library(books=[
        BookAnnaKarenina,
        BookJungleBook,
        BookToKillAMockingbird,
    ], authors=[
        AuthorLeoTolstoy,
        AuthorHarperLee,
        AuthorRudyardKipling,
    ])
    LibraryTwo = Library(books=[
        BookPrideAndPrejudice,
        BookJungleBook,
    ], authors=[
        AuthorJaneAustin,
        AuthorRudyardKipling,
    ])

    @Resolver("Query.libraries", schema=ttftt.schema)
    async def func_field_libraries_resolver(parent, arguments, request_ctx, info: Info):
        return [LibraryOne, LibraryTwo]

    ttftt.schema.bake()
    result = await ttftt.execute("""
        query TestQueriesFromEnd2End{
            libraries {
                books {
                    title
                    author {
                        name
                    }
                    price
                    category
                }
                authors {
                    name
                }
            }
        }
        """)

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
                       }
                   ]
               }
           } == result
