from typing import Any, List, Optional

from tartiflette.language.ast.base import TypeExtensionNode


class ObjectTypeExtensionNode(TypeExtensionNode):
    """
    TODO:
    """

    __slots__ = ("name", "interfaces", "directives", "fields", "location")

    def __init__(
        self,
        name: "NameNode",
        interfaces: Optional[List["NamedTypeNode"]] = None,
        directives: Optional[List["DirectiveNode"]] = None,
        fields: Optional[List["FieldDefinitionNode"]] = None,
        location: Optional["Location"] = None,
    ) -> None:
        """
        TODO:
        :param name: TODO:
        :param interfaces: TODO:
        :param directives: TODO:
        :param fields: TODO:
        :param location: TODO:
        :type name: NameNode
        :type interfaces: Optional[List[NamedTypeNode]]
        :type directives: Optional[List[DirectiveNode]]
        :type fields: Optional[List[FieldDefinitionNode]]
        :type location: Optional[Location]
        """
        self.name = name
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
            isinstance(other, ObjectTypeExtensionNode)
            and (
                self.name == other.name
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
            "ObjectTypeExtensionNode(name=%r, interfaces=%r, directives=%r, fields=%r, location=%r)"
            % (
                self.name,
                self.interfaces,
                self.directives,
                self.fields,
                self.location,
            )
        )
