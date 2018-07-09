from tartiflette.executors.types import ExecutionData
from .node import Node
import asyncio


async def _exec_list(
    resolver, lst, path, args, request_ctx, name, field, location, schema
):
    coroutines = []

    for index, item in enumerate(lst):
        new_path = path[:]
        new_path.append(index)
        if isinstance(item, list):
            coroutines.append(
                _exec_list(
                    resolver,
                    item,
                    new_path[:],
                    args,
                    request_ctx,
                    name,
                    field,
                    location,
                    schema,
                )
            )
        else:
            coroutines.append(
                resolver(
                    request_ctx,
                    ExecutionData(
                        item, new_path[:], args, name, field, location, schema
                    ),
                )
            )

    raw_result = await asyncio.gather(*coroutines, return_exceptions=True)
    result = []
    errors = []
    coerced_result = []
    for tmp_res, tmp_error, tmp_coerced in raw_result:
        result.append(tmp_res)
        coerced_result.append(tmp_coerced)
        if tmp_error:
            errors += tmp_error
    return result, errors, coerced_result


class NodeField(Node):
    def __init__(
        self,
        resolver,
        location,
        path,
        name,
        type_condition,
        gql_type=None,
        field=None,
    ):
        super().__init__(path, "Field", location, name)
        # TODO: This can be simplified if we have the field & schema
        self.field = field
        self.resolver = resolver
        self.gql_type = gql_type
        self.arguments = {}
        self.results = None
        self.coerced = None
        self.errors = []
        self.schema = None
        self.type_condition = type_condition
        self.as_jsonable = None
        self.in_introspection = (
            True if name in ["__type", "__schema", "__typename"] else False
        )

    async def _get_results(self, request_ctx):
        if self.parent and isinstance(self.parent.results, list):
            self.results, self.errors, self.coerced = await _exec_list(
                self.resolver,
                self.parent.results,
                self.path,
                self.arguments,
                request_ctx,
                self.name,
                self.field,
                self.location,
                self.schema,
            )
        else:
            raw_result = await self.resolver(
                request_ctx,
                ExecutionData(
                    self.parent.results if self.parent else {},
                    self.path,
                    self.arguments,
                    self.name,
                    self.field,
                    self.location,
                    self.schema,
                ),
            )
            self.results, self.errors, self.coerced = raw_result

    async def __call__(self, request_ctx, schema):
        self.schema = schema
        await self._get_results(request_ctx)

        def manage_list(par, lii):
            for iii, vvv in enumerate(lii):
                if isinstance(par[iii], list):
                    manage_list(par[iii], vvv)
                else:
                    try:
                        par[iii][self.name] = vvv
                    except TypeError:
                        par[iii] = {self.name: vvv}

        self.as_jsonable = self.coerced

        if self.parent:
            if self.parent.in_introspection:
                self.in_introspection = True
                # TODO: Make better error management on instrospection
                self.errors = []

            if isinstance(self.parent.as_jsonable, list):
                for index, value in enumerate(self.as_jsonable):
                    if isinstance(self.parent.as_jsonable[index], list):
                        manage_list(self.parent.as_jsonable[index], value)
                    else:
                        if self.parent.as_jsonable[index] is None:
                            self.parent.as_jsonable[index] = {}
                        self.parent.as_jsonable[index][self.name] = value
            else:
                if self.parent.as_jsonable is None:
                    self.parent.as_jsonable = {}
                self.parent.as_jsonable[self.name] = self.as_jsonable

        return self.results  # TODO: Leave or remove ? It's currently unused
