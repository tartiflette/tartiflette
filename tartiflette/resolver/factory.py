from functools import partial
from typing import Any

from tartiflette.types.helpers import reduce_type, has_typename
from tartiflette.types.exceptions.tartiflette import NullError, InvalidValue


def _built_in_coercer(func, val, _):
    if val is None:
        return val

    # Don't pass info, cause this is a builtin python type
    return func(val)


def _object_coercer(raw_type, val, *_, **__) -> dict:
    _set_typename(val, raw_type)
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


def _is_an_enum(rtype, schema):
    enum = schema.find_enum(rtype)
    if enum:
        return partial(
            _enum_coercer,
            [x.value for x in enum.values],
            partial(
                _built_in_coercer, schema.find_scalar("String").coerce_output
            ),
        )

    return None


def _is_a_scalar(rtype, schema):
    scalar = schema.find_scalar(rtype)
    if scalar:
        return partial(_built_in_coercer, scalar.coerce_output)
    return None


def _is_union(rtype, schema):
    try:
        return schema.find_type(rtype).is_union
    except (AttributeError, KeyError):
        pass

    return False


def _get_coercer(field):
    if not field.schema:
        return None

    field_type = field.gql_type
    rtype = reduce_type(field_type)
    is_union = _is_union(rtype, field.schema)

    if rtype == "__Type":
        # preserve None
        coercer = partial(
            _built_in_coercer,
            partial(_object_coercer, rtype if not is_union else None),
        )
    else:
        try:
            coercer = _is_an_enum(rtype, field.schema)
            if not coercer:
                coercer = _is_a_scalar(rtype, field.schema)
                if not coercer:
                    # per default you're an object
                    coercer = partial(
                        _object_coercer, rtype if not is_union else None
                    )
        except AttributeError:
            coercer = partial(_object_coercer, rtype if not is_union else None)

    # Manage List and NonNull
    coercer = _list_and_null_coercer(field_type, coercer)

    return coercer


def _surround_with_execution_directives(func, directives):
    for directive in reversed(directives):
        func = partial(
            directive["callables"].on_execution, directive["args"], func
        )
    return func


def _introspection_directive_endpoint(element):
    return element


def _introspection_directives(directives):
    func = _introspection_directive_endpoint
    for directive in reversed(directives):
        func = partial(
            directive["callables"].on_introspection, directive["args"], func
        )
    return func


def _execute_introspection_directives(elements):
    ret = []
    for ele in elements:
        try:
            directives = _introspection_directives(ele.directives)
            res = directives(ele)
            if res:
                ret.append(res)
        except (AttributeError, TypeError):
            ret.append(ele)
    return ret


def _set_typename(res, typename):
    if res is None or typename is None or has_typename(res):
        return

    try:
        res["_typename"] = typename
        return
    except TypeError:
        pass

    try:
        setattr(res, "_typename", typename)
    except AttributeError:
        pass  # Res is unmutable

    return


class _ResolverExecutor:
    def __init__(self, func, schema_field):
        self._raw_func = func
        self._func = func
        self._schema_field = schema_field
        self._coercer = _get_coercer(schema_field)
        self._shall_produce_list = _shall_return_a_list(schema_field.gql_type)

    async def _introspection(self, element):
        if isinstance(element, list):
            return _execute_introspection_directives(element)

        element = _execute_introspection_directives([element])
        if element is not None:
            element = element[0]

        return element

    async def __call__(
        self, parent_result, arguments: dict, req_ctx: dict, info
    ) -> (Any, Any):
        try:
            dfv = self._schema_field.get_arguments_default_values()
            dfv.update(arguments)
            res = await self._func(parent_result, dfv, req_ctx, info)
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

    def update_coercer(self):
        self._coercer = _get_coercer(self.schema_field)

    def bake(self, custom_default_resolver):
        self.update_coercer()
        if (
            self._raw_func is default_resolver
            and custom_default_resolver is not None
        ):
            self.update_func(custom_default_resolver)
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


async def default_resolver(
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


def default_error_coercer(exception: Exception) -> dict:
    return exception.coerce_value()


class ResolverExecutorFactory:
    @staticmethod
    def get_resolver_executor(func, field):
        return _ResolverExecutor(func or default_resolver, field)
