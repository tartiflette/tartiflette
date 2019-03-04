from functools import partial
from typing import Any, Callable, Dict, List, Optional, Union

from tartiflette.types.exceptions.tartiflette import InvalidValue, NullError
from tartiflette.types.helpers import has_typename, reduce_type
from tartiflette.utils.arguments import coerce_arguments


def _built_in_coercer(func: Callable, val: Optional[Any], _: "Info") -> Any:
    if val is None:
        return val
    # Don't pass info, cause this is a builtin python type
    return func(val)


def _object_coercer(
    raw_type: Optional[str], val: Optional[Any], *_args, **_kwargs
) -> dict:
    if val is None:
        return None

    _set_typename(val, raw_type)
    return {}


def _list_coercer(
    func: Callable, val: Optional[Any], info: "Info"
) -> Optional[list]:
    if val is None:
        return val

    if isinstance(val, list):
        return [func(v, info) for v in val]
    return [func(val, info)]


def _not_null_coercer(func: Callable, val: Optional[Any], info: "Info") -> Any:
    if val is None:
        raise NullError(val, info)
    return func(val, info)


def _get_type_coercers(field_type: "GraphQLType") -> List[Callable]:
    coercer_list = []
    current_type = field_type
    while hasattr(current_type, "gql_type"):
        if current_type.is_list:
            coercer_list.append(_list_coercer)
        if current_type.is_not_null:
            coercer_list.append(_not_null_coercer)
        current_type = current_type.gql_type
    return coercer_list


def _list_and_null_coercer(
    field_type: Union["GraphQLList", "GraphQLNonNull"], coercer: Callable
) -> Callable:
    field_type_coercers = _get_type_coercers(field_type)
    for field_type_coercer in reversed(field_type_coercers):
        coercer = partial(field_type_coercer, coercer)
    return coercer


def _shall_return_a_list(field_type: Union[str, "GraphQLType"]) -> bool:
    try:
        return (
            field_type.gql_type.is_list
            if field_type.is_not_null
            else field_type.is_list
        )
    except AttributeError:
        pass
    return False


def _enum_coercer(
    enum_valid_values: List[str],
    func: Callable,
    val: Optional[str],
    info: "Info",
) -> Optional[str]:
    if val is None:
        return val

    if val not in enum_valid_values:
        raise InvalidValue(val, info)
    return func(val, info)


def _is_an_enum(
    reduced_type: str, schema: "GraphQLSchema"
) -> Optional[Callable]:
    enum = schema.find_enum(reduced_type)
    if enum:
        return partial(
            _enum_coercer,
            [x.value for x in enum.values],
            partial(
                _built_in_coercer, schema.find_scalar("String").coerce_output
            ),
        )
    return None


def _is_a_scalar(
    reduced_type: str, schema: "GraphQLSchema"
) -> Optional[Callable]:
    scalar = schema.find_scalar(reduced_type)
    if scalar:
        return partial(_built_in_coercer, scalar.coerce_output)
    return None


def _is_union(reduced_type: str, schema: "GraphQLSchema") -> bool:
    try:
        return schema.find_type(reduced_type).is_union
    except (AttributeError, KeyError):
        pass
    return False


def _get_coercer(field: "GraphQLField") -> Optional[Callable]:
    if not field.schema:
        return None

    field_type = field.gql_type
    reduced_type = reduce_type(field_type)
    is_union = _is_union(reduced_type, field.schema)

    if reduced_type == "__Type":
        # preserve None
        coercer = partial(
            _built_in_coercer,
            partial(_object_coercer, reduced_type if not is_union else None),
        )
    else:
        try:
            coercer = _is_an_enum(reduced_type, field.schema)
            if not coercer:
                coercer = _is_a_scalar(reduced_type, field.schema)
                if not coercer:
                    # per default you're an object
                    coercer = partial(
                        _object_coercer, reduced_type if not is_union else None
                    )
        except AttributeError:
            coercer = partial(
                _object_coercer, reduced_type if not is_union else None
            )

    # Manage List and NonNull
    return _list_and_null_coercer(field_type, coercer)


def _surround_with_execution_directives(
    func: Callable, directives: list
) -> Callable:
    for directive in reversed(directives):
        func = partial(
            directive["callables"].on_field_execution, directive["args"], func
        )
    return func


def _introspection_directive_endpoint(element: Any) -> Any:
    return element


def _introspection_directives(directives: list) -> Callable:
    func = _introspection_directive_endpoint
    for directive in reversed(directives):
        func = partial(
            directive["callables"].on_introspection, directive["args"], func
        )
    return func


def _execute_introspection_directives(elements: list, ctx, info) -> list:
    results = []
    for element in elements:
        try:
            directives = _introspection_directives(element.directives)
            result = directives(element, ctx, info)
            if result:
                results.append(result)
        except (AttributeError, TypeError):
            results.append(element)
    return results


def _set_typename(result: Any, typename: Optional[str]) -> None:
    if result is None or typename is None or has_typename(result):
        return

    try:
        result["_typename"] = typename
        return
    except TypeError:
        pass

    try:
        setattr(result, "_typename", typename)
    except AttributeError:
        pass  # Res is unmutable


class _ResolverExecutor:
    def __init__(self, func: Callable, schema_field: "GraphQLField") -> None:
        self._raw_func = func
        self._func = func
        self._schema_field = schema_field
        self._coercer = _get_coercer(schema_field)
        self._shall_produce_list = _shall_return_a_list(schema_field.gql_type)

    async def _introspection(self, element: Any, ctx, info) -> Optional[Any]:
        if isinstance(element, list):
            return _execute_introspection_directives(element, ctx, info)

        elements = _execute_introspection_directives([element], ctx, info)
        try:
            return elements[0]
        except IndexError:
            pass
        return None

    async def __call__(
        self,
        parent_result: Optional[Any],
        args: Dict[str, Any],
        ctx: Optional[Dict[str, Any]],
        info: "Info",
    ) -> (Any, Any):
        try:
            result = await self._func(
                parent_result,
                await coerce_arguments(
                    self._schema_field.arguments, args, ctx, info
                ),
                ctx,
                info,
            )

            if info.execution_ctx.is_introspection:
                result = await self._introspection(result, ctx, info)
            return result, self._coercer(result, info)
        except Exception as e:  # pylint: disable=broad-except
            return e, None

    def apply_directives(self) -> None:
        try:
            self._func = _surround_with_execution_directives(
                self._raw_func, self._schema_field.directives
            )
        except AttributeError:
            self._func = self._raw_func

    def update_func(self, func: Callable) -> None:
        self._raw_func = func

    def update_coercer(self) -> None:
        self._coercer = _get_coercer(self.schema_field)

    def bake(self, custom_default_resolver: Optional[Callable]) -> None:
        self.update_coercer()
        if (
            self._raw_func is default_resolver
            and custom_default_resolver is not None
        ):
            self.update_func(custom_default_resolver)

        if self._schema_field.subscribe and self._raw_func is default_resolver:
            self._raw_func = default_subscription_resolver(self._raw_func)

        self.apply_directives()

    @property
    def schema_field(self) -> None:
        return self._schema_field

    @property
    def shall_produce_list(self) -> None:
        return self._shall_produce_list

    @property
    def cant_be_null(self) -> bool:
        try:
            return self._schema_field.gql_type.is_not_null
        except AttributeError:
            pass
        return False

    @property
    def contains_not_null(self) -> bool:
        try:
            return self._schema_field.gql_type.contains_not_null
        except AttributeError:
            pass
        return False


def default_subscription_resolver(func: Callable):
    async def func_wrapper(
        parent_result: Optional[Any],
        args: Dict[str, Any],
        ctx: Optional[Dict[str, Any]],
        info: "Info",
    ) -> Optional[Any]:
        return await func(
            {info.schema_field.name: parent_result}, args, ctx, info
        )

    return func_wrapper


async def default_resolver(
    parent_result: Optional[Any],
    _args: Dict[str, Any],
    _ctx: Optional[Dict[str, Any]],
    info: "Info",
) -> Optional[Any]:
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
    def get_resolver_executor(func: Callable, field: "GraphQLField"):
        return _ResolverExecutor(func or default_resolver, field)
