from functools import partial
from typing import Any, Dict, Optional

from tartiflette.types.argument import GraphQLArgument
from tartiflette.types.field import GraphQLField
from tartiflette.types.non_null import GraphQLNonNull

__all__ = (
    "SCHEMA_ROOT_FIELD_DEFINITION",
    "prepare_type_root_field",
    "TYPENAME_ROOT_FIELD_DEFINITION",
)


async def __schema_resolver(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Optional[Any],
    info: "ResolveInfo",
) -> "GraphQLSchema":
    """
    Callable to use to resolve the `__schema` field.
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
    if info.schema.is_introspectable:
        info.is_introspection = True
        return info.schema
    return None


SCHEMA_ROOT_FIELD_DEFINITION = partial(
    GraphQLField,
    name="__schema",
    description="Access the current type schema of this server.",
    arguments=None,
    resolver=__schema_resolver,
)


async def __type_resolver(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Optional[Any],
    info: "ResolveInfo",
) -> "GraphQLType":
    """
    Callable to use to resolve the `__type` field.
    :param parent: default root value or field parent value
    :param args: computed arguments related to the resolved field
    :param ctx: context passed to the query execution
    :param info: information related to the execution and the resolved field
    :type parent: Optional[Any]
    :type args: Dict[str, Any]
    :type ctx: Optional[Any]
    :type info: ResolveInfo
    :return: the computed field value
    :rtype: GraphQLType
    """
    # pylint: disable=unused-argument
    if not info.schema.is_introspectable:
        return None

    info.is_introspection = True
    try:
        return info.schema.find_type(args["name"])
    except KeyError:
        pass
    return None


def prepare_type_root_field(schema: "GraphQLSchema") -> "GraphQLField":
    """
    Factory to generate a `__type` field.
    :param schema: the GraphQLSchema instance linked to the engine
    :type schema: GraphQLSchema
    :return: the `__type` field
    :rtype: GraphQLField
    """
    return GraphQLField(
        name="__type",
        description="Request the type information of a single type.",
        arguments={
            "name": GraphQLArgument(
                name="name", gql_type=GraphQLNonNull("String", schema=schema)
            )
        },
        gql_type="__Type",
        resolver=__type_resolver,
    )


async def __typename_resolver(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Optional[Any],
    info: "ResolveInfo",
) -> "GraphQLType":
    """
    Callable to use to resolve the `__typename` field.
    :param parent: default root value or field parent value
    :param args: computed arguments related to the resolved field
    :param ctx: context passed to the query execution
    :param info: information related to the execution and the resolved field
    :type parent: Optional[Any]
    :type args: Dict[str, Any]
    :type ctx: Optional[Any]
    :type info: ResolveInfo
    :return: the computed field value
    :rtype: GraphQLType
    """
    # pylint: disable=unused-argument
    if not info.schema.is_introspectable:
        return None
    return info.parent_type.name


TYPENAME_ROOT_FIELD_DEFINITION = partial(
    GraphQLField,
    name="__typename",
    description="The name of the current Object type at runtime.",
    arguments=None,
    resolver=__typename_resolver,
)
