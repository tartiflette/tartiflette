from collections import Iterable, Mapping
from typing import Any, List, Optional, Union

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.types.exceptions import GraphQLError
from tartiflette.types.helpers.definition import (
    is_enum_type,
    is_input_object_type,
    is_list_type,
    is_non_null_type,
    is_scalar_type,
)
from tartiflette.utils.values import is_invalid_value


class CoercionResult:
    """
    TODO:
    """

    __slots__ = ("value", "errors")

    def __init__(
        self,
        value: Optional[Any] = None,
        errors: Optional[List["GraphQLError"]] = None,
    ) -> None:
        """
        :param value: TODO:
        :param errors: TODO:
        :type value: TODO:
        :type errors: TODO:
        """
        # TODO: if errors `value` shouldn't it be "UNDEFINED_VALUE" instead?
        self.value = value if not errors else None
        self.errors = errors

    def __repr__(self) -> str:
        """
        TODO:
        :return: TODO:
        :rtype: TODO:
        """
        return "CoercionResult(value=%r, errors=%r)" % (
            self.value,
            self.errors,
        )

    def __iter__(self) -> Iterable:
        """
        TODO:
        :return: TODO:
        :rtype: TODO:
        """
        yield from [self.value, self.errors]


class Path:
    """
    TODO:
    """

    __slots__ = ("prev", "key")

    def __init__(self, prev: Optional["Path"], key: Union[str, int]) -> None:
        """
        :param prev: TODO:
        :param key: TODO:
        :type prev: TODO:
        :type key: TODO:
        """
        self.prev = prev
        self.key = key

    def __repr__(self) -> str:
        """
        TODO:
        :return: TODO:
        :rtype: TODO:
        """
        return "Path(prev=%r, key=%r)" % (self.prev, self.key)

    def __str__(self) -> str:
        """
        TODO:
        :return: TODO:
        :rtype: TODO:
        """
        path_str = ""
        current_path = self
        while current_path:
            path_str = (
                f".{current_path.key}"
                if isinstance(current_path.key, str)
                else f"[{current_path.key}]"
            ) + path_str
            current_path = current_path.prev
        return f"value{path_str}" if path_str else ""


def coercion_error(
    message, node=None, path=None, sub_message=None, original_error=None
):
    """
    TODO:
    :param message: TODO:
    :param node: TODO:
    :param path: TODO:
    :param sub_message: TODO:
    :param original_error: TODO:
    :type message: TODO:
    :type node: TODO:
    :type path: TODO:
    :type sub_message: TODO:
    :type original_error: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return GraphQLError(
        message
        + (" at " + str(path) if path else "")
        + ("; " + sub_message if sub_message else "."),
        locations=[node.location] if node else None,
        path=None,
        original_error=original_error,
    )


def coerce_value(
    value: Any,
    schema_type: "GraphQLType",
    node: Optional["Node"] = None,
    path: Optional["Path"] = None,
) -> "CoercionResult":
    """
    TODO:
    :param value: TODO:
    :param schema_type: TODO:
    :param node: TODO:
    :param path: TODO:
    :type value: TODO:
    :type schema_type: TODO:
    :type node: TODO:
    :type path: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    if is_non_null_type(schema_type):
        if value is None:
            return CoercionResult(
                errors=[
                    coercion_error(
                        f"Expected non-nullable type < {schema_type} > not to be null",
                        node,
                        path,
                    )
                ]
            )
        return coerce_value(value, schema_type.ofType, node, path)

    if value is None:
        return CoercionResult(value=None)

    if is_scalar_type(schema_type):
        try:
            coerced_value = schema_type.coerce_input(value)
            if is_invalid_value(coerced_value):
                return CoercionResult(
                    errors=[
                        coercion_error(
                            f"Expected type < {schema_type.name} >", node, path
                        )
                    ]
                )
        except Exception as e:
            return CoercionResult(
                errors=[
                    coercion_error(
                        f"Expected type < {schema_type.name} >",
                        node,
                        path,
                        sub_message=str(e),
                        original_error=e,
                    )
                ]
            )
        return CoercionResult(value=coerced_value)

    if is_enum_type(schema_type):
        try:
            return CoercionResult(value=schema_type.get_value(value))
        except KeyError:
            # TODO: try to compute a suggestion list of valid values depending
            # on the invalid value sent and returns it as error sub message
            return CoercionResult(
                errors=[
                    coercion_error(
                        f"Expected type < {schema_type.name} >", node, path
                    )
                ]
            )

    if is_list_type(schema_type):
        item_type = schema_type.ofType

        if isinstance(value, Iterable):  # TODO: str are iterable so?...
            errors = []
            coerced_values = []
            for index, item_value in enumerate(value):
                coerced_value, coerce_errors = coerce_value(
                    item_value, item_type, node, Path(path, index)
                )
                if coerce_errors:
                    errors.extend(coerce_errors)
                elif not errors:
                    coerced_values.append(coerced_value)
            return CoercionResult(value=coerced_values, errors=errors)

        coerced_item_value, coerced_item_errors = coerce_value(
            value, item_type, node
        )
        return CoercionResult(
            value=[coerced_item_value], errors=coerced_item_errors
        )

    if is_input_object_type(schema_type):
        if not isinstance(value, Mapping):
            return CoercionResult(
                errors=[
                    coercion_error(
                        f"Expected type < {schema_type.name} > to be an object",
                        node,
                        path,
                    )
                ]
            )

        errors = []
        coerced_values = {}
        fields = schema_type.arguments

        for field_name, field in fields.items():
            try:
                field_value = value[field_name]
            except KeyError:
                field_value = UNDEFINED_VALUE

            if is_invalid_value(field_value):
                # TODO: at schema build we should use UNDEFINED_VALUE for
                # `default_value` attribute of a field to know if a field has
                # a defined default value (since default value could be `None`)
                # once done, we should check for `UNDEFINED_VALUE` here.
                if field.default_value is not None:
                    coerced_values[field_name] = field.default_value
                # TODO: check if `gql_type` is the correct attr to call here
                elif is_non_null_type(field.gql_type):
                    errors.append(
                        coercion_error(
                            f"Field < {Path(path, field_name)} > of required type "
                            f"< {field.gql_type} > was not provided",
                            node,
                        )
                    )
            else:
                coerced_field_value, coerced_field_errors = coerce_value(
                    field_value,
                    field.get_gql_type(),
                    node,
                    Path(path, field_name),
                )
                if coerced_field_errors:
                    errors.extend(coerced_field_errors)
                elif not errors:
                    coerced_values[field_name] = coerced_field_value

        for field_name in value:
            if field_name not in fields:
                # TODO: try to compute a suggestion list of valid fields
                # depending on the invalid field name returns it as
                # error sub message
                errors.append(
                    coercion_error(
                        f"Field < {field_name} > is not defined by type "
                        f"< {schema_type.name} >.",
                        node,
                        path,
                    )
                )

        return CoercionResult(value=coerced_values, errors=errors)

    raise TypeError(f"Unexpected input type: < {schema_type} >.")
