from functools import partial
from typing import Any, Callable, Dict, List, Optional

from tartiflette.coercers.outputs.directives_coercer import (
    output_directives_coercer,
)
from tartiflette.coercers.outputs.object_coercer import object_coercer
from tartiflette.types.helpers.get_directive_instances import (
    compute_directive_nodes,
)
from tartiflette.types.type import GraphQLType
from tartiflette.utils.directives import wraps_with_directives

__all__ = ("GraphQLObjectType",)


class GraphQLObjectType(GraphQLType):
    """
    Definition of a GraphQL object.
    """

    # Introspection attributes
    kind = "OBJECT"

    def __init__(
        self,
        name: str,
        fields: Dict[str, "GraphQLField"],
        interfaces: Optional[List[str]] = None,
        description: Optional[str] = None,
        directives: Optional[List["DirectiveNode"]] = None,
    ) -> None:
        """
        :param name: name of the object
        :param fields: map of fields linked to the object
        :param interfaces: list of interface names implemented by the object
        :param description: description of the object
        :param directives: list of directives linked to the object
        :type name: str
        :type fields: Dict[str, GraphQLField]
        :type interfaces: Optional[List[str]]
        :type description: Optional[str]
        :type directives: Optional[List[DirectiveNode]]
        """
        self.name = name
        self.implemented_fields = fields or {}
        self.interfaces_names = interfaces or []
        self.description = description

        # Directives
        self.directives = directives
        self.introspection_directives: Optional[Callable] = None

        # Coercers
        self.output_coercer: Optional[Callable] = None

        # Introspection attributes
        self.interfaces: Optional[List["GraphQLInterfaceType"]] = None
        self.fields: Optional[List["GraphQLField"]] = None

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if `other` instance is identical to `self`.
        :param other: object instance to compare to `self`
        :type other: Any
        :return: whether or not `other` is identical to `self`
        :rtype: bool
        """
        return self is other or (
            isinstance(other, GraphQLObjectType)
            and self.name == other.name
            and self.implemented_fields == other.implemented_fields
            and self.interfaces_names == other.interfaces_names
            and self.description == other.description
            and self.directives == other.directives
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a GraphQLObjectType instance.
        :return: the representation of a GraphQLObjectType instance
        :rtype: str
        """
        return (
            "GraphQLObjectType(name={!r}, fields={!r}, "
            "interfaces={!r}, description={!r}, directives={!r})".format(
                self.name,
                self.implemented_fields,
                self.interfaces_names,
                self.description,
                self.directives,
            )
        )

    def __str__(self) -> str:
        """
        Returns a human-readable representation of the object.
        :return: a human-readable representation of the object
        :rtype: str
        """
        return self.name

    def add_field(self, field: "GraphQLField") -> None:
        """
        Adds the filled in field to the list of implemented fields.
        :param field: field to add to the list
        :type field: GraphQLField
        """
        self.implemented_fields[field.name] = field

    def find_field(self, name: str) -> "GraphQLField":
        """
        Returns the field corresponding to the filled in name.
        :param name: name of the field to return
        :type name: str
        :return: the field corresponding to the filled in name
        :rtype: GraphQLField
        """
        return self.implemented_fields[name]

    def bake(self, schema: "GraphQLSchema") -> None:
        """
        Bakes the GraphQLObjectType and computes all the necessary stuff for
        execution.
        :param schema: the GraphQLSchema instance linked to the engine
        :type schema: GraphQLSchema
        """
        if self.interfaces_names:
            self.interfaces: List["GraphQLInterfaceType"] = []
            for interface_name in self.interfaces_names:
                interface = schema.find_type(interface_name)
                self.interfaces.append(interface)
                interface.add_possible_type(self)

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
            coercer=partial(object_coercer, object_type=self),
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
        Bakes object's fields.
        :param schema: the GraphQLSchema instance linked to the engine
        :param custom_default_resolver: callable that will replace the builtin
        default_resolver
        :type schema: GraphQLSchema
        :type custom_default_resolver: Optional[Callable]
        """
        if self.implemented_fields:
            self.fields: List["GraphQLField"] = []
            for field in self.implemented_fields.values():
                field.bake(schema, custom_default_resolver)
                field = await field.on_post_bake()

                if not field.name.startswith("__"):
                    self.fields.append(field)
