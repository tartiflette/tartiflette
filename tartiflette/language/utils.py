from typing import Union

from tartiflette.language.ast.types import ListTypeNode, NonNullTypeNode


def get_wrapped_named_type(
    node: Union[ListTypeNode, NonNullTypeNode, "NamedTypeNode"]
) -> "NamedTypeNode":
    """Find the NamedTypeNode inside any kind of NonNull node and List node combination.

    :param node: Node to unwrap
    :type node: Union[ListTypeNode, NonNullTypeNode, NamedTypeNode]
    :return: the unwrapped inner NamedTypeNode node
    :rtype: NamedTypeNode
    """
    if isinstance(node, (ListTypeNode, NonNullTypeNode)):
        return get_wrapped_named_type(node.type)
    return node
