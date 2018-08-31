from functools import partial
from typing import Any

from tartiflette.types.helpers import reduce_type


def _built_in_coerser(func, val):
    if val is None:
        return val

    return func(val)


# TODO change coercer to also have _schema and validate _string(val) is in val list
def _enum_coerser(val):
    return _string_coerser(val)


_COERSER = {
    "String": partial(_built_in_coerser, str),
    "Int": partial(_built_in_coerser, int),
    "Float": partial(_built_in_coerser, float),
    "Boolean": partial(_built_in_coerser, bool),
}


def _object_coerser(_v) -> dict:
    return {}


def _list_coerser(func, val) -> list:
    if val is None:
        return val

    if isinstance(val, list):
        return [func(v) for v in val]

    return [func(val)]


def _not_null_coerser(func, val):
    if val is None:
        raise Exception("Shouldn't be null")

    return func(val)


def _get_type_coercers(field_type):
    coercer_list = []
    current_type = field_type
    while hasattr(current_type, "gql_type"):
        if current_type.is_list:
            coercer_list.append(_list_coerser)
        if current_type.is_not_null:
            coercer_list.append(_not_null_coerser)

        current_type = current_type.gql_type

    return coercer_list


def _list_and_null_coerser(field_type, coerser):
    coerser_list = _get_type_coercers(field_type)
    for coer in reversed(coerser_list):
        coerser = partial(coer, coerser)

    return coerser


def _shall_return_a_list(field_type):
    try:
        if field_type.is_not_null:
            return field_type.gql_type.is_list
        return field_type.is_list
    except AttributeError:
        pass
    return False


def _get_coerser(field_type):
    rtype = reduce_type(field_type)

    coerser = _object_coerser
    try:
        coerser = _COERSER[rtype]
    except (TypeError, KeyError):
        pass

    coerser = _list_and_null_coerser(field_type, coerser)

    return coerser


class _ResolverExecutor:
    def __init__(self, func, schema_field):
        self._func = func
        self._schema_field = schema_field
        self._coerser = _get_coerser(schema_field.gql_type)
        self._shall_produce_list = _shall_return_a_list(schema_field.gql_type)

    async def __call__(
        self, parent_result, arguments: dict, req_ctx: dict, info
    ) -> (Any, Any):
        try:
            res = await self._func(parent_result, arguments, req_ctx, info)
            coersed = self._coerser(res)
            return res, coersed
        except Exception as e:  # pylint: disable=broad-except
            return e, None

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
    def get_resolver_executor(func, field):
        return _ResolverExecutor(func or _default_resolver, field)
