from tartiflette.executors.types import ExecutionData
from tartiflette.types.exceptions.tartiflette import GraphQLError
from .node import Node
import asyncio


async def _exec_list(resolver, lst, path, args, request_ctx, name):
    coroutines = []

    for index, item in enumerate(lst):
        new_path = path[:]
        new_path.append(index)
        if isinstance(item, list):
            coroutines.append(
                _exec_list(
                    resolver, item, new_path[:], args, request_ctx,
                    name
                )
            )
        else:
            coroutines.append(
                resolver(
                    request_ctx,
                    ExecutionData(item, new_path[:], args, name)
                )
            )

    return await asyncio.gather(*coroutines, return_exceptions=True)


def _to_jsonable(thing):
    if isinstance(thing, dict):
        # Makes a copy of the contents so it's not modified by the child
        return {x: v for x, v in thing.items()}

    try:
        # TODO: Is this still useful ? Check.
        val = thing.collect_value()
        return val
    except AttributeError:
        pass

    # It's a base python type so no need to do anything
    return thing


class NodeField(Node):
    def __init__(self, resolver, location, path, name, type_condition, gql_type = None):
        super().__init__(path, 'Field', location, name)
        self.resolver = resolver
        self.gql_type = gql_type
        self.arguments = {}
        self.results = None
        self.errors = []

        self.type_condition = type_condition
        self.as_jsonable = None

    async def _get_results(self, request_ctx):
        if self.parent and isinstance(self.parent.results, list):
            self.results = await _exec_list(
                self.resolver, self.parent.results, self.path, self.arguments,
                request_ctx, self.name
            )
        else:
            self.results = await self.resolver(
                request_ctx,
                ExecutionData(
                    self.parent.results if self.parent else {},
                    self.path,
                    self.arguments,
                    self.name
                )
            )

    def _results_to_jsonable(self):
        # TODO: Make cleaner Error management.
        if isinstance(self.results, list):
            self.as_jsonable = []
            for index, result in enumerate(self.results):
                if isinstance(result, GraphQLError):
                    self.errors.append(result.collect_value())
                else:
                    self.as_jsonable.append(_to_jsonable(result))
        else:
            if isinstance(self.results, GraphQLError):
                self.errors.append(self.results.collect_value())
            else:
                self.as_jsonable = _to_jsonable(self.results)

    async def __call__(self, request_ctx):
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
