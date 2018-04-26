from typing import Dict, Any

from tartiflette.parser import TartifletteRequestParser
from tartiflette.executors.basic import execute

import rapidjson as json

from tartiflette.sdl.builder import build_graphql_schema_from_sdl
from tartiflette.schema import GraphQLSchema


class Tartiflette:

    def __init__(self, sdl=None, schema=None, serialize_callback=None):
        self.schema = schema or GraphQLSchema()
        if sdl:
            build_graphql_schema_from_sdl(sdl, schema=self.schema)
        self._serialize_callback = serialize_callback \
            if serialize_callback else json.dumps
        self._parser = TartifletteRequestParser()
        self.schema.bake_schema()

    async def execute(self, query: str, context: Dict[str, Any]=None,
                      variables: Dict[str, Any]=None) -> str:
        """
        Parse and execute a GraphQL Request (as string).
        :param query: The GraphQL request / query as UTF8-encoded string
        :param context: a dict containing anything you need
        :param variables: The variables used in the GraphQL request
        :return: a GraphQL Response (as string)
        """
        return self._serialize_callback(
            await execute(
                self._parser.parse_and_tartify(
                    query,
                    variables=variables,
                    schema=self.schema
                ),
                request_ctx=context
            )
        )
