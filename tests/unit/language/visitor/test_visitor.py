import json
import os

from unittest.mock import Mock

import pytest

from tartiflette import UNDEFINED_VALUE
from tartiflette.language.ast import (
    DocumentNode,
    FieldNode,
    NameNode,
    OperationDefinitionNode,
    SelectionSetNode,
)
from tartiflette.language.ast.base import Node
from tartiflette.language.parsers.libgraphqlparser import parse_to_document
from tartiflette.language.visitor.constants import (
    BREAK,
    OK,
    QUERY_DOCUMENT_KEYS,
    REMOVE,
    SKIP,
)
from tartiflette.language.visitor.visit import visit
from tartiflette.language.visitor.visitor import ParallelVisitor, Visitor

_BASE_DIR = os.path.dirname(__file__)

_SCHEMA_MOCK = Mock()
_SCHEMA_MOCK.json_loader = json.loads


def check_visitor_fn_args(
    ast, node, key, parent, path, ancestors, is_edited=False
):
    assert isinstance(node, Node)

    is_root = key is None
    if is_root:
        if not is_edited:
            assert node is ast
        assert parent is None
        assert path == []
        assert ancestors == []
        return

    assert isinstance(key, (int, str))

    if isinstance(key, str):
        assert isinstance(parent, Node)
        assert hasattr(parent, key)
    else:
        assert isinstance(parent, list)
        assert 0 <= key <= len(parent)

    assert isinstance(path, list)
    assert path[-1] == key

    assert isinstance(ancestors, list)
    assert len(ancestors) == len(path) - 1

    if not is_edited:
        current_node = ast
        for index, ancestors in enumerate(ancestors):
            assert ancestors is current_node
            path_key = path[index]
            assert isinstance(path_key, (int, str))
            if isinstance(path_key, int):
                assert isinstance(current_node, list)
                assert 0 <= path_key <= len(current_node)
                current_node = current_node[path_key]
            else:
                assert isinstance(current_node, Node)
                assert hasattr(current_node, path_key)
                current_node = getattr(current_node, path_key)
            assert current_node is not None

        assert parent is current_node
        if isinstance(key, int):
            assert parent[key] is node
        else:
            assert getattr(parent, key) is node


def get_value(node):
    return node.value if hasattr(node, "value") else UNDEFINED_VALUE


def test_visit_invalid_node():
    class NotNode:
        def __str__(self):
            return "Sorry, I'm not a node."

    class MyVisitor(Visitor):
        def __init__(self):
            self.visited = []

        def enter(self, node, key, parent, path, ancestors):
            self.visited.append(("enter", node.__class__.__name__, path[:]))

        def leave(self, node, key, parent, path, ancestors):
            self.visited.append(("leave", node.__class__.__name__, path[:]))

    visitor = MyVisitor()
    assert visitor.visited == []

    with pytest.raises(
        Exception, match=f"Invalid AST node: < Sorry, I'm not a node. >.",
    ):
        visit(
            DocumentNode(
                definitions=[
                    OperationDefinitionNode(
                        operation_type="query",
                        selection_set=SelectionSetNode(
                            selections=[
                                FieldNode(name=NameNode(value="a")),
                                NotNode(),
                            ],
                        ),
                    )
                ],
            ),
            visitor,
        )

    assert visitor.visited == [
        ("enter", "DocumentNode", []),
        ("enter", "OperationDefinitionNode", ["definitions", 0]),
        ("enter", "SelectionSetNode", ["definitions", 0, "selection_set"]),
        (
            "enter",
            "FieldNode",
            ["definitions", 0, "selection_set", "selections", 0],
        ),
        (
            "enter",
            "NameNode",
            ["definitions", 0, "selection_set", "selections", 0, "name"],
        ),
        (
            "leave",
            "NameNode",
            ["definitions", 0, "selection_set", "selections", 0, "name"],
        ),
        (
            "leave",
            "FieldNode",
            ["definitions", 0, "selection_set", "selections", 0],
        ),
    ]


def test_validates_path_argument():
    class MyVisitor(Visitor):
        def __init__(self, ast):
            self.ast = ast
            self.visited = []

        def enter(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            self.visited.append(("enter", path[:]))

        def leave(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            self.visited.append(("leave", path[:]))

    ast = parse_to_document("{ a }", _SCHEMA_MOCK)
    visitor = MyVisitor(ast)
    assert visitor.visited == []
    visit(ast, visitor)
    assert visitor.visited == [
        ("enter", []),
        ("enter", ["definitions", 0]),
        ("enter", ["definitions", 0, "selection_set"]),
        ("enter", ["definitions", 0, "selection_set", "selections", 0]),
        (
            "enter",
            ["definitions", 0, "selection_set", "selections", 0, "name"],
        ),
        (
            "leave",
            ["definitions", 0, "selection_set", "selections", 0, "name"],
        ),
        ("leave", ["definitions", 0, "selection_set", "selections", 0]),
        ("leave", ["definitions", 0, "selection_set"]),
        ("leave", ["definitions", 0]),
        ("leave", []),
    ]


def test_validates_ancestors_argument():
    class MyVisitor(Visitor):
        def __init__(self, ast):
            self.ast = ast
            self.visited = []

        def enter(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            if isinstance(key, int):
                self.visited.append(parent)
            self.visited.append(node)
            assert ancestors == self.visited[0:-2]
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)

        def leave(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            assert ancestors == self.visited[0:-2]
            if isinstance(key, int):
                self.visited.pop()
            self.visited.pop()

    ast = parse_to_document("{ a }", _SCHEMA_MOCK)
    visit(ast, MyVisitor(ast))


def test_allows_visiting_only_specified_nodes():
    class MyVisitor(Visitor):
        def __init__(self, ast):
            self.ast = ast
            self.visited = []

        def enter_Field(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            self.visited.append(("enter", node.__class__.__name__))

        def leave_Field(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            self.visited.append(("leave", node.__class__.__name__))

    ast = parse_to_document("{ a }", _SCHEMA_MOCK)
    visitor = MyVisitor(ast)
    assert visitor.visited == []
    visit(ast, visitor)
    assert visitor.visited == [
        ("enter", "FieldNode"),
        ("leave", "FieldNode"),
    ]


def test_allows_editing_a_node_both_on_enter_and_on_leave():
    class MyVisitor(Visitor):
        def __init__(self, ast):
            self.ast = ast
            self.visited = []
            self.selection_set = None

        def enter_OperationDefinition(
            self, node, key, parent, path, ancestors
        ):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            assert len(node.selection_set.selections) == 3
            self.selection_set = node.selection_set
            node.selection_set = SelectionSetNode(selections=[])
            self.visited.append(("enter", node.__class__.__name__))
            return node

        def leave_OperationDefinition(
            self, node, key, parent, path, ancestors
        ):
            check_visitor_fn_args(
                self.ast, node, key, parent, path, ancestors, is_edited=True
            )
            assert len(node.selection_set.selections) == 0
            node.selection_set = self.selection_set
            self.visited.append(("leave", node.__class__.__name__))
            return node

    ast = parse_to_document("{ a, b, c { a, b, c } }", _SCHEMA_MOCK)
    visitor = MyVisitor(ast)
    assert visitor.visited == []
    edited_ast = visit(ast, visitor)
    assert edited_ast == ast
    assert visitor.visited == [
        ("enter", "OperationDefinitionNode"),
        ("leave", "OperationDefinitionNode"),
    ]


def test_allows_editing_the_root_node_on_enter_and_on_leave():
    class MyVisitor(Visitor):
        def __init__(self, ast):
            self.ast = ast
            self.visited = []
            self.definitions = None

        def enter_Document(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            assert len(node.definitions) == 1
            self.definitions = node.definitions
            node.definitions = []
            self.visited.append(("enter", node.__class__.__name__))
            return node

        def leave_Document(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(
                self.ast, node, key, parent, path, ancestors, is_edited=True
            )
            assert len(node.definitions) == 0
            node.definitions = self.definitions
            self.visited.append(("leave", node.__class__.__name__))
            return node

    ast = parse_to_document("{ a, b, c { a, b, c } }", _SCHEMA_MOCK)
    visitor = MyVisitor(ast)
    assert visitor.visited == []
    edited_ast = visit(ast, visitor)
    assert edited_ast == ast
    assert visitor.visited == [
        ("enter", "DocumentNode"),
        ("leave", "DocumentNode"),
    ]


def test_allows_for_editing_on_enter():
    class MyVisitor(Visitor):
        def __init__(self, ast):
            self.ast = ast

        def enter(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            return (
                REMOVE
                if isinstance(node, FieldNode) and node.name.value == "b"
                else OK
            )

    ast = parse_to_document("{ a, b, c { a, b, c } }", _SCHEMA_MOCK)
    visitor = MyVisitor(ast)
    edited_ast = visit(ast, visitor)
    assert ast == parse_to_document("{ a, b, c { a, b, c } }", _SCHEMA_MOCK)
    assert edited_ast == parse_to_document(
        "{ a,    c { a,    c } }", _SCHEMA_MOCK
    )


def test_allows_for_editing_on_leave():
    class MyVisitor(Visitor):
        def __init__(self, ast):
            self.ast = ast

        def leave(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(
                self.ast, node, key, parent, path, ancestors, is_edited=True
            )
            return (
                REMOVE
                if isinstance(node, FieldNode) and node.name.value == "b"
                else OK
            )

    ast = parse_to_document("{ a, b, c { a, b, c } }", _SCHEMA_MOCK)
    visitor = MyVisitor(ast)
    edited_ast = visit(ast, visitor)
    assert ast == parse_to_document("{ a, b, c { a, b, c } }", _SCHEMA_MOCK)
    assert edited_ast == parse_to_document(
        "{ a,    c { a,    c } }", _SCHEMA_MOCK
    )


def test_ignores_false_returned_on_leave():
    class MyVisitor(Visitor):
        def __init__(self, ast):
            self.ast = ast

        def leave(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            return SKIP

    ast = parse_to_document("{ a, b, c { a, b, c } }", _SCHEMA_MOCK)
    visitor = MyVisitor(ast)
    edited_ast = visit(ast, visitor)
    assert edited_ast == ast


def test_visits_edited_node():
    added_field = FieldNode(name=NameNode(value="__typename"))

    class MyVisitor(Visitor):
        def __init__(self, ast):
            self.ast = ast
            self.did_visit_added_field = False

        def enter(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(
                self.ast, node, key, parent, path, ancestors, is_edited=True
            )
            if isinstance(node, FieldNode) and node.name.value == "a":
                if not node.selection_set:
                    node.selection_set = SelectionSetNode(
                        selections=[added_field]
                    )
                else:
                    node.selection_set.selections.insert(0, added_field)
                return node
            if node is added_field:
                self.did_visit_added_field = True

    ast = parse_to_document("{ a, b, c { a, b, c } }", _SCHEMA_MOCK)
    visitor = MyVisitor(ast)
    assert not visitor.did_visit_added_field
    visit(ast, visitor)
    assert visitor.did_visit_added_field


def test_allows_skipping_a_sub_tree():
    class MyVisitor(Visitor):
        def __init__(self, ast):
            self.ast = ast
            self.visited = []

        def enter(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            self.visited.append(
                ("enter", node.__class__.__name__, get_value(node))
            )
            if isinstance(node, FieldNode) and node.name.value == "b":
                return SKIP

        def leave(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            self.visited.append(
                ("leave", node.__class__.__name__, get_value(node))
            )

    ast = parse_to_document("{ a, b { x }, c }", _SCHEMA_MOCK)
    visitor = MyVisitor(ast)
    assert visitor.visited == []
    visit(ast, visitor)
    assert visitor.visited == [
        ("enter", "DocumentNode", UNDEFINED_VALUE),
        ("enter", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("enter", "FieldNode", UNDEFINED_VALUE),
        ("enter", "NameNode", "a"),
        ("leave", "NameNode", "a"),
        ("leave", "FieldNode", UNDEFINED_VALUE),
        ("enter", "FieldNode", UNDEFINED_VALUE),
        ("enter", "FieldNode", UNDEFINED_VALUE),
        ("enter", "NameNode", "c"),
        ("leave", "NameNode", "c"),
        ("leave", "FieldNode", UNDEFINED_VALUE),
        ("leave", "SelectionSetNode", UNDEFINED_VALUE),
        ("leave", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("leave", "DocumentNode", UNDEFINED_VALUE),
    ]


def test_allows_early_exit_while_visiting():
    class MyVisitor(Visitor):
        def __init__(self, ast):
            self.ast = ast
            self.visited = []

        def enter(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            self.visited.append(
                ("enter", node.__class__.__name__, get_value(node))
            )
            if isinstance(node, NameNode) and node.value == "x":
                return BREAK

        def leave(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            self.visited.append(
                ("leave", node.__class__.__name__, get_value(node))
            )

    ast = parse_to_document("{ a, b { x }, c }", _SCHEMA_MOCK)
    visitor = MyVisitor(ast)
    assert visitor.visited == []
    visit(ast, visitor)
    assert visitor.visited == [
        ("enter", "DocumentNode", UNDEFINED_VALUE),
        ("enter", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("enter", "FieldNode", UNDEFINED_VALUE),
        ("enter", "NameNode", "a"),
        ("leave", "NameNode", "a"),
        ("leave", "FieldNode", UNDEFINED_VALUE),
        ("enter", "FieldNode", UNDEFINED_VALUE),
        ("enter", "NameNode", "b"),
        ("leave", "NameNode", "b"),
        ("enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("enter", "FieldNode", UNDEFINED_VALUE),
        ("enter", "NameNode", "x"),
    ]


def test_allows_early_exit_while_leaving():
    class MyVisitor(Visitor):
        def __init__(self, ast):
            self.ast = ast
            self.visited = []

        def enter(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            self.visited.append(
                ("enter", node.__class__.__name__, get_value(node))
            )

        def leave(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            self.visited.append(
                ("leave", node.__class__.__name__, get_value(node))
            )
            if isinstance(node, NameNode) and node.value == "x":
                return BREAK

    ast = parse_to_document("{ a, b { x }, c }", _SCHEMA_MOCK)
    visitor = MyVisitor(ast)
    assert visitor.visited == []
    visit(ast, visitor)
    assert visitor.visited == [
        ("enter", "DocumentNode", UNDEFINED_VALUE),
        ("enter", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("enter", "FieldNode", UNDEFINED_VALUE),
        ("enter", "NameNode", "a"),
        ("leave", "NameNode", "a"),
        ("leave", "FieldNode", UNDEFINED_VALUE),
        ("enter", "FieldNode", UNDEFINED_VALUE),
        ("enter", "NameNode", "b"),
        ("leave", "NameNode", "b"),
        ("enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("enter", "FieldNode", UNDEFINED_VALUE),
        ("enter", "NameNode", "x"),
        ("leave", "NameNode", "x"),
    ]


def test_allows_a_named_functions_visitor_api():
    class MyVisitor(Visitor):
        def __init__(self, ast):
            self.ast = ast
            self.visited = []

        def enter_Name(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            self.visited.append(
                ("enter", node.__class__.__name__, get_value(node))
            )

        def enter_SelectionSet(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            self.visited.append(
                ("enter", node.__class__.__name__, get_value(node))
            )

        def leave_SelectionSet(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            self.visited.append(
                ("leave", node.__class__.__name__, get_value(node))
            )

    ast = parse_to_document("{ a, b { x }, c }", _SCHEMA_MOCK)
    visitor = MyVisitor(ast)
    assert visitor.visited == []
    visit(ast, visitor)
    assert visitor.visited == [
        ("enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("enter", "NameNode", "a"),
        ("enter", "NameNode", "b"),
        ("enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("enter", "NameNode", "x"),
        ("leave", "SelectionSetNode", UNDEFINED_VALUE),
        ("enter", "NameNode", "c"),
        ("leave", "SelectionSetNode", UNDEFINED_VALUE),
    ]


def tests_visits_kitchen_sink():
    class MyVisitor(Visitor):
        def __init__(self, ast):
            self.ast = ast
            self.visited = []
            self.args_stack = []

        def enter(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            self.visited.append(
                (
                    "enter",
                    node.__class__.__name__,
                    key,
                    (
                        parent.__class__.__name__
                        if isinstance(parent, Node)
                        else UNDEFINED_VALUE
                    ),
                )
            )
            self.args_stack.append((node, key, parent, path, ancestors))

        def leave(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            self.visited.append(
                (
                    "leave",
                    node.__class__.__name__,
                    key,
                    (
                        parent.__class__.__name__
                        if isinstance(parent, Node)
                        else UNDEFINED_VALUE
                    ),
                )
            )
            assert self.args_stack.pop() == (
                node,
                key,
                parent,
                path,
                ancestors,
            )

    kitchen_sink_query = ""
    with open(
        os.path.join(_BASE_DIR, "fixtures", "kitchen-sink.graphql")
    ) as query_file:
        kitchen_sink_query = query_file.read()

    ast = parse_to_document(kitchen_sink_query, _SCHEMA_MOCK)
    visitor = MyVisitor(ast)
    assert visitor.visited == []
    visit(ast, visitor)
    assert visitor.visited == [
        ("enter", "DocumentNode", None, UNDEFINED_VALUE),
        ("enter", "OperationDefinitionNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "OperationDefinitionNode"),
        ("leave", "NameNode", "name", "OperationDefinitionNode"),
        ("enter", "VariableDefinitionNode", 0, UNDEFINED_VALUE),
        ("enter", "VariableNode", "variable", "VariableDefinitionNode"),
        ("enter", "NameNode", "name", "VariableNode"),
        ("leave", "NameNode", "name", "VariableNode"),
        ("leave", "VariableNode", "variable", "VariableDefinitionNode"),
        ("enter", "NamedTypeNode", "type", "VariableDefinitionNode"),
        ("enter", "NameNode", "name", "NamedTypeNode"),
        ("leave", "NameNode", "name", "NamedTypeNode"),
        ("leave", "NamedTypeNode", "type", "VariableDefinitionNode"),
        ("leave", "VariableDefinitionNode", 0, UNDEFINED_VALUE),
        ("enter", "VariableDefinitionNode", 1, UNDEFINED_VALUE),
        ("enter", "VariableNode", "variable", "VariableDefinitionNode"),
        ("enter", "NameNode", "name", "VariableNode"),
        ("leave", "NameNode", "name", "VariableNode"),
        ("leave", "VariableNode", "variable", "VariableDefinitionNode"),
        ("enter", "NamedTypeNode", "type", "VariableDefinitionNode"),
        ("enter", "NameNode", "name", "NamedTypeNode"),
        ("leave", "NameNode", "name", "NamedTypeNode"),
        ("leave", "NamedTypeNode", "type", "VariableDefinitionNode"),
        ("enter", "EnumValueNode", "default_value", "VariableDefinitionNode"),
        ("leave", "EnumValueNode", "default_value", "VariableDefinitionNode"),
        ("leave", "VariableDefinitionNode", 1, UNDEFINED_VALUE),
        ("enter", "DirectiveNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "DirectiveNode"),
        ("leave", "NameNode", "name", "DirectiveNode"),
        ("leave", "DirectiveNode", 0, UNDEFINED_VALUE),
        (
            "enter",
            "SelectionSetNode",
            "selection_set",
            "OperationDefinitionNode",
        ),
        ("enter", "FieldNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "alias", "FieldNode"),
        ("leave", "NameNode", "alias", "FieldNode"),
        ("enter", "NameNode", "name", "FieldNode"),
        ("leave", "NameNode", "name", "FieldNode"),
        ("enter", "ArgumentNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "ArgumentNode"),
        ("leave", "NameNode", "name", "ArgumentNode"),
        ("enter", "ListValueNode", "value", "ArgumentNode"),
        ("enter", "IntValueNode", 0, UNDEFINED_VALUE),
        ("leave", "IntValueNode", 0, UNDEFINED_VALUE),
        ("enter", "IntValueNode", 1, UNDEFINED_VALUE),
        ("leave", "IntValueNode", 1, UNDEFINED_VALUE),
        ("leave", "ListValueNode", "value", "ArgumentNode"),
        ("leave", "ArgumentNode", 0, UNDEFINED_VALUE),
        ("enter", "SelectionSetNode", "selection_set", "FieldNode"),
        ("enter", "FieldNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "FieldNode"),
        ("leave", "NameNode", "name", "FieldNode"),
        ("leave", "FieldNode", 0, UNDEFINED_VALUE),
        ("enter", "InlineFragmentNode", 1, UNDEFINED_VALUE),
        ("enter", "NamedTypeNode", "type_condition", "InlineFragmentNode"),
        ("enter", "NameNode", "name", "NamedTypeNode"),
        ("leave", "NameNode", "name", "NamedTypeNode"),
        ("leave", "NamedTypeNode", "type_condition", "InlineFragmentNode"),
        ("enter", "DirectiveNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "DirectiveNode"),
        ("leave", "NameNode", "name", "DirectiveNode"),
        ("leave", "DirectiveNode", 0, UNDEFINED_VALUE),
        ("enter", "SelectionSetNode", "selection_set", "InlineFragmentNode"),
        ("enter", "FieldNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "FieldNode"),
        ("leave", "NameNode", "name", "FieldNode"),
        ("enter", "SelectionSetNode", "selection_set", "FieldNode"),
        ("enter", "FieldNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "FieldNode"),
        ("leave", "NameNode", "name", "FieldNode"),
        ("leave", "FieldNode", 0, UNDEFINED_VALUE),
        ("enter", "FieldNode", 1, UNDEFINED_VALUE),
        ("enter", "NameNode", "alias", "FieldNode"),
        ("leave", "NameNode", "alias", "FieldNode"),
        ("enter", "NameNode", "name", "FieldNode"),
        ("leave", "NameNode", "name", "FieldNode"),
        ("enter", "ArgumentNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "ArgumentNode"),
        ("leave", "NameNode", "name", "ArgumentNode"),
        ("enter", "IntValueNode", "value", "ArgumentNode"),
        ("leave", "IntValueNode", "value", "ArgumentNode"),
        ("leave", "ArgumentNode", 0, UNDEFINED_VALUE),
        ("enter", "ArgumentNode", 1, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "ArgumentNode"),
        ("leave", "NameNode", "name", "ArgumentNode"),
        ("enter", "VariableNode", "value", "ArgumentNode"),
        ("enter", "NameNode", "name", "VariableNode"),
        ("leave", "NameNode", "name", "VariableNode"),
        ("leave", "VariableNode", "value", "ArgumentNode"),
        ("leave", "ArgumentNode", 1, UNDEFINED_VALUE),
        ("enter", "DirectiveNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "DirectiveNode"),
        ("leave", "NameNode", "name", "DirectiveNode"),
        ("enter", "ArgumentNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "ArgumentNode"),
        ("leave", "NameNode", "name", "ArgumentNode"),
        ("enter", "VariableNode", "value", "ArgumentNode"),
        ("enter", "NameNode", "name", "VariableNode"),
        ("leave", "NameNode", "name", "VariableNode"),
        ("leave", "VariableNode", "value", "ArgumentNode"),
        ("leave", "ArgumentNode", 0, UNDEFINED_VALUE),
        ("leave", "DirectiveNode", 0, UNDEFINED_VALUE),
        ("enter", "SelectionSetNode", "selection_set", "FieldNode"),
        ("enter", "FieldNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "FieldNode"),
        ("leave", "NameNode", "name", "FieldNode"),
        ("leave", "FieldNode", 0, UNDEFINED_VALUE),
        ("enter", "FragmentSpreadNode", 1, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "FragmentSpreadNode"),
        ("leave", "NameNode", "name", "FragmentSpreadNode"),
        ("enter", "DirectiveNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "DirectiveNode"),
        ("leave", "NameNode", "name", "DirectiveNode"),
        ("leave", "DirectiveNode", 0, UNDEFINED_VALUE),
        ("leave", "FragmentSpreadNode", 1, UNDEFINED_VALUE),
        ("leave", "SelectionSetNode", "selection_set", "FieldNode"),
        ("leave", "FieldNode", 1, UNDEFINED_VALUE),
        ("leave", "SelectionSetNode", "selection_set", "FieldNode"),
        ("leave", "FieldNode", 0, UNDEFINED_VALUE),
        ("leave", "SelectionSetNode", "selection_set", "InlineFragmentNode"),
        ("leave", "InlineFragmentNode", 1, UNDEFINED_VALUE),
        ("enter", "InlineFragmentNode", 2, UNDEFINED_VALUE),
        ("enter", "DirectiveNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "DirectiveNode"),
        ("leave", "NameNode", "name", "DirectiveNode"),
        ("enter", "ArgumentNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "ArgumentNode"),
        ("leave", "NameNode", "name", "ArgumentNode"),
        ("enter", "VariableNode", "value", "ArgumentNode"),
        ("enter", "NameNode", "name", "VariableNode"),
        ("leave", "NameNode", "name", "VariableNode"),
        ("leave", "VariableNode", "value", "ArgumentNode"),
        ("leave", "ArgumentNode", 0, UNDEFINED_VALUE),
        ("leave", "DirectiveNode", 0, UNDEFINED_VALUE),
        ("enter", "SelectionSetNode", "selection_set", "InlineFragmentNode"),
        ("enter", "FieldNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "FieldNode"),
        ("leave", "NameNode", "name", "FieldNode"),
        ("leave", "FieldNode", 0, UNDEFINED_VALUE),
        ("leave", "SelectionSetNode", "selection_set", "InlineFragmentNode"),
        ("leave", "InlineFragmentNode", 2, UNDEFINED_VALUE),
        ("enter", "InlineFragmentNode", 3, UNDEFINED_VALUE),
        ("enter", "SelectionSetNode", "selection_set", "InlineFragmentNode"),
        ("enter", "FieldNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "FieldNode"),
        ("leave", "NameNode", "name", "FieldNode"),
        ("leave", "FieldNode", 0, UNDEFINED_VALUE),
        ("leave", "SelectionSetNode", "selection_set", "InlineFragmentNode"),
        ("leave", "InlineFragmentNode", 3, UNDEFINED_VALUE),
        ("leave", "SelectionSetNode", "selection_set", "FieldNode"),
        ("leave", "FieldNode", 0, UNDEFINED_VALUE),
        (
            "leave",
            "SelectionSetNode",
            "selection_set",
            "OperationDefinitionNode",
        ),
        ("leave", "OperationDefinitionNode", 0, UNDEFINED_VALUE),
        ("enter", "OperationDefinitionNode", 1, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "OperationDefinitionNode"),
        ("leave", "NameNode", "name", "OperationDefinitionNode"),
        ("enter", "DirectiveNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "DirectiveNode"),
        ("leave", "NameNode", "name", "DirectiveNode"),
        ("leave", "DirectiveNode", 0, UNDEFINED_VALUE),
        (
            "enter",
            "SelectionSetNode",
            "selection_set",
            "OperationDefinitionNode",
        ),
        ("enter", "FieldNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "FieldNode"),
        ("leave", "NameNode", "name", "FieldNode"),
        ("enter", "ArgumentNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "ArgumentNode"),
        ("leave", "NameNode", "name", "ArgumentNode"),
        ("enter", "IntValueNode", "value", "ArgumentNode"),
        ("leave", "IntValueNode", "value", "ArgumentNode"),
        ("leave", "ArgumentNode", 0, UNDEFINED_VALUE),
        ("enter", "DirectiveNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "DirectiveNode"),
        ("leave", "NameNode", "name", "DirectiveNode"),
        ("leave", "DirectiveNode", 0, UNDEFINED_VALUE),
        ("enter", "SelectionSetNode", "selection_set", "FieldNode"),
        ("enter", "FieldNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "FieldNode"),
        ("leave", "NameNode", "name", "FieldNode"),
        ("enter", "SelectionSetNode", "selection_set", "FieldNode"),
        ("enter", "FieldNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "FieldNode"),
        ("leave", "NameNode", "name", "FieldNode"),
        ("enter", "DirectiveNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "DirectiveNode"),
        ("leave", "NameNode", "name", "DirectiveNode"),
        ("leave", "DirectiveNode", 0, UNDEFINED_VALUE),
        ("leave", "FieldNode", 0, UNDEFINED_VALUE),
        ("leave", "SelectionSetNode", "selection_set", "FieldNode"),
        ("leave", "FieldNode", 0, UNDEFINED_VALUE),
        ("leave", "SelectionSetNode", "selection_set", "FieldNode"),
        ("leave", "FieldNode", 0, UNDEFINED_VALUE),
        (
            "leave",
            "SelectionSetNode",
            "selection_set",
            "OperationDefinitionNode",
        ),
        ("leave", "OperationDefinitionNode", 1, UNDEFINED_VALUE),
        ("enter", "OperationDefinitionNode", 2, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "OperationDefinitionNode"),
        ("leave", "NameNode", "name", "OperationDefinitionNode"),
        ("enter", "VariableDefinitionNode", 0, UNDEFINED_VALUE),
        ("enter", "VariableNode", "variable", "VariableDefinitionNode"),
        ("enter", "NameNode", "name", "VariableNode"),
        ("leave", "NameNode", "name", "VariableNode"),
        ("leave", "VariableNode", "variable", "VariableDefinitionNode"),
        ("enter", "NamedTypeNode", "type", "VariableDefinitionNode"),
        ("enter", "NameNode", "name", "NamedTypeNode"),
        ("leave", "NameNode", "name", "NamedTypeNode"),
        ("leave", "NamedTypeNode", "type", "VariableDefinitionNode"),
        ("leave", "VariableDefinitionNode", 0, UNDEFINED_VALUE),
        ("enter", "DirectiveNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "DirectiveNode"),
        ("leave", "NameNode", "name", "DirectiveNode"),
        ("leave", "DirectiveNode", 0, UNDEFINED_VALUE),
        (
            "enter",
            "SelectionSetNode",
            "selection_set",
            "OperationDefinitionNode",
        ),
        ("enter", "FieldNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "FieldNode"),
        ("leave", "NameNode", "name", "FieldNode"),
        ("enter", "ArgumentNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "ArgumentNode"),
        ("leave", "NameNode", "name", "ArgumentNode"),
        ("enter", "VariableNode", "value", "ArgumentNode"),
        ("enter", "NameNode", "name", "VariableNode"),
        ("leave", "NameNode", "name", "VariableNode"),
        ("leave", "VariableNode", "value", "ArgumentNode"),
        ("leave", "ArgumentNode", 0, UNDEFINED_VALUE),
        ("enter", "SelectionSetNode", "selection_set", "FieldNode"),
        ("enter", "FieldNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "FieldNode"),
        ("leave", "NameNode", "name", "FieldNode"),
        ("enter", "SelectionSetNode", "selection_set", "FieldNode"),
        ("enter", "FieldNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "FieldNode"),
        ("leave", "NameNode", "name", "FieldNode"),
        ("enter", "SelectionSetNode", "selection_set", "FieldNode"),
        ("enter", "FieldNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "FieldNode"),
        ("leave", "NameNode", "name", "FieldNode"),
        ("leave", "FieldNode", 0, UNDEFINED_VALUE),
        ("leave", "SelectionSetNode", "selection_set", "FieldNode"),
        ("leave", "FieldNode", 0, UNDEFINED_VALUE),
        ("enter", "FieldNode", 1, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "FieldNode"),
        ("leave", "NameNode", "name", "FieldNode"),
        ("enter", "SelectionSetNode", "selection_set", "FieldNode"),
        ("enter", "FieldNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "FieldNode"),
        ("leave", "NameNode", "name", "FieldNode"),
        ("leave", "FieldNode", 0, UNDEFINED_VALUE),
        ("leave", "SelectionSetNode", "selection_set", "FieldNode"),
        ("leave", "FieldNode", 1, UNDEFINED_VALUE),
        ("leave", "SelectionSetNode", "selection_set", "FieldNode"),
        ("leave", "FieldNode", 0, UNDEFINED_VALUE),
        ("leave", "SelectionSetNode", "selection_set", "FieldNode"),
        ("leave", "FieldNode", 0, UNDEFINED_VALUE),
        (
            "leave",
            "SelectionSetNode",
            "selection_set",
            "OperationDefinitionNode",
        ),
        ("leave", "OperationDefinitionNode", 2, UNDEFINED_VALUE),
        ("enter", "FragmentDefinitionNode", 3, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "FragmentDefinitionNode"),
        ("leave", "NameNode", "name", "FragmentDefinitionNode"),
        ("enter", "NamedTypeNode", "type_condition", "FragmentDefinitionNode"),
        ("enter", "NameNode", "name", "NamedTypeNode"),
        ("leave", "NameNode", "name", "NamedTypeNode"),
        ("leave", "NamedTypeNode", "type_condition", "FragmentDefinitionNode"),
        ("enter", "DirectiveNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "DirectiveNode"),
        ("leave", "NameNode", "name", "DirectiveNode"),
        ("leave", "DirectiveNode", 0, UNDEFINED_VALUE),
        (
            "enter",
            "SelectionSetNode",
            "selection_set",
            "FragmentDefinitionNode",
        ),
        ("enter", "FieldNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "FieldNode"),
        ("leave", "NameNode", "name", "FieldNode"),
        ("enter", "ArgumentNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "ArgumentNode"),
        ("leave", "NameNode", "name", "ArgumentNode"),
        ("enter", "VariableNode", "value", "ArgumentNode"),
        ("enter", "NameNode", "name", "VariableNode"),
        ("leave", "NameNode", "name", "VariableNode"),
        ("leave", "VariableNode", "value", "ArgumentNode"),
        ("leave", "ArgumentNode", 0, UNDEFINED_VALUE),
        ("enter", "ArgumentNode", 1, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "ArgumentNode"),
        ("leave", "NameNode", "name", "ArgumentNode"),
        ("enter", "VariableNode", "value", "ArgumentNode"),
        ("enter", "NameNode", "name", "VariableNode"),
        ("leave", "NameNode", "name", "VariableNode"),
        ("leave", "VariableNode", "value", "ArgumentNode"),
        ("leave", "ArgumentNode", 1, UNDEFINED_VALUE),
        ("enter", "ArgumentNode", 2, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "ArgumentNode"),
        ("leave", "NameNode", "name", "ArgumentNode"),
        ("enter", "ObjectValueNode", "value", "ArgumentNode"),
        ("enter", "ObjectFieldNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "ObjectFieldNode"),
        ("leave", "NameNode", "name", "ObjectFieldNode"),
        ("enter", "StringValueNode", "value", "ObjectFieldNode"),
        ("leave", "StringValueNode", "value", "ObjectFieldNode"),
        ("leave", "ObjectFieldNode", 0, UNDEFINED_VALUE),
        ("enter", "ObjectFieldNode", 1, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "ObjectFieldNode"),
        ("leave", "NameNode", "name", "ObjectFieldNode"),
        ("enter", "StringValueNode", "value", "ObjectFieldNode"),
        ("leave", "StringValueNode", "value", "ObjectFieldNode"),
        ("leave", "ObjectFieldNode", 1, UNDEFINED_VALUE),
        ("leave", "ObjectValueNode", "value", "ArgumentNode"),
        ("leave", "ArgumentNode", 2, UNDEFINED_VALUE),
        ("leave", "FieldNode", 0, UNDEFINED_VALUE),
        (
            "leave",
            "SelectionSetNode",
            "selection_set",
            "FragmentDefinitionNode",
        ),
        ("leave", "FragmentDefinitionNode", 3, UNDEFINED_VALUE),
        ("enter", "OperationDefinitionNode", 4, UNDEFINED_VALUE),
        (
            "enter",
            "SelectionSetNode",
            "selection_set",
            "OperationDefinitionNode",
        ),
        ("enter", "FieldNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "FieldNode"),
        ("leave", "NameNode", "name", "FieldNode"),
        ("enter", "ArgumentNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "ArgumentNode"),
        ("leave", "NameNode", "name", "ArgumentNode"),
        ("enter", "BooleanValueNode", "value", "ArgumentNode"),
        ("leave", "BooleanValueNode", "value", "ArgumentNode"),
        ("leave", "ArgumentNode", 0, UNDEFINED_VALUE),
        ("enter", "ArgumentNode", 1, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "ArgumentNode"),
        ("leave", "NameNode", "name", "ArgumentNode"),
        ("enter", "BooleanValueNode", "value", "ArgumentNode"),
        ("leave", "BooleanValueNode", "value", "ArgumentNode"),
        ("leave", "ArgumentNode", 1, UNDEFINED_VALUE),
        ("enter", "ArgumentNode", 2, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "ArgumentNode"),
        ("leave", "NameNode", "name", "ArgumentNode"),
        ("enter", "NullValueNode", "value", "ArgumentNode"),
        ("leave", "NullValueNode", "value", "ArgumentNode"),
        ("leave", "ArgumentNode", 2, UNDEFINED_VALUE),
        ("leave", "FieldNode", 0, UNDEFINED_VALUE),
        ("enter", "FieldNode", 1, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "FieldNode"),
        ("leave", "NameNode", "name", "FieldNode"),
        ("leave", "FieldNode", 1, UNDEFINED_VALUE),
        (
            "leave",
            "SelectionSetNode",
            "selection_set",
            "OperationDefinitionNode",
        ),
        ("leave", "OperationDefinitionNode", 4, UNDEFINED_VALUE),
        ("enter", "OperationDefinitionNode", 5, UNDEFINED_VALUE),
        (
            "enter",
            "SelectionSetNode",
            "selection_set",
            "OperationDefinitionNode",
        ),
        ("enter", "FieldNode", 0, UNDEFINED_VALUE),
        ("enter", "NameNode", "name", "FieldNode"),
        ("leave", "NameNode", "name", "FieldNode"),
        ("leave", "FieldNode", 0, UNDEFINED_VALUE),
        (
            "leave",
            "SelectionSetNode",
            "selection_set",
            "OperationDefinitionNode",
        ),
        ("leave", "OperationDefinitionNode", 5, UNDEFINED_VALUE),
        ("leave", "DocumentNode", None, UNDEFINED_VALUE),
    ]


def test_does_not_traverse_unknown_node_kinds():
    class CustomFieldNode(Node):
        def __init__(self, name, selection_set=None):
            self.name = name
            self.selection_set = selection_set

    ast = parse_to_document("{ a }", _SCHEMA_MOCK)
    ast.definitions[0].selection_set.selections.append(
        CustomFieldNode(
            name=NameNode(value="b"),
            selection_set=SelectionSetNode(
                selections=[CustomFieldNode(name=NameNode(value="c"))],
            ),
        )
    )

    class MyVisitor(Visitor):
        def __init__(self, ast):
            self.ast = ast
            self.visited = []

        def enter(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            self.visited.append(
                ("enter", node.__class__.__name__, get_value(node))
            )

        def leave(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            self.visited.append(
                ("leave", node.__class__.__name__, get_value(node))
            )

    visitor = MyVisitor(ast)
    assert visitor.visited == []
    visit(ast, visitor)
    assert visitor.visited == [
        ("enter", "DocumentNode", UNDEFINED_VALUE),
        ("enter", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("enter", "FieldNode", UNDEFINED_VALUE),
        ("enter", "NameNode", "a"),
        ("leave", "NameNode", "a"),
        ("leave", "FieldNode", UNDEFINED_VALUE),
        ("enter", "CustomFieldNode", UNDEFINED_VALUE),
        ("leave", "CustomFieldNode", UNDEFINED_VALUE),
        ("leave", "SelectionSetNode", UNDEFINED_VALUE),
        ("leave", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("leave", "DocumentNode", UNDEFINED_VALUE),
    ]


def test_does_traverse_unknown_node_kinds_with_visitor_keys():
    class CustomFieldNode(Node):
        def __init__(self, name, selection_set=None):
            self.name = name
            self.selection_set = selection_set

    ast = parse_to_document("{ a }", _SCHEMA_MOCK)
    ast.definitions[0].selection_set.selections.append(
        CustomFieldNode(
            name=NameNode(value="b"),
            selection_set=SelectionSetNode(
                selections=[CustomFieldNode(name=NameNode(value="c"))],
            ),
        )
    )

    class MyVisitor(Visitor):
        def __init__(self, ast):
            self.ast = ast
            self.visited = []

        def enter(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            self.visited.append(
                ("enter", node.__class__.__name__, get_value(node))
            )

        def leave(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            self.visited.append(
                ("leave", node.__class__.__name__, get_value(node))
            )

    visitor = MyVisitor(ast)
    assert visitor.visited == []
    visit(
        ast,
        visitor,
        visitor_keys={
            **QUERY_DOCUMENT_KEYS,
            "CustomFieldNode": ("name", "selection_set"),
        },
    )
    assert visitor.visited == [
        ("enter", "DocumentNode", UNDEFINED_VALUE),
        ("enter", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("enter", "FieldNode", UNDEFINED_VALUE),
        ("enter", "NameNode", "a"),
        ("leave", "NameNode", "a"),
        ("leave", "FieldNode", UNDEFINED_VALUE),
        ("enter", "CustomFieldNode", UNDEFINED_VALUE),
        ("enter", "NameNode", "b"),
        ("leave", "NameNode", "b"),
        ("enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("enter", "CustomFieldNode", UNDEFINED_VALUE),
        ("enter", "NameNode", "c"),
        ("leave", "NameNode", "c"),
        ("leave", "CustomFieldNode", UNDEFINED_VALUE),
        ("leave", "SelectionSetNode", UNDEFINED_VALUE),
        ("leave", "CustomFieldNode", UNDEFINED_VALUE),
        ("leave", "SelectionSetNode", UNDEFINED_VALUE),
        ("leave", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("leave", "DocumentNode", UNDEFINED_VALUE),
    ]


def test_visit_in_parallel_allows_skipping_a_sub_tree():
    class MyVisitor(Visitor):
        def __init__(self, ast):
            self.ast = ast
            self.visited = []

        def enter(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            self.visited.append(
                ("enter", node.__class__.__name__, get_value(node))
            )
            if isinstance(node, FieldNode) and node.name.value == "b":
                return SKIP

        def leave(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            self.visited.append(
                ("leave", node.__class__.__name__, get_value(node))
            )

    ast = parse_to_document("{ a, b { x }, c }", _SCHEMA_MOCK)
    visitor = MyVisitor(ast)
    assert visitor.visited == []
    visit(ast, ParallelVisitor([visitor]))
    assert visitor.visited == [
        ("enter", "DocumentNode", UNDEFINED_VALUE),
        ("enter", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("enter", "FieldNode", UNDEFINED_VALUE),
        ("enter", "NameNode", "a"),
        ("leave", "NameNode", "a"),
        ("leave", "FieldNode", UNDEFINED_VALUE),
        ("enter", "FieldNode", UNDEFINED_VALUE),
        ("enter", "FieldNode", UNDEFINED_VALUE),
        ("enter", "NameNode", "c"),
        ("leave", "NameNode", "c"),
        ("leave", "FieldNode", UNDEFINED_VALUE),
        ("leave", "SelectionSetNode", UNDEFINED_VALUE),
        ("leave", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("leave", "DocumentNode", UNDEFINED_VALUE),
    ]


def test_visit_in_parallel_allows_skipping_different_sub_trees():
    parallel_visited = []

    class MyVisitor(Visitor):
        def __init__(self, ast, field_name_to_skip):
            self.ast = ast
            self.field_name_to_skip = field_name_to_skip
            self.visited = []

        def enter(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            describe = (
                f"no-{self.field_name_to_skip}",
                "enter",
                node.__class__.__name__,
                get_value(node),
            )
            parallel_visited.append(describe)
            self.visited.append(describe)
            if (
                isinstance(node, FieldNode)
                and node.name.value == self.field_name_to_skip
            ):
                return SKIP

        def leave(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            describe = (
                f"no-{self.field_name_to_skip}",
                "leave",
                node.__class__.__name__,
                get_value(node),
            )
            parallel_visited.append(describe)
            self.visited.append(describe)

    ast = parse_to_document("{ a { x }, b { y} }", _SCHEMA_MOCK)
    visitor_a = MyVisitor(ast, "a")
    visitor_b = MyVisitor(ast, "b")
    assert parallel_visited == []
    assert visitor_a.visited == []
    assert visitor_b.visited == []
    visit(ast, ParallelVisitor([visitor_a, visitor_b]))
    assert visitor_a.visited == [
        ("no-a", "enter", "DocumentNode", UNDEFINED_VALUE),
        ("no-a", "enter", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("no-a", "enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("no-a", "enter", "FieldNode", UNDEFINED_VALUE),
        ("no-a", "enter", "FieldNode", UNDEFINED_VALUE),
        ("no-a", "enter", "NameNode", "b"),
        ("no-a", "leave", "NameNode", "b"),
        ("no-a", "enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("no-a", "enter", "FieldNode", UNDEFINED_VALUE),
        ("no-a", "enter", "NameNode", "y"),
        ("no-a", "leave", "NameNode", "y"),
        ("no-a", "leave", "FieldNode", UNDEFINED_VALUE),
        ("no-a", "leave", "SelectionSetNode", UNDEFINED_VALUE),
        ("no-a", "leave", "FieldNode", UNDEFINED_VALUE),
        ("no-a", "leave", "SelectionSetNode", UNDEFINED_VALUE),
        ("no-a", "leave", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("no-a", "leave", "DocumentNode", UNDEFINED_VALUE),
    ]
    assert visitor_b.visited == [
        ("no-b", "enter", "DocumentNode", UNDEFINED_VALUE),
        ("no-b", "enter", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("no-b", "enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("no-b", "enter", "FieldNode", UNDEFINED_VALUE),
        ("no-b", "enter", "NameNode", "a"),
        ("no-b", "leave", "NameNode", "a"),
        ("no-b", "enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("no-b", "enter", "FieldNode", UNDEFINED_VALUE),
        ("no-b", "enter", "NameNode", "x"),
        ("no-b", "leave", "NameNode", "x"),
        ("no-b", "leave", "FieldNode", UNDEFINED_VALUE),
        ("no-b", "leave", "SelectionSetNode", UNDEFINED_VALUE),
        ("no-b", "leave", "FieldNode", UNDEFINED_VALUE),
        ("no-b", "enter", "FieldNode", UNDEFINED_VALUE),
        ("no-b", "leave", "SelectionSetNode", UNDEFINED_VALUE),
        ("no-b", "leave", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("no-b", "leave", "DocumentNode", UNDEFINED_VALUE),
    ]
    assert parallel_visited == [
        ("no-a", "enter", "DocumentNode", UNDEFINED_VALUE),
        ("no-b", "enter", "DocumentNode", UNDEFINED_VALUE),
        ("no-a", "enter", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("no-b", "enter", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("no-a", "enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("no-b", "enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("no-a", "enter", "FieldNode", UNDEFINED_VALUE),
        ("no-b", "enter", "FieldNode", UNDEFINED_VALUE),
        ("no-b", "enter", "NameNode", "a"),
        ("no-b", "leave", "NameNode", "a"),
        ("no-b", "enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("no-b", "enter", "FieldNode", UNDEFINED_VALUE),
        ("no-b", "enter", "NameNode", "x"),
        ("no-b", "leave", "NameNode", "x"),
        ("no-b", "leave", "FieldNode", UNDEFINED_VALUE),
        ("no-b", "leave", "SelectionSetNode", UNDEFINED_VALUE),
        ("no-b", "leave", "FieldNode", UNDEFINED_VALUE),
        ("no-a", "enter", "FieldNode", UNDEFINED_VALUE),
        ("no-b", "enter", "FieldNode", UNDEFINED_VALUE),
        ("no-a", "enter", "NameNode", "b"),
        ("no-a", "leave", "NameNode", "b"),
        ("no-a", "enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("no-a", "enter", "FieldNode", UNDEFINED_VALUE),
        ("no-a", "enter", "NameNode", "y"),
        ("no-a", "leave", "NameNode", "y"),
        ("no-a", "leave", "FieldNode", UNDEFINED_VALUE),
        ("no-a", "leave", "SelectionSetNode", UNDEFINED_VALUE),
        ("no-a", "leave", "FieldNode", UNDEFINED_VALUE),
        ("no-a", "leave", "SelectionSetNode", UNDEFINED_VALUE),
        ("no-b", "leave", "SelectionSetNode", UNDEFINED_VALUE),
        ("no-a", "leave", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("no-b", "leave", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("no-a", "leave", "DocumentNode", UNDEFINED_VALUE),
        ("no-b", "leave", "DocumentNode", UNDEFINED_VALUE),
    ]


def test_visit_in_parallel_allows_early_exit_while_visiting():
    class MyVisitor(Visitor):
        def __init__(self, ast):
            self.ast = ast
            self.visited = []

        def enter(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            self.visited.append(
                ("enter", node.__class__.__name__, get_value(node))
            )
            if isinstance(node, NameNode) and node.value == "x":
                return BREAK

        def leave(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            self.visited.append(
                ("leave", node.__class__.__name__, get_value(node))
            )

    ast = parse_to_document("{ a, b { x }, c }", _SCHEMA_MOCK)
    visitor = MyVisitor(ast)
    assert visitor.visited == []
    visit(ast, ParallelVisitor([visitor]))
    assert visitor.visited == [
        ("enter", "DocumentNode", UNDEFINED_VALUE),
        ("enter", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("enter", "FieldNode", UNDEFINED_VALUE),
        ("enter", "NameNode", "a"),
        ("leave", "NameNode", "a"),
        ("leave", "FieldNode", UNDEFINED_VALUE),
        ("enter", "FieldNode", UNDEFINED_VALUE),
        ("enter", "NameNode", "b"),
        ("leave", "NameNode", "b"),
        ("enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("enter", "FieldNode", UNDEFINED_VALUE),
        ("enter", "NameNode", "x"),
    ]


def test_visit_in_parallel_allows_early_exit_from_different_points():
    parallel_visited = []

    class MyVisitor(Visitor):
        def __init__(self, ast, name_to_break):
            self.ast = ast
            self.name_to_break = name_to_break
            self.visited = []

        def enter(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            describe = (
                f"break-{self.name_to_break}",
                "enter",
                node.__class__.__name__,
                get_value(node),
            )
            parallel_visited.append(describe)
            self.visited.append(describe)
            if isinstance(node, NameNode) and node.value == self.name_to_break:
                return BREAK

        def leave(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            describe = (
                f"break-{self.name_to_break}",
                "leave",
                node.__class__.__name__,
                get_value(node),
            )
            parallel_visited.append(describe)
            self.visited.append(describe)

    ast = parse_to_document("{ a { y }, b { x } }", _SCHEMA_MOCK)
    visitor_a = MyVisitor(ast, "a")
    visitor_b = MyVisitor(ast, "b")
    assert parallel_visited == []
    assert visitor_a.visited == []
    assert visitor_b.visited == []
    visit(ast, ParallelVisitor([visitor_a, visitor_b]))
    assert visitor_a.visited == [
        ("break-a", "enter", "DocumentNode", UNDEFINED_VALUE),
        ("break-a", "enter", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("break-a", "enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("break-a", "enter", "FieldNode", UNDEFINED_VALUE),
        ("break-a", "enter", "NameNode", "a"),
    ]
    assert visitor_b.visited == [
        ("break-b", "enter", "DocumentNode", UNDEFINED_VALUE),
        ("break-b", "enter", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("break-b", "enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("break-b", "enter", "FieldNode", UNDEFINED_VALUE),
        ("break-b", "enter", "NameNode", "a"),
        ("break-b", "leave", "NameNode", "a"),
        ("break-b", "enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("break-b", "enter", "FieldNode", UNDEFINED_VALUE),
        ("break-b", "enter", "NameNode", "y"),
        ("break-b", "leave", "NameNode", "y"),
        ("break-b", "leave", "FieldNode", UNDEFINED_VALUE),
        ("break-b", "leave", "SelectionSetNode", UNDEFINED_VALUE),
        ("break-b", "leave", "FieldNode", UNDEFINED_VALUE),
        ("break-b", "enter", "FieldNode", UNDEFINED_VALUE),
        ("break-b", "enter", "NameNode", "b"),
    ]
    assert parallel_visited == [
        ("break-a", "enter", "DocumentNode", UNDEFINED_VALUE),
        ("break-b", "enter", "DocumentNode", UNDEFINED_VALUE),
        ("break-a", "enter", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("break-b", "enter", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("break-a", "enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("break-b", "enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("break-a", "enter", "FieldNode", UNDEFINED_VALUE),
        ("break-b", "enter", "FieldNode", UNDEFINED_VALUE),
        ("break-a", "enter", "NameNode", "a"),
        ("break-b", "enter", "NameNode", "a"),
        ("break-b", "leave", "NameNode", "a"),
        ("break-b", "enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("break-b", "enter", "FieldNode", UNDEFINED_VALUE),
        ("break-b", "enter", "NameNode", "y"),
        ("break-b", "leave", "NameNode", "y"),
        ("break-b", "leave", "FieldNode", UNDEFINED_VALUE),
        ("break-b", "leave", "SelectionSetNode", UNDEFINED_VALUE),
        ("break-b", "leave", "FieldNode", UNDEFINED_VALUE),
        ("break-b", "enter", "FieldNode", UNDEFINED_VALUE),
        ("break-b", "enter", "NameNode", "b"),
    ]


def test_visit_in_parallel_allows_early_exit_while_leaving():
    class MyVisitor(Visitor):
        def __init__(self, ast):
            self.ast = ast
            self.visited = []

        def enter(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            self.visited.append(
                ("enter", node.__class__.__name__, get_value(node))
            )

        def leave(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            self.visited.append(
                ("leave", node.__class__.__name__, get_value(node))
            )
            if isinstance(node, NameNode) and node.value == "x":
                return BREAK

    ast = parse_to_document("{ a, b { x }, c }", _SCHEMA_MOCK)
    visitor = MyVisitor(ast)
    assert visitor.visited == []
    visit(ast, ParallelVisitor([visitor]))
    assert visitor.visited == [
        ("enter", "DocumentNode", UNDEFINED_VALUE),
        ("enter", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("enter", "FieldNode", UNDEFINED_VALUE),
        ("enter", "NameNode", "a"),
        ("leave", "NameNode", "a"),
        ("leave", "FieldNode", UNDEFINED_VALUE),
        ("enter", "FieldNode", UNDEFINED_VALUE),
        ("enter", "NameNode", "b"),
        ("leave", "NameNode", "b"),
        ("enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("enter", "FieldNode", UNDEFINED_VALUE),
        ("enter", "NameNode", "x"),
        ("leave", "NameNode", "x"),
    ]


def test_visit_in_parallel_allows_early_exit_from_leaving_different_points():
    parallel_visited = []

    class MyVisitor(Visitor):
        def __init__(self, ast, field_name_to_break):
            self.ast = ast
            self.field_name_to_break = field_name_to_break
            self.visited = []

        def enter(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            describe = (
                f"break-{self.field_name_to_break}",
                "enter",
                node.__class__.__name__,
                get_value(node),
            )
            parallel_visited.append(describe)
            self.visited.append(describe)

        def leave(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            describe = (
                f"break-{self.field_name_to_break}",
                "leave",
                node.__class__.__name__,
                get_value(node),
            )
            parallel_visited.append(describe)
            self.visited.append(describe)
            if (
                isinstance(node, FieldNode)
                and node.name.value == self.field_name_to_break
            ):
                return BREAK

    ast = parse_to_document("{ a { y }, b { x } }", _SCHEMA_MOCK)
    visitor_a = MyVisitor(ast, "a")
    visitor_b = MyVisitor(ast, "b")
    assert parallel_visited == []
    assert visitor_a.visited == []
    assert visitor_b.visited == []
    visit(ast, ParallelVisitor([visitor_a, visitor_b]))
    assert visitor_a.visited == [
        ("break-a", "enter", "DocumentNode", UNDEFINED_VALUE),
        ("break-a", "enter", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("break-a", "enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("break-a", "enter", "FieldNode", UNDEFINED_VALUE),
        ("break-a", "enter", "NameNode", "a"),
        ("break-a", "leave", "NameNode", "a"),
        ("break-a", "enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("break-a", "enter", "FieldNode", UNDEFINED_VALUE),
        ("break-a", "enter", "NameNode", "y"),
        ("break-a", "leave", "NameNode", "y"),
        ("break-a", "leave", "FieldNode", UNDEFINED_VALUE),
        ("break-a", "leave", "SelectionSetNode", UNDEFINED_VALUE),
        ("break-a", "leave", "FieldNode", UNDEFINED_VALUE),
    ]
    assert visitor_b.visited == [
        ("break-b", "enter", "DocumentNode", UNDEFINED_VALUE),
        ("break-b", "enter", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("break-b", "enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("break-b", "enter", "FieldNode", UNDEFINED_VALUE),
        ("break-b", "enter", "NameNode", "a"),
        ("break-b", "leave", "NameNode", "a"),
        ("break-b", "enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("break-b", "enter", "FieldNode", UNDEFINED_VALUE),
        ("break-b", "enter", "NameNode", "y"),
        ("break-b", "leave", "NameNode", "y"),
        ("break-b", "leave", "FieldNode", UNDEFINED_VALUE),
        ("break-b", "leave", "SelectionSetNode", UNDEFINED_VALUE),
        ("break-b", "leave", "FieldNode", UNDEFINED_VALUE),
        ("break-b", "enter", "FieldNode", UNDEFINED_VALUE),
        ("break-b", "enter", "NameNode", "b"),
        ("break-b", "leave", "NameNode", "b"),
        ("break-b", "enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("break-b", "enter", "FieldNode", UNDEFINED_VALUE),
        ("break-b", "enter", "NameNode", "x"),
        ("break-b", "leave", "NameNode", "x"),
        ("break-b", "leave", "FieldNode", UNDEFINED_VALUE),
        ("break-b", "leave", "SelectionSetNode", UNDEFINED_VALUE),
        ("break-b", "leave", "FieldNode", UNDEFINED_VALUE),
    ]
    assert parallel_visited == [
        ("break-a", "enter", "DocumentNode", UNDEFINED_VALUE),
        ("break-b", "enter", "DocumentNode", UNDEFINED_VALUE),
        ("break-a", "enter", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("break-b", "enter", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("break-a", "enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("break-b", "enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("break-a", "enter", "FieldNode", UNDEFINED_VALUE),
        ("break-b", "enter", "FieldNode", UNDEFINED_VALUE),
        ("break-a", "enter", "NameNode", "a"),
        ("break-b", "enter", "NameNode", "a"),
        ("break-a", "leave", "NameNode", "a"),
        ("break-b", "leave", "NameNode", "a"),
        ("break-a", "enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("break-b", "enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("break-a", "enter", "FieldNode", UNDEFINED_VALUE),
        ("break-b", "enter", "FieldNode", UNDEFINED_VALUE),
        ("break-a", "enter", "NameNode", "y"),
        ("break-b", "enter", "NameNode", "y"),
        ("break-a", "leave", "NameNode", "y"),
        ("break-b", "leave", "NameNode", "y"),
        ("break-a", "leave", "FieldNode", UNDEFINED_VALUE),
        ("break-b", "leave", "FieldNode", UNDEFINED_VALUE),
        ("break-a", "leave", "SelectionSetNode", UNDEFINED_VALUE),
        ("break-b", "leave", "SelectionSetNode", UNDEFINED_VALUE),
        ("break-a", "leave", "FieldNode", UNDEFINED_VALUE),
        ("break-b", "leave", "FieldNode", UNDEFINED_VALUE),
        ("break-b", "enter", "FieldNode", UNDEFINED_VALUE),
        ("break-b", "enter", "NameNode", "b"),
        ("break-b", "leave", "NameNode", "b"),
        ("break-b", "enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("break-b", "enter", "FieldNode", UNDEFINED_VALUE),
        ("break-b", "enter", "NameNode", "x"),
        ("break-b", "leave", "NameNode", "x"),
        ("break-b", "leave", "FieldNode", UNDEFINED_VALUE),
        ("break-b", "leave", "SelectionSetNode", UNDEFINED_VALUE),
        ("break-b", "leave", "FieldNode", UNDEFINED_VALUE),
    ]


def test_visit_in_parallel_allows_for_editing_on_enter():
    class MyVisitor1(Visitor):
        def __init__(self, ast):
            self.ast = ast

        def enter(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(
                self.ast, node, key, parent, path, ancestors, is_edited=True
            )
            return (
                REMOVE
                if isinstance(node, FieldNode) and node.name.value == "b"
                else OK
            )

    class MyVisitor2(Visitor):
        def __init__(self, ast):
            self.ast = ast
            self.visited = []

        def enter(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            self.visited.append(
                ("enter", node.__class__.__name__, get_value(node))
            )

        def leave(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(
                self.ast, node, key, parent, path, ancestors, is_edited=True
            )
            self.visited.append(
                ("leave", node.__class__.__name__, get_value(node))
            )

    ast = parse_to_document("{ a, b, c { a, b, c } }", _SCHEMA_MOCK)
    visitor_1 = MyVisitor1(ast)
    visitor_2 = MyVisitor2(ast)
    assert visitor_2.visited == []
    edited_ast = visit(ast, ParallelVisitor([visitor_1, visitor_2]))
    assert ast == parse_to_document("{ a, b, c { a, b, c } }", _SCHEMA_MOCK)
    assert edited_ast == parse_to_document(
        "{ a,    c { a,    c } }", _SCHEMA_MOCK
    )
    assert visitor_2.visited == [
        ("enter", "DocumentNode", UNDEFINED_VALUE),
        ("enter", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("enter", "FieldNode", UNDEFINED_VALUE),
        ("enter", "NameNode", "a"),
        ("leave", "NameNode", "a"),
        ("leave", "FieldNode", UNDEFINED_VALUE),
        ("enter", "FieldNode", UNDEFINED_VALUE),
        ("enter", "NameNode", "c"),
        ("leave", "NameNode", "c"),
        ("enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("enter", "FieldNode", UNDEFINED_VALUE),
        ("enter", "NameNode", "a"),
        ("leave", "NameNode", "a"),
        ("leave", "FieldNode", UNDEFINED_VALUE),
        ("enter", "FieldNode", UNDEFINED_VALUE),
        ("enter", "NameNode", "c"),
        ("leave", "NameNode", "c"),
        ("leave", "FieldNode", UNDEFINED_VALUE),
        ("leave", "SelectionSetNode", UNDEFINED_VALUE),
        ("leave", "FieldNode", UNDEFINED_VALUE),
        ("leave", "SelectionSetNode", UNDEFINED_VALUE),
        ("leave", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("leave", "DocumentNode", UNDEFINED_VALUE),
    ]


def test_visit_in_parallel_allows_for_editing_on_leave():
    class MyVisitor1(Visitor):
        def __init__(self, ast):
            self.ast = ast

        def leave(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(
                self.ast, node, key, parent, path, ancestors, is_edited=True
            )
            return (
                REMOVE
                if isinstance(node, FieldNode) and node.name.value == "b"
                else OK
            )

    class MyVisitor2(Visitor):
        def __init__(self, ast):
            self.ast = ast
            self.visited = []

        def enter(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            self.visited.append(
                ("enter", node.__class__.__name__, get_value(node))
            )

        def leave(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(
                self.ast, node, key, parent, path, ancestors, is_edited=True
            )
            self.visited.append(
                ("leave", node.__class__.__name__, get_value(node))
            )

    ast = parse_to_document("{ a, b, c { a, b, c } }", _SCHEMA_MOCK)
    visitor_1 = MyVisitor1(ast)
    visitor_2 = MyVisitor2(ast)
    assert visitor_2.visited == []
    edited_ast = visit(ast, ParallelVisitor([visitor_1, visitor_2]))
    assert ast == parse_to_document("{ a, b, c { a, b, c } }", _SCHEMA_MOCK)
    assert edited_ast == parse_to_document(
        "{ a,    c { a,    c } }", _SCHEMA_MOCK
    )
    assert visitor_2.visited == [
        ("enter", "DocumentNode", UNDEFINED_VALUE),
        ("enter", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("enter", "FieldNode", UNDEFINED_VALUE),
        ("enter", "NameNode", "a"),
        ("leave", "NameNode", "a"),
        ("leave", "FieldNode", UNDEFINED_VALUE),
        ("enter", "FieldNode", UNDEFINED_VALUE),
        ("enter", "NameNode", "b"),
        ("leave", "NameNode", "b"),
        ("enter", "FieldNode", UNDEFINED_VALUE),
        ("enter", "NameNode", "c"),
        ("leave", "NameNode", "c"),
        ("enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("enter", "FieldNode", UNDEFINED_VALUE),
        ("enter", "NameNode", "a"),
        ("leave", "NameNode", "a"),
        ("leave", "FieldNode", UNDEFINED_VALUE),
        ("enter", "FieldNode", UNDEFINED_VALUE),
        ("enter", "NameNode", "b"),
        ("leave", "NameNode", "b"),
        ("enter", "FieldNode", UNDEFINED_VALUE),
        ("enter", "NameNode", "c"),
        ("leave", "NameNode", "c"),
        ("leave", "FieldNode", UNDEFINED_VALUE),
        ("leave", "SelectionSetNode", UNDEFINED_VALUE),
        ("leave", "FieldNode", UNDEFINED_VALUE),
        ("leave", "SelectionSetNode", UNDEFINED_VALUE),
        ("leave", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("leave", "DocumentNode", UNDEFINED_VALUE),
    ]


def test_visit_in_parallel_allows_editing_a_node_both_on_enter_and_on_leave():
    parallel_visited = []

    class MyVisitor1(Visitor):
        def __init__(self, ast):
            self.ast = ast
            self.visited = []

        def enter_OperationDefinition(
            self, node, key, parent, path, ancestors
        ):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            assert len(node.selection_set.selections) == 3
            describe = (
                "visitor-1",
                "enter",
                node.__class__.__name__,
                get_value(node),
            )
            parallel_visited.append(describe)
            self.visited.append(describe)
            node.selection_set.selections[1].selection_set = SelectionSetNode(
                selections=[FieldNode(name=NameNode(value="x"))],
            )
            return node

        def leave_OperationDefinition(
            self, node, key, parent, path, ancestors
        ):
            check_visitor_fn_args(
                self.ast, node, key, parent, path, ancestors, is_edited=True
            )
            describe = (
                "visitor-1",
                "leave",
                node.__class__.__name__,
                get_value(node),
            )
            parallel_visited.append(describe)
            self.visited.append(describe)

        def enter_Field(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(
                self.ast, node, key, parent, path, ancestors, is_edited=True
            )
            describe = (
                "visitor-1",
                "enter",
                node.__class__.__name__,
                get_value(node),
            )
            parallel_visited.append(describe)
            self.visited.append(describe)
            if node.name.value == "y":
                node.name = NameNode(value="w")
            return node

    class MyVisitor2(Visitor):
        def __init__(self, ast):
            self.ast = ast
            self.visited = []

        def enter(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(self.ast, node, key, parent, path, ancestors)
            describe = (
                "visitor-2",
                "enter",
                node.__class__.__name__,
                get_value(node),
            )
            parallel_visited.append(describe)
            self.visited.append(describe)

        def leave(self, node, key, parent, path, ancestors):
            check_visitor_fn_args(
                self.ast, node, key, parent, path, ancestors, is_edited=True
            )
            describe = (
                "visitor-2",
                "leave",
                node.__class__.__name__,
                get_value(node),
            )
            parallel_visited.append(describe)
            self.visited.append(describe)

    ast = parse_to_document("{ a, y, c { a, b, c } }", _SCHEMA_MOCK)
    visitor_1 = MyVisitor1(ast)
    visitor_2 = MyVisitor2(ast)
    assert parallel_visited == []
    assert visitor_1.visited == []
    assert visitor_2.visited == []
    visit(ast, ParallelVisitor([visitor_1, visitor_2]))
    assert visitor_1.visited == [
        ("visitor-1", "enter", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("visitor-1", "enter", "FieldNode", UNDEFINED_VALUE),
        ("visitor-1", "enter", "FieldNode", UNDEFINED_VALUE),
        ("visitor-1", "enter", "FieldNode", UNDEFINED_VALUE),
        ("visitor-1", "enter", "FieldNode", UNDEFINED_VALUE),
        ("visitor-1", "enter", "FieldNode", UNDEFINED_VALUE),
        ("visitor-1", "enter", "FieldNode", UNDEFINED_VALUE),
        ("visitor-1", "enter", "FieldNode", UNDEFINED_VALUE),
        ("visitor-1", "leave", "OperationDefinitionNode", UNDEFINED_VALUE),
    ]
    assert visitor_2.visited == [
        ("visitor-2", "enter", "DocumentNode", UNDEFINED_VALUE),
        ("visitor-2", "enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("visitor-2", "enter", "NameNode", "a"),
        ("visitor-2", "leave", "NameNode", "a"),
        ("visitor-2", "leave", "FieldNode", UNDEFINED_VALUE),
        ("visitor-2", "enter", "NameNode", "w"),
        ("visitor-2", "leave", "NameNode", "w"),
        ("visitor-2", "enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("visitor-2", "enter", "NameNode", "x"),
        ("visitor-2", "leave", "NameNode", "x"),
        ("visitor-2", "leave", "FieldNode", UNDEFINED_VALUE),
        ("visitor-2", "leave", "SelectionSetNode", UNDEFINED_VALUE),
        ("visitor-2", "leave", "FieldNode", UNDEFINED_VALUE),
        ("visitor-2", "enter", "NameNode", "c"),
        ("visitor-2", "leave", "NameNode", "c"),
        ("visitor-2", "enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("visitor-2", "enter", "NameNode", "a"),
        ("visitor-2", "leave", "NameNode", "a"),
        ("visitor-2", "leave", "FieldNode", UNDEFINED_VALUE),
        ("visitor-2", "enter", "NameNode", "b"),
        ("visitor-2", "leave", "NameNode", "b"),
        ("visitor-2", "leave", "FieldNode", UNDEFINED_VALUE),
        ("visitor-2", "enter", "NameNode", "c"),
        ("visitor-2", "leave", "NameNode", "c"),
        ("visitor-2", "leave", "FieldNode", UNDEFINED_VALUE),
        ("visitor-2", "leave", "SelectionSetNode", UNDEFINED_VALUE),
        ("visitor-2", "leave", "FieldNode", UNDEFINED_VALUE),
        ("visitor-2", "leave", "SelectionSetNode", UNDEFINED_VALUE),
        ("visitor-2", "leave", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("visitor-2", "leave", "DocumentNode", UNDEFINED_VALUE),
    ]
    assert parallel_visited == [
        ("visitor-2", "enter", "DocumentNode", UNDEFINED_VALUE),
        ("visitor-1", "enter", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("visitor-2", "enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("visitor-1", "enter", "FieldNode", UNDEFINED_VALUE),
        ("visitor-2", "enter", "NameNode", "a"),
        ("visitor-2", "leave", "NameNode", "a"),
        ("visitor-2", "leave", "FieldNode", UNDEFINED_VALUE),
        ("visitor-1", "enter", "FieldNode", UNDEFINED_VALUE),
        ("visitor-2", "enter", "NameNode", "w"),
        ("visitor-2", "leave", "NameNode", "w"),
        ("visitor-2", "enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("visitor-1", "enter", "FieldNode", UNDEFINED_VALUE),
        ("visitor-2", "enter", "NameNode", "x"),
        ("visitor-2", "leave", "NameNode", "x"),
        ("visitor-2", "leave", "FieldNode", UNDEFINED_VALUE),
        ("visitor-2", "leave", "SelectionSetNode", UNDEFINED_VALUE),
        ("visitor-2", "leave", "FieldNode", UNDEFINED_VALUE),
        ("visitor-1", "enter", "FieldNode", UNDEFINED_VALUE),
        ("visitor-2", "enter", "NameNode", "c"),
        ("visitor-2", "leave", "NameNode", "c"),
        ("visitor-2", "enter", "SelectionSetNode", UNDEFINED_VALUE),
        ("visitor-1", "enter", "FieldNode", UNDEFINED_VALUE),
        ("visitor-2", "enter", "NameNode", "a"),
        ("visitor-2", "leave", "NameNode", "a"),
        ("visitor-2", "leave", "FieldNode", UNDEFINED_VALUE),
        ("visitor-1", "enter", "FieldNode", UNDEFINED_VALUE),
        ("visitor-2", "enter", "NameNode", "b"),
        ("visitor-2", "leave", "NameNode", "b"),
        ("visitor-2", "leave", "FieldNode", UNDEFINED_VALUE),
        ("visitor-1", "enter", "FieldNode", UNDEFINED_VALUE),
        ("visitor-2", "enter", "NameNode", "c"),
        ("visitor-2", "leave", "NameNode", "c"),
        ("visitor-2", "leave", "FieldNode", UNDEFINED_VALUE),
        ("visitor-2", "leave", "SelectionSetNode", UNDEFINED_VALUE),
        ("visitor-2", "leave", "FieldNode", UNDEFINED_VALUE),
        ("visitor-2", "leave", "SelectionSetNode", UNDEFINED_VALUE),
        ("visitor-1", "leave", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("visitor-2", "leave", "OperationDefinitionNode", UNDEFINED_VALUE),
        ("visitor-2", "leave", "DocumentNode", UNDEFINED_VALUE),
    ]
