from functools import lru_cache, partial
from typing import Callable, Dict, List, Optional, Set, Tuple, Union

from tartiflette.execution.nodes.field import ExecutableFieldNode
from tartiflette.language.ast import (
    FieldNode,
    FragmentDefinitionNode,
    FragmentSpreadNode,
    InlineFragmentNode,
)
from tartiflette.language.parsers.libgraphqlparser import parse_to_document
from tartiflette.types.exceptions.tartiflette import MultipleException
from tartiflette.types.helpers import reduce_type
from tartiflette.types.helpers.definition import is_abstract_type
from tartiflette.utils.arguments import coerce_arguments
from tartiflette.utils.type_from_ast import schema_type_from_ast

__all__ = ["collect_executables"]


@lru_cache(maxsize=1024)
def parse_and_validate_query(
    query: Union[str, bytes]
) -> Tuple[Optional["DocumentNode"], Optional[List["GraphQLError"]]]:
    from tartiflette.types.exceptions import GraphQLError
    from tartiflette.utils.errors import to_graphql_error

    try:
        document: "DocumentNode" = parse_to_document(query)
    except GraphQLError as e:
        return None, [e]
    except Exception as e:  # pylint: disable=broad-except
        return (
            None,
            [to_graphql_error(e, message="Server encountered an error.")],
        )
    # TODO: implements function which validate a document against rules
    # errors = validate_document(document)
    # if errors:
    #     return None, errors
    return document, None


def _does_fragment_condition_match(
    schema: "GraphQLSchema",
    fragment_definition: Union["FragmentDefinitionNode", "InlineFragmentNode"],
    schema_type: "GraphQLType",
) -> bool:
    type_condition_node = fragment_definition.type_condition
    if not type_condition_node:
        return True

    conditional_type = schema_type_from_ast(schema, type_condition_node)
    if conditional_type is schema_type:
        return True

    return is_abstract_type(schema_type) and schema_type.is_possible_types(
        conditional_type
    )


def _surround_with_collection_directives(
    func: Callable, directives: list
) -> Callable:
    for directive in reversed(directives):
        func = partial(directive["callable"], directive["args"], func)
    return func


async def _collect_directive(selection):
    return selection


async def _should_include_node(
    execution_context: "ExecutionContext",
    selection: Union["FieldNode", "FragmentSpreadNode", "InlineFragmentNode"],
    path: Optional[List[str]],
) -> bool:
    from tartiflette.execution import get_argument_values
    from tartiflette.types.exceptions.tartiflette import SkipCollection

    if not selection.directives:
        return True

    callable_directives = []
    for directive_node in selection.directives:
        directive_definition = execution_context.schema.find_directive(
            directive_node.name.value
        )

        func = (
            "on_field_collection"
            if isinstance(selection, FieldNode)
            else (
                "on_fragment_spread_collection"
                if isinstance(selection, FragmentSpreadNode)
                else "on_inline_fragment_collection"
            )
        )

        try:
            callable_directives.append(
                {
                    "callable": getattr(
                        directive_definition.implementation, func
                    ),
                    "args": await coerce_arguments(
                        directive_definition.arguments,
                        get_argument_values(
                            directive_definition.arguments,
                            directive_node,
                            execution_context.variable_values,
                        ),
                        execution_context.context,
                        None,  # TODO: should be a "Info" instance
                    ),
                }
            )
        except Exception as e:
            execution_context.add_error(
                e, path=path, locations=[directive_node.location]
            )
            return False

    try:
        await _surround_with_collection_directives(
            _collect_directive, callable_directives
        )(selection)
    except SkipCollection:
        return False
    except Exception as e:
        execution_context.add_error(
            e, path=path, locations=[selection.location]
        )
        return False
    return True


async def collect_executables(
    execution_context: "ExecutionContext",
    runtime_type: "GraphQLObjectType",
    selection_set: "SelectionSetNode",
    fields: Optional[Dict[str, "ExecutableFieldNode"]] = None,
    errors: Optional[List["GraphQLError"]] = None,
    visited_fragments: Optional[Set[str]] = None,
    type_condition: Optional[str] = None,
    path: Optional[List[str]] = None,
    parent: Optional["ExecutableFieldNode"] = None,
) -> Dict[str, "ExecutableFieldNode"]:
    if fields is None:
        fields: Dict[str, "ExecutableFieldNode"] = {}

    if errors is None:
        errors: List["GraphQLError"] = []

    if visited_fragments is None:
        visited_fragments: Set[str] = set()

    for selection in selection_set.selections:
        if not await _should_include_node(execution_context, selection, path):
            continue

        selection_path: List[str] = path if path is not None else []

        if isinstance(selection, FieldNode):
            response_key: str = (
                selection.alias.value
                if selection.alias
                else selection.name.value
            )

            # Computes field's path
            field_path: List[str] = selection_path + [response_key]

            parent_field_type = (
                execution_context.schema.find_type(type_condition)
                if type_condition
                else runtime_type
            )
            field_type_condition = str(parent_field_type)
            graphql_field = parent_field_type.find_field(selection.name.value)
            field_type = execution_context.schema.find_type(
                reduce_type(graphql_field.gql_type)
            )

            fields.setdefault(field_type_condition, {}).setdefault(
                response_key,
                ExecutableFieldNode(
                    name=response_key,
                    schema=execution_context.schema,
                    resolver=graphql_field.resolver,
                    subscribe=graphql_field.subscribe,
                    path=field_path,
                    type_condition=field_type_condition,
                    parent=parent,
                    arguments=selection.arguments,
                    directives=selection.directives,
                ),
            )

            # Adds `FieldNode` to `ExecutableFieldNode` to have all locations
            # and definitions into `Info` resolver object
            fields[field_type_condition][response_key].definitions.append(
                selection
            )

            # Collects selection set fields
            if selection.selection_set:
                await collect_executables(
                    execution_context,
                    field_type,
                    selection.selection_set,
                    fields=fields[field_type_condition][response_key].fields,
                    errors=errors,
                    path=field_path,
                    parent=fields[field_type_condition][response_key],
                )
        elif isinstance(selection, InlineFragmentNode):
            if not _does_fragment_condition_match(
                execution_context.schema, selection, runtime_type
            ):
                continue

            await collect_executables(
                execution_context,
                runtime_type,
                selection.selection_set,
                fields=fields,
                errors=errors,
                visited_fragments=visited_fragments,
                type_condition=(
                    selection.type_condition.name.value
                    if selection.type_condition
                    else type_condition
                ),
                path=selection_path,
                parent=parent,
            )
        elif isinstance(selection, FragmentSpreadNode):
            fragment_name = selection.name.value
            if fragment_name in visited_fragments:
                continue

            visited_fragments.add(fragment_name)

            fragment_definition = execution_context.fragments.get(
                fragment_name
            )
            if not fragment_definition:
                continue

            if not _does_fragment_condition_match(
                execution_context.schema, fragment_definition, runtime_type
            ):
                continue

            await collect_executables(
                execution_context,
                runtime_type,
                fragment_definition.selection_set,
                fields=fields,
                errors=errors,
                visited_fragments=visited_fragments,
                type_condition=fragment_definition.type_condition.name.value,
                path=selection_path,
                parent=parent,
            )

    return fields
