from tartiflette.parser.cffi import LibGraphqlParser
from tartiflette.parser.visitor import TartifletteVisitor


class TartifletteRequestParser(LibGraphqlParser):
    def parse_and_tartify(self, query, variables=None, schema_definition=None):
        visitor = TartifletteVisitor(variables, schema_definition)
        self.parse_and_visit(query, visitor)
        if visitor.exception:
            raise visitor.exception
        return visitor.nodes
