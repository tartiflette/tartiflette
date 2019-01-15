from unittest.mock import Mock

import pytest


@pytest.mark.parametrize(
    "query, attr, expected",
    [
        ("query ab { lol{ name } }", None, None),
        ("query ab { lol(number: 1) { name } }", "get_value", 1),
        ('query ab { lol(str: "naa") { name }}', "get_value", "naa"),
        ("query ab { lol(flt: 3.6){ name }}", "get_value", 3.6),
        ("query ab { lol(bool: true){ name }}", "get_value", True),
        (
            "fragment ab on lol { name } query ab { lol{ ...ab } }",
            "get_type_condition",
            "lol",
        ),
        ("query ab($lol: Int = 3) { lol(a: $lol) }", "get_operation", "Query"),
        ("query ab($lol: Float = 3.6) { b: lol(a: $lol) }", "get_alias", "b"),
        ('query ab($lol: String = "fret") { lol(a: $lol) }', None, None),
        ("query ab($lol: Boolean = True) { lol(a: $lol) }", None, None),
        ("query ab { lol ... on ninja { name } }", "get_named_type", "ninja"),
        (
            "query ab { lol ...lol on ninja2 { name }}",
            "get_named_type",
            "ninja2",
        ),
    ],
)
def test_libgraphqlparser_parsing(query, attr, expected):
    from tartiflette.parser.cffi import Visitor
    from tartiflette.parser.cffi import LibGraphqlParser

    class myVisitor(Visitor):
        def update(self, event, element):
            if attr:
                try:
                    r = getattr(element, attr)()
                except AttributeError:
                    return

                assert r == expected

            assert element.get_location() is not None

    libgqlp = LibGraphqlParser()

    libgqlp.parse_and_visit(query, myVisitor())

    assert libgqlp.parse_and_jsonify(query) is not None


def test_libgraphqlparser_parsing_nok():
    from tartiflette.parser.cffi import Visitor
    from tartiflette.parser.cffi import LibGraphqlParser

    class myVisitor(Visitor):
        def update(self, event, element):
            pass

    libgqlp = LibGraphqlParser()

    with pytest.raises(Exception):
        libgqlp.parse_and_visit("query a {", myVisitor())


def test_cffi__visitor_element__get_name_string_nok():
    from tartiflette.parser.cffi import _VisitorElement
    from cffi import FFI

    ffi = FFI()

    ve = _VisitorElement(Mock(), ffi, "Name", ffi.NULL)

    assert ve.name is None


def test_cffi__visitor_element__get_type_condition_nok():
    from tartiflette.parser.cffi import _VisitorElementFragmentDefinition
    from cffi import FFI

    ffi = FFI()
    lib = Mock()
    lib.GraphQLAstFragmentDefinition_get_type_condition = Mock(
        return_value=ffi.NULL
    )

    ve = _VisitorElementFragmentDefinition(lib, ffi, ffi.NULL)

    assert ve.get_type_condition() is None


def test_cffi_libgqlparser_parse_and_visit_default_visitor():
    from tartiflette.parser.cffi import LibGraphqlParser

    libgqlparser = LibGraphqlParser()

    libgqlparser._lib = Mock()

    assert libgqlparser.parse_and_visit("query a { lol }") is None
