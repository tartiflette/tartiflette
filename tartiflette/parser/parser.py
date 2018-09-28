from typing import Any, Dict

from tartiflette.parser.cffi import LibGraphqlParser
from tartiflette.parser.visitor import TartifletteVisitor
from tartiflette.schema import GraphQLSchema


class TartifletteRequestParser(LibGraphqlParser):
    def parse_and_tartify(
        self,
        schema: GraphQLSchema,
        query: str,
        variables: Dict[str, Any] = None,
    ):

        visitor = TartifletteVisitor(schema, variables)
        self.parse_and_visit(query, visitor)
        if visitor.exception:
            raise visitor.exception  # pylint: disable=raising-bad-type
        return visitor.root_nodes
