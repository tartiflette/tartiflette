from typing import Any, List, Optional

from tartiflette.language.ast.base import TypeSystemExtensionNode


class EnumTypeExtensionNode(TypeSystemExtensionNode):
    """
    TODO:
    """

    __slots__ = ("name", "directives", "values", "location")

    def __init__(
        self,
        name: "NameNode",
        directives: Optional[List["DirectiveNode"]] = None,
        values: Optional[List["EnumValueDefinitionNode"]] = None,
        location: Optional["Location"] = None,
    ) -> None:
        """
        TODO:
        :param name: TODO:
        :param directives: TODO:
        :param values: TODO:
        :param location: TODO:
        :type name: NameNode
        :type directives: Optional[List[DirectiveNode]]
        :type values: Optional[List[EnumValueDefinitionNode]]
        :type location: Optional[Location]
        """
        self.name = name
        self.directives = directives
        self.values = values
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
            isinstance(other, EnumTypeExtensionNode)
            and (
                self.name == other.name
                and self.directives == other.directives
                and self.values == other.values
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
            "EnumTypeExtensionNode(name=%r, directives=%r, values=%r, location=%r)"
            % (self.name, self.directives, self.values, self.location)
        )
