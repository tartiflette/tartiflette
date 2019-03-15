from typing import List, Optional, Union

from tartiflette.language.ast.base import Node


class DocumentNode(Node):
    """
    TODO:
    """

    __slots__ = ("definitions", "location")

    def __init__(
        self,
        definitions: List[
            Union["FragmentDefinitionNode", "OperationDefinitionNode"]
        ],
        location: Optional["Location"] = None,
    ) -> None:
        """
        TODO:
        :param definitions: TODO:
        :param location: TODO:
        :type definitions: TODO:
        :type location: TODO:
        """
        self.definitions = definitions
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
            isinstance(other, DocumentNode)
            and (
                self.definitions == other.definitions
                and self.location == other.location
            )
        )

    def __repr__(self) -> str:
        """
        TODO:
        :return: TODO:
        :rtype: TODO:
        """
        return "DocumentNode(definitions=%r, location=%r)" % (
            self.definitions,
            self.location,
        )
