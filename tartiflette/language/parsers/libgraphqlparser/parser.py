import json
import os

from typing import Any, Union

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
_LIBGRAPHQLPARSER_DIR = os.path.dirname(__file__)
try:
    _LIB = _FFI.dlopen(f"{_LIBGRAPHQLPARSER_DIR}/libgraphqlparser.so")
except OSError:
    _LIB = _FFI.dlopen(f"{_LIBGRAPHQLPARSER_DIR}/libgraphqlparser.dylib")


class ParsedData:
    """
    TODO:
    """

    def __init__(self, c_parsed: "CData", destroy_cb: "CData") -> None:
        """
        TODO:
        :param c_parsed: TODO:
        :param destroy_cb: TODO:
        :type c_parsed: TODO:
        :type destroy_cb: TODO:
        """
        self._c_parsed = c_parsed
        self._destroy_cb = destroy_cb

    def __enter__(self) -> None:
        """
        TODO:
        :return: TODO:
        :rtype: TODO:
        """
        return self._c_parsed

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        """
        TODO:
        :param exc_type: TODO:
        :param exc_value: TODO:
        :param traceback: TODO:
        :type exc_type: TODO:
        :type exc_value: TODO:
        :type traceback: TODO:
        :return: TODO:
        :rtype: TODO:
        """
        self._destroy_cb(self._c_parsed)


def _parse_context_manager(query: Union[str, bytes]) -> ParsedData:
    """
    TODO:
    :param query: TODO:
    :type query: TODO:
    :return: TODO:
    :rtype: TODO:
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
    TODO:
    :param query: TODO:
    :type query: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    with _parse_context_manager(query) as parsed:
        return _FFI.string(_LIB.graphql_ast_to_json(parsed))


def parse_to_document(query: Union[str, bytes]) -> "DocumentNode":
    """
    TODO:
    :param query: TODO:
    :type query: TODO:
    :return: TODO:
    :rtype: TODO:

    :Example:
    TODO:
    """
    return document_from_ast_json(json.loads(_parse_to_json_ast(query)))
