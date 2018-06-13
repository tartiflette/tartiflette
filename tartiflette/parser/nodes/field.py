from tartiflette.executors.types import ExecutionData
from .node import Node
import asyncio


async def _exec_list(resolver, lst, path, args, request_ctx, name, field, location, schema):
    coroutines = []

    for index, item in enumerate(lst):
        new_path = path[:]
        new_path.append(index)
        if isinstance(item, list):
            coroutines.append(
                _exec_list(
                    resolver, item, new_path[:], args, request_ctx,
                    name, field, location, schema,
                )
            )
        else:
            coroutines.append(
                resolver(
                    request_ctx,
                    ExecutionData(item, new_path[:], args, name, field, location, schema)
                )
            )

    return await asyncio.gather(*coroutines, return_exceptions=True)


def _to_jsonable(thing, execution_data: ExecutionData):
    if isinstance(thing, dict):
        # Makes a copy of the contents so it's not modified by the child
        return {k: v for k, v in thing.items()}, []

    # TODO: This has to be upgraded, it does not manage errors gracefully :x
    return execution_data.field.gql_type.coerce_value(thing), []


class NodeField(Node):
    def __init__(self, resolver, location, path, name, type_condition,
                 gql_type=None, field=None):
        super().__init__(path, 'Field', location, name)
        # TODO: This can be simplified if we have the field & schema
        self.field = field
        self.resolver = resolver
        self.gql_type = gql_type
        self.arguments = {}
        self.results = None
        self.errors = []
        self.schema = None
        self.type_condition = type_condition
        self.as_jsonable = None

    async def _get_results(self, request_ctx):
        if self.parent and isinstance(self.parent.results, list):
            self.results = await _exec_list(
                self.resolver, self.parent.results, self.path, self.arguments,
                request_ctx, self.name, self.field, self.location,
                self.schema,
            )
        else:
            self.results = await self.resolver(
                request_ctx,
                ExecutionData(
                    self.parent.results if self.parent else {},
                    self.path,
                    self.arguments,
                    self.name,
                    self.field,
                    self.location,
                    self.schema,
                )
            )

    def _results_to_jsonable(self):
        self.as_jsonable, self.errors = _to_jsonable(
            self.results,
            ExecutionData(
                self.parent.results if self.parent else {},
                self.path,
                self.arguments,
                self.name,
                self.field,
                self.location,
                self.schema,
            )
        )

    async def __call__(self, request_ctx, schema):
        self.schema = schema
        await self._get_results(request_ctx)
        self._results_to_jsonable()

        if self.parent:
            if isinstance(self.parent.results, list):
                for index, _ in enumerate(self.parent.results):
                    self.parent.as_jsonable[index][self.name
                                                   ] = self.as_jsonable[index]
            else:
                self.parent.as_jsonable[self.name] = self.as_jsonable

        return self.results  # TODO: Leave or remove ? It's currently unused
