from functools import partial
from typing import Any, Callable, Dict, List, Optional, Set

from tartiflette.coercers.outputs.abstract_coercer import abstract_coercer
from tartiflette.coercers.outputs.directives_coercer import (
    output_directives_coercer,
)
from tartiflette.types.helpers.get_directive_instances import (
    compute_directive_nodes,
)
from tartiflette.types.type import GraphQLAbstractType
from tartiflette.utils.directives import wraps_with_directives

__all__ = ("GraphQLInterfaceType",)


class GraphQLInterfaceType(GraphQLAbstractType):
    """
    Definition of a GraphQL interface.
    """

    # Introspection attributes
    kind = "INTERFACE"

    def __init__(
        self,
        name: str,
        fields: Dict[str, "GraphQLField"],
        description: Optional[str] = None,
        directives: Optional[List["DirectiveNode"]] = None,
    ) -> None:
        """
        :param name: name of the interface
        :param fields: map of fields linked to the interface
        :param description: description of the interface
        :param directives: list of directives linked to the interface
        :type name: str
        :type fields: Dict[str, GraphQLField]
        :type description: Optional[str]
        :type directives: Optional[List[DirectiveNode]]
        """
        super().__init__()
        self.name = name
        self.implemented_fields = fields or {}
        self.description = description
        self._possible_types: List["GraphQLType"] = []
        self._possible_types_set: Set[str] = set()

        # Directives
        self.directives = directives
        self.introspection_directives: Optional[Callable] = None

        # Coercers
        self.output_coercer: Optional[Callable] = None

        # Introspection attributes
        self.fields: List["GraphQLField"] = []

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if `other` instance is identical to `self`.
        :param other: object instance to compare to `self`
        :type other: Any
        :return: whether or not `other` is identical to `self`
        :rtype: bool
        """
        return self is other or (
            isinstance(other, GraphQLInterfaceType)
            and self.name == other.name
            and self.implemented_fields == other.implemented_fields
            and self.description == other.description
            and self.directives == other.directives
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a GraphQLInterfaceType instance.
        :return: the representation of a GraphQLInterfaceType instance
        :rtype: str
        """
        return (
            "GraphQLInterfaceType(name={!r}, fields={!r}, "
            "description={!r}, directives={!r})".format(
                self.name,
                self.implemented_fields,
                self.description,
                self.directives,
            )
        )

    def __str__(self) -> str:
        """
        Returns a human-readable representation of the interface.
        :return: a human-readable representation of the interface
        :rtype: str
        """
        return self.name

    # Introspection attribute
    @property
    def possibleTypes(  # pylint: disable=invalid-name
        self
    ) -> List["GraphQLObjectType"]:
        """
        Returns the list of possible types of the interface which is used by
        the introspection query.
        :return: the list of possible types
        :rtype: List[GraphQLObjectType]
        """
        return self._possible_types

    def find_field(self, name: str) -> "GraphQLField":
        """
        Returns the field corresponding to the filled in name.
        :param name: name of the field to return
        :type name: str
        :return: the field corresponding to the filled in name
        :rtype: GraphQLField
        """
        return self.implemented_fields[name]

    def add_possible_type(self, possible_type: "GraphQLObjectType") -> None:
        """
        Adds a GraphQLObjectType that implements the interface to its possible
        types.
        :param possible_type: GraphQLObjectType which implements the interface
        :type possible_type: GraphQLObjectType
        """
        self._possible_types.append(possible_type)
        self._possible_types_set.add(possible_type.name)

    def is_possible_type(self, gql_type: "GraphQLType") -> bool:
        """
        Determines if a GraphQLType is a possible types for the interface.
        :param gql_type: the GraphQLType to check
        :type gql_type: GraphQLType
        :return: whether or not the GraphQLType is a possible type
        :rtype: bool
        """
        return gql_type.name in self._possible_types_set

    def bake(self, schema: "GraphQLSchema") -> None:
        """
        Bakes the GraphQLInterfaceType and computes all the necessary stuff for
        execution.
        :param schema: the GraphQLSchema instance linked to the engine
        :type schema: GraphQLSchema
        """
        # Directives
        directives_definition = compute_directive_nodes(
            schema, self.directives
        )
        self.introspection_directives = wraps_with_directives(
            directives_definition=directives_definition,
            directive_hook="on_introspection",
        )

        # Coercers
        self.output_coercer = partial(
            output_directives_coercer,
            coercer=partial(abstract_coercer, abstract_type=self),
            directives=wraps_with_directives(
                directives_definition=directives_definition,
                directive_hook="on_pre_output_coercion",
                with_default=True,
            ),
        )

    async def bake_fields(
        self,
        schema: "GraphQLSchema",
        custom_default_resolver: Optional[Callable],
    ) -> None:
        """
        Bakes interface's fields.
        :param schema: the GraphQLSchema instance linked to the engine
        :param custom_default_resolver: callable that will replace the builtin
        default_resolver
        :type schema: GraphQLSchema
        :type custom_default_resolver: Optional[Callable]
        """
        if self.implemented_fields:
            for field in self.implemented_fields.values():
                field.bake(schema, custom_default_resolver)
                field = await field.on_post_bake()

                if not field.name.startswith("__"):
                    self.fields.append(field)
