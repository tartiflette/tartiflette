from unittest.mock import Mock, patch

import pytest

from tartiflette.types.list import GraphQLList
from tartiflette.types.non_null import GraphQLNonNull


def test_resolver_factory__built_in_coercer():
    from tartiflette.resolver.factory import _built_in_coercer

    func = Mock(return_value="a")

    assert _built_in_coercer(func, 1, None) == "a"
    assert func.call_args_list == [((1,),)]


def test_resolver_factory__built_in_coercer_none_val():
    from tartiflette.resolver.factory import _built_in_coercer

    func = Mock(return_value="a")
    assert _built_in_coercer(func, None, None) is None
    assert func.called is False


def test_resolver_factory__object_coercer():
    from tartiflette.resolver.factory import _object_coercer

    assert _object_coercer(None, None, None) == None
    assert _object_coercer(None, Mock(), None) == {}


def test_resolver_factory__list_coercer():
    from tartiflette.resolver.factory import _list_coercer

    func = Mock(return_value="a")
    info = Mock()

    assert _list_coercer(func, "r", info) == ["a"]
    assert func.call_args_list == [(("r", info),)]


def test_resolver_factory__list_coercer_is_alist():
    from tartiflette.resolver.factory import _list_coercer

    func = Mock(return_value="a")
    info = Mock()

    assert _list_coercer(func, ["r", "d"], info) == ["a", "a"]
    assert func.call_args_list == [(("r", info),), (("d", info),)]


def test_resolver_factory__list_coercer_none_val():
    from tartiflette.resolver.factory import _list_coercer

    func = Mock(return_value="a")
    assert _list_coercer(func, None, None) is None
    assert func.called is False


def test_resolver_factory__not_null_coercer():
    from tartiflette.resolver.factory import _not_null_coercer

    func = Mock(return_value="a")
    info = Mock()

    assert _not_null_coercer(func, "T", info) == "a"
    assert func.call_args_list == [(("T", info),)]


def test_resolver_factory__not_null_coercer_none_value():
    from tartiflette.resolver.factory import _not_null_coercer
    from tartiflette.types.exceptions.tartiflette import NullError

    func = Mock(return_value="a")
    info = Mock()

    with pytest.raises(NullError):
        assert _not_null_coercer(func, None, info)
    assert func.called is False


def test_resolver_factory__get_type_coercers():
    from tartiflette.resolver.factory import _get_type_coercers
    from tartiflette.types.list import GraphQLList
    from tartiflette.types.non_null import GraphQLNonNull
    from tartiflette.resolver.factory import _list_coercer, _not_null_coercer

    assert _get_type_coercers("aType") == []
    assert _get_type_coercers(None) == []
    assert _get_type_coercers(GraphQLList(gql_type="aType")) == [_list_coercer]
    assert _get_type_coercers(GraphQLNonNull(gql_type="aType")) == [
        _not_null_coercer
    ]
    assert _get_type_coercers(
        GraphQLList(gql_type=GraphQLNonNull(gql_type="aType"))
    ) == [_list_coercer, _not_null_coercer]
    assert _get_type_coercers(
        GraphQLNonNull(
            gql_type=GraphQLList(gql_type=GraphQLNonNull(gql_type="aType"))
        )
    ) == [_not_null_coercer, _list_coercer, _not_null_coercer]


def test_resolver_factory__list_and_null_coercer():
    from tartiflette.resolver.factory import _list_and_null_coercer
    from tartiflette.resolver.factory import _list_coercer, _not_null_coercer
    from functools import partial
    from tartiflette.types.list import GraphQLList
    from tartiflette.types.non_null import GraphQLNonNull

    def lol():
        pass

    assert _list_and_null_coercer("aType", lol) is lol
    assert _list_and_null_coercer(None, lol) is lol

    a = _list_and_null_coercer(GraphQLList(gql_type="aType"), lol)

    assert a.func is _list_coercer
    assert lol in a.args

    a = _list_and_null_coercer(GraphQLNonNull(gql_type="aType"), lol)

    assert a.func is _not_null_coercer
    assert lol in a.args

    a = _list_and_null_coercer(
        GraphQLList(gql_type=GraphQLNonNull(gql_type="aType")), lol
    )

    assert a.func is _list_coercer
    a1, = a.args
    assert a1.func is _not_null_coercer
    assert lol in a1.args

    a = _list_and_null_coercer(
        GraphQLNonNull(
            gql_type=GraphQLList(gql_type=GraphQLNonNull(gql_type="aType"))
        ),
        lol,
    )

    assert a.func is _not_null_coercer
    a1, = a.args
    assert a1.func is _list_coercer
    a1, = a1.args
    assert a1.func is _not_null_coercer
    assert lol in a1.args


@pytest.mark.parametrize(
    "field_type,expected",
    [
        (GraphQLList(gql_type="aType"), True),
        (GraphQLNonNull(gql_type="aType"), False),
        (GraphQLNonNull(gql_type=GraphQLList(gql_type="aType")), True),
        (None, False),
    ],
)
def test_resolver_factory__shall_return_a_list(field_type, expected):
    from tartiflette.resolver.factory import _shall_return_a_list

    assert _shall_return_a_list(field_type) == expected


def test_resolver_factory__enum_coercer_none():
    from tartiflette.resolver.factory import _enum_coercer

    assert _enum_coercer(None, None, None, None) is None


def test_resolver_factory__enum_coercer_raise():
    from tartiflette.resolver.factory import _enum_coercer
    from tartiflette.types.exceptions.tartiflette import InvalidValue

    with pytest.raises(InvalidValue):
        assert _enum_coercer([], None, 4, Mock())


def test_resolver_factory__enum_coercer():
    from tartiflette.resolver.factory import _enum_coercer

    a = Mock(return_value="TopTop")
    info = Mock()

    assert _enum_coercer([4], a, 4, info) == "TopTop"
    assert a.call_args_list == [((4, info),)]


@pytest.fixture
def scalar_mock():
    a_scalar = Mock()
    a_scalar.coerce_output = Mock()
    return a_scalar


@pytest.fixture
def enum_mock():
    a_type = Mock()
    val_a = Mock()
    val_a.value = "A"
    val_b = Mock()
    val_b.value = "B"
    a_type.values = [val_a, val_b]
    return a_type


@pytest.fixture
def schema_mock(scalar_mock, enum_mock):
    schema = Mock()
    schema.find_enum = Mock(return_value=enum_mock)
    schema.find_scalar = Mock(return_value=scalar_mock)

    return schema


@pytest.fixture
def field_mock(schema_mock):
    field = Mock()
    field.gql_type = "aType"
    field.schema = schema_mock

    return field


def test_resovler_factory__is_an_enum(schema_mock, scalar_mock):
    from tartiflette.resolver.factory import _is_an_enum
    from tartiflette.resolver.factory import _built_in_coercer
    from tartiflette.resolver.factory import _enum_coercer

    r = _is_an_enum("A", schema_mock)

    assert r.func is _enum_coercer
    assert schema_mock.find_scalar.call_args_list == [(("String",),)]
    a, b = r.args
    assert a == ["A", "B"]
    assert b.func == _built_in_coercer
    assert scalar_mock.coerce_output in b.args


def test_resovler_factory__is_an_enum_not():
    from tartiflette.resolver.factory import _is_an_enum

    sch = Mock()
    sch.find_enum = Mock(return_value=None)

    assert _is_an_enum("A", sch) is None


def test_resolver_factory__is_a_scalar(schema_mock, scalar_mock):
    from tartiflette.resolver.factory import _is_a_scalar
    from tartiflette.resolver.factory import _built_in_coercer

    schema_mock.find_enum = Mock(return_value=None)

    r = _is_a_scalar("A", schema_mock)

    assert schema_mock.find_scalar.call_args_list == [(("A",),)]

    assert r.func is _built_in_coercer
    assert scalar_mock.coerce_output in r.args


def test_resolver_factory__is_a_scalar_not():
    from tartiflette.resolver.factory import _is_a_scalar

    sch = Mock()
    sch.find_scalar = Mock(return_value=None)

    assert _is_a_scalar("A", sch) is None


def test_resolver_factory__get_coercer___Type():
    from tartiflette.resolver.factory import _get_coercer
    from tartiflette.resolver.factory import _built_in_coercer
    from tartiflette.resolver.factory import _object_coercer

    field = Mock()
    field.gql_type = "__Type"

    c = _get_coercer(field)

    assert c.func is _built_in_coercer
    a, = c.args
    assert a.func is _object_coercer
    assert a.args == (None,)


def test_resolver_factory__get_coercer(field_mock):
    from tartiflette.resolver.factory import _get_coercer

    assert _get_coercer(field_mock) is not None
    assert field_mock.schema.find_enum.call_args_list == [(("aType",),)]
    assert field_mock.schema.find_scalar.call_args_list == [(("String",),)]

    field_mock.schema.find_enum = Mock(return_value=None)

    assert _get_coercer(field_mock) is not None
    assert field_mock.schema.find_enum.call_args_list == [(("aType",),)]
    assert field_mock.schema.find_scalar.call_args_list == [
        (("String",),),
        (("aType",),),
    ]

    field_mock.schema.find_scalar = Mock(return_value=None)

    assert _get_coercer(field_mock) is not None
    assert field_mock.schema.find_enum.call_args_list == [
        (("aType",),),
        (("aType",),),
    ]
    assert field_mock.schema.find_scalar.call_args_list == [(("aType",),)]


def test_resolver_factory__get_coercer_not_ok(field_mock):
    from tartiflette.resolver.factory import _get_coercer

    field_mock.schema.find_scalar = Mock(return_value=None)
    assert _get_coercer(field_mock) is not None


def test_resolver_factory__get_coercer_no_schema():
    from tartiflette.resolver.factory import _get_coercer

    f = Mock()
    f.schema = None

    assert _get_coercer(f) is None


def test_resolver_factory__surround_with_execution_directives():
    from tartiflette.resolver.factory import (
        _surround_with_execution_directives,
    )

    cllbs_a = Mock()
    cllbs_a.on_execution = Mock()
    cllbs_b = Mock()
    cllbs_b.on_execution = Mock()

    directives = [
        {"callables": cllbs_a, "args": {"a": "b"}},
        {"callables": cllbs_b, "args": {"c": "d"}},
    ]

    r = _surround_with_execution_directives("A", directives)
    assert r is not None
    assert r.func is cllbs_a.on_execution
    a, b = r.args
    assert a == {"a": "b"}
    assert b.func is cllbs_b.on_execution
    a, b = b.args
    assert a == {"c": "d"}
    assert b == "A"

    assert _surround_with_execution_directives("A", []) == "A"


def test_resolver_factory__introspection_directive_endpoint():
    from tartiflette.resolver.factory import _introspection_directive_endpoint

    assert _introspection_directive_endpoint("A") == "A"
    assert _introspection_directive_endpoint(None) is None


@pytest.fixture
def directive_list_mock():
    cllbs_a = Mock()
    cllbs_a.on_introspection = Mock(return_val="intro_a")
    cllbs_b = Mock()
    cllbs_b.on_introspection = Mock(return_val="intro_b")

    directives = [
        {"callables": cllbs_a, "args": {"a": "b"}},
        {"callables": cllbs_b, "args": {"c": "d"}},
    ]
    return directives


def test_resolver_factory__introspection_directives(directive_list_mock):
    from tartiflette.resolver.factory import _introspection_directives
    from tartiflette.resolver.factory import _introspection_directive_endpoint

    r = _introspection_directives(directive_list_mock)
    assert r is not None
    assert r.func is directive_list_mock[0]["callables"].on_introspection
    a, b = r.args
    assert a == directive_list_mock[0]["args"]
    assert b.func is directive_list_mock[1]["callables"].on_introspection
    a, b = b.args
    assert a == directive_list_mock[1]["args"]
    assert b is _introspection_directive_endpoint

    assert _introspection_directives([]) is _introspection_directive_endpoint


def test_resolver_factory__execute_introspection_directives(
    directive_list_mock
):
    from tartiflette.resolver.factory import _execute_introspection_directives

    elements = ["A", "B"]

    assert _execute_introspection_directives(elements) == elements

    elem = Mock()
    elem.directives = directive_list_mock

    assert _execute_introspection_directives([elem]) is not None
    directive_list_mock[0]["callables"].on_introspection.assert_called_once()


@pytest.mark.asyncio
async def test_resolver_factory_default_resolver():
    from tartiflette.resolver.factory import default_resolver

    info = Mock()
    info.schema_field = Mock()
    info.schema_field.name = "aField"

    assert await default_resolver(None, None, None, info) is None

    bob = Mock()
    bob.aField = "Lol"

    assert await default_resolver(bob, None, None, info) == "Lol"
    assert await default_resolver({"aField": "TTP"}, None, None, info) == "TTP"


def test_resolver_factory_resolver_executor_factory():
    from tartiflette.resolver.factory import ResolverExecutorFactory
    from tartiflette.resolver.factory import default_resolver

    field = Mock()
    field.gql_type = "aType"
    field.schema = None

    res_ex = ResolverExecutorFactory.get_resolver_executor("A", field)
    assert res_ex._raw_func == "A"
    assert res_ex._schema_field == field

    res_ex = ResolverExecutorFactory.get_resolver_executor(None, field)
    assert res_ex._raw_func is default_resolver
    assert res_ex._schema_field == field


_A_MOCKED_UNION = Mock()
_A_MOCKED_UNION.is_union = True
_A_MOCKED_FIELD = Mock()
_A_MOCKED_FIELD.is_union = False


@pytest.mark.parametrize(
    "find_type_mock,expected",
    [
        (Mock(return_value=_A_MOCKED_UNION), True),
        (Mock(side_effect=AttributeError), False),
        (Mock(side_effect=KeyError), False),
        (Mock(return_value=_A_MOCKED_FIELD), False),
    ],
)
def test_resolver_factory__is_union(find_type_mock, expected):
    from tartiflette.resolver.factory import _is_union

    schema = Mock()
    schema.find_type = find_type_mock

    assert _is_union("A", schema) == expected


_A_MOCKED_FIELD._typename = None


@pytest.mark.parametrize(
    "res,typename,expected",
    [
        (None, "a", "NoneType"),
        ("a", None, "str"),
        ({"a": 1}, "A", "A"),
        ({"a": 1, "_typename": "B"}, "A", "B"),
        ("A", "B", "str"),
        (_A_MOCKED_FIELD, "U", "U"),
    ],
)
def test_resolver_factory__set_typename(res, typename, expected):
    from tartiflette.resolver.factory import _set_typename
    from tartiflette.types.helpers import get_typename

    assert _set_typename(res, typename) is None
    assert get_typename(res) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "parent_result",
    [
        None,
        1,
        "value",
        {
            "none": None,
            "int": 1,
            "string": "value",
            "dict": {"value": "value"},
        },
    ],
)
async def test_default_subscription_resolver(parent_result):
    from tartiflette.resolver.factory import (
        default_resolver,
        default_subscription_resolver,
    )

    info = Mock()
    info.schema_field = Mock()
    info.schema_field.name = "myField"

    default_resolver_mock = Mock(wraps=default_resolver)

    subscription_resolver = default_subscription_resolver(
        default_resolver_mock
    )

    assert (
        await subscription_resolver(parent_result, None, None, info)
        == parent_result
    )

    default_resolver_mock.assert_called_once_with(
        {"myField": parent_result}, None, None, info
    )


_CUSTOM_DEFAULT_RESOLVER = lambda *args, **kwargs: {}


@pytest.mark.parametrize(
    (
        "is_subscription",
        "custom_default_resolver",
        "update_func_called",
        "default_subscription_resolver_called",
    ),
    [
        (False, None, False, False),
        (True, None, False, True),
        (False, _CUSTOM_DEFAULT_RESOLVER, True, False),
        (True, _CUSTOM_DEFAULT_RESOLVER, True, False),
    ],
)
def test_resolverexecutor_bake(
    is_subscription,
    custom_default_resolver,
    update_func_called,
    default_subscription_resolver_called,
):
    from tartiflette.resolver.factory import (
        _ResolverExecutor,
        default_resolver,
        default_subscription_resolver,
    )

    schema_field = Mock(schema=None)
    schema_field.subscribe = Mock() if is_subscription else None

    with patch(
        "tartiflette.resolver.factory.default_subscription_resolver",
        wraps=default_subscription_resolver,
    ) as default_subscription_resolver_mock:
        resolver_executor = _ResolverExecutor(default_resolver, schema_field)
        resolver_executor.update_coercer = Mock()
        resolver_executor.update_func = Mock(
            wraps=resolver_executor.update_func
        )
        resolver_executor.apply_directives = Mock()

        resolver_executor.bake(custom_default_resolver)

        resolver_executor.update_coercer.assert_called_once()

        if update_func_called:
            resolver_executor.update_func.assert_called_once_with(
                custom_default_resolver
            )
        else:
            resolver_executor.update_func.assert_not_called()

        if default_subscription_resolver_called:
            default_subscription_resolver_mock.assert_called_once_with(
                default_resolver
            )
        else:
            default_subscription_resolver_mock.assert_not_called()

        resolver_executor.apply_directives.assert_called_once()
