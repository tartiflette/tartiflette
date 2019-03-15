from typing import Any, List, Optional

from tartiflette.language.ast.base import SelectionNode


class FragmentSpreadNode(SelectionNode):
    """
    TODO:
    """

    __slots__ = ("name", "directives", "location")

    def __init__(
        self,
        name: "NameNode",
        directives: Optional[List["DirectiveNode"]] = None,
        location: Optional["Location"] = None,
    ) -> None:
        """
        TODO:
        :param name: TODO:
        :param directives: TODO:
        :param location: TODO:
        :type name: NameNode
        :type directives: Optional[List[DirectiveNode]]
        :type location: Optional[Location]
        """
        self.name = name
        self.directives = directives
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
            isinstance(other, FragmentSpreadNode)
            and (
                self.name == other.name
                and self.directives == other.directives
                and self.location == other.location
            )
        )

    def __repr__(self) -> str:
        """
        TODO:
        :return: TODO:
        :rtype: str
        """
        return "FragmentSpreadNode(name=%r, directives=%r, location=%r)" % (
            self.name,
            self.directives,
            self.location,
        )
