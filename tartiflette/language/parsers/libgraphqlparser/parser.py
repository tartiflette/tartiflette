import json
import os

from types import TracebackType
from typing import Optional, Type, Union

from cffi import FFI

from tartiflette.language.parsers.libgraphqlparser.transformers import (
    document_from_ast_json,
)
from tartiflette.types.exceptions.tartiflette import GraphQLSyntaxError

# TODO: automatize read from headers files
_FFI = FFI()
_FFI.cdef(
    """
struct GraphQLAstNode *graphql_parse_string(
    const char *text, const char **error);

struct GraphQLAstNode *graphql_parse_string_with_experimental_schema_support(
    const char *text, const char **error);

void graphql_error_free(const char *error);

void graphql_node_free(struct GraphQLAstNode *node);

const char *graphql_ast_to_json(const struct GraphQLAstNode *node);
"""
)

# TODO: use importlib.resource in Python 3.7
_LIBGRAPHQLPARSER_DIR = os.path.join(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    ),
    "parser",
    "cffi",
)
try:
    _LIB = _FFI.dlopen(f"{_LIBGRAPHQLPARSER_DIR}/libgraphqlparser.so")
except OSError:
    _LIB = _FFI.dlopen(f"{_LIBGRAPHQLPARSER_DIR}/libgraphqlparser.dylib")


class ParsedData:
    """
    Utils context manager to properly read and free a query parsed with the
    libgraphqlparser library.
    """

    def __init__(self, c_parsed: "CData", destroy_cb: "CData") -> None:
        """
        :param c_parsed: struct GraphQLAstNode *
        :param destroy_cb: void(*)(struct GraphQLAstNode *)
        :type c_parsed: CData
        :type destroy_cb: CData
        """
        self._c_parsed = c_parsed
        self._destroy_cb = destroy_cb

    def __enter__(self) -> None:
        """
        Returns the result of the query parsed with the libgraphqlparser
        library.
        :return: struct GraphQLAstNode *
        :rtype: CData
        """
        return self._c_parsed

    def __exit__(
        self,
        exc_type: Optional[Type],
        exc_value: Optional[Exception],
        traceback: Optional[TracebackType],
    ) -> None:
        """
        Frees the resource related to the parsing of the query made by the
        libgraphqlparser library.
        :param exc_type: class of the exception potentially raised
        :param exc_value: instance of the exception potentially raised
        :param traceback: traceback of the exception potentially raised
        :type exc_type: Optional[Type]
        :type exc_value: Optional[Exception]
        :type traceback: Optional[TracebackType]
        :rtype: None
        """
        self._destroy_cb(self._c_parsed)


def _parse_context_manager(query: Union[str, bytes]) -> ParsedData:
    """
    Parses the query with the libgraphqlparser library and returns a ParsedData
    instance.
    :param query: query to parse with libgraphqlparser
    :type query: Union[str, bytes]
    :return: a ParsedData instance which is a context manager
    :rtype: ParsedData
    :raises GraphQLSyntaxError: raised when the libgraphqlparser library
    couldn't parse the query due to a syntax error.
    """
    if isinstance(query, str):
        query = query.encode("UTF-8")

    errors = _FFI.new("char **")

    parsed_data = ParsedData(
        _LIB.graphql_parse_string_with_experimental_schema_support(
            _FFI.new("char[]", query), errors
        ),
        _LIB.graphql_node_free,
    )

    if errors[0] != _FFI.NULL:
        # TODO: parse libgraphqlparser error string and fill location
        e = GraphQLSyntaxError(
            _FFI.string(errors[0]).decode("UTF-8", "replace")
        )
        _LIB.graphql_error_free(errors[0])
        raise e

    return parsed_data


def _parse_to_json_ast(query: Union[str, bytes]) -> bytes:
    """
    Parses the query and returns its AST JSON representation as bytes.
    :param query: query to parse
    :type query: Union[str, bytes]
    :return: bytes AST JSON representation of the query
    :rtype: bytes
    """
    with _parse_context_manager(query) as parsed:
        return _FFI.string(_LIB.graphql_ast_to_json(parsed))


def parse_to_document(query: Union[str, bytes]) -> "DocumentNode":
    """
    Returns a DocumentNode instance which represents the query after being
    parsed.
    :param query: query to parse and transform into a DocumentNode
    :type query: Union[str, bytes]
    :return: a DocumentNode representing the query
    :rtype: DocumentNode

    :Example:

    >>> from tartiflette.language.parsers.libgraphqlparser import (
    >>>     parse_to_document
    >>> )
    >>>
    >>>
    >>> query_document = parse_to_document('''query MyOperation {
    >>>   cat(id: 1) {
    >>>     id
    >>>     name
    >>>   }
    >>> }''')
    """
    return document_from_ast_json(json.loads(_parse_to_json_ast(query)))
