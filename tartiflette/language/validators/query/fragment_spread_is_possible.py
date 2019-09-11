from tartiflette.language.validators.query.rule import (
    June2018ReleaseValidationRule,
)
from tartiflette.language.validators.query.utils import find_nodes_by_name
from tartiflette.types.type import GraphQLCompositeType
from tartiflette.utils.errors import graphql_error_from_nodes


def _get_spreaded_fragment(fragments, spreads):
    spreaded_fragments = []
    for spread in spreads:
        nodes = find_nodes_by_name(fragments, spread["spread"].name.value)
        if nodes:
            spreaded_fragments.append(nodes[0])
    return spreaded_fragments


def _validate_node(node, schema, possible_types_set):
    if node.type_condition is None:
        return True  # Cases for ... @directive { field }

    if not schema.has_type(node.type_condition.name.value):
        return True  # Handled by another Validator (5.5.1.2)

    node_type = schema.find_type(node.type_condition.name.value)
    if not isinstance(node_type, GraphQLCompositeType):
        return True  # Handled by another Validator (5.5.1.3)

    if not node_type.possible_types_set.intersection(possible_types_set):
        return False
    return True


class FragmentSpreadIsPossible(June2018ReleaseValidationRule):
    """
    This validator validates that a Fragment is speadable where it is spread.

    I.E it validates that the type condition of the spreaded fragment (or inline)
    is a possibleType in the context of the spread

    More details @ https://graphql.github.io/graphql-spec/June2018/#sec-Fragment-spread-is-possible
    """

    RULE_NAME = "fragment-spread-is-possible"
    RULE_LINK = "https://graphql.github.io/graphql-spec/June2018/#sec-Fragment-spread-is-possible"
    RULE_NUMBER = "5.5.2.3"

    def _validate_is_possible(
        self, type_name, nodes, message, path, schema, locations=None
    ):  # pylint: disable=too-many-locals
        errors = []

        if not schema.has_type(type_name):
            return []  # Handled by another Validator (5.5.2.1)

        schema_type = schema.find_type(type_name)
        if not isinstance(schema_type, GraphQLCompositeType):
            return []  # Handled by another Validator (5.5.1.3)

        for index, node in enumerate(nodes):
            if not _validate_node(
                node, schema, schema_type.possible_types_set
            ):
                location = node.type_condition
                details = ""
                if message == "spread":
                    details = f" via < {node.name.value} > Fragment "
                    location = locations[index]["spread"]
                    path = locations[index]["path"]

                errors.append(
                    graphql_error_from_nodes(
                        message=f"Can't {message} < {node.type_condition.name.value} >{details}on Type < {type_name} >.",
                        nodes=location,
                        path=path,
                        extensions=self._extensions,
                    )
                )

        return errors

    def _validate_inlines(self, inlined_in, path, schema):
        errors = []
        for type_name, inlines in inlined_in.items():
            errors.extend(
                self._validate_is_possible(
                    path=path,
                    schema=schema,
                    message="inline",
                    type_name=type_name,
                    nodes=inlines,
                )
            )

        return errors

    def _validate_spreads(self, fragments, spreaded_in, path, schema):
        errors = []

        for type_name, spreads in spreaded_in.items():
            spreaded_fragments = _get_spreaded_fragment(fragments, spreads)
            errors.extend(
                self._validate_is_possible(
                    type_name=type_name,
                    nodes=spreaded_fragments,
                    message="spread",
                    path=path,
                    schema=schema,
                    locations=spreads,
                )
            )

        return errors

    def validate(
        self, path, schema, fragments, inlined_in=None, spreaded_in=None, **__
    ):
        if not inlined_in:
            inlined_in = {}

        if not spreaded_in:
            spreaded_in = {}

        return self._validate_inlines(
            inlined_in, path, schema
        ) + self._validate_spreads(fragments, spreaded_in, path, schema)
