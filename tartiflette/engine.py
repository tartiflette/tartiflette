from typing import Any, Callable, Dict, List, Optional, Union

from tartiflette.executors.basic import execute as basic_execute
from tartiflette.parser import TartifletteRequestParser
from tartiflette.resolver.factory import default_error_coercer
from tartiflette.schema.bakery import SchemaBakery
from tartiflette.schema.registry import SchemaRegistry
from tartiflette.types.exceptions.tartiflette import GraphQLError


class Engine:
    def __init__(
        self,
        sdl: Union[str, List[str], "GraphQLSchema"],
        schema_name: str = "default",
        error_coercer: Callable[[Exception], dict] = default_error_coercer,
        custom_default_resolver: Optional[Callable] = None,
        exclude_builtins_scalars: Optional[List[str]] = None,
    ) -> None:
        # TODO: Use the kwargs and add them to the schema
        # SDL can be: raw SDL, file path, folder path, file list, schema object
        self._error_coercer = error_coercer
        self._parser = TartifletteRequestParser()
        SchemaRegistry.register_sdl(schema_name, sdl, exclude_builtins_scalars)
        self._schema = SchemaBakery.bake(
            schema_name, custom_default_resolver, exclude_builtins_scalars
        )

    async def execute(
        self,
        query: str,
        operation_name: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        variables: Optional[Dict[str, Any]] = None,
    ) -> dict:
        """
        Parse and execute a GraphQL request (as string).
        :param query: the GraphQL request / query as UTF8-encoded string
        :param context: a dict containing anything you need
        :param variables: the variables used in the GraphQL request
        :return: a GraphQL response (as dict)
        """
        try:
            root_nodes, errors = self._parser.parse_and_tartify(
                self._schema, query, variables=variables
            )
        except GraphQLError as e:
            errors = [e]
        except Exception:  # pylint: disable=broad-except
            errors = [GraphQLError("Server encountered an error.")]

        if errors:
            return {
                "data": None,
                "errors": [self._error_coercer(err) for err in errors],
            }

        return await basic_execute(
            root_nodes,
            operation_name,
            request_ctx=context,
            error_coercer=self._error_coercer,
        )
