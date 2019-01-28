from typing import List, Union


class Node:
    def __init__(
        self,
        path: Union[str, List[str]],
        libgraphql_type: str,
        location: "Location",
        name: str,
    ) -> None:
        self.path = path
        self.parent = None
        self.children = []
        self.libgraphql_type = libgraphql_type
        self.location = location
        self.name = name

    def __repr__(self) -> str:
        return "%s(%s)" % (self.libgraphql_type, self.name)

    def add_child(self, node: "Node") -> None:
        self.children.append(node)

    def set_parent(self, node: "Node") -> None:
        self.parent = node
