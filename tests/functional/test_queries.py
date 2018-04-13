import pytest
from unittest.mock import Mock, call
from tartiflette.parser.nodes.field import ExecutionData


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

    field = Mock()
    field.name = "test"
    field.gql_type = "Object"
    field.resolver = _resolver

    sdm = Mock()
    sdm.query_type = "Query"
    sdm.get_field_by_name = Mock(return_value=field)

    ttftt = Tartiflette(schema_definition=sdm)
    await ttftt.execute(query, context={}, variables=varis)

    sdm.get_field_by_name.assert_has_calls(expected, any_order=False)


@pytest.mark.asyncio
async def test_calling_get_field_by_name_with_correct_value():
    class default_resolver(Mock):
        async def __call__(self, ctx, exe):
            super(default_resolver, self).__call__(ctx, exe)
            try:
                return getattr(exe.parent_result, exe.name)
            except:
                return {}

    from tartiflette.tartiflette import Tartiflette

    class resolver_a(Mock):
        async def __call__(self, ctx, exedata):
            super(resolver_a, self).__call__(ctx, exedata)
            return [{"id": 1}, {"id": 2}]

    class resolver_b(Mock):
        class resolver_b_result():
            def __init__(self):
                self.C = {"id": "b.c"}

            def __repr__(self):
                return "IAmABResults"

            def collect_value(self):
                return {"C": self.C}

        def __init__(self, *args, **kwargs):
            super(resolver_b, self).__init__(*args, **kwargs)
            self.rtrn = resolver_b.resolver_b_result()

        async def __call__(self, ctx, exedata):
            super(resolver_b, self).__call__(ctx, exedata)
            return self.rtrn

    class resolver_d(Mock):
        async def __call__(self, ctx, exedata):
            super(resolver_d, self).__call__(ctx, exedata)
            return "ValueD"

    field_a = Mock()
    field_a.resolver = resolver_a()
    field_a.gql_type = "Test"
    field_a.name = "test"

    field_b = Mock()
    field_b.resolver = resolver_b()
    field_b.gql_type = "Test"
    field_b.name = "test"

    field_d = Mock()
    field_d.resolver = resolver_d()
    field_d.gql_type = "Test"
    field_d.name = "test"

    default_field = Mock()
    default_field.resolver = default_resolver()
    default_field.gql_type = "Test"
    default_field.name = "test"

    def get_field(name):
        fields = {"Query.A": field_a, "Test.B": field_b, "Test.D": field_d}
        return fields.get(name, default_field)

    sdm = Mock()
    sdm.query_type = "Query"
    sdm.get_field_by_name = get_field

    ttftt = Tartiflette(schema_definition=sdm)
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

    field_a.resolver.assert_has_calls(
        [
            call(
                {},
                ExecutionData(
                    parent_result={},
                    path=['A'],
                    arguments={},
                    name='A',
                )
            )
        ],
        any_order=True,
    )

    field_b.resolver.assert_has_calls(
        [
            call(
                {},
                ExecutionData(
                    parent_result={"id": 1},
                    path=['A', 'B', 0],
                    arguments={},
                    name='B',
                )
            ),
            call(
                {},
                ExecutionData(
                    parent_result={"id": 2},
                    path=['A', 'B', 1],
                    arguments={},
                    name='B',
                )
            )
        ],
        any_order=True
    )

    field_d.resolver.assert_has_calls(
        [
            call(
                {},
                ExecutionData(
                    parent_result={"id": 1},
                    path=['A', 'D', 0],
                    arguments={},
                    name='D',
                )
            ),
            call(
                {},
                ExecutionData(
                    parent_result={"id": 2},
                    path=['A', 'D', 1],
                    arguments={},
                    name='D',
                )
            )
        ],
        any_order=True
    )

    default_field.resolver.assert_has_calls(
        [
            call(
                {},
                ExecutionData(
                    parent_result={"id": 1},
                    path=['A', 'F', 0],
                    arguments={},
                    name='F',
                )
            ),
            call(
                {},
                ExecutionData(
                    parent_result={"id": 1},
                    path=['A', 'E', 0],
                    arguments={},
                    name='E',
                )
            ),
            call(
                {},
                ExecutionData(
                    parent_result={"id": 2},
                    path=['A', 'F', 1],
                    arguments={},
                    name='F',
                )
            ),
            call(
                {},
                ExecutionData(
                    parent_result={"id": 2},
                    path=['A', 'E', 1],
                    arguments={},
                    name='E',
                )
            ),
            call(
                {},
                ExecutionData(
                    parent_result=field_b.resolver.rtrn,
                    path=['A', 'B', 'C', 0],
                    arguments={},
                    name='C',
                )
            ),
            call(
                {},
                ExecutionData(
                    parent_result=field_b.resolver.rtrn,
                    path=['A', 'B', 'C', 1],
                    arguments={},
                    name='C',
                )
            ),
            call(
                {},
                ExecutionData(
                    parent_result={"id": "b.c"},
                    path=['A', 'B', 'C', 'K', 0],
                    arguments={},
                    name='K',
                )
            ),
            call(
                {},
                ExecutionData(
                    parent_result={"id": "b.c"},
                    path=['A', 'B', 'C', 'K', 1],
                    arguments={},
                    name='K',
                )
            ),
            call(
                {},
                ExecutionData(
                    parent_result={},
                    path=['A', 'F', 'H', 1],
                    arguments={},
                    name='H',
                )
            ),
            call(
                {},
                ExecutionData(
                    parent_result={},
                    path=['A', 'F', 'H', 0],
                    arguments={},
                    name='H',
                )
            ),
            call(
                {},
                ExecutionData(
                    parent_result={},
                    path=['A', 'F', 'H', 'I', 1],
                    arguments={},
                    name='I',
                )
            ),
            call(
                {},
                ExecutionData(
                    parent_result={},
                    path=['A', 'F', 'H', 'I', 0],
                    arguments={},
                    name='I',
                )
            ),
        ],
        any_order=True
    )


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

    field = Mock()
    field.gql_type = "Test"
    field.name = "test"
    field.resolver = default_resolver()

    def get_field_by_name(name):
        return field

    sdm = Mock()
    sdm.query_type = "Query"
    sdm.get_field_by_name = get_field_by_name

    ttftt = Tartiflette(schema_definition=sdm)
    results = await ttftt.execute(query, context={}, variables={})

    assert json.loads(results) == json.loads(expected)
