import pytest


def test_parser_nodes_node___repr__():
    from tartiflette.parser.nodes.node import Node

    n = Node(["K"], "R", None, "T")

    assert n.__repr__() == "R(T)"


def test_parser_nodes_node_add_child():
    from tartiflette.parser.nodes.node import Node

    n = Node(["K"], "R", None, "T")

    n.add_child("T")

    assert n.children == ["T"]


def test_parser_nodes_node_set_parent():
    from tartiflette.parser.nodes.node import Node

    n = Node(["K"], "R", None, "T")

    n.set_parent("T")

    assert n.parent == "T"
