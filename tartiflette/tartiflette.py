from tartiflette.parser import TartifletteRequestParser
from tartiflette.executors.basic import execute

import rapidjson as json


class Tartiflette():
    def __init__(self, schema_definition, serialize_cbk=None):
        self._schema_definition = schema_definition
        self._serialize_cbk = serialize_cbk if serialize_cbk else json.dumps
        self._parser = TartifletteRequestParser()

    async def execute(self, g_req, context=None, variables=None):
        """
        take a graphql request (as text) and execute it.
        Asynchronally of course. #2018
        """
        return self._serialize_cbk(
            await execute(
                self._parser.parse_and_tartify(
                    g_req,
                    variables=variables,
                    schema_definition=self._schema_definition
                ),
                request_ctx=context
            )
        )
