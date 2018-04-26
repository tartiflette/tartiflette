from tartiflette.parser.cffi import LibGraphqlParser
from tartiflette.parser.visitor import TartifletteVisitor


class TartifletteRequestParser(LibGraphqlParser):
    def parse_and_tartify(self, query, variables=None, schema=None):
        visitor = TartifletteVisitor(variables, schema)
        self.parse_and_visit(query, visitor)
        if visitor.exception:
            raise visitor.exception
        return visitor.nodes
