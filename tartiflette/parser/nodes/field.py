from .node import Node
import asyncio
from collections import namedtuple

ExecutionData = namedtuple(
    'ExecutionData', ['parent_result', 'path', 'arguments', 'name']
)


async def _exec_list(func, alist, path, args, request_ctx, name):
    coroutines = []

    for index, item in enumerate(alist):
        if isinstance(item, list):
            coroutines.append(
                _exec_list(
                    func, item, "%s[%s]" % (path, index), args, request_ctx,
                    name
                )
            )
        else:
            coroutines.append(
                func(
                    request_ctx,
                    ExecutionData(item, "%s[%s]" % (path, index), args, name)
                )
            )

    return await asyncio.gather(*coroutines, return_exceptions=True)


def _to_dict(thing):
    if isinstance(thing, dict):
        # Makes a copy of the contents so it's not modified by the child
        return {x: v for x, v in thing.items()}

    # TODO call the correct method when SDL thing
    # generation will be done.
    try:
        return thing.as_ttftt_dict()
    except AttributeError:
        pass

    # Means it's a scalar
    return thing


class NodeField(Node):
    def __init__(self, func, location, path, name, type_condition):
        super().__init__(path, 'Field', location, name)
        self._func = func
        self.results = None
        self.arguments = {}
        self.type_condition = type_condition
        self.as_jsonable = {}

    async def __call__(self, request_ctx):
        # TODO reduce this function (too much if and for)

        if self.parent and isinstance(self.parent.results, list):
            self.results = await _exec_list(
                self._func, self.parent.results, self.path, self.arguments,
                request_ctx, self.name
            )
        else:
            self.results = await self._func(
                request_ctx,
                ExecutionData(
                    self.parent.results if self.parent else {}, self.path,
                    self.arguments, self.name
                )
            )

        if isinstance(self.results, list):
            self.as_jsonable = []
            for result in self.results:
                self.as_jsonable.append(_to_dict(result))
        else:
            self.as_jsonable = _to_dict(self.results)

        if self.parent:
            if isinstance(self.parent.results, list):
                for index, _ in enumerate(self.parent.results):
                    self.parent.as_jsonable[index][self.name
                                                   ] = self.as_jsonable[index]
            else:
                self.parent.as_jsonable[self.name] = self.as_jsonable

        return self.results
