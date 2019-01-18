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
        self._fields: Dict[str, GraphQLArgument] = fields
        self._input_fields = [x for _, x in self._fields.items()]

    def __repr__(self) -> str:
        return "{}(name={!r}, fields={!r}, description={!r})".format(
            self.__class__.__name__, self.name, self._fields, self.description
        )

    def __eq__(self, other):
        return super().__eq__(other) and self._fields == other._fields

    # Introspection Attribute
    @property
    def kind(self):
        return "INPUT_OBJECT"

    @property
    def inputFields(self):
        return self._input_fields
