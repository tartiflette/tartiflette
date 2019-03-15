from typing import Any, List, Optional

from tartiflette.language.ast.base import TypeDefinitionNode


class ObjectTypeDefinitionNode(TypeDefinitionNode):
    """
    TODO:
    """

    __slots__ = ("description", "name", "interfaces", "directives", "fields")

    def __init__(
        self,
        name: "NameNode",
        description: Optional["DescriptionNode"] = None,
        interfaces: Optional[List["NamedTypeNode"]] = None,
        directives: Optional[List["DirectiveNode"]] = None,
        fields: Optional[List["FieldDefinitionNode"]] = None,
        location: Optional["Location"] = None,
    ) -> None:
        """
        TODO:
        :param name: TODO:
        :param description: TODO:
        :param interfaces: TODO:
        :param directives: TODO:
        :param fields: TODO:
        :param location: TODO:
        :type name: NameNode
        :type description: Optional[DescriptionNode]
        :type interfaces: Optional[List[NamedTypeNode]]
        :type directives: Optional[List[DirectiveNode]]
        :type fields: Optional[List[FieldDefinitionNode]]
        :type location: Optional[Location]
        """
        self.name = name
        self.description = description
        self.interfaces = interfaces
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
            isinstance(other, ObjectTypeDefinitionNode)
            and (
                self.description == other.description
                and self.name == other.name
                and self.interfaces == other.interfaces
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
            "ObjectTypeDefinitionNode(description=%r, name=%r, interfaces=%r, directives=%r, fields=%r, location=%r)"
            % (
                self.description,
                self.name,
                self.interfaces,
                self.directives,
                self.fields,
                self.location,
            )
        )
