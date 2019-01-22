from .definition import NodeDefinition


class NodeOperationDefinition(NodeDefinition):
    def __init__(self, path, location, name, otype):
        super().__init__(path, "OperationDefinition", location, name)

        self.type = otype
