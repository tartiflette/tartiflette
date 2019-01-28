from .definition import NodeDefinition


class NodeOperationDefinition(NodeDefinition):
    def __init__(
        self, path: str, location: "Location", name: str, operation_type: str
    ) -> None:
        super().__init__(path, "OperationDefinition", location, name)
        self.type = operation_type
