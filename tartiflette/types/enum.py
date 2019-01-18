from typing import Any, List, Optional

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
        directives=None,
    ):
        self.value = value
        self.description = description
        self._directives = directives
        self._schema = None
        self._directives_implementations = None

        # Introspection Attribute
        self.isDeprecated = False  # pylint: disable=invalid-name

    def __repr__(self):
        return "{}(value={!r}, description={!r})".format(
            self.__class__.__name__, self.value, self.description
        )

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return self is other or (
            type(self) is type(other) and self.value == other.value
        )

    # Introspection Attribute
    @property
    def name(self):
        return self.value

    @property
    def directives(self):
        return self._directives_implementations

    def bake(self, schema):
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
        schema=None,
    ):
        super().__init__(
            name=name,
            description=description,
            is_enum_value=True,
            schema=schema,
        )
        self.values = values

    def __repr__(self):
        return "{}(name={!r}, values={!r}, description={!r})".format(
            self.__class__.__name__, self.name, self.values, self.description
        )

    def __eq__(self, other):
        return super().__eq__(other) and self.values == other.values

    # Introspection Attribute
    @property
    def kind(self):
        return "ENUM"

    # Introspection Attribute
    @property
    def enumValues(self):  # pylint: disable=invalid-name
        return self.values

    def bake(self, schema, cdr):
        super().bake(schema, cdr)
        for value in self.values:
            value.bake(schema)
