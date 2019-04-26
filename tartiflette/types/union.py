from typing import Any, Callable, List, Optional, Set

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
    ) -> None:
        super().__init__(name=name, description=description, schema=schema)
        self.gql_types = gql_types
        self._possible_types = []
        self._possible_types_set: Set[str] = set()

    def __repr__(self) -> str:
        return "{}(name={!r}, gql_types={!r}, description={!r})".format(
            self.__class__.__name__,
            self.name,
            self.gql_types,
            self.description,
        )

    def __eq__(self, other: Any) -> bool:
        return super().__eq__(other) and self.gql_types == other.gql_types

    def is_possible_types(self, gql_type: "GraphQLType") -> bool:
        """
        Determines if a GraphQLType is a possible types for the union.
        :param gql_type: the GraphQLType to check
        :type gql_type: GraphQLType
        :return: whether or not the GraphQLType is a possible type
        :rtype: bool
        """
        return gql_type.name in self._possible_types_set

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

    def bake(
        self,
        schema: "GraphQLSchema",
        custom_default_resolver: Optional[Callable],
    ) -> None:
        super().bake(schema, custom_default_resolver)
        for gql_type_name in self.gql_types:
            schema_type = schema.find_type(gql_type_name)
            self._possible_types.append(schema_type)
            self._possible_types_set.add(gql_type_name)
