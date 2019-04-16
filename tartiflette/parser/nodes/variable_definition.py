from tartiflette.utils.arguments import UNDEFINED_VALUE

from .definition import NodeDefinition


class NodeVariableDefinition(NodeDefinition):
    def __init__(self, path: str, location: "Location", name: str) -> None:
        super().__init__(path, "VariableDefinition", location, name)
        self.var_name = None
        self.default_value = UNDEFINED_VALUE
        self.is_nullable = True
        self.is_list = False
