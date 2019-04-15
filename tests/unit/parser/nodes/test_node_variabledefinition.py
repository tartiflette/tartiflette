from tartiflette.utils.arguments import UNDEFINED_VALUE


def test_parser_nodes_node_variable_definition_inst():
    from tartiflette.parser.nodes.variable_definition import (
        NodeVariableDefinition,
    )

    nvd = NodeVariableDefinition(["A"], "Lol", "Nija")

    assert nvd.var_name is None
    assert nvd.default_value is UNDEFINED_VALUE
    assert nvd.is_nullable is True
    assert nvd.is_list is False
    assert nvd.libgraphql_type == "VariableDefinition"
