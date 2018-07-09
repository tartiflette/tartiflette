from collections import namedtuple
from typing import Any, List

import pytest
from unittest.mock import Mock, call

from tartiflette import Resolver
from tartiflette.executors.types import CoercedValue
from tartiflette.parser.nodes.field import ExecutionData
from tartiflette.schema import GraphQLSchema
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

    async def _resolver(ctx, exec_data):
        return {}

    def coerce_value(value: Any, execution_data: ExecutionData) -> (
        Any, List):
        return CoercedValue(value, None)

    field = Mock()
    field.name = "test"
    field.gql_type = GQLTypeMock(name="Object", coerce_value=coerce_value)
    field.resolver = _resolver
    GraphQLSchema.wrap_field_resolver(field)

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
async def test_calling_get_field_by_name_with_correct_value():
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
            A: AType
        }
        '''

    ttftt = Tartiflette(sdl=sdl)

    class default_resolver(Mock):
        async def __call__(self, ctx, exe):
            super(default_resolver, self).__call__(ctx, exe)
            try:
                return getattr(exe.parent_result, exe.name)
            except:
                return {}

    class resolver_a(Mock):
        async def __call__(self, ctx, exedata):
            super(resolver_a, self).__call__(ctx, exedata)
            return [{"id": 1}, {"id": 2}]

    stuff_a = resolver_a()

    @Resolver("Query.A", schema=ttftt.schema)
    async def wrap_1(ctx, exe):
        return await stuff_a(ctx, exe)

    class resolver_b(Mock):
        class resolver_b_result:
            def __init__(self):
                self.C = {"id": "b.c"}

            def __repr__(self):
                return "IAmABResults"

        def __init__(self, *args, **kwargs):
            super(resolver_b, self).__init__(*args, **kwargs)
            self.rtrn = resolver_b.resolver_b_result()

        async def __call__(self, ctx, exedata):
            super(resolver_b, self).__call__(ctx, exedata)
            return self.rtrn

    stuff_b = resolver_b()

    @Resolver("AType.B", schema=ttftt.schema)
    async def wrap_2(ctx, exe):
        return await stuff_b(ctx, exe)

    class resolver_d(Mock):

        @Resolver("AType.B", schema=ttftt.schema)
        async def __call__(self, ctx, exedata):
            super(resolver_d, self).__call__(ctx, exedata)
            return "ValueD"

    stuff_d = resolver_d()

    @Resolver("AType.D", schema=ttftt.schema)
    async def wrap_3(ctx, exe):
        return await stuff_d(ctx, exe)

    # TODO: Repair this test
    # field_a = Mock()
    # field_a.resolver = resolver_a()
    # field_a.gql_type = Mock()
    # field_a.gql_type.name = "Test"
    # field_a.gql_type.collect_value = simple_collect_value
    # field_a.name = "test"
    #
    # field_b = Mock()
    # field_b.resolver = resolver_b()
    # field_b.gql_type = Mock()
    # field_b.gql_type.name = "Test"
    # field_b.gql_type.collect_value = simple_collect_value
    # field_b.name = "test"
    #
    # field_d = Mock()
    # field_d.resolver = resolver_d()
    # field_d.gql_type = Mock()
    # field_d.gql_type.name = "Test"
    # field_d.gql_type.collect_value = simple_collect_value
    # field_d.name = "test"
    #
    # default_field = Mock()
    # default_field.resolver = default_resolver()
    # default_field.gql_type = Mock()
    # default_field.gql_type.name = "Test"
    # default_field.gql_type.collect_value = simple_collect_value
    # default_field.name = "test"

    # def get_field(name):
    #     fields = {"Query.A": field_a, "Test.B": field_b, "Test.D": field_d}
    #     return fields.get(name, default_field)

    # sdm = Mock()
    # sdm.query_type = "Query"
    # sdm.get_field_by_name = get_field

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
                ExecutionData(
                    parent_result={},
                    path=['A'],
                    arguments={},
                    name='A',
                    field=ttftt.schema.types["Query"].fields["A"],
                    location=Location(line=1, column=40,
                                      line_end=1, column_end=313, context=''),
                    schema=ttftt.schema,
                )
            )
        ],
        any_order=True,
    )

    stuff_b.assert_has_calls(
        [
            call(
                {},
                ExecutionData(
                    parent_result={"id": 1},
                    path=['A', 'B', 0],
                    arguments={},
                    name='B',
                    field=ttftt.schema.types["AType"].fields["B"],
                    location=Location(line=1, column=60,
                                      line_end=1, column_end=153,
                                      context=''),
                    schema=ttftt.schema,
                )
            ),
            call(
                {},
                ExecutionData(
                    parent_result={"id": 2},
                    path=['A', 'B', 1],
                    arguments={},
                    name='B',
                    field=ttftt.schema.types["AType"].fields["B"],
                    location=Location(line=1, column=60,
                                      line_end=1, column_end=153,
                                      context=''),
                    schema=ttftt.schema,
                )
            )
        ],
        any_order=True
    )

    stuff_d.assert_has_calls(
        [
            call(
                {},
                ExecutionData(
                    parent_result={"id": 1},
                    path=['A', 'D', 0],
                    arguments={},
                    name='D',
                    field=ttftt.schema.types["AType"].fields["D"],
                    location=Location(line=1, column=170,
                                      line_end=1, column_end=171,
                                      context=''),
                    schema=ttftt.schema,
                )
            ),
            call(
                {},
                ExecutionData(
                    parent_result={"id": 2},
                    path=['A', 'D', 1],
                    arguments={},
                    name='D',
                    field=ttftt.schema.types["AType"].fields["D"],
                    location=Location(line=1, column=170,
                                      line_end=1, column_end=171,
                                      context=''),
                    schema=ttftt.schema,
                )
            )
        ],
        any_order=True
    )

    # default_field.resolver.assert_has_calls(
    #     [
    #         call(
    #             {},
    #             ExecutionData(
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
    #             ExecutionData(
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
    #             ExecutionData(
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
    #             ExecutionData(
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
    #             ExecutionData(
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
    #             ExecutionData(
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
    #             ExecutionData(
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
    #             ExecutionData(
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
    #             ExecutionData(
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
    #             ExecutionData(
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
    #             ExecutionData(
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
    #             ExecutionData(
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
@pytest.mark.parametrize(
    'query, expected', [
        (
            """
            query LOL {
                A
            }
            """, '{"data":{"A":{"iam": "A"}}}'
        ), (
            """
            query a_request {
                A {
                    B
                    C
                    D
                    E {
                        F
                    }
                }
            }
            """,
            '{"data":{"A":{"iam": "A", "B": {"iam":"B"}, "C": {"iam":"C"}, "D": {"iam":"D"}, "E": {"iam":"E", "F":{"iam":"F"}}}}}'
        )
    ]
)
async def test_result_value(query, expected):
    import json
    from tartiflette.tartiflette import Tartiflette

    class default_resolver(Mock):
        async def __call__(self, ctx, exe):
            super(default_resolver, self).__call__(ctx, exe)
            return {"iam": exe.name}

    def coerce_value(value: Any, execution_data: ExecutionData) -> (
        Any, List):
        return CoercedValue(value, None)

    field = Mock()
    field.name = "test"
    field.gql_type = GQLTypeMock(name="Test", coerce_value=coerce_value)
    field.resolver = default_resolver()
    GraphQLSchema.wrap_field_resolver(field)

    def get_field_by_name(name):
        return field

    sdm = Mock()
    sdm.query_type = "Query"
    sdm.get_field_by_name = get_field_by_name
    sdm.types = {
        "Query": GQLTypeMock(name="Query", coerce_value=coerce_value),
    }

    ttftt = Tartiflette(schema=sdm)
    results = await ttftt.execute(query, context={}, variables={})

    assert json.loads(expected) == json.loads(results)
