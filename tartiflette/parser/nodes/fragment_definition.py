from .definition import NodeDefinition


class NodeFragmentDefinition(NodeDefinition):
    def __init__(
        self, path: str, location: "Location", name: str, type_condition: str
    ) -> None:
        super().__init__(path, "FragmentDefinition", location, name)
        self.callbacks = []
        self.type_condition = type_condition
