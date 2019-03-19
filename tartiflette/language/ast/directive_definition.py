from typing import Any, List, Optional

from tartiflette.language.ast.base import TypeSystemDefinitionNode


class DirectiveDefinitionNode(TypeSystemDefinitionNode):
    """
    AST node representing a GraphQL directive definition.
    """

    __slots__ = ("description", "name", "arguments", "locations", "location")

    def __init__(
        self,
        name: "NameNode",
        locations: List["NameNode"],
        description: Optional["DescriptionNode"] = None,
        arguments: Optional[List["InputValueDefinitionNode"]] = None,
        location: Optional["Location"] = None,
    ) -> None:
        """
        :param name: name of the directive definition
        :param locations: locations where the directive definition can be used
        :param description: description of the directive definition
        :param arguments: arguments of the directive definition
        :param location: location of the directive definition in the query/SDL
        :type name: NameNode
        :type locations: List[NameNode]
        :type description: Optional[DescriptionNode]
        :type arguments: Optional[List[InputValueDefinitionNode]]
        :type location: Optional[Location]
        """
        self.name = name
        self.locations = locations
        self.description = description
        self.arguments = arguments
        self.location = location

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if `other` instance is identical to `self`.
        :param other: object instance to compare to `self`
        :type other: Any
        :return: whether or not `other` is identical to `self`
        :rtype: bool
        """
        return self is other or (
            isinstance(other, DirectiveDefinitionNode)
            and (
                self.description == other.description
                and self.name == other.name
                and self.arguments == other.arguments
                and self.locations == other.locations
                and self.location == other.location
            )
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a DirectiveDefinitionNode instance.
        :return: the representation of a DirectiveDefinitionNode instance
        :rtype: str
        """
        return (
            "DirectiveDefinitionNode(description=%r, name=%r, arguments=%r, "
            "locations=%r, location=%r)"
            % (
                self.description,
                self.name,
                self.arguments,
                self.locations,
                self.location,
            )
        )
