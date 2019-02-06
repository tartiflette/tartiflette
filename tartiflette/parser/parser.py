from typing import Any, Dict, List, Optional, Tuple

from tartiflette.parser.cffi import LibGraphqlParser
from tartiflette.parser.visitor import TartifletteVisitor
from tartiflette.schema import GraphQLSchema


class TartifletteRequestParser(LibGraphqlParser):
    def parse_and_tartify(
        self,
        schema: GraphQLSchema,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
    ) -> Tuple[
        Optional[Dict[str, List["NodeField"]]], Optional[List[Exception]]
    ]:
        visitor = TartifletteVisitor(schema, variables)
        self.parse_and_visit(query, visitor)
        if visitor.exceptions:
            return None, visitor.exceptions  # pylint: disable=raising-bad-type
        return visitor.operations, None
