import os

from tartiflette.parser import TartifletteRequestParser
from tartiflette.schema import GraphQLSchema
from tartiflette.sdl.builder import build_graphql_schema_from_sdl


class Engine:
    def __init__(self, schema,
                 resolver_middlewares=None,
                 resolvers=None,
                 directive_resolvers=None):
        # TODO: Use the kwargs and add them to the schema
        # schema can be: file path, file list, folder path, schema object
        self._parser = TartifletteRequestParser()
        if isinstance(schema, GraphQLSchema):
            self.schema = schema
            return
        # Always create a file list
        sdl_files_list = None
        full_sdl = ""
        if isinstance(schema, list):
            sdl_files_list = schema
        elif os.path.isfile(schema):
            sdl_files_list = [schema]
        elif os.path.isdir(schema):
            sdl_files_list = [os.path.join(schema, f) for f in
                              os.listdir(schema) if os.path.isfile(
                    os.path.join(schema, f)) and f.endswith('.sdl')]
        else:
            sdl_files_list = []
            full_sdl = schema
        # Convert SDL files into big schema and parse it
        for filepath in sdl_files_list:
            print("Loading SDL file: {}".format(filepath))
            with open(filepath, 'r') as sdl_file:
                data = sdl_file.read().replace('\n', ' ')
                full_sdl += " " + data
        self.schema = GraphQLSchema()
        build_graphql_schema_from_sdl(full_sdl, schema=self.schema)
