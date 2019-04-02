from typing import Any, Optional, Union

from lark import Tree, v_args
from lark.lexer import Token
from lark.visitors import Transformer_InPlace

_STRING_VALUE_TOKEN_TYPE = "STRING_VALUE"
_ENUM_VALUE_TOKEN_TYPE = "NAME"


def _find_token(
    node: Union["Token", "Tree", list], searched_token_type: str
) -> Optional["Token"]:
    """
    Searches for token type in the node provided. The first token corresponding
    to the searched type is returned. If no token matches the searched type
    then the value "None" is returned.
    :param node: object instance in which to search
    :param searched_token_type: token type to search
    :type node: Union[Token, Tree, list]
    :type searched_token_type: str
    :return: the first token corresponding to the searched type or None
    :rtype: Optional[Token]
    """
    if isinstance(node, Token):
        return node if node.type == searched_token_type else None
    if isinstance(node, Tree):
        for child in node.children:
            res = _find_token(child, searched_token_type)
            if res:
                return res
    if isinstance(node, list):
        for child in node:
            res = _find_token(child, searched_token_type)
            if res:
                return res
    return None


def _override_tree_children(tree: "Tree", new_child: Any) -> "Tree":
    """
    Replaces the children of a Tree instance with a single child.
    :param tree: Tree instance to update
    :param new_child: new single child of the tree
    :type tree: Tree
    :type new_child: Any
    :return: the tree instance with its single child
    :rtype: Tree
    """
    tree.children = [new_child]
    return tree


@v_args(tree=True)
class TokenTransformer(Transformer_InPlace):
    """
    Lark transformer which is in charge of cleaning and casting miscellaneous
    rules in order to be easily reused in NodeTransformer.
    """

    def int_value(self, tree: "Tree") -> "Tree":
        """
        Replaces the children of the tree with a custom INT_VALUE token and
        casts the string value to an int value.
        :param tree: the Tree instance to update
        :type tree: Tree
        :return: the three with its INT_VALUE token child
        :rtype: Tree
        """
        # pylint: disable=no-self-use
        token = tree.children[0]
        return _override_tree_children(
            tree,
            Token(
                "INT_VALUE",
                int(token.value),
                token.pos_in_stream,
                token.line,
                token.column,
            ),
        )

    def float_value(self, tree: "Tree") -> "Tree":
        """
        Replaces the children of the tree with a custom FLOAT_VALUE token and
        casts the string value to a float value.
        :param tree: the Tree instance to update
        :type tree: Tree
        :return: the three with its FLOAT_VALUE token child
        :rtype: Tree
        """
        # pylint: disable=no-self-use
        first_token = tree.children[0]
        return _override_tree_children(
            tree,
            Token(
                "FLOAT_VALUE",
                float("".join([child.value for child in tree.children])),
                first_token.pos_in_stream,
                first_token.line,
                first_token.column,
            ),
        )

    def string_value(self, tree: "Tree") -> "Tree":
        """
        Replaces the children of the tree with a custom STRING_VALUE token and
        removes quotes from the value (single or triple double quotes).
        :param tree: the Tree instance to update
        :type tree: Tree
        :return: the three with its STRING_VALUE token child
        :rtype: Tree
        """
        # pylint: disable=no-self-use
        token = tree.children[0]
        slicing = 1 if token.type == "STRING" else 3
        return _override_tree_children(
            tree,
            Token(
                "STRING_VALUE",
                bytes(token.value[slicing:-slicing], "utf-8").decode(
                    "unicode-escape"
                ),
                token.pos_in_stream,
                token.line,
                token.column,
            ),
        )

    def boolean_value(self, tree: "Tree") -> "Tree":
        """
        Replaces the children of the tree with a custom BOOLEAN_VALUE token and
        casts the string value to a boolean value.
        :param tree: the Tree instance to update
        :type tree: Tree
        :return: the three with its BOOLEAN_VALUE token child
        :rtype: Tree
        """
        # pylint: disable=no-self-use
        token = tree.children[0]
        return _override_tree_children(
            tree,
            Token(
                "BOOLEAN_VALUE",
                token.type == "TRUE",
                token.pos_in_stream,
                token.line,
                token.column,
            ),
        )

    def null_value(self, tree: "Tree") -> "Tree":
        """
        Replaces the children of the tree with a custom NULL_VALUE token and
        force its value to None.
        :param tree: the Tree instance to update
        :type tree: Tree
        :return: the three with its NULL_VALUE token child
        :rtype: Tree
        """
        # pylint: disable=no-self-use
        token = tree.children[0]
        return _override_tree_children(
            tree,
            Token(
                "NULL_VALUE",
                None,
                token.pos_in_stream,
                token.line,
                token.column,
            ),
        )

    def enum_value(self, tree: "Tree") -> "Tree":
        """
        Replaces the children of the tree with a custom ENUM token and set its
        value to the underlying name's token value.
        :param tree: the Tree instance to update
        :type tree: Tree
        :return: the three with its ENUM token child
        :rtype: Tree
        """
        # pylint: disable=no-self-use
        token = _find_token(tree.children, _ENUM_VALUE_TOKEN_TYPE)
        return _override_tree_children(
            tree,
            Token(
                "ENUM",
                token.value,
                token.pos_in_stream,
                token.line,
                token.column,
            ),
        )

    def name(self, tree: "Tree") -> "Tree":
        """
        Replaces the children of the tree with a custom NAME token and set its
        value to the underlying anonymous's token value.
        :param tree: the Tree instance to update
        :type tree: Tree
        :return: the three with its NAME token child
        :rtype: Tree
        """
        # pylint: disable=no-self-use
        token = tree.children[0]
        return _override_tree_children(
            tree,
            Token(
                "NAME",
                token.value,
                token.pos_in_stream,
                token.line,
                token.column,
            ),
        )

    def description(self, tree: "Tree") -> "Tree":
        """
        Replaces the children of the tree with a custom DESCRIPTION token and
        set its value to the underlying string value's token value.
        :param tree: the Tree instance to update
        :type tree: Tree
        :return: the three with its DESCRIPTION token child
        :rtype: Tree
        """
        # pylint: disable=no-self-use
        token = _find_token(tree, _STRING_VALUE_TOKEN_TYPE)
        return _override_tree_children(
            tree,
            Token(
                "DESCRIPTION",
                token.value,
                token.pos_in_stream,
                token.line,
                token.column,
            ),
        )
