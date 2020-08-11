from functools import partial
from typing import Any, Callable, Dict, List, Optional, Set

from tartiflette.coercers.outputs.abstract_coercer import abstract_coercer
from tartiflette.coercers.outputs.directives_coercer import (
    output_directives_coercer,
)
from tartiflette.types.helpers.get_directive_instances import (
    compute_directive_nodes,
)
from tartiflette.types.type import (
    GraphQLAbstractType,
    GraphQLCompositeType,
    GraphQLExtension,
    GraphQLType,
)
from tartiflette.utils.directives import wraps_with_directives

__all__ = ("GraphQLUnionType",)


class GraphQLUnionType(GraphQLAbstractType, GraphQLCompositeType):
    """
    Definition of a GraphQL union.
    """

    # Introspection attributes
    kind = "UNION"

    def __init__(
        self,
        name: str,
        types: List[str],
        description: Optional[str] = None,
        directives: Optional[List["DirectiveNode"]] = None,
    ) -> None:
        """
        :param name: name of the union
        :param types: list of types which compose the union
        :param description: description of the union
        :param directives: list of directives linked to the union
        :type name: str
        :type types: List[str]
        :type description: Optional[str]
        :type directives: Optional[List[DirectiveNode]]
        """
        super().__init__()
        self.name = name
        self.types = types
        self.description = description
        self.possible_types: List["GraphQLType"] = []
        self._possible_types_set: Set[str] = set()
        self._fields: Dict[str, "GraphQLField"] = {}

        # Directives
        self.directives = directives
        self.introspection_directives: Optional[Callable] = None

        # Coercers
        self.output_coercer: Optional[Callable] = None

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if `other` instance is identical to `self`.
        :param other: object instance to compare to `self`
        :type other: Any
        :return: whether or not `other` is identical to `self`
        :rtype: bool
        """
        return self is other or (
            isinstance(other, GraphQLUnionType)
            and self.name == other.name
            and self.types == other.types
            and self.description == other.description
            and self.directives == other.directives
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a GraphQLUnionType instance.
        :return: the representation of a GraphQLUnionType instance
        :rtype: str
        """
        return (
            "GraphQLUnionType(name={!r}, types={!r}, "
            "description={!r}, directives={!r})".format(
                self.name, self.types, self.description, self.directives
            )
        )

    def __str__(self) -> str:
        """
        Returns a human-readable representation of the union.
        :return: a human-readable representation of the union
        :rtype: str
        """
        return self.name

    # Introspection attribute
    @property
    def possibleTypes(  # pylint: disable=invalid-name
        self,
    ) -> List["GraphQLObjectType"]:
        """
        Returns the list of possible types of the union which is used by the
        introspection query.
        :return: the list of possible types
        :rtype: List[GraphQLObjectType]
        """
        return self.possible_types

    def add_field(self, field: "GraphQLField") -> None:
        """
        Adds the filled in field to the list of implemented fields.
        :param field: field to add to the list
        :type field: GraphQLField
        """
        if field.name == "__typename":
            self._fields[field.name] = field

    def find_field(self, name: str) -> "GraphQLField":
        """
        Returns the field corresponding to the filled in name.
        :param name: name of the field to return
        :type name: str
        :return: the field corresponding to the filled in name
        :rtype: GraphQLField
        """
        return self._fields[name]

    def is_possible_type(self, gql_type: "GraphQLType") -> bool:
        """
        Determines if a GraphQLType is a possible types for the union.
        :param gql_type: the GraphQLType to check
        :type gql_type: GraphQLType
        :return: whether or not the GraphQLType is a possible type
        :rtype: bool
        """
        return gql_type.name in self._possible_types_set

    @property
    def possible_types_set(self) -> set:
        return self._possible_types_set

    def bake(self, schema: "GraphQLSchema") -> None:
        """
        Bakes the GraphQLUnionType and computes all the necessary stuff for
        execution.
        :param schema: the GraphQLSchema instance linked to the engine
        :type schema: GraphQLSchema
        """
        for type_name in self.types:
            schema_type = schema.find_type(type_name)
            self.possible_types.append(schema_type)
            self._possible_types_set.add(type_name)

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
        Bakes union's fields.
        :param schema: the GraphQLSchema instance linked to the engine
        :param custom_default_resolver: callable that will replace the builtin
        default_resolver
        :type schema: GraphQLSchema
        :type custom_default_resolver: Optional[Callable]
        """
        for field in self._fields.values():
            field.bake(schema, custom_default_resolver)
            await field.on_post_bake()


class GraphQLUnionTypeExtension(GraphQLType, GraphQLExtension):
    def __init__(self, name, directives, types):
        self.name = name
        self.directives = directives
        self.types = types or []

    def bake(self, schema):
        extended = schema.find_type(self.name)

        extended.directives.extend(self.directives)
        extended.types.extend(self.types)

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if `other` instance is identical to `self`.
        :param other: object instance to compare to `self`
        :type other: Any
        :return: whether or not `other` is identical to `self`
        :rtype: bool
        """
        return self is other or (
            isinstance(other, GraphQLUnionTypeExtension)
            and other.directives == self.directives
            and other.name == self.name
            and other.types == self.types
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a GraphQLType instance.
        :return: the representation of a GraphQLType instance
        :rtype: str
        """
        return (
            f"GraphQLUnionTypeExtension("
            f"name={repr(self.name)}, "
            f"directives={repr(self.directives)}, "
            f"types={repr(self.types)})"
        )
