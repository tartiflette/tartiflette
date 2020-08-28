import asyncio

from functools import partial
from typing import Any, AsyncGenerator, Callable, Dict, List, Optional, Union

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.utils.values import is_invalid_value

__all__ = (
    "introspection_directives_executor",
    "default_post_input_coercion_directive",
    "default_pre_output_coercion_directive",
    "wraps_with_directives",
)


async def _execute_introspection_directive(
    element: Any,
    ctx: Optional[Any],
    info: "ResolveInfo",
    context_coercer: Optional[Any] = None,
) -> Any:
    """
    Applies introspection directives on the element.
    :param element: element to treat
    :param ctx: context passed to the query execution
    :param info: information related to the execution and the resolved field
    :param context_coercer: context passed to the query execution to use on
    argument coercion process
    :type element: Any
    :type ctx: Optional[Any]
    :type info: ResolveInfo
    :type context_coercer: Optional[Any]
    :return: the coerced element
    :rtype: Any
    """
    try:
        if element.introspection_directives:
            result = await element.introspection_directives(
                element, ctx, info, context_coercer=context_coercer
            )
            if result:
                return result
            return UNDEFINED_VALUE
    except (AttributeError, TypeError):
        pass
    return element


async def introspection_directives_executor(
    element: Any,
    ctx: Optional[Any],
    info: "ResolveInfo",
    context_coercer: Optional[Any] = None,
) -> Any:
    """
    Applies introspection directives on the element or a list of elements.
    :param element: element to treat
    :param ctx: context passed to the query execution
    :param info: information related to the execution and the resolved field
    :param context_coercer: context passed to the query execution to use on
    argument coercion process
    :type element: Any
    :type ctx: Optional[Any]
    :type info: ResolveInfo
    :type context_coercer: Optional[Any]
    :return: the coerced element
    :rtype: Any
    """
    if not isinstance(element, list):
        computed_element = await _execute_introspection_directive(
            element, ctx, info, context_coercer=context_coercer
        )
        if not is_invalid_value(computed_element):
            return computed_element
        return None

    results = await asyncio.gather(
        *[
            _execute_introspection_directive(
                item, ctx, info, context_coercer=context_coercer
            )
            for item in element
        ]
    )
    return [result for result in results if not is_invalid_value(result)]


async def default_post_input_coercion_directive(
    parent_node: Union[
        "FieldNode",
        "DirectiveNode",
        "VariableDefinitionNode",
        "InputValueDefinitionNode",
    ],
    input_definition_node: Union[
        "InputObjectTypeDefinitionNode",
        "InputValueDefinitionNode",
        "EnumTypeDefinitionNode",
        "EnumValueDefinitionNode",
        "ScalarTypeDefinitionNode",
    ],
    value: Any,
    *args,
    **kwargs,
) -> Any:
    """
    Default callable to use to wrap with directives on `on_post_input_coercion`
    hook name.
    :param parent_node: the root parent AST node
    :param input_definition_node: the input definition AST node
    :param value: the coerced value of the argument
    :type parent_node: Union[
        FieldNode,
        DirectiveNode,
        VariableDefinitionNode,
        InputValueDefinitionNode,
    ]
    :type input_definition_node: Union[
        InputObjectTypeDefinitionNode,
        InputValueDefinitionNode,
        EnumTypeDefinitionNode,
        EnumValueDefinitionNode,
        ScalarTypeDefinitionNode,
    ]
    :type value: Any
    :return: the coerced value of the input
    :rtype: Any
    """
    # pylint: disable=unused-argument
    return value


async def default_pre_output_coercion_directive(
    output_definition_node: Union[
        "InterfaceTypeDefinitionNode",
        "ObjectTypeDefinitionNode",
        "UnionTypeDefinitionNode",
        "EnumTypeDefinitionNode",
        "EnumValueDefinitionNode",
        "ScalarTypeDefinitionNode",
    ],
    value: Any,
    *args,
    **kwargs,
) -> Any:
    """
    Default callable to use to wrap with directives on `on_pre_output_coercion`
    hook name.
    :param output_definition_node: the input definition AST node
    :param value: the coerced value of the argument
    :type output_definition_node: Union[
        InterfaceTypeDefinitionNode,
        ObjectTypeDefinitionNode,
        UnionTypeDefinitionNode,
        EnumTypeDefinitionNode,
        EnumValueDefinitionNode,
        ScalarTypeDefinitionNode,
    ]
    :type value: Any
    :return: the coerced value of the output
    :rtype: Any
    """
    # pylint: disable=unused-argument
    return value


async def _default_directive_callable(value: Any, *args, **kwargs) -> Any:
    """
    Default callable to use to wrap with directives when the hook doesn't
    implements a specific callable.
    :param value: the coerced value
    :type value: Any
    :return: the coerced value
    :rtype: Any
    """
    # pylint: disable=unused-argument
    return value


async def _directive_executor(
    directive_func: Callable,
    directive_arguments_coercer: Callable,
    wrapped_func: Callable,
    *args,
    context_coercer: Optional[Any] = None,
    **kwargs,
) -> Any:
    """
    Wraps the execution of directives in order to handle properly the fact that
    directive arguments can be a dictionary or a callable.
    :param directive_func: callable representing the directive implementation
    :param directive_arguments_coercer: callable to use to coerce directive
    arguments
    :param context_coercer: context passed to the query execution to use on
    argument coercion process
    :param wrapped_func: the inner callable to call after the directive
    :type directive_func: Callable
    :type directive_args: Callable
    :type wrapped_func: Callable
    :type context_coercer: Optional[Any]
    :return: the computed value
    :rtype: Any
    """
    return await directive_func(
        await directive_arguments_coercer(ctx=context_coercer),
        partial(wrapped_func, context_coercer=context_coercer),
        *args,
        **kwargs,
    )


async def _directive_generator(
    directive_func: AsyncGenerator,
    directive_arguments_coercer: Callable,
    wrapped_func: Callable,
    *args,
    context_coercer: Optional[Any] = None,
    **kwargs,
):
    async for payload in directive_func(
        await directive_arguments_coercer(ctx=context_coercer),
        partial(wrapped_func, context_coercer=context_coercer),
        *args,
        **kwargs,
    ):
        yield payload


async def _resolver_executor(resolver: Callable, *args, **kwargs) -> Any:
    """
    Wraos the execution of the raw resolver in order to pop the
    `context_coercer` keyword arguments to avoid exception.
    :param resolver: callable to wrap
    :type resolver: Callable
    :return: resolved value
    :rtype: Any
    """
    kwargs.pop("context_coercer", None)
    return await resolver(*args, **kwargs)


async def subscription_generator(generator: AsyncGenerator, *args, **kwargs):
    kwargs.pop("context_coercer", None)
    async for payload in generator(*args, **kwargs):
        yield payload


def wraps_with_directives(
    directives_definition: List[Dict[str, Any]],
    directive_hooks: List[str],
    func: Optional[Callable] = None,
    is_resolver: bool = False,
    with_default: bool = False,
    is_async_generator: bool = False,
) -> Optional[Callable]:
    """
    Wraps a callable with directives.
    :param directives_definition: directives to wrap with
    :param directive_hooks: name(s) of the hook to wrap with
    :param func: callable to wrap
    :param is_resolver: determines whether or not the wrapped func is a
    resolver
    :param with_default: determines whether or not if there is no directives
    :param is_async_generator: determines whether or not the wrapped func is a
    generator
    definition we should return or not a callable
    :type directives_definition: List[Dict[str, Any]]
    :type directive_hooks: List[str]
    :type func: Optional[Callable]
    :type is_resolver: bool
    :type with_default: bool
    :type is_async_generator: bool
    :return: wrapped callable
    :rtype: Optional[Callable]
    """
    directive_wrapper = _directive_executor

    if func is None:
        if not with_default and not directives_definition:
            return None

        func = _default_directive_callable

    if is_resolver and not isinstance(func, partial):
        func = partial(_resolver_executor, func)

    if is_async_generator and not isinstance(func, partial):
        func = partial(subscription_generator, func)
        directive_wrapper = _directive_generator

    for directive in reversed(directives_definition):
        for directive_hook in directive_hooks:
            if directive_hook in directive["callables"]:
                func = partial(
                    directive_wrapper,
                    directive["callables"][directive_hook],
                    directive["arguments_coercer"],
                    func,
                )
                break
    return func
