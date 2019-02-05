from typing import Any, Dict

from tartiflette.types.location import Location

from .node import Node


class NodeDirective(Node):
    def __init__(self, path: str, location: Location, name: str) -> None:
        super().__init__(path, "Directive", location, name)
        self.arguments: Dict[str, Any] = {}
