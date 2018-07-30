from typing import Any, Dict

from tartiflette.executors.basic import execute
from tartiflette.parser import TartifletteRequestParser
from tartiflette.schema import GraphQLSchema, DefaultGraphQLSchema
from tartiflette.sdl.builder import build_graphql_schema_from_sdl


class Tartiflette:
    def __init__(self, sdl: str=None, schema: GraphQLSchema=None):
        if sdl:
            self.schema = GraphQLSchema()
            build_graphql_schema_from_sdl(sdl, schema=self.schema)
        else:
            self.schema = schema if schema else DefaultGraphQLSchema
        self._parser = TartifletteRequestParser()

    async def execute(
        self,
        query: str,
        context: Dict[str, Any] = None,
        variables: Dict[str, Any] = None,
    ) -> str:
        """
        Parse and execute a GraphQL Request (as string).
        :param query: The GraphQL request / query as UTF8-encoded string
        :param context: a dict containing anything you need
        :param variables: The variables used in the GraphQL request
        :return: a GraphQL Response (as dict)
        """
        return await execute(
            self._parser.parse_and_tartify(
                self.schema, query, variables=variables
            ),
            request_ctx=context,
        )
