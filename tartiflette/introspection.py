from tartiflette.types.argument import GraphQLArgument

from tartiflette.types.field import GraphQLField
from tartiflette.types.non_null import GraphQLNonNull


async def __schema_resolver(_pr, _arg, _rctx, info):
    info.execution_ctx.is_introspection = True
    return info.schema


async def __type_resolver(_pr, args, _rctx, info):
    info.execution_ctx.is_introspection = True
    return info.schema.find_type(args["name"])


async def __typename_resolver(_pr, _arg, _rctx, _info):
    info.execution_ctx.is_introspection = True
    return "TODO TYPENAME"


SCHEMA_ROOT_FIELD_DEFINITION = GraphQLField(
    name="__schema",
    gql_type=GraphQLNonNull("__Schema"),
    description="Access the current type schema of this server.",
    arguments={},
    resolver=__schema_resolver,
)

TYPE_ROOT_FIELD_DEFINITION = GraphQLField(
    name="__type",
    gql_type="__Type",
    description="Request the type information of a single type.",
    arguments={
        "name": GraphQLArgument(name="name", gql_type=GraphQLNonNull("String"))
    },
    resolver=__type_resolver,
)

TYPENAME_ROOT_FIELD_DEFINITION = GraphQLField(
    name="__typename",
    gql_type=GraphQLNonNull("String"),
    description="The name of the current Object type at runtime.",
    arguments={},
    resolver=__typename_resolver,
)
