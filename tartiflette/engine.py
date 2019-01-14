from typing import Any, Dict

from tartiflette.executors.basic import execute as basic_execute
from tartiflette.parser import TartifletteRequestParser
from tartiflette.schema.registry import SchemaRegistry
from tartiflette.schema.bakery import SchemaBakery
from tartiflette.types.exceptions.tartiflette import GraphQLError


class Engine:
    def __init__(
        self,
        sdl,
        schema_name="default",
        custom_default_resolver=None,
        exclude_builtins_scalars=None,
    ):
        # TODO: Use the kwargs and add them to the schema
        # schema can be: file path, file list, folder path, schema object
        self._parser = TartifletteRequestParser()
        SchemaRegistry.register_sdl(schema_name, sdl, exclude_builtins_scalars)
        self._schema = SchemaBakery.bake(
            schema_name, custom_default_resolver, exclude_builtins_scalars
        )

    async def execute(
        self,
        query: str,
        context: Dict[str, Any] = None,
        variables: Dict[str, Any] = None,
    ) -> dict:
        """
        Parse and execute a GraphQL Request (as string).
        :param query: The GraphQL request / query as UTF8-encoded string
        :param context: a dict containing anything you need
        :param variables: The variables used in the GraphQL request
        :return: a GraphQL Response (as dict)
        """
        errors = None
        try:
            root_nodes, exceptions = self._parser.parse_and_tartify(
                self._schema, query, variables=variables
            )
            if exceptions:
                errors = [err.coerce_value() for err in exceptions]
        except GraphQLError as e:
            errors = [e.coerce_value()]
        except Exception:  # pylint: disable=broad-except
            gql_error = GraphQLError("Server encountered an error.")
            errors = [gql_error.coerce_value()]

        if errors:
            return {"data": None, "errors": errors}

        return await basic_execute(root_nodes, request_ctx=context)
