from typing import Any, Dict, Optional, Union

__all__ = ("default_field_resolver", "default_type_resolver")


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
