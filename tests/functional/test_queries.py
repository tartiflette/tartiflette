import pytest
from unittest.mock import Mock, call
from tests.functional.utils import AsyncMock
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
                        H {
                            I
                        }
                    }
                }
            }
            """, {}, [
                call("A"),
                call("B"),
                call("C"),
                call("D"),
                call("E"),
                call("F"),
                call("H"),
                call("I")
            ]
        )
    ],
    ids=["Simple Order"]
)
async def test_get_resolver_call_order(query, varis, expected):
    from tartiflette.tartiflette import Tartiflette

    async def _resolver(ctx, exec_data):
        pass

    sdm = Mock()
    sdm.get_resolver = Mock(return_value=_resolver)

    ttftt = Tartiflette(schema_definition=sdm)
    await ttftt.execute(query, context={}, variables=varis)

    sdm.get_resolver.assert_has_calls(expected, any_order=False)


@pytest.mark.asyncio
async def test_calling_resolver_with_correct_value(monkeypatch):
    import tartiflette.parser.visitor

    class default_resolver(Mock):
        async def __call__(self, ctx, exe):
            super(default_resolver, self).__call__(ctx, exe)
            try:
                return getattr(exe.parent_result, exe.name)
            except:
                return {}

    _default_resolver = default_resolver()

    monkeypatch.setattr(
        tartiflette.parser.visitor, "_default_resolver", _default_resolver
    )

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

            def as_ttftt_dict(self):
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

    rslvr_a = resolver_a()
    rslvr_b = resolver_b()
    rslvr_d = resolver_d()

    def get_resolver(name):
        resolvers = {"A": rslvr_a, "B": rslvr_b, "D": rslvr_d}
        return resolvers[name]

    sdm = Mock()
    sdm.get_resolver = get_resolver

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

    rslvr_a.assert_has_calls(
        [
            call(
                {},
                ExecutionData(
                    parent_result={},
                    path='/Document/OperationDefinition(a_request)/Field(A)',
                    arguments={},
                    name='A'
                )
            )
        ],
        any_order=True
    )

    rslvr_b.assert_has_calls(
        [
            call(
                {},
                ExecutionData(
                    parent_result={"id": 1},
                    path=
                    '/Document/OperationDefinition(a_request)/Field(A)/Field(B)[0]',
                    arguments={},
                    name='B'
                )
            ),
            call(
                {},
                ExecutionData(
                    parent_result={"id": 2},
                    path=
                    '/Document/OperationDefinition(a_request)/Field(A)/Field(B)[1]',
                    arguments={},
                    name='B'
                )
            )
        ],
        any_order=True
    )

    rslvr_d.assert_has_calls(
        [
            call(
                {},
                ExecutionData(
                    parent_result={"id": 1},
                    path=
                    '/Document/OperationDefinition(a_request)/Field(A)/Field(D)[0]',
                    arguments={},
                    name='D'
                )
            ),
            call(
                {},
                ExecutionData(
                    parent_result={"id": 2},
                    path=
                    '/Document/OperationDefinition(a_request)/Field(A)/Field(D)[1]',
                    arguments={},
                    name='D'
                )
            )
        ],
        any_order=True
    )

    _default_resolver.assert_has_calls(
        [
            call(
                {},
                ExecutionData(
                    parent_result={"id": 1},
                    path=
                    '/Document/OperationDefinition(a_request)/Field(A)/Field(F)[0]',
                    arguments={},
                    name='F'
                )
            ),
            call(
                {},
                ExecutionData(
                    parent_result={"id": 1},
                    path=
                    '/Document/OperationDefinition(a_request)/Field(A)/Field(E)[0]',
                    arguments={},
                    name='E'
                )
            ),
            call(
                {},
                ExecutionData(
                    parent_result={"id": 2},
                    path=
                    '/Document/OperationDefinition(a_request)/Field(A)/Field(F)[1]',
                    arguments={},
                    name='F'
                )
            ),
            call(
                {},
                ExecutionData(
                    parent_result={"id": 2},
                    path=
                    '/Document/OperationDefinition(a_request)/Field(A)/Field(E)[1]',
                    arguments={},
                    name='E'
                )
            ),
            call(
                {},
                ExecutionData(
                    parent_result=rslvr_b.rtrn,
                    path=
                    '/Document/OperationDefinition(a_request)/Field(A)/Field(B)/Field(C)[0]',
                    arguments={},
                    name='C'
                )
            ),
            call(
                {},
                ExecutionData(
                    parent_result=rslvr_b.rtrn,
                    path=
                    '/Document/OperationDefinition(a_request)/Field(A)/Field(B)/Field(C)[1]',
                    arguments={},
                    name='C'
                )
            ),
            call(
                {},
                ExecutionData(
                    parent_result={"id": "b.c"},
                    path=
                    '/Document/OperationDefinition(a_request)/Field(A)/Field(B)/Field(C)/Field(K)[0]',
                    arguments={},
                    name='K'
                )
            ),
            call(
                {},
                ExecutionData(
                    parent_result={"id": "b.c"},
                    path=
                    '/Document/OperationDefinition(a_request)/Field(A)/Field(B)/Field(C)/Field(K)[1]',
                    arguments={},
                    name='K'
                )
            ),
            call(
                {},
                ExecutionData(
                    parent_result={},
                    path=
                    '/Document/OperationDefinition(a_request)/Field(A)/Field(F)/Field(H)[1]',
                    arguments={},
                    name='H'
                )
            ),
            call(
                {},
                ExecutionData(
                    parent_result={},
                    path=
                    '/Document/OperationDefinition(a_request)/Field(A)/Field(F)/Field(H)[0]',
                    arguments={},
                    name='H'
                )
            ),
            call(
                {},
                ExecutionData(
                    parent_result={},
                    path=
                    '/Document/OperationDefinition(a_request)/Field(A)/Field(F)/Field(H)/Field(I)[1]',
                    arguments={},
                    name='I'
                )
            ),
            call(
                {},
                ExecutionData(
                    parent_result={},
                    path=
                    '/Document/OperationDefinition(a_request)/Field(A)/Field(F)/Field(H)/Field(I)[0]',
                    arguments={},
                    name='I'
                )
            ),
        ],
        any_order=True
    )

    monkeypatch.undo()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'query, expected', [
        (
            """
            query LOL {
                A
            }
            """, '{"A":{"iam": "A"}}'
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
            '{"A":{"iam": "A", "B": {"iam":"B"}, "C": {"iam":"C"}, "D": {"iam":"D"}, "E": {"iam":"E", "F":{"iam":"F"}}}}'
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

    _default_resolver = default_resolver()

    def get_resolver(name):
        return _default_resolver

    sdm = Mock()
    sdm.get_resolver = get_resolver

    ttftt = Tartiflette(schema_definition=sdm)
    results = await ttftt.execute(query, context={}, variables={})

    assert json.loads(results) == json.loads(expected)
