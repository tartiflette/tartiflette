import pytest


def test_parser_nodes_node_fragment_definition_inst():
    from tartiflette.parser.nodes.fragment_definition import (
        NodeFragmentDefinition,
    )

    nfd = NodeFragmentDefinition(["A"], "Here", "Lol", "Nija")

    assert nfd.callbacks == []
    assert nfd.type_condition == "Nija"
    assert nfd.libgraphql_type == "FragmentDefinition"
