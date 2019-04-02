from functools import partial
from typing import Any, Callable, Dict, Optional, Union

from tartiflette.types.exceptions.tartiflette import SkipExecution
from tartiflette.utils.arguments import coerce_arguments
from tartiflette.utils.coercer import get_coercer


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


class _ResolverExecutor:
    def __init__(self, func: Callable, schema_field: "GraphQLField") -> None:
        self._raw_func = func
        self._func = func
        self._schema_field = schema_field
        self._coercer = get_coercer(schema_field)
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
        except SkipExecution as e:
            raise e
        except Exception as e:  # pylint: disable=broad-except
            return e, None

    def apply_directives(self) -> None:
        try:
            self._func = _surround_with_execution_directives(
                self._raw_func, self._schema_field.directives
            )
        except AttributeError:
            self._func = self._raw_func

    def add_directive(
        self, directive: Dict[str, Union["Directive", Dict[str, Any]]]
    ) -> None:
        self._func = _surround_with_execution_directives(
            self._func, [directive]
        )

    def update_func(self, func: Callable) -> None:
        self._raw_func = func

    def update_coercer(self) -> None:
        self._coercer = get_coercer(self._schema_field)

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
    def schema_field(self) -> "GraphQLField":
        return self._schema_field

    @property
    def shall_produce_list(self) -> bool:
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
