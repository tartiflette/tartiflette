from typing import Any, Dict, List, Optional, Union

from tartiflette.types.helpers import (
    get_directive_instances,
    wraps_with_directives,
)
from tartiflette.types.type import GraphQLType
from tartiflette.utils.coercer_way import CoercerWay


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
        fields: Dict[str, "GraphQLArgument"],
        description: Optional[str] = None,
        schema: Optional["GraphQLSchema"] = None,
        directives: Optional[Dict[str, Union[str, Dict[str, Any]]]] = None,
    ) -> None:
        super().__init__(name=name, description=description, schema=schema)
        self._fields = fields
        self._input_fields: List["GraphQLArgument"] = list(
            self._fields.values()
        )
        self._directives = directives
        self._directives_implementations = {}

    def __repr__(self) -> str:
        return "{}(name={!r}, fields={!r}, description={!r})".format(
            self.__class__.__name__, self.name, self._fields, self.description
        )

    def __eq__(self, other: Any) -> bool:
        return super().__eq__(other) and self._fields == other._fields

    @property
    def arguments(self) -> Dict[str, "GraphQLArgument"]:
        return self._fields

    # Introspection Attribute
    @property
    def kind(self) -> str:
        return "INPUT_OBJECT"

    # Introspection Attribute
    @property
    def inputFields(  # pylint: disable=invalid-name
        self
    ) -> List["GraphQLArgument"]:
        return self.input_fields

    def bake(self, schema: "GraphQLSchema") -> None:
        super().bake(schema)
        directives_definition = get_directive_instances(
            self._directives, self._schema
        )
        self._directives_implementations = {
            CoercerWay.INPUT: wraps_with_directives(
                directives_definition=directives_definition,
                directive_hook="on_post_input_coercion",
            )
        }

        self._introspection_directives = wraps_with_directives(
            directives_definition=directives_definition,
            directive_hook="on_introspection",
        )

        for arg in self._fields.values():
            arg.bake(self._schema)

    @property
    def input_fields(self):
        return self._input_fields

    @property
    def directives(self):
        return self._directives_implementations
