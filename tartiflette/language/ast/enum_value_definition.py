from typing import Any, List, Optional

from tartiflette.language.ast.base import Node


class EnumValueDefinitionNode(Node):
    """
    AST node representing a GraphQL enum value definition.
    """

    __slots__ = ("description", "name", "directives", "location")

    def __init__(
        self,
        name: "NameNode",
        description: Optional["DescriptionNode"] = None,
        directives: Optional[List["DirectiveNode"]] = None,
        location: Optional["Location"] = None,
    ) -> None:
        """
        :param name: name of the enum value definition
        :param description: description of the enum value definition
        :param directives: directives of the enum value definition
        :param location: location of the enum value definition in the query/SDL
        :type name: NameNode
        :type description: Optional[DescriptionNode]
        :type directives: Optional[List[DirectiveNode]]
        :type location: Optional[Location]
        """
        self.name = name
        self.description = description
        self.directives = directives
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
            isinstance(other, EnumValueDefinitionNode)
            and (
                self.description == other.description
                and self.name == other.name
                and self.directives == other.directives
                and self.location == other.location
            )
        )

    def __repr__(self) -> str:
        """
        Returns the representation of an EnumValueDefinitionNode instance.
        :return: the representation of an EnumValueDefinitionNode instance
        :rtype: str
        """
        return (
            "EnumValueDefinitionNode(description=%r, name=%r, directives=%r, "
            "location=%r)"
            % (self.description, self.name, self.directives, self.location)
        )
