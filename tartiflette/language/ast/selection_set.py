from typing import List, Optional, Union

from tartiflette.language.ast.base import Node


class SelectionSetNode(Node):
    """
    TODO:
    """

    __slots__ = ("selections", "location")

    def __init__(
        self,
        selections: List[
            Union["FieldNode", "FragmentSpreadNode", "InlineFragmentNode"]
        ],
        location: Optional["Location"] = None,
    ) -> None:
        """
        TODO:
        :param selections: TODO:
        :param location: TODO:
        :type selections: TODO:
        :type location: TODO:
        """
        self.selections = selections
        self.location = location

    def __eq__(self, other):
        """
        TODO:
        :param other: TODO:
        :type other: TODO:
        :return: TODO:
        :rtype: TODO:
        """
        return self is other or (
            isinstance(other, SelectionSetNode)
            and (
                self.selections == other.selections
                and self.location == other.location
            )
        )

    def __repr__(self) -> str:
        """
        TODO:
        :return: TODO:
        :rtype: TODO:
        """
        return "SelectionSetNode(selections=%r, location=%r)" % (
            self.selections,
            self.location,
        )
