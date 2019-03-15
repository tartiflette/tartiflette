from typing import Any, List, Optional

from tartiflette.language.ast.base import TypeSystemDefinitionNode


class DirectiveDefinitionNode(TypeSystemDefinitionNode):
    """
    TODO:
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
        TODO:
        :param name: TODO:
        :param locations: TODO:
        :param description: TODO:
        :param arguments: TODO:
        :param location: TODO:
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
        TODO:
        :param other: TODO:
        :type other: Any
        :return: TODO:
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
        TODO:
        :return: TODO:
        :rtype: str
        """
        return (
            "DirectiveDefinitionNode(description=%r, name=%r, arguments=%r, locations=%r, location=%r)"
            % (
                self.description,
                self.name,
                self.arguments,
                self.locations,
                self.location,
            )
        )
