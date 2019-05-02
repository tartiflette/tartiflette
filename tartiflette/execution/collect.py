from functools import lru_cache
from typing import Dict, List, Optional, Set, Tuple, Union

from tartiflette.execution.nodes import (
    ExecutableFieldNode,
    ExecutableOperationNode,
)
from tartiflette.language.ast import (
    FieldNode,
    FragmentDefinitionNode,
    FragmentSpreadNode,
    InlineFragmentNode,
    OperationDefinitionNode,
)
from tartiflette.language.parsers.libgraphqlparser import parse_to_document
from tartiflette.types.helpers import reduce_type
from tartiflette.types.helpers.definition import is_abstract_type
from tartiflette.utils.type_from_ast import schema_type_from_ast

__all__ = ["parse_query_to_executable_operations"]


def _does_fragment_condition_match(
    schema: "GraphQLSchema",
    fragment_definition: Union["FragmentDefinitionNode", "InlineFragmentNode"],
    schema_type: "GraphQLType",
) -> bool:
    """
    Determines if a fragment is applicable to the given schema type.
    :param schema: GraphQLSchema on which the execution of the query is based
    :param fragment_definition: fragment to check
    :param schema_type: GraphQLType of reference
    :type schema: GraphQLSchema
    :type fragment_definition: Union[FragmentDefinitionNode, InlineFragmentNode]
    :type schema_type: GraphQLType
    :return: whether or not the fragment is applicable to the given schema type
    :rtype: bool
    """
    type_condition_node = fragment_definition.type_condition
    if not type_condition_node:
        return True

    conditional_type = schema_type_from_ast(schema, type_condition_node)
    if conditional_type is schema_type:
        return True

    return is_abstract_type(schema_type) and schema_type.is_possible_types(
        conditional_type
    )


def _collect_fields(
    schema: "GraphQLSchema",
    fragment_definitions: Dict[str, "FragmentDefinitionNode"],
    runtime_type: "GraphQLObjectType",
    selection_set: "SelectionSetNode",
    fields: Optional[Dict[str, "ExecutableFieldNode"]] = None,
    visited_fragments: Optional[Set[str]] = None,
    type_condition: Optional[str] = None,
    path: Optional[List[str]] = None,
    directives: Optional[List["DirectiveNode"]] = None,
    parent: Optional["ExecutableFieldNode"] = None,
) -> Dict[str, "ExecutableFieldNode"]:
    """
    Calculates fields of a selection set.
    :param schema: GraphQLSchema on which the execution of the query is based
    :param fragment_definitions: fragment definitions mapping defined in the
    query
    :param runtime_type: GraphQLObjectType of the selection set
    :param selection_set: SelectionSetNode to work with
    :param fields: a field name mapping of `ExecutableFieldNode`
    :param visited_fragments: set of visited fragments while parsing the
    selection set
    :param type_condition: type condition of the last fragment parsed
    :param path: root path of the selection set
    :param directives: directives collected during the parsing
    :type schema: GraphQLSchema
    :type fragment_definitions: Dict[str, FragmentDefinitionNode]
    :type runtime_type: GraphQLObjectType
    :type selection_set: SelectionSetNode
    :type fields: Optional[Dict[str, ExecutableFieldNode]]
    :type visited_fragments: Optional[Set[str]]
    :type type_condition: Optional[str]
    :type path: Optional[List[str]]
    :type directives: Optional[List[DirectiveNode]]
    :return: a field name mapping of `ExecutableFieldNode`
    :rtype: Dict[str, ExecutableFieldNode]
    """
    # pylint: disable=too-many-arguments,too-many-locals,too-many-branches
    if fields is None:
        fields: Dict[str, "ExecutableFieldNode"] = {}

    if visited_fragments is None:
        visited_fragments: Set[str] = set()

    for selection in selection_set.selections:
        selection_path: List[str] = path if path is not None else []
        selection_directives: List["DirectiveNode"] = (
            directives if directives is not None else []
        )

        if isinstance(selection, FieldNode):
            response_field: str = (
                selection.alias.value
                if selection.alias
                else selection.name.value
            )

            # Computes field's path & field's directives
            field_path: List[str] = selection_path + [response_field]
            field_directives: List["DirectiveNode"] = selection_directives + (
                selection.directives if selection.directives else []
            )

            parent_field_type = (
                schema.find_type(type_condition)
                if type_condition
                else runtime_type
            )
            field_type_condition = str(parent_field_type)
            graphql_field = parent_field_type.find_field(selection.name.value)
            field_type = schema.find_type(reduce_type(graphql_field.gql_type))

            fields.setdefault(field_type_condition, {}).setdefault(
                response_field,
                ExecutableFieldNode(
                    name=response_field,
                    schema=schema,
                    resolver=graphql_field.resolver,
                    subscribe=graphql_field.subscribe,
                    path=field_path,
                    type_condition=field_type_condition,
                    directives=field_directives,
                    parent=parent,
                ),
            )

            # Adds `FieldNode` to `ExecutableFieldNode` to have all locations
            # and definitions into `Info` resolver object
            fields[field_type_condition][response_field].definitions.append(
                selection
            )

            # Collects selection set fields
            if selection.selection_set:
                _collect_fields(
                    schema,
                    fragment_definitions,
                    field_type,
                    selection.selection_set,
                    fields=fields[field_type_condition][response_field].fields,
                    path=field_path,
                    parent=fields[field_type_condition][response_field],
                )
        elif isinstance(selection, InlineFragmentNode):
            if not _does_fragment_condition_match(
                schema, selection, runtime_type
            ):
                continue

            if selection.directives:
                selection_directives.extend(selection.directives)

            _collect_fields(
                schema,
                fragment_definitions,
                runtime_type,
                selection.selection_set,
                fields,
                visited_fragments,
                type_condition=(
                    selection.type_condition.name.value
                    if selection.type_condition
                    else type_condition
                ),
                path=selection_path,
                directives=selection_directives,
                parent=parent,
            )
        elif isinstance(selection, FragmentSpreadNode):
            fragment_name = selection.name.value
            if fragment_name in visited_fragments:
                continue

            visited_fragments.add(fragment_name)

            fragment_definition = fragment_definitions.get(fragment_name)
            if not fragment_definition:
                continue

            if not _does_fragment_condition_match(
                schema, fragment_definition, runtime_type
            ):
                continue

            if fragment_definition.directives:
                selection_directives.extend(fragment_definition.directives)

            if selection.directives:
                selection_directives.extend(selection.directives)

            _collect_fields(
                schema,
                fragment_definitions,
                runtime_type,
                fragment_definition.selection_set,
                fields,
                visited_fragments,
                type_condition=fragment_definition.type_condition.name.value,
                path=selection_path,
                directives=selection_directives,
                parent=parent,
            )

    return fields


def _operation_definition_to_executable_operation(
    schema: "GraphQLSchema",
    fragment_definitions: Dict[str, "FragmentDefinitionNode"],
    operation_definition: "OperationDefinitionNode",
) -> "ExecutableOperationNode":
    """
    Converts an `OperationDefinitionNode` to an `ExecutableOperationNode`.
    :param schema: GraphQLSchema on which the execution of the query is based
    :param fragment_definitions: fragment definitions mapping defined in the
    query
    :param operation_definition: `OperationDefinitionNode` to convert
    :type schema: GraphQLSchema
    :type fragment_definitions: Dict[str, FragmentDefinitionNode]
    :type operation_definition: OperationDefinitionNode
    :return: an `ExecutableOperationNode` instance
    :rtype: ExecutableOperationNode
    """
    operation_type = schema.find_type(
        schema.get_operation_type(
            operation_definition.operation_type.capitalize()
        )
    )

    return ExecutableOperationNode(
        name=(
            operation_definition.name.value
            if operation_definition.name
            else None
        ),
        operation_type=operation_definition.operation_type,
        fields=_collect_fields(
            schema,
            fragment_definitions,
            operation_type,
            operation_definition.selection_set,
        ),
        definition=operation_definition,
    )


def _document_to_executable_operations(
    schema: "GraphQLSchema", document: "DocumentNode"
) -> Dict[Union[str, None], "ExecutableOperationNode"]:
    """
    Converts a DocumentNode instance to an operation name mapping of
    `ExecutableOperationNode`.
    :param schema: GraphQLSchema on which the execution of the query is based
    :param document: DocumentNode representing the query to execute
    :type schema: GraphQLSchema
    :type document: DocumentNode
    :return: an operation name mapping of `ExecutableOperationNode`
    :rtype: Dict[Union[str, None], ExecutableOperationNode]
    """
    operation_definitions: List["OperationDefinitionNode"] = []
    fragment_definitions: Dict[str, "FragmentDefinitionNode"] = {}

    for definition in document.definitions:
        if isinstance(definition, OperationDefinitionNode):
            operation_definitions.append(definition)
        elif isinstance(definition, FragmentDefinitionNode):
            fragment_definitions[definition.name.value] = definition

    return {
        operation.name.value
        if operation.name
        else None: _operation_definition_to_executable_operation(
            schema, fragment_definitions, operation
        )
        for operation in operation_definitions
    }


@lru_cache(maxsize=1024)
def parse_query_to_executable_operations(
    schema: "GraphQLSchema", query: Union[str, bytes]
) -> Tuple[
    Optional[Dict[Union[str, None], "ExecutableOperationNode"]],
    Optional[List["GraphQLError"]],
]:
    """
    Parse and validate the request in order to convert it to a cached
    operation name mapping of `ExecutableOperationNode`.
    :param schema: GraphQLSchema on which the execution of the query is based
    :param query: GraphQL query to execute
    :type schema: GraphQLSchema
    :type query: Union[str, bytes]
    :return: an operation name mapping of `ExecutableOperationNode` or a list
    of encountered errors
    :rtype: Tuple[
        Optional[Dict[Union[str, None], ExecutableOperationNode]],
        Optional[List[GraphQLError]],
    ]
    """
    document: "DocumentNode" = parse_to_document(query)
    # TODO:
    # errors = validate_document(document)
    # if errors:
    #     return None, errors
    return _document_to_executable_operations(schema, document), None
