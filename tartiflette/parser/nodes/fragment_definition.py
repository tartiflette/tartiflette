from .definition import NodeDefinition


class NodeFragmentDefinition(NodeDefinition):
    def __init__(self, path, location, name, type_condition):
        super().__init__(path, "FragmentDefinition", location, name)

        self.callbacks = []
        self.type_condition = type_condition
