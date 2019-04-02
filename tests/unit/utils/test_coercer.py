from unittest.mock import Mock

import pytest


def test_resolver_factory__built_in_coercer():
    from tartiflette.utils.coercer import _built_in_coercer

    func = Mock(return_value="a")

    assert _built_in_coercer(func, 1, None) == "a"
    assert func.call_args_list == [((1,),)]


def test_resolver_factory__built_in_coercer_none_val():
    from tartiflette.utils.coercer import _built_in_coercer

    func = Mock(return_value="a")
    assert _built_in_coercer(func, None, None) is None
    assert func.called is False


def test_resolver_factory__object_coercer():
    from tartiflette.utils.coercer import _object_coercer

    assert _object_coercer(None, None, None) == None
    assert _object_coercer(None, Mock(), None) == {}


def test_resolver_factory__list_coercer():
    from tartiflette.utils.coercer import _list_coercer

    func = Mock(return_value="a")
    info = Mock()

    assert _list_coercer(func, "r", info) == ["a"]
    assert func.call_args_list == [(("r", info),)]


def test_resolver_factory__list_coercer_is_alist():
    from tartiflette.utils.coercer import _list_coercer

    func = Mock(return_value="a")
    info = Mock()

    assert _list_coercer(func, ["r", "d"], info) == ["a", "a"]
    assert func.call_args_list == [(("r", info),), (("d", info),)]


def test_resolver_factory__list_coercer_none_val():
    from tartiflette.utils.coercer import _list_coercer

    func = Mock(return_value="a")
    assert _list_coercer(func, None, None) is None
    assert func.called is False


def test_resolver_factory__not_null_coercer():
    from tartiflette.utils.coercer import _not_null_coercer

    func = Mock(return_value="a")
    info = Mock()

    assert _not_null_coercer(func, "T", info) == "a"
    assert func.call_args_list == [(("T", info),)]


def test_resolver_factory__not_null_coercer_none_value():
    from tartiflette.utils.coercer import _not_null_coercer
    from tartiflette.types.exceptions.tartiflette import NullError

    func = Mock(return_value="a")
    info = Mock()

    with pytest.raises(NullError):
        assert _not_null_coercer(func, None, info)
    assert func.called is False


def test_resolver_factory__get_type_coercers():
    from tartiflette.utils.coercer import _get_type_coercers
    from tartiflette.types.list import GraphQLList
    from tartiflette.types.non_null import GraphQLNonNull
    from tartiflette.utils.coercer import _list_coercer, _not_null_coercer

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
    from tartiflette.utils.coercer import _list_and_null_coercer
    from tartiflette.utils.coercer import _list_coercer, _not_null_coercer
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


def test_resolver_factory__enum_coercer_none():
    from tartiflette.utils.coercer import _enum_coercer

    assert _enum_coercer(None, None, None, None) is None


def test_resolver_factory__enum_coercer_raise():
    from tartiflette.utils.coercer import _enum_coercer
    from tartiflette.types.exceptions.tartiflette import InvalidValue

    with pytest.raises(InvalidValue):
        assert _enum_coercer([], None, 4, Mock())


def test_resolver_factory__enum_coercer():
    from tartiflette.utils.coercer import _enum_coercer

    a = Mock(return_value="TopTop")
    info = Mock()

    assert _enum_coercer([4], a, 4, info) == "TopTop"
    assert a.call_args_list == [((4, info),)]


@pytest.fixture
def scalar_mock():
    a_scalar = Mock()
    a_scalar.coerce_output = Mock()
    a_scalar.coerce_input = Mock()
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
    field = Mock()
    field.gql_type = "aType"
    field.schema = schema
    schema.find_enum = Mock(return_value=enum_mock)
    schema.find_scalar = Mock(return_value=scalar_mock)
    schema.find_type = Mock(return_value=field)

    return schema


@pytest.fixture
def field_mock(schema_mock):
    field = Mock()
    field.gql_type = "aType"
    field.schema = schema_mock

    return field


def test_resovler_factory__is_an_enum(schema_mock, scalar_mock):
    from tartiflette.utils.coercer import _is_an_enum
    from tartiflette.utils.coercer import _built_in_coercer
    from tartiflette.utils.coercer import _enum_coercer
    from tartiflette.utils.coercer import CoercerWay

    r = _is_an_enum("A", schema_mock, CoercerWay.OUTPUT)

    assert r.func is _enum_coercer
    assert schema_mock.find_scalar.call_args_list == [(("String",),)]
    a, b = r.args
    assert a == ["A", "B"]
    assert b.func == _built_in_coercer
    assert scalar_mock.coerce_output in b.args


def test_resovler_factory__is_an_enum_not():
    from tartiflette.utils.coercer import _is_an_enum
    from tartiflette.utils.coercer import CoercerWay

    sch = Mock()
    sch.find_enum = Mock(return_value=None)

    assert _is_an_enum("A", sch, CoercerWay.OUTPUT) is None


def test_resolver_factory__is_a_scalar(schema_mock, scalar_mock):
    from tartiflette.utils.coercer import _is_a_scalar
    from tartiflette.utils.coercer import _built_in_coercer
    from tartiflette.utils.coercer import CoercerWay

    schema_mock.find_enum = Mock(return_value=None)

    r = _is_a_scalar("A", schema_mock, CoercerWay.OUTPUT)

    assert schema_mock.find_scalar.call_args_list == [(("A",),)]

    assert r.func is _built_in_coercer
    assert scalar_mock.coerce_output in r.args


def test_resolver_factory__is_a_scalar_not():
    from tartiflette.utils.coercer import _is_a_scalar
    from tartiflette.utils.coercer import CoercerWay

    sch = Mock()
    sch.find_scalar = Mock(return_value=None)

    assert _is_a_scalar("A", sch, CoercerWay.OUTPUT) is None


def test_resolver_factory__get_coercer___Type():
    from tartiflette.utils.coercer import get_coercer
    from tartiflette.utils.coercer import _built_in_coercer
    from tartiflette.utils.coercer import _object_coercer

    field = Mock()
    field.gql_type = "__Type"

    c = get_coercer(field)

    assert c.func is _built_in_coercer
    a, = c.args
    assert a.func is _object_coercer
    assert a.args == (None,)


def test_resolver_factory__get_coercer(field_mock):
    from tartiflette.utils.coercer import get_coercer

    field_mock.schema.find_type = Mock(return_value=None)

    assert get_coercer(field_mock) is not None
    assert field_mock.schema.find_enum.call_args_list == [(("aType",),)]
    assert field_mock.schema.find_scalar.call_args_list == [(("String",),)]

    field_mock.schema.find_enum = Mock(return_value=None)

    assert get_coercer(field_mock) is not None
    assert field_mock.schema.find_enum.call_args_list == [(("aType",),)]
    assert field_mock.schema.find_scalar.call_args_list == [
        (("String",),),
        (("aType",),),
    ]

    field_mock.schema.find_scalar = Mock(return_value=None)

    assert get_coercer(field_mock) is not None
    assert field_mock.schema.find_enum.call_args_list == [
        (("aType",),),
        (("aType",),),
    ]
    assert field_mock.schema.find_scalar.call_args_list == [(("aType",),)]


def test_resolver_factory__get_coercer_not_ok(field_mock):
    from tartiflette.utils.coercer import get_coercer

    field_mock.schema.find_scalar = Mock(return_value=None)
    assert get_coercer(field_mock) is not None


def test_resolver_factory__get_coercer_no_schema():
    from tartiflette.utils.coercer import get_coercer

    f = Mock()
    f.schema = None

    assert get_coercer(f) is None


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
def test_coercer__is_union(find_type_mock, expected):
    from tartiflette.utils.coercer import _is_union

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
def test_coercer_factory__set_typename(res, typename, expected):
    from tartiflette.utils.coercer import _set_typename
    from tartiflette.types.helpers import get_typename

    assert _set_typename(res, typename) is None
    assert get_typename(res) == expected
