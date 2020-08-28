from functools import partial
from typing import Any, Callable, Dict, List, Optional, Union

from tartiflette.coercers.outputs.compute import get_output_coercer
from tartiflette.resolver.default import default_field_resolver
from tartiflette.resolver.factory import resolve_field
from tartiflette.types.helpers.get_directive_instances import (
    compute_directive_nodes,
)
from tartiflette.types.helpers.type import get_graphql_type
from tartiflette.utils.directives import wraps_with_directives

__all__ = ("GraphQLField",)


class GraphQLField:
    """
    Definition of a GraphQL field.
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(
        self,
        name: str,
        gql_type: Union["GraphQLList", "GraphQLNonNull", str],
        arguments: Optional[Dict[str, "GraphQLArgument"]] = None,
        resolver: Optional[Callable] = None,
        description: Optional[str] = None,
        directives: Optional[List["DirectiveNode"]] = None,
    ) -> None:
        """
        :param name: name of the field
        :param gql_type: GraphQL type of the field
        :param arguments: map of arguments linked to the field
        :param resolver: callable in charge of resolving the field
        :param description: description of the field
        :param directives: list of directives linked to the field
        :type name: str
        :type gql_type: Union[GraphQLList, GraphQLNonNull, str]
        :type arguments: Optional[Dict[str, GraphQLArgument]]
        :type resolver: Optional[Callable]
        :type description: Optional[str]
        :type directives: Optional[List[DirectiveNode]]
        """
        self.name = name
        self.gql_type = gql_type
        self.arguments = arguments or {}
        self.description = description
        self.graphql_type: Optional["GraphQLType"] = None

        # Directives
        self.directives = directives
        self.on_post_bake: Optional[Callable] = None
        self.introspection_directives: Optional[Callable] = None

        # Resolvers
        self.raw_resolver = resolver
        self.resolver: Optional[Callable] = None
        self.subscribe: Optional[Callable] = None

        # Arguments coercer
        self.arguments_coercer: Optional[Callable] = None
        self.query_arguments_coercer: Optional[Callable] = None
        self.subscription_arguments_coercer: Optional[Callable] = None

        # Introspection attributes
        self.isDeprecated: bool = False  # pylint: disable=invalid-name
        self.args: List["GraphQLArgument"] = []

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if `other` instance is identical to `self`.
        :param other: object instance to compare to `self`
        :type other: Any
        :return: whether or not `other` is identical to `self`
        :rtype: bool
        """
        return self is other or (
            isinstance(other, GraphQLField)
            and self.name == other.name
            and self.gql_type == other.gql_type
            and self.arguments == other.arguments
            and self.description == other.description
            and self.resolver == other.resolver
            and self.directives == other.directives
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a GraphQLField instance.
        :return: the representation of a GraphQLField instance
        :rtype: str
        """
        return (
            "GraphQLField(name={!r}, gql_type={!r}, arguments={!r}, "
            "resolver={!r}, description={!r}, directives={!r})".format(
                self.name,
                self.gql_type,
                self.arguments,
                self.resolver,
                self.description,
                self.directives,
            )
        )

    def __str__(self) -> str:
        """
        Returns a human-readable representation of the field.
        :return: a human-readable representation of the field
        :rtype: str
        """
        return self.name

    # Introspection attribute
    @property
    def kind(self) -> str:
        """
        Returns the kind of the field which is used by the introspection query.
        :return: the kind of the field
        :rtype: str
        """
        try:
            return self.gql_type.kind
        except AttributeError:
            pass
        return "FIELD"

    # Introspection attribute
    @property
    def type(self) -> Union[str, "GraphQLType"]:
        """
        Returns the GraphQL type of the field which is used by the
        introspection query.
        :return: the GraphQL type of the field
        :rtype: Union[str, GraphQLType]
        """
        return self.graphql_type

    def bake(
        self,
        schema: "GraphQLSchema",
        custom_default_resolver: Optional[Callable],
        interface_names: Optional[List[str]] = None,
    ) -> None:
        """
        Bakes the GraphQLField and computes all the necessary stuff for
        execution.
        :param schema: the GraphQLSchema instance linked to the SDL
        :param custom_default_resolver: callable that will replace the builtin
        default_resolver
        :param interface_names: interfaces which parent object type implements
        :type schema: GraphQLSchema
        :type custom_default_resolver: Optional[Callable]
        :type interface_names: Optional[List[str]]
        """
        self.graphql_type = get_graphql_type(schema, self.gql_type)

        if self.subscription_arguments_coercer is not None:
            self.arguments_coercer = self.subscription_arguments_coercer
        elif self.query_arguments_coercer is not None:
            self.arguments_coercer = self.query_arguments_coercer
        else:
            self.arguments_coercer = schema.default_arguments_coercer

        # Directives
        directives_definition = compute_directive_nodes(
            schema, self.directives
        )
        self.on_post_bake = partial(
            wraps_with_directives(
                directives_definition=directives_definition,
                directive_hook="on_post_bake",
                with_default=True,
            ),
            self,
        )
        self.introspection_directives = wraps_with_directives(
            directives_definition=directives_definition,
            directive_hook="on_introspection",
        )

        for interface_name in interface_names or []:
            interface = schema.find_type(interface_name)
            if interface.has_field(self.name):
                raw_resolver = interface.find_field(self.name).raw_resolver
                if raw_resolver:
                    interface_resolver = raw_resolver
                    break
        else:
            interface_resolver = None

        # Resolvers
        self.resolver = partial(
            resolve_field,
            field_definition=self,
            resolver=wraps_with_directives(
                directives_definition=directives_definition,
                directive_hook="on_field_execution",
                func=(
                    self.raw_resolver
                    or interface_resolver
                    or custom_default_resolver
                    or default_field_resolver
                ),
                is_resolver=True,
                with_default=True,
            ),
            output_coercer=get_output_coercer(self.graphql_type),
        )

        for argument in self.arguments.values():
            argument.bake(schema)
            self.args.append(argument)
