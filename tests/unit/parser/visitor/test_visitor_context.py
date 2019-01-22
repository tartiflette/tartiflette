from unittest.mock import Mock

import pytest


@pytest.mark.parametrize("args,expected", [(["a", "b"], "a(b)"), (["a"], "a")])
def test_parser_visitor_create_node_name(args, expected):
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
def test_parser_visitor__compute_type_cond(
    current_depth,
    type_cond_depth,
    inline_frag_info,
    current_type_condition,
    expected,
):
    from tartiflette.parser.visitor.visitor_context import (
        InternalVisitorContext,
    )

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
