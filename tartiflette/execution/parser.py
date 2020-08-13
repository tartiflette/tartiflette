from typing import Callable, List, Optional, Tuple, Union

from tartiflette.language.parsers.libgraphqlparser import parse_to_document
from tartiflette.types.exceptions.tartiflette import TartifletteError
from tartiflette.utils.errors import to_graphql_error
from tartiflette.validation.validate import validate_query


def parse_and_validate_query(
    query: Union[str, bytes],
    schema: "GraphQLSchema",
    parser: Optional[Callable] = None,
    rules: Optional[List["ValidationRule"]] = None,
) -> Tuple[Optional["DocumentNode"], Optional[List["TartifletteError"]]]:
    """
    Analyzes & validates a query by converting it to a DocumentNode.
    :param query: the GraphQL request / query as UTF8-encoded string
    :param schema: the GraphQLSchema instance linked to the SDL
    :param parser: callable to parse/convert the query to a DocumentNode
    :param rules: list of validation rules to apply to the DocumentNode
    :type query: Union[str, bytes]
    :type schema: GraphQLSchema
    :type parser: Optional[Callable]
    :type rules: Optional[List[ValidationRule]]
    :return: a DocumentNode representing the query
    :rtype: Tuple[Optional[DocumentNode], Optional[List[TartifletteError]]]
    """
    if parser is None:
        parser = parse_to_document

    try:
        document: "DocumentNode" = parser(query)
    except TartifletteError as e:
        return (None, [e])
    except Exception as e:  # pylint: disable=broad-except
        return (
            None,
            [to_graphql_error(e, message="Server encountered an error.")],
        )

    errors = validate_query(schema, document, rules=rules)
    return (document, None) if not errors else (None, errors)
