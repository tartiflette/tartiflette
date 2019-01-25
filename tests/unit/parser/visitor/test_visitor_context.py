from unittest.mock import Mock, patch

import pytest

from tartiflette.parser.visitor.visitor_context import InternalVisitorContext


@pytest.mark.parametrize("args,expected", [(["a", "b"], "a(b)"), (["a"], "a")])
def test_visitor_context_create_node_name(args, expected):
    from tartiflette.parser.visitor.visitor_context import _create_node_name

    assert _create_node_name(*args) == expected


@pytest.mark.parametrize(
    "current_depth,type_cond_depth,inline_frag_info,current_type_condition,expected",
    [
        (1, 1, None, "A", "A"),
        (1, 0, None, "A", None),
        (1, 2, ("B", 1), None, None),
        (2, 2, ("B", 2), "B", "B"),
    ],
)
def test_visitor_context__compute_type_cond(
    current_depth,
    type_cond_depth,
    inline_frag_info,
    current_type_condition,
    expected,
):

    ifi = inline_frag_info
    if isinstance(ifi, tuple):
        ifi = Mock()
        ifi.type, ifi.depth = inline_frag_info

    ivc = InternalVisitorContext(
        field_path=["a"] * current_depth,
        inline_fragment_info=ifi,
        type_condition=current_type_condition,
    )

    assert ivc.compute_type_cond(type_cond_depth) == expected


@pytest.mark.parametrize(
    "current_path,libgraphql_type,name,expected",
    [
        ("", "FakeType", "nodeName", "/FakeType(nodeName)"),
        ("/Document", "FakeType", "nodeName", "/Document/FakeType(nodeName)"),
    ],
)
def test_visitor_context_move_in(
    current_path, libgraphql_type, name, expected
):
    def _my_create_node_name(a, b):
        return a + ("" if not b else "(" + b + ")")

    visitor_context = InternalVisitorContext(path=current_path)

    assert visitor_context.path == current_path

    element = Mock()
    element.libgraphql_type = libgraphql_type
    element.name = name

    with patch(
        "tartiflette.parser.visitor.visitor_context._create_node_name",
        side_effect=_my_create_node_name,
    ):
        visitor_context.move_in(element)

    assert visitor_context.path == expected


@pytest.mark.parametrize(
    "current_path,expected",
    [
        ("", ""),
        ("/Document", ""),
        ("/Document/FakeType(nodeName)", "/Document"),
    ],
)
def test_visitor_context_move_out(current_path, expected):
    visitor_context = InternalVisitorContext(path=current_path)

    assert visitor_context.path == current_path
    visitor_context.move_out()
    assert visitor_context.path == expected


@pytest.mark.parametrize(
    "current_field_path,element_name,expected",
    [
        ([], "fieldName", ["fieldName"]),
        (["rootField"], "fieldName", ["rootField", "fieldName"]),
    ],
)
def test_visitor_context_move_in_field(
    current_field_path, element_name, expected
):
    visitor_context = InternalVisitorContext(field_path=current_field_path)

    element = Mock()
    element.name = element_name

    field_mock = Mock()

    assert visitor_context.field_path == current_field_path
    visitor_context.move_in_field(element, field_mock)
    assert visitor_context.field_path == expected
    assert (
        visitor_context._fields[visitor_context._hashed_field_path]
        is field_mock
    )


_PARENT_NODE_MOCK = Mock()
_NODE_MOCK = Mock()
_NODE_MOCK.parent = _PARENT_NODE_MOCK


@pytest.mark.parametrize(
    "current_depth,current_field_path,current_node,expected_field_path,expected_node",
    [
        (0, [], _PARENT_NODE_MOCK, [], _PARENT_NODE_MOCK),
        (1, ["rootField"], _NODE_MOCK, [], _PARENT_NODE_MOCK),
        (
            2,
            ["rootField", "fieldName"],
            _NODE_MOCK,
            ["rootField"],
            _PARENT_NODE_MOCK,
        ),
    ],
)
def test_visitor_context_move_out_field(
    current_depth,
    current_field_path,
    current_node,
    expected_field_path,
    expected_node,
):
    field_mock = Mock()

    visitor_context = InternalVisitorContext(
        node=current_node,
        depth=current_depth,
        field_path=current_field_path,
        fields={"/".join(current_field_path): field_mock},
    )

    assert visitor_context.depth == current_depth
    assert visitor_context.field_path == current_field_path
    assert (
        visitor_context._fields[visitor_context._hashed_field_path]
        is field_mock
    )

    visitor_context.move_out_field()

    assert visitor_context._hashed_field_path not in visitor_context._fields
    assert visitor_context.field_path == expected_field_path
    assert visitor_context.node is expected_node


@pytest.mark.parametrize(
    "current_field_path,expected",
    [
        ([], ""),
        (["rootField"], "rootField"),
        (["rootField", "fieldName"], "rootField/fieldName"),
    ],
)
def test_visitor_context_hashed_field_path(current_field_path, expected):
    visitor_context = InternalVisitorContext(field_path=current_field_path)
    assert visitor_context._hashed_field_path == expected


_FIELD_1 = Mock()
_FIELD_2 = Mock()


@pytest.mark.parametrize(
    "current_field_path,expected",
    [([], None), (["field1"], _FIELD_1), (["rootField/field2"], _FIELD_2)],
)
def test_visitor_context_current_field(current_field_path, expected):
    visitor_context = InternalVisitorContext(
        field_path=current_field_path,
        fields={"field1": _FIELD_1, "rootField/field2": _FIELD_2},
    )
    assert visitor_context.current_field is expected
