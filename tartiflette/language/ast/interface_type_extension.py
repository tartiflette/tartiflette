from typing import Any, List, Optional

from tartiflette.language.ast.base import TypeExtensionNode


class InterfaceTypeExtensionNode(TypeExtensionNode):
    """
    TODO:
    """

    __slots__ = ("name", "directives", "fields", "location")

    def __init__(
        self,
        name: "NameNode",
        directives: Optional[List["DirectiveNode"]] = None,
        fields: Optional[List["FieldDefinitionNode"]] = None,
        location: Optional["Location"] = None,
    ) -> None:
        """
        TODO:
        :param name: TODO:
        :param directives: TODO:
        :param fields: TODO:
        :param location: TODO:
        :type name: NameNode
        :type directives: Optional[List[DirectiveNode]]
        :type fields: Optional[List[FieldDefinitionNode]]
        :type location: Optional[Location]
        """
        self.name = name
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
            isinstance(other, InterfaceTypeExtensionNode)
            and (
                self.name == other.name
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
            "InterfaceTypeExtensionNode(name=%r, directives=%r, fields=%r, location=%r)"
            % (self.name, self.directives, self.fields, self.location)
        )
