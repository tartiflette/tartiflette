from functools import partial
from typing import Any

from tartiflette.types.helpers import reduce_type
from tartiflette.types.exceptions.tartiflette import NullError, InvalidValue


def _built_in_coercer(func, val, _):
    if val is None:
        return val

    # Don't pass info, cause this is a builtin python type
    return func(val)


def _object_coercer(*_, **__) -> dict:
    return {}


def _list_coercer(func, val, info) -> list:
    if val is None:
        return val

    if isinstance(val, list):
        return [func(v, info) for v in val]

    return [func(val, info)]


def _not_null_coercer(func, val, info):
    if val is None:
        raise NullError(val, info)

    return func(val, info)


def _get_type_coercers(field_type):
    coercer_list = []
    current_type = field_type
    while hasattr(current_type, "gql_type"):
        if current_type.is_list:
            coercer_list.append(_list_coercer)
        if current_type.is_not_null:
            coercer_list.append(_not_null_coercer)

        current_type = current_type.gql_type

    return coercer_list


def _list_and_null_coercer(field_type, coercer):
    coercer_list = _get_type_coercers(field_type)
    for coer in reversed(coercer_list):
        coercer = partial(coer, coercer)

    return coercer


def _shall_return_a_list(field_type):
    try:
        if field_type.is_not_null:
            return field_type.gql_type.is_list
        return field_type.is_list
    except AttributeError:
        pass
    return False


def _enum_coercer(enum_valid_values, func, val, info):
    if val is None:
        return val

    if val not in enum_valid_values:
        raise InvalidValue(val, info)
    return func(val, info)


def _get_coercer(field):
    field_type = field.gql_type
    rtype = reduce_type(field_type)

    # Per default you're an object
    coercer = _object_coercer

    if rtype == "__Type":
        coercer = partial(_built_in_coercer, _object_coercer)
    else:
        # Is this an enum ?
        try:
            coercer = partial(
                _enum_coercer,
                [x.value for x in field.schema.enums[rtype].values],
                partial(
                    _built_in_coercer,
                    field.schema.find_scalar("String").coerce_output,
                ),
            )
        except (AttributeError, KeyError, TypeError):
            pass

        # Is this a custom scalar ?
        try:
            coercer = partial(
                partial(
                    _built_in_coercer,
                    field.schema.find_scalar(rtype).coerce_output,
                )
            )
        except (AttributeError, KeyError):
            pass

    # Manage List and NonNull
    coercer = _list_and_null_coercer(field_type, coercer)

    return coercer


def _surround_with_execution_directives(func, directives):
    for directive in reversed(directives):
        try:
            func = partial(
                directive["callables"].on_execution, directive["args"], func
            )
        except AttributeError:
            pass
    return func


def _introspection_directive_endpoint(element):
    return element


def _introspection_directives(directives):
    func = _introspection_directive_endpoint
    for directive in reversed(directives):
        try:
            func = partial(
                directive["callables"].on_introspection,
                directive["args"],
                func,
            )
        except AttributeError:
            pass
    return func


def _execute_introspection_directives(elements):
    ret = []
    for ele in elements:
        try:
            directives = _introspection_directives(ele.directives)
            res = directives(ele)
            if res:
                ret.append(res)
        except AttributeError:
            ret.append(ele)
    return ret


class _ResolverExecutor:
    def __init__(self, func, schema_field, directives):
        self._raw_func = func
        self._func = func
        self._schema_field = schema_field
        self._coercer = _get_coercer(schema_field)
        self._shall_produce_list = _shall_return_a_list(schema_field.gql_type)
        self._directives = directives or {}

    async def _introspection(self, element):
        try:
            if isinstance(element, list):
                element = _execute_introspection_directives(element)
            else:
                element = _execute_introspection_directives([element])
                if element is not None:
                    element = element[0]
        except (AttributeError, TypeError):
            pass

        return element

    async def __call__(
        self, parent_result, arguments: dict, req_ctx: dict, info
    ) -> (Any, Any):
        try:
            res = await self._func(parent_result, arguments, req_ctx, info)
            if info.execution_ctx.is_introspection:
                res = await self._introspection(res)

            coerced = self._coercer(res, info)
            return res, coerced
        except Exception as e:  # pylint: disable=broad-except
            return e, None

    def apply_directives(self):
        try:
            self._func = _surround_with_execution_directives(
                self._raw_func, self._schema_field.directives
            )
        except AttributeError:
            self._func = self._raw_func

    def update_func(self, func):
        self._raw_func = func
        self.apply_directives()

    def update_coercer(self):
        self._coercer = _get_coercer(self.schema_field)

    @property
    def schema_field(self):
        return self._schema_field

    @property
    def shall_produce_list(self):
        return self._shall_produce_list

    @property
    def cant_be_null(self):
        ret = False
        try:
            ret = self._schema_field.gql_type.is_not_null
        except AttributeError:
            pass
        return ret

    @property
    def contains_not_null(self):
        try:
            return self._schema_field.gql_type.contains_not_null
        except AttributeError:
            pass
        return False


async def _default_resolver(
    parent_result, _arguments: dict, _request_ctx: dict, info
) -> Any:
    try:
        return getattr(parent_result, info.schema_field.name)
    except AttributeError:
        pass

    try:
        return parent_result[info.schema_field.name]
    except (KeyError, TypeError):
        pass

    return None


class ResolverExecutorFactory:
    @staticmethod
    def get_resolver_executor(func, field, directives):
        return _ResolverExecutor(func or _default_resolver, field, directives)
