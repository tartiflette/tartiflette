from tartiflette.types.location import Location

from .node import Node


class NodeArgument(Node):
    def __init__(self, path: str, location: Location, name: str) -> None:
        super().__init__(path, "Argument", location, name)
        self.value = None
