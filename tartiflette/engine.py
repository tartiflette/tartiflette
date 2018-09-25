import os

from typing import Dict, Any
from tartiflette.parser import TartifletteRequestParser
from tartiflette.schema import GraphQLSchema
from tartiflette.sdl.builder import build_graphql_schema_from_sdl
from tartiflette.executors.basic import execute as basic_execute


class Engine:
    def __init__(
        self,
        schema,
        _resolver_middlewares=None,
        _resolvers=None,
        _directive_resolvers=None,
        bake_later=False,
    ):
        # TODO: Use the kwargs and add them to the schema
        # schema can be: file path, file list, folder path, schema object
        self._parser = TartifletteRequestParser()
        if isinstance(schema, GraphQLSchema):
            self.schema = schema
            return
        # Always create a file list
        sdl_files_list = [
            "%s/sdl/builtins/scalar.sdl" % os.path.dirname(__file__),
            "%s/sdl/builtins/directives.sdl" % os.path.dirname(__file__),
            "%s/sdl/builtins/introspection.sdl" % os.path.dirname(__file__),
        ]
        full_sdl = ""
        if isinstance(schema, list):
            sdl_files_list = sdl_files_list + schema
        elif os.path.isfile(schema):
            sdl_files_list = sdl_files_list + [schema]
        elif os.path.isdir(schema):
            sdl_files_list = sdl_files_list + [
                os.path.join(schema, f)
                for f in os.listdir(schema)
                if os.path.isfile(os.path.join(schema, f))
                and f.endswith(".sdl")
            ]
        else:
            full_sdl = schema
        # Convert SDL files into big schema and parse it

        for filepath in sdl_files_list:
            with open(filepath, "r") as sdl_file:
                data = sdl_file.read().replace("\n", " ")
                full_sdl += " " + data
        self.schema = GraphQLSchema()
        build_graphql_schema_from_sdl(full_sdl, schema=self.schema)
        if not bake_later:
            self.schema.bake()

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
                self.schema, query, variables=variables
            ),
            request_ctx=context,
        )
