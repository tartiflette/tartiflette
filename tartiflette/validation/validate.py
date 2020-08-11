from typing import List, Optional

from tartiflette.language.visitor.type_info import (
    TypeInfo,
    WithTypeInfoVisitor,
)
from tartiflette.language.visitor.visit import visit
from tartiflette.language.visitor.visitor import MultipleVisitor
from tartiflette.validation.context import (
    ASTValidationContext,
    QueryValidationContext,
)
from tartiflette.validation.rules import (
    SPECIFIED_QUERY_RULES,
    SPECIFIED_SDL_RULES,
)


def validate_sdl(
    document_node: "DocumentNode",
    rules: Optional[List["ValidationRule"]] = None,
) -> List["TartifletteError"]:
    """
    Validate a SDL AST document node against defined rules.
    :param document_node: SDL AST document node to validate
    :param rules: list of validation rules to apply
    :type document_node: DocumentNode
    :type rules: Optional[List[ValidationRule]]
    :return: list of errors that may have occurred
    :rtype: List[TartifletteError]
    """
    if rules is None:
        rules = SPECIFIED_SDL_RULES

    context = ASTValidationContext(document_node)
    visit(document_node, MultipleVisitor([rule(context) for rule in rules]))
    return context.errors


def validate_query(
    schema: "GraphQLSchema",
    document_node: "DocumentNode",
    rules: Optional[List["ValidationRule"]] = None,
    type_info: Optional["TypeInfo"] = None,
) -> List["TartifletteError"]:
    """
    Validate a query AST document node against defined rules.
    :param schema: the GraphQLSchema instance linked to the query
    :param document_node: query AST document node to validate
    :param rules: list of validation rules to apply
    :param type_info: TypeInfo instance to keep track of stacks
    :type schema: GraphQLSchema
    :type document_node: DocumentNode
    :type rules: Optional[List[ValidationRule]]
    :type type_info: Optional[TypeInfo]
    :return: list of errors that may have occurred
    :rtype: List[TartifletteError]
    """
    if rules is None:
        rules = SPECIFIED_QUERY_RULES

    if type_info is None:
        type_info = TypeInfo(schema)

    context = QueryValidationContext(schema, document_node, type_info)
    visit(
        document_node,
        WithTypeInfoVisitor(
            type_info, MultipleVisitor([rule(context) for rule in rules])
        ),
    )
    return context.errors
