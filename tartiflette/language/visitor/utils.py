from typing import Callable, Optional

__all__ = ("get_visit_function",)


def get_visit_function(
    visitor: "Visitor", node: "Node", is_leaving: bool = False
) -> Optional[Callable]:
    """
    Given a visitor instance, an AST node and if it is leaving or not, return
    the function the visitor runtime should call.
    :param visitor: instance of the visitor for whom to find the function
    :param node: AST node instance to visit
    :param is_leaving: whether or not the visitor is leaving the node
    :type visitor: Visitor
    :type node: Node
    :type is_leaving: bool
    :return: the function the visitor runtime should call
    :rtype: Optional[Callable]
    """
    method_name = "leave" if is_leaving else "enter"
    node_class_name = node.__class__.__name__[:-4]
    visit_function = getattr(visitor, f"{method_name}_{node_class_name}", None)
    if visit_function:
        return visit_function
    return getattr(visitor, method_name, None)
