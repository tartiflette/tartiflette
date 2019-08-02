from functools import partial
from typing import Any, Callable, Dict, List, Optional, Union

from tartiflette.coercers.argument import argument_coercer
from tartiflette.coercers.literals.compute import get_literal_coercer
from tartiflette.types.helpers.get_directive_instances import (
    compute_directive_nodes,
)
from tartiflette.types.helpers.type import get_graphql_type
from tartiflette.types.type import GraphQLType
from tartiflette.utils.directives import wraps_with_directives

__all__ = ("GraphQLArgument",)


class GraphQLArgument:
    """
    Definition of a GraphQL argument.
    """

    def __init__(
        self,
        name: str,
        gql_type: Union["GraphQLList", "GraphQLNonNull", str],
        default_value: Optional["ValueNode"] = None,
        description: Optional[str] = None,
        directives: Optional[List["DirectiveNode"]] = None,
        definition: Optional["InputValueDefinitionNode"] = None,
    ) -> None:
        """
        :param name: name of the argument
        :param gql_type: GraphQL type of the argument
        :param default_value: AST node which represents the default value
        :param description: description of the argument
        :param directives: list of directives linked to the argument
        :param definition: the input value definition AST node
        :type name: str
        :type gql_type: Union[GraphQLList, GraphQLNonNull, str]
        :type default_value: Optional[ValueNode]
        :type description: Optional[str]
        :type directives: Optional[List[DirectiveNode]]
        :type definition: Optional[InputValueDefinitionNode]
        """
        self.name = name
        self.gql_type = gql_type
        self.default_value = default_value
        self.description = description
        self.definition = definition
        self.graphql_type: Optional["GraphQLType"] = None

        # Directives
        self.directives = directives
        self.introspection_directives: Optional[Callable] = None

        # Coercers
        self.literal_coercer: Optional[Callable] = None
        self.coercer: Optional[Callable] = None

        # Introspection attributes
        self.type: Union["GraphQLType", Dict[str, Any]] = {}

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if `other` instance is identical to `self`.
        :param other: object instance to compare to `self`
        :type other: Any
        :return: whether or not `other` is identical to `self`
        :rtype: bool
        """
        return self is other or (
            isinstance(other, GraphQLArgument)
            and self.name == other.name
            and self.gql_type == other.gql_type
            and self.default_value == other.default_value
            and self.description == other.description
            and self.directives == other.directives
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a GraphQLArgument instance.
        :return: the representation of a GraphQLArgument instance
        :rtype: str
        """
        return (
            "GraphQLArgument(name={!r}, gql_type={!r}, default_value={!r}, "
            "description={!r}, directives={!r})".format(
                self.name,
                self.gql_type,
                self.default_value,
                self.description,
                self.directives,
            )
        )

    def __str__(self) -> str:
        """
        Returns a human-readable representation of the argument.
        :return: a human-readable representation of the argument
        :rtype: str
        """
        return self.name

    # Introspection attribute
    @property
    def defaultValue(  # pylint: disable=invalid-name
        self
    ) -> Optional["ValueNode"]:
        """
        Returns the default value of the argument which is used by the
        introspection query.
        :return: the default value of the argument
        :rtype: Optional[ValueNode]
        """
        return self.default_value

    def bake(self, schema: "GraphQLSchema") -> None:
        """
        Bakes the GraphQLArgument and computes all the necessary stuff for
        execution.
        :param schema: the GraphQLSchema instance linked to the engine
        :type schema: GraphQLSchema
        """
        self.graphql_type = get_graphql_type(schema, self.gql_type)

        if isinstance(self.gql_type, GraphQLType):
            self.type = self.gql_type
        else:
            self.type["name"] = self.gql_type
            self.type["kind"] = self.graphql_type.kind

        # Directives
        directives_definition = compute_directive_nodes(
            schema, self.directives
        )
        self.introspection_directives = wraps_with_directives(
            directives_definition=directives_definition,
            directive_hook="on_introspection",
        )

        # Coercers
        self.literal_coercer = get_literal_coercer(self.graphql_type)
        self.coercer = partial(
            argument_coercer,
            directives=wraps_with_directives(
                directives_definition=directives_definition,
                directive_hook="on_argument_execution",
            ),
        )
