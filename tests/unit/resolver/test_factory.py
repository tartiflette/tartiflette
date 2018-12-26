from unittest.mock import Mock

import pytest


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

    assert _object_coercer(None, None, None) == {}


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


from tartiflette.types.list import GraphQLList
from tartiflette.types.non_null import GraphQLNonNull


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
    assert _object_coercer in c.args


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
