from typing import Any, Optional, Union

from lark import Tree, v_args
from lark.lexer import Token
from lark.visitors import Transformer_InPlace

_STRING_VALUE_TOKEN_TYPE = "STRING_VALUE"
_ENUM_VALUE_TOKEN_TYPE = "NAME"


def _find_token(
    node: Union["Token", "Tree"], searched_token_type: str
) -> Optional["Token"]:
    """
    TODO:
    :param node: TODO:
    :param searched_token_type: TODO:
    :type node: Union[Token, Tree]
    :type searched_token_type: str
    :return: TODO:
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
    TODO:
    :param tree: TODO:
    :param new_child: TODO:
    :type tree: Tree
    :type new_child: Any
    :return: TODO:
    :rtype: Tree
    """
    tree.children = [new_child]
    return tree


@v_args(tree=True)
class TokenTransformer(Transformer_InPlace):
    """
    TODO:
    """

    def int_value(self, tree: "Tree") -> "Tree":
        """
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
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
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
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
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
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
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
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
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
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
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
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
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
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
        TODO:
        :param tree: TODO:
        :type tree: Tree
        :return: TODO:
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
