from typing import Dict, Any
from tartiflette.parser import TartifletteRequestParser
from tartiflette.schema.registry import SchemaRegistry
from tartiflette.schema.bakery import SchemaBakery
from tartiflette.executors.basic import execute as basic_execute


class Engine:
    def __init__(self, sdl, schema_name="default"):
        # TODO: Use the kwargs and add them to the schema
        # schema can be: file path, file list, folder path, schema object
        self._parser = TartifletteRequestParser()
        SchemaRegistry.register_sdl(schema_name, sdl)
        self._schema = SchemaBakery.bake(schema_name)

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
        return await basic_execute(
            self._parser.parse_and_tartify(
                self._schema, query, variables=variables
            ),
            request_ctx=context,
        )
