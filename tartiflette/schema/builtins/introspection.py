import os

from typing import Any, Dict, List, Optional

from tartiflette import Resolver
from tartiflette.types.enum import GraphQLEnumType
from tartiflette.types.interface import GraphQLInterfaceType
from tartiflette.types.object import GraphQLObjectType


async def resolve_type_fields(
    parent: "GraphQLType",
    args: Dict[str, Any],
    ctx: Optional[Any],
    info: "ResolveInfo",
) -> Optional[List["GraphQLField"]]:
    """
    Returns the list of fields implemented by the parent type.
    :param parent: parent field resolved value
    :param args: computed arguments related to the resolved field
    :param ctx: context passed to the query execution
    :param info: information related to the execution and the resolved field
    :type parent: GraphQLType
    :type args: Dict[str, Any]
    :type ctx: Optional[Any]
    :type info: ResolveInfo
    :return: a list of GraphQLField
    :rtype: Optional[List[GraphQLField]]
    """
    # pylint: disable=unused-argument
    if not isinstance(parent, (GraphQLObjectType, GraphQLInterfaceType)):
        return None

    if args.get("includeDeprecated") is not False:
        return parent.fields

    return [field for field in parent.fields if not field.isDeprecated]


async def resolve_type_enum_values(
    parent: "GraphQLType",
    args: Dict[str, Any],
    ctx: Optional[Any],
    info: "ResolveInfo",
) -> Optional[List["GraphQLEnumValue"]]:
    """
    Returns the list of enum values of an enum type.
    :param parent: parent field resolved value
    :param args: computed arguments related to the resolved field
    :param ctx: context passed to the query execution
    :param info: information related to the execution and the resolved field
    :type parent: GraphQLType
    :type args: Dict[str, Any]
    :type ctx: Optional[Any]
    :type info: ResolveInfo
    :return: the list of enum values of an enum type
    :rtype: Optional[List[GraphQLEnumValue]]
    """
    # pylint: disable=unused-argument
    if not isinstance(parent, GraphQLEnumType):
        return None

    if args.get("includeDeprecated") is not False:
        return parent.enumValues

    return [
        enum_value
        for enum_value in parent.enumValues
        if not enum_value.isDeprecated
    ]


def bake(schema_name: str, config: Optional[Dict[str, Any]] = None) -> str:
    """
    Adds the introspection SDL.
    :param schema_name: schema name to link with
    :param config: configuration of the introspection
    :type schema_name: str
    :type config: Optional[Dict[str, Any]]
    :return: the SDL related to the introspection
    :rtype: str
    """
    # pylint: disable=unused-argument
    Resolver("__Type.enumValues", schema_name=schema_name)(
        resolve_type_enum_values
    )
    Resolver("__Type.fields", schema_name=schema_name)(resolve_type_fields)
    with open(
        os.path.join(os.path.dirname(__file__), "introspection.sdl"),
        encoding="UTF-8",
    ) as file:
        return file.read()
