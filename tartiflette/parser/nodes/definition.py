from typing import Any, Union

from .node import Node


class NodeDefinition(Node):
    def __init__(
        self, path: str, libgraphql_type: str, location: "Location", name: str
    ) -> None:
        super().__init__(path, libgraphql_type, location, name)
        self._types = {
            "String": str,
            "Int": int,
            "Boolean": bool,
            "Float": float,
        }
        self._type = None

    @property
    def var_type(self) -> Union[str, int, bool, float, Any]:
        return self._type

    @var_type.setter
    def var_type(self, var_type: Union[str, Any]) -> None:
        try:
            self._type = self._types[var_type]
        except KeyError:
            # TODO Maybe validate it's a known type from idl(s)
            self._type = var_type
