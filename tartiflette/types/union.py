from typing import Any, Dict, List, Optional

from tartiflette.types.helpers import (
    get_directive_instances,
    wraps_with_directives,
)
from tartiflette.types.type import GraphQLType


class GraphQLUnionType(GraphQLType):
    """
    Union Type Definition

    When a field can return one of a heterogeneous set of types, a Union
    type is used to describe what types are possible as well as providing
    a function to determine which type is actually used when the field
    if resolved.
    """

    def __init__(
        self,
        name: str,
        gql_types: List[GraphQLType],
        description: Optional[str] = None,
        schema: Optional["GraphQLSchema"] = None,
        directives: Optional[List[Dict[Any, Any]]] = None,
    ) -> None:
        super().__init__(name=name, description=description, schema=schema)
        self.gql_types = gql_types
        self._possible_types = []
        self._directives = directives

    def __repr__(self) -> str:
        return "{}(name={!r}, gql_types={!r}, description={!r})".format(
            self.__class__.__name__,
            self.name,
            self.gql_types,
            self.description,
        )

    def __eq__(self, other: Any) -> bool:
        return super().__eq__(other) and self.gql_types == other.gql_types

    # Introspection Attribute
    @property
    def kind(self) -> str:
        return "UNION"

    @property
    def is_union(self) -> bool:
        return True

    # Introspection Attribute
    @property
    def possibleTypes(  # pylint: disable=invalid-name
        self
    ) -> List[GraphQLType]:
        return self._possible_types

    def bake(self, schema: "GraphQLSchema") -> None:
        super().bake(schema)

        self._possible_types = [
            self._schema.find_type(x) for x in self.gql_types
        ]

        self._introspection_directives = wraps_with_directives(
            directives_definition=get_directive_instances(
                self._directives, self._schema
            ),
            directive_hook="on_introspection",
        )
