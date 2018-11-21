import pytest


@pytest.mark.parametrize(
    "vtype,expected",
    [
        ("Lol", "Lol"),
        ("String", str),
        ("Int", int),
        ("Boolean", bool),
        ("Float", float),
    ],
)
def test_parser_nodes_node_definition(vtype, expected):
    from tartiflette.parser.nodes.definition import NodeDefinition

    nd = NodeDefinition(["a", "b"], "FragmentDefinition", None, "a")

    assert nd.var_type is None
    nd.var_type = vtype
    assert nd.var_type == expected
