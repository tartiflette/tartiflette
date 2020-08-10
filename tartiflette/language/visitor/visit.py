from copy import copy
from typing import Any, Dict, List, Optional, Tuple, Union

from tartiflette.language.ast.base import Node
from tartiflette.language.visitor.constants import (
    BREAK,
    OK,
    QUERY_DOCUMENT_KEYS,
    REMOVE,
    SKIP,
)
from tartiflette.language.visitor.utils import get_visit_function

__all__ = ("visit",)


class Stack:
    """
    Saves information related to a node visit.
    """

    __slots__ = ("in_array", "index", "keys", "edits", "prev")

    def __init__(
        self,
        in_array: bool,
        index: int,
        keys: Union[List["Node"], List[str]],
        edits: List[Tuple[Optional[Union[int, str]], Union["Node", Any]]],
        prev: Optional["Stack"] = None,
    ) -> None:
        """
        :param in_array: whether or not the stack is in an array
        :param index: the index of the stack
        :param keys: list of visited keys
        :param edits: list of edited nodes with their index
        :param prev: the previous Stack instance
        :type in_array: bool
        :type index: int
        :type keys: Union[List["Node"], List[str]]
        :type edits: List[Tuple[Optional[Union[int, str]], Union["Node", Any]]]
        :type prev: Optional["Stack"]
        """
        self.in_array = in_array
        self.index = index
        self.keys = keys
        self.edits = edits
        self.prev = prev


def visit(
    root: "Node",
    visitor: "Visitor",
    visitor_keys: Optional[Dict[str, Tuple[str]]] = None,
) -> "Node":
    """
    Walk through an AST using a depth first traversal, calling the visitor's
    enter function at each node in the traversal, and calling the leave
    function after visiting that node and all of its child nodes.
    :param root: root AST node to visit
    :param visitor: visitor to use to visit the AST node
    :param visitor_keys: mapping attributes that can be visited according to
    the type of nodes
    :type root: Node
    :type visitor: Visitor
    :type visitor_keys: Optional[Dict[str, Tuple[str]]]
    :return: the visited node or the edited node
    :rtype: Node
    """
    # pylint: disable=too-many-nested-blocks,too-many-locals,too-complex,too-many-branches
    if visitor_keys is None:
        visitor_keys = QUERY_DOCUMENT_KEYS

    stack: Optional["Stack"] = None
    in_array: bool = isinstance(root, list)
    keys: Any = [root]
    index: int = -1
    edits: List[Any] = []
    parent: Optional[Any] = None
    path: List[Any] = []
    ancestors: List[Any] = []
    new_root: "Node" = root

    while True:
        index += 1
        is_leaving: bool = index == len(keys)
        is_edited: bool = is_leaving and edits

        if is_leaving:
            key = path[-1] if ancestors else None
            node = parent
            parent = ancestors.pop() if ancestors else None

            if is_edited:
                node = (
                    node[:]  # pylint: disable=unsubscriptable-object
                    if in_array
                    else copy(node)
                )

                edit_offset = 0
                for edit_key, edit_value in edits:
                    if in_array:
                        edit_key -= edit_offset
                    if in_array and edit_value is REMOVE:
                        node.pop(edit_key)
                        edit_offset += 1
                    else:
                        if isinstance(node, list):
                            node[edit_key] = edit_value
                        else:
                            setattr(node, edit_key, edit_value)

            index = stack.index
            keys = stack.keys
            edits = stack.edits
            in_array = stack.in_array
            stack = stack.prev
        else:
            if parent:
                if in_array:
                    key = index
                    node = parent[  # pylint: disable=unsubscriptable-object
                        key
                    ]
                else:
                    key = keys[index]
                    node = getattr(parent, key, None)
            else:
                key = None
                node = new_root

            if node is REMOVE or node is OK:
                continue

            if parent:
                path.append(key)

        result = None
        if not isinstance(node, list):
            if not isinstance(node, Node):
                raise Exception(f"Invalid AST node: < {node} >.")

            visit_function = get_visit_function(visitor, node, is_leaving)
            if visit_function:
                result = visit_function(node, key, parent, path, ancestors)

                if result is BREAK:
                    break

                if result is SKIP:
                    if not is_leaving:
                        path.pop()
                        continue
                elif result is not OK:
                    edits.append((key, result))
                    if not is_leaving:
                        if isinstance(result, Node):
                            node = result
                        else:
                            path.pop()
                            continue

        if result is OK and is_edited:
            edits.append((key, node))

        if is_leaving:
            if path:
                path.pop()
        else:
            stack = Stack(in_array, index, keys, edits, prev=stack)
            in_array = isinstance(node, list)
            keys = (
                node
                if in_array
                else visitor_keys.get(node.__class__.__name__, [])
            )
            index = -1
            edits = []
            if parent:
                ancestors.append(parent)
            parent = node

        if not stack:
            break

    if edits:
        new_root = edits[-1][1]

    return new_root
