from functools import partial
from typing import Any

from tartiflette.types.helpers import reduce_type
from tartiflette.types.exceptions.tartiflette import NullError, InvalidValue


def _built_in_coerser(func, val, _):
    if val is None:
        return val

    # Don't pass info, cause this is a buildin python type caster
    return func(val)


def ___type_coerser(val, _):
    if val is None:
        return val

    return {}


_COERSER = {
    "String": partial(_built_in_coerser, str),
    "Int": partial(_built_in_coerser, int),
    "Float": partial(_built_in_coerser, float),
    "Boolean": partial(_built_in_coerser, bool),
    "__Type": ___type_coerser,
}


def _object_coerser(_, __) -> dict:
    return {}


def _list_coerser(func, val, info) -> list:
    if val is None:
        return val

    if isinstance(val, list):
        return [func(v, info) for v in val]

    return [func(val, info)]


def _not_null_coerser(func, val, info):
    if val is None:
        raise NullError(val, info)

    return func(val, info)


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


def _enum_coerser(enum_valid_values, func, val, info):
    if val is None:
        return val

    if val not in enum_valid_values:
        raise InvalidValue(val, info)
    return func(val, info)


def _get_coerser(field):
    field_type = field.gql_type
    rtype = reduce_type(field_type)
    coerser = _object_coerser
    try:
        coerser = _COERSER[rtype]
    except (TypeError, KeyError):
        pass

    try:
        coerser = partial(
            _enum_coerser,
            [x.value for x in field.schema.enums[rtype].values],
            _COERSER["String"],
        )
    except (AttributeError, KeyError, TypeError):
        pass

    coerser = _list_and_null_coerser(field_type, coerser)

    return coerser


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
        self._coerser = _get_coerser(schema_field)
        self._shall_produce_list = _shall_return_a_list(schema_field.gql_type)
        self._directives = directives or {}

    async def _introspection(self, parent_result, arguments, req_ctx, info):
        element = await self._func(parent_result, arguments, req_ctx, info)
        try:
            if isinstance(element, list):
                element = _execute_introspection_directives(element)
            else:
                element = _execute_introspection_directives([element])
                if element is not None:
                    element = element[0]
        except AttributeError:
            pass

        return element

    async def __call__(
        self, parent_result, arguments: dict, req_ctx: dict, info
    ) -> (Any, Any):
        try:
            if not info.execution_ctx.is_introspection:
                res = await self._func(parent_result, arguments, req_ctx, info)
            else:
                res = await self._introspection(
                    parent_result, arguments, req_ctx, info
                )

            coersed = self._coerser(res, info)
            return res, coersed
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
