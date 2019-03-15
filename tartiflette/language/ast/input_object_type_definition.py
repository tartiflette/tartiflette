from typing import Any, List, Optional

from tartiflette.language.ast.base import TypeDefinitionNode


class InputObjectTypeDefinitionNode(TypeDefinitionNode):
    """
    TODO:
    """

    __slots__ = ("description", "name", "directives", "fields", "location")

    def __init__(
        self,
        name: "NameNode",
        description: Optional["DescriptionNode"] = None,
        directives: Optional[List["DirectiveNode"]] = None,
        fields: Optional[List["InputValueDefinitionNode"]] = None,
        location: Optional["Location"] = None,
    ) -> None:
        """
        TODO:
        :param name: TODO:
        :param description: TODO:
        :param directives: TODO:
        :param fields: TODO:
        :param location: TODO:
        :type name: NameNode
        :type description: Optional[DescriptionNode]
        :type directives: Optional[List[DirectiveNode]]
        :type fields: Optional[List[InputValueDefinitionNode]]
        :type location: Optional[Location]
        """
        self.name = name
        self.description = description
        self.directives = directives
        self.fields = fields
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
            isinstance(other, InputObjectTypeDefinitionNode)
            and (
                self.description == other.description
                and self.name == other.name
                and self.directives == other.directives
                and self.fields == other.fields
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
            "InputObjectTypeDefinitionNode(description=%r, name=%r, directives=%r, fields=%r, location=%r)"
            % (
                self.description,
                self.name,
                self.directives,
                self.fields,
                self.location,
            )
        )
