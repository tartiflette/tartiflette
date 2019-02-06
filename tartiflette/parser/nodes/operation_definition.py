from .definition import NodeDefinition


class NodeOperationDefinition(NodeDefinition):
    def __init__(
        self, path: str, location: "Location", name: str, operation_type: str
    ) -> None:
        super().__init__(path, "OperationDefinition", location, name)
        self.type = operation_type

    @property
    def allow_parallelization(self) -> bool:
        return self.type != "Mutation"
