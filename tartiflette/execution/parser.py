from typing import List, Optional, Tuple, Union

from tartiflette.language.parsers.libgraphqlparser import parse_to_document
from tartiflette.types.exceptions.tartiflette import TartifletteError
from tartiflette.utils.errors import to_graphql_error
from tartiflette.validation.validate import validate_query


def parse_and_validate_query(
    query: Union[str, bytes], schema: "GraphQLSchema"
) -> Tuple[Optional["DocumentNode"], Optional[List["TartifletteError"]]]:
    """
    Analyzes & validates a query by converting it to a DocumentNode.
    :param query: the GraphQL request / query as UTF8-encoded string
    :type query: Union[str, bytes]
    :param schema: the GraphQLSchema instance linked to the engine
    :type schema: GraphQLSchema
    :return: a DocumentNode representing the query
    :rtype: Tuple[Optional[DocumentNode], Optional[List[TartifletteError]]]
    """
    try:
        document: "DocumentNode" = parse_to_document(query, schema)
    except TartifletteError as e:
        return None, [e]
    except Exception as e:  # pylint: disable=broad-except
        return (
            None,
            [to_graphql_error(e, message="Server encountered an error.")],
        )

    errors = validate_query(schema, document)
    if errors:
        return None, errors

    return document, None
