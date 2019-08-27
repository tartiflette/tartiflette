from tartiflette.language.validators.query.rule import (
    June2018ReleaseValidationRule,
)
from tartiflette.language.validators.query.utils import (
    find_nodes_by_name,
    get_defined_vars,
    get_used_vars,
)
from tartiflette.utils.errors import graphql_error_from_nodes


def _get_message(operation, varname):
    operation_message = (
        f"Operation < {operation.name.value} >"
        if operation.name
        else "anonymous Operation"
    )
    return f"Unused Varibable < {varname} > in {operation_message}."


def _validate_operation(operation, per_operation, per_fragment):
    error_per_var = {}
    used_vars = get_used_vars(operation, per_operation, per_fragment)

    for a_var in get_defined_vars(operation):
        if not find_nodes_by_name(used_vars, a_var.name.value):
            error_per_var.setdefault(a_var.name.value, []).append(a_var)

    return error_per_var


class AllVariablesUsed(June2018ReleaseValidationRule):
    """
    This validator will look through all variables defined in an operation and
    validate that they are used.

    More details @ https://graphql.github.io/graphql-spec/June2018/#sec-All-Variables-Used
    """

    RULE_NAME = "all-variables-used"
    RULE_LINK = "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variables-Used"
    RULE_NUMBER = "5.8.4"

    def validate(
        self, operations=None, per_operation=None, per_fragment=None, **_
    ):

        errors = []

        if not operations:
            return []  # No operation

        if not per_operation:
            per_operation = {}

        if not per_fragment:
            per_fragment = {}

        for operation in operations:
            errors.extend(
                [
                    graphql_error_from_nodes(
                        message=_get_message(operation, k),
                        nodes=[operation] + v,
                        path=None,
                        extensions=self._extensions,
                    )
                    for k, v in _validate_operation(
                        operation, per_operation, per_fragment
                    ).items()
                ]
            )

        return errors
