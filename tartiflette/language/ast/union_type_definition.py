from typing import Any, List, Optional

from tartiflette.language.ast.base import TypeDefinitionNode


class UnionTypeDefinitionNode(TypeDefinitionNode):
    """
    TODO:
    """

    __slots__ = ("description", "name", "directives", "types", "location")

    def __init__(
        self,
        name: "NameNode",
        description: Optional["DescriptionNode"] = None,
        directives: Optional[List["DirectiveNode"]] = None,
        types: Optional[List["NamedTypeNode"]] = None,
        location: Optional["Location"] = None,
    ) -> None:
        """
        TODO:
        :param name: TODO:
        :param description: TODO:
        :param directives: TODO:
        :param types: TODO:
        :param location: TODO:
        :type name: NameNode
        :type description: Optional[DescriptionNode]
        :type directives: Optional[List[DirectiveNode]]
        :type types: Optional[List[NamedTypeNode]]
        :type location: Optional[Location]
        """
        self.name = name
        self.description = description
        self.directives = directives
        self.types = types
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
            isinstance(other, UnionTypeDefinitionNode)
            and (
                self.description == other.description
                and self.name == other.name
                and self.directives == other.directives
                and self.types == other.types
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
            "UnionTypeDefinitionNode(description=%r, name=%r, directives=%r, types=%r, location=%r)"
            % (
                self.description,
                self.name,
                self.directives,
                self.types,
                self.location,
            )
        )
