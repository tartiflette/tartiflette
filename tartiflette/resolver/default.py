import asyncio

from typing import Any, Coroutine, Dict, List, Optional, Union

__all__ = (
    "default_field_resolver",
    "default_type_resolver",
    "gather_arguments_coercer",
    "sync_arguments_coercer",
)


async def default_field_resolver(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Optional[Any],
    info: "ResolveInfo",
) -> Any:
    """
    Default callable to use as resolver for field which doesn't implement a
    custom one.
    :param parent: default root value or field parent value
    :param args: computed arguments related to the resolved field
    :param ctx: context passed to the query execution
    :param info: information related to the execution and the resolved field
    :type parent: Optional[Any]
    :type args: Dict[str, Any]
    :type ctx: Optional[Any]
    :type info: ResolveInfo
    :return: the computed field value
    :rtype: Any
    """
    # pylint: disable=unused-argument
    try:
        return getattr(parent, info.field_name)
    except AttributeError:
        pass

    try:
        return parent[info.field_name]
    except (KeyError, TypeError):
        pass
    return None


def default_type_resolver(
    result: Any,
    ctx: Optional[Any],
    info: "ResolverInfo",
    abstract_type: Union["GraphQLInterfaceType", "GraphQLUnionType"],
) -> str:
    """
    Default callable to use to resolve the type of an abstract type.
    :param result: resolved field value
    :param ctx: context passed to the query execution
    :param info: information related to the execution and the resolved field
    :param abstract_type: the GraphQLAbstractType instance to resolve
    :type result: Any
    :type ctx: Optional[Any]
    :type info: ResolverInfo
    :type abstract_type: Union[GraphQLInterfaceType, GraphQLUnionType]
    :return: the type name of the resolved field value
    :rtype: str
    """
    # pylint: disable=unused-argument
    try:
        return result["_typename"]
    except (KeyError, TypeError):
        pass

    try:
        return result._typename  # pylint: disable=protected-access
    except AttributeError:
        pass

    return result.__class__.__name__


async def gather_arguments_coercer(
    *coroutines: List[Coroutine],
) -> List[Union[Any, Exception]]:
    """
    Coerce arguments asynchronously with asyncio.gather function.

    :param coroutines: list of coroutine to await
    :type coroutines: List[Coroutine]
    :return: the result of coroutines
    :rtype: List[Union[Any, Exception]]
    """
    return await asyncio.gather(*coroutines, return_exceptions=True)


async def sync_arguments_coercer(
    *coroutines: List[Coroutine],
) -> List[Union[Any, Exception]]:
    """
    Coerce arguments synchronously.

    :param coroutines: list of coroutine to await
    :type coroutines: List[Coroutine]
    :return: the result of coroutines
    :rtype: List[Union[Any, Exception]]
    """
    results = []
    for coroutine in coroutines:
        try:
            result = await coroutine
        except Exception as e:  # pylint: disable=broad-except
            result = e
        results.append(result)
    return results
