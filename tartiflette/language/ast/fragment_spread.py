from typing import Any, List, Optional

from tartiflette.language.ast.base import SelectionNode


class FragmentSpreadNode(SelectionNode):
    """
    AST node representing a GraphQL fragment spread.
    """

    __slots__ = ("name", "directives", "location")

    def __init__(
        self,
        name: "NameNode",
        directives: Optional[List["DirectiveNode"]] = None,
        location: Optional["Location"] = None,
    ) -> None:
        """
        :param name: name of the fragment spread
        :param directives: directives of the fragment spread
        :param location: location of the fragment spread in the query/SDL
        :type name: NameNode
        :type directives: Optional[List[DirectiveNode]]
        :type location: Optional[Location]
        """
        self.name = name
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
            isinstance(other, FragmentSpreadNode)
            and (
                self.name == other.name
                and self.directives == other.directives
                and self.location == other.location
            )
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a FragmentSpreadNode instance.
        :return: the representation of a FragmentSpreadNode instance
        :rtype: str
        """
        return "FragmentSpreadNode(name=%r, directives=%r, location=%r)" % (
            self.name,
            self.directives,
            self.location,
        )
