from typing import Dict, Optional

from tartiflette.types.argument import GraphQLArgument
from tartiflette.types.type import GraphQLType


class GraphQLInputObjectType(GraphQLType):
    """Input Object Type Definition
    Input Object Type Definition

    An input object defines a structured collection of fields which may be
    supplied to a field argument.

    Using `NonNull` will ensure that a value must be provided by the query
    """

    def __init__(
        self,
        name: str,
        fields: Dict[str, GraphQLArgument],
        description: Optional[str] = None,
        schema=None,
    ):
        super().__init__(name=name, description=description, schema=schema)
        self.fields: Dict[str, GraphQLArgument] = fields

    def __repr__(self) -> str:
        return "{}(name={!r}, fields={!r}, description={!r})".format(
            self.__class__.__name__, self.name, self.fields, self.description
        )

    def __eq__(self, other):
        return super().__eq__(other) and self.fields == other.fields

    # Introspection Attribute
    @property
    def kind(self):
        return "INPUT_OBJECT"
