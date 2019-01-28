from typing import Any, Callable, Dict, List, Optional

from tartiflette.types.helpers import get_directive_implem_list
from tartiflette.types.type import GraphQLType


class GraphQLEnumValue:
    """
    Enums are special leaf values.
    `GraphQLEnumValue`s is a way to represent them.
    """

    def __init__(
        self,
        value: Any = None,
        description: Optional[str] = None,
        directives: Optional[Dict[str, Optional[dict]]] = None,
    ) -> None:
        self.value = value
        self.description = description
        self._directives = directives
        self._schema = None
        self._directives_implementations = None

        # Introspection Attribute
        self.isDeprecated = False  # pylint: disable=invalid-name

    def __repr__(self) -> str:
        return "{}(value={!r}, description={!r})".format(
            self.__class__.__name__, self.value, self.description
        )

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, other: Any) -> bool:
        return self is other or (
            type(self) is type(other) and self.value == other.value
        )

    # Introspection Attribute
    @property
    def name(self) -> str:
        return self.value

    @property
    def directives(self) -> List[Dict[str, Any]]:
        return self._directives_implementations

    def bake(self, schema: "GraphQLSchema") -> None:
        self._schema = schema
        self._directives_implementations = get_directive_implem_list(
            self._directives, self._schema
        )


class GraphQLEnumType(GraphQLType):
    """
    Enum Type Definition

    Some leaf values of requests and input values are Enums.
    GraphQL serializes Enum values as strings, however internally
    Enums can be represented by any kind of type, often integers.

    Note: If a value is not provided in a definition,
    the name of the enum value will be used as its internal value.
    """

    def __init__(
        self,
        name: str,
        values: List[GraphQLEnumValue],
        description: Optional[str] = None,
        schema: Optional["GraphQLSchema"] = None,
    ) -> None:
        super().__init__(
            name=name,
            description=description,
            is_enum_value=True,
            schema=schema,
        )
        self.values = values

    def __repr__(self) -> str:
        return "{}(name={!r}, values={!r}, description={!r})".format(
            self.__class__.__name__, self.name, self.values, self.description
        )

    def __eq__(self, other: Any) -> bool:
        return super().__eq__(other) and self.values == other.values

    # Introspection Attribute
    @property
    def kind(self) -> str:
        return "ENUM"

    # Introspection Attribute
    @property
    def enumValues(  # pylint: disable=invalid-name
        self
    ) -> List[GraphQLEnumValue]:
        return self.values

    def bake(
        self,
        schema: "GraphQLSchema",
        custom_default_resolver: Optional[Callable],
    ) -> None:
        super().bake(schema, custom_default_resolver)
        for value in self.values:
            value.bake(schema)
