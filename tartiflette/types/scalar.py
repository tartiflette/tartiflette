from typing import Any, Callable, Dict, List, Optional

from tartiflette.types.helpers import get_directive_implem_list
from tartiflette.types.type import GraphQLType


class GraphQLScalarType(GraphQLType):
    """
    Scalar Type Definition

    The leaf values of any request and input values to arguments are
    Scalars (or Enums which are special Scalars) and are defined with a name
    and a series of functions used to convert to and from the request or SDL.

    Example: see the default Int, String or Boolean scalars.
    """

    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        directives: Optional[Dict[str, Optional[dict]]] = None,
        schema: Optional["GraphQLSchema"] = None,
    ) -> None:
        super().__init__(name=name, description=description, schema=schema)
        self.coerce_output = None
        self.coerce_input = None
        self.parse_literal = None

        self._directives = directives

        # Introspection Attribute
        self._directives_implementations = None

    def __repr__(self) -> str:
        return "{}(name={!r}, description={!r})".format(
            self.__class__.__name__, self.name, self.description
        )

    def __eq__(self, other: Any) -> bool:
        # TODO: Comparing function pointers is not ideal here...
        return (
            super().__eq__(other)
            and self.coerce_output == other.coerce_output
            and self.coerce_input == other.coerce_input
            and self.parse_literal == other.parse_literal
        )

    # Introspection Attribute
    @property
    def kind(self) -> str:
        return "SCALAR"

    @property
    def directives(self) -> List[Dict[str, Any]]:
        return self._directives_implementations

    def bake(
        self,
        schema: "GraphQLSchema",
        custom_default_resolver: Optional[Callable],
    ) -> None:
        super().bake(schema, custom_default_resolver)
        self._directives_implementations = get_directive_implem_list(
            self._directives, self._schema
        )
