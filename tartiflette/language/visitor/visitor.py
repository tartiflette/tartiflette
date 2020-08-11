from typing import Any, List, Optional, Union

from tartiflette.language.visitor.constants import BREAK, OK, SKIP
from tartiflette.language.visitor.utils import get_visit_function

__all__ = ("Visitor", "MultipleVisitor")


class Visitor:
    """
    Base class for AST visitor.
    """


class MultipleVisitor(Visitor):
    """
    Visitor which delegates to many visitors to run in parallel.
    """

    def __init__(self, visitors: List["Visitor"]) -> None:
        """
        :param visitors: list of visitor to run in parallel
        :type visitors: List["Visitor"]
        """
        self._visitors = visitors
        self._skipping: List[Any] = [None] * len(visitors)

    def enter(
        self,
        node: "Node",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> Optional[Any]:
        """
        Visit the go in node with each defined visitors.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: Node
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        :return: an edited node or None
        :rtype: Optional[Any]
        """
        # pylint: disable=too-many-locals
        for i, visitor in enumerate(self._visitors):
            if not self._skipping[i]:
                fn = get_visit_function(visitor, node)
                if fn:
                    result = fn(node, key, parent, path, ancestors)
                    if result is SKIP:
                        self._skipping[i] = node
                    elif result is BREAK:
                        self._skipping[i] = BREAK
                    elif result is not OK:
                        return result
        return None

    def leave(
        self,
        node: "Node",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> Optional[Any]:
        """
        Visit the go out node with each defined visitors.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: Node
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        :return: an edited node or None
        :rtype: Optional[Any]
        """
        # pylint: disable=too-many-locals
        for i, visitor in enumerate(self._visitors):
            if not self._skipping[i]:
                fn = get_visit_function(visitor, node, is_leaving=True)
                if fn:
                    result = fn(node, key, parent, path, ancestors)
                    if result is BREAK:
                        self._skipping[i] = BREAK
                    elif result is not OK and result is not SKIP:
                        return result
            elif self._skipping[i] is node:
                self._skipping[i] = None
        return None
