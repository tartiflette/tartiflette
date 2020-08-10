from difflib import get_close_matches
from functools import partial
from typing import List, Optional, Union

from tartiflette.language.ast import EnumValueNode
from tartiflette.language.visitor.constants import SKIP
from tartiflette.language.visitor.type_info import get_nullable_type
from tartiflette.types.exceptions.tartiflette import TartifletteError
from tartiflette.types.helpers.definition import (
    get_wrapped_type,
    is_enum_type,
    is_input_object_type,
    is_leaf_type,
    is_list_type,
    is_non_null_type,
    is_required_input_field,
)
from tartiflette.utils.errors import (
    did_you_mean,
    graphql_error_from_nodes as raw_graphql_error_from_nodes,
)
from tartiflette.utils.values import is_invalid_value
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("ValuesOfCorrectTypeRule",)


graphql_error_from_nodes = partial(
    raw_graphql_error_from_nodes,
    extensions={
        "spec": "June 2018",
        "rule": "5.6.1",
        "tag": "values-of-correct-type",
        "details": (
            "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type"
        ),
    },
)


class ValuesOfCorrectTypeRule(ASTValidationRule):
    """
    A GraphQL document is only valid if all value literals are of the
    type expected at their position.
    """

    def _is_valid_value_node(self, node: "ValueNode") -> None:
        """
        Check that a value node is valid at its location.
        :param node: the current node being visiting
        :type node: ValueNode
        """
        location_type = self.context.get_input_type()
        if not location_type:
            return None

        gql_type = get_wrapped_type(location_type)

        if not is_leaf_type(gql_type):
            self.context.report_error(
                graphql_error_from_nodes(
                    f"Expected value of type < {gql_type} >, found "
                    f"< {node} >.",
                    nodes=[node],
                )
            )
            return None

        try:
            if is_enum_type(gql_type):
                if isinstance(node, EnumValueNode):
                    if not gql_type.has_value(node.value):
                        self.context.report_error(
                            graphql_error_from_nodes(
                                f"Value < {node} > does not exist in "
                                f"< {gql_type.name} > enum.",
                                nodes=[node],
                            )
                        )
                else:
                    self.context.report_error(
                        graphql_error_from_nodes(
                            f"Enum < {gql_type.name} > cannot represent "
                            f"non-enum value: {node}.",
                            nodes=[node],
                        )
                    )
            else:
                parse_result = gql_type.parse_literal(node)
                if is_invalid_value(parse_result):
                    self.context.report_error(
                        graphql_error_from_nodes(
                            f"Expected value of type < {gql_type} >, found "
                            f"< {node} >.",
                            nodes=[node],
                        )
                    )
        except TartifletteError as e:
            self.context.report_error(e)
        except Exception as e:  # pylint: disable=broad-except
            self.context.report_error(
                graphql_error_from_nodes(
                    f"Expected value of type < {gql_type} >, found "
                    f"< {node} >; " + str(e),
                    nodes=[node],
                    original_error=e,
                )
            )
        return None

    def enter_ListValue(  # pylint: disable=invalid-name
        self,
        node: "ListValueNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> Optional["SKIP"]:
        """
        Check that the list value is expected at this location.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: ListValueNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        :return: the SKIP visitor constant or None
        :rtype: Optional["SKIP"]
        """
        # pylint: disable=unused-argument
        gql_type = get_nullable_type(self.context.get_parent_input_type())
        if not is_list_type(gql_type):
            self._is_valid_value_node(node)
            return SKIP
        return None

    def enter_ObjectValue(  # pylint: disable=invalid-name
        self,
        node: "ObjectValueNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> Optional["SKIP"]:
        """
        Check that value of object fields is valid.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: ObjectValueNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        :return: the SKIP visitor constant or None
        :rtype: Optional["SKIP"]
        """
        # pylint: disable=unused-argument
        gql_type = get_wrapped_type(self.context.get_input_type())
        if not is_input_object_type(gql_type):
            self._is_valid_value_node(node)
            return SKIP

        input_field_node_map = {
            input_field.name.value: input_field for input_field in node.fields
        }
        for (
            input_field_name,
            input_field_definition,
        ) in gql_type.input_fields.items():
            input_field_node = input_field_node_map.get(input_field_name)
            if not input_field_node and is_required_input_field(
                input_field_definition
            ):
                self.context.report_error(
                    graphql_error_from_nodes(
                        f"Field < {gql_type.name}.{input_field_definition.name} > "
                        f"of required type < {input_field_definition.type} > was "
                        "not provided.",
                        nodes=[node],
                    )
                )
        return None

    def enter_ObjectField(  # pylint: disable=invalid-name
        self,
        node: "ObjectFieldNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Check that the field is defined by its input type.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: ObjectFieldNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        """
        # pylint: disable=unused-argument
        parent_type = get_wrapped_type(self.context.get_parent_input_type())
        field_type = self.context.get_input_type()
        if not field_type and is_input_object_type(parent_type):
            suggestions = get_close_matches(
                node.name.value, parent_type.input_fields.keys(), n=5
            )
            error_message = (
                f"Field < {node.name.value} > is not defined by type "
                f"< ${parent_type.name} >."
            )
            if suggestions:
                error_message = f"{error_message} {did_you_mean(suggestions)}"
            self.context.report_error(
                graphql_error_from_nodes(error_message, nodes=[node])
            )

    def enter_NullValue(  # pylint: disable=invalid-name
        self,
        node: "NullValueNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Check that the null value is expected at this location.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: NullValueNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        """
        # pylint: disable=unused-argument
        gql_type = self.context.get_input_type()
        if is_non_null_type(gql_type):
            self.context.report_error(
                graphql_error_from_nodes(
                    f"Expected value of type < {gql_type} >, found "
                    f"< {node} >.",
                    nodes=[node],
                )
            )

    def enter_EnumValue(  # pylint: disable=invalid-name
        self,
        node: "EnumValueNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Check that the enum value is expected at this location.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: EnumValueNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        """
        # pylint: disable=unused-argument
        self._is_valid_value_node(node)

    def enter_IntValue(  # pylint: disable=invalid-name
        self,
        node: "IntValueNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Check that the int value is expected at this location.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: IntValueNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        """
        # pylint: disable=unused-argument
        self._is_valid_value_node(node)

    def enter_FloatValue(  # pylint: disable=invalid-name
        self,
        node: "FloatValueNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Check that the float value is expected at this location.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: FloatValueNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        """
        # pylint: disable=unused-argument
        self._is_valid_value_node(node)

    def enter_StringValue(  # pylint: disable=invalid-name
        self,
        node: "StringValueNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Check that the string value is expected at this location.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: StringValueNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        """
        # pylint: disable=unused-argument
        self._is_valid_value_node(node)

    def enter_BooleanValue(  # pylint: disable=invalid-name
        self,
        node: "BooleanValueNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Check that the boolean value is expected at this location.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: BooleanValueNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        """
        # pylint: disable=unused-argument
        self._is_valid_value_node(node)
