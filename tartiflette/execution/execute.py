import asyncio

from typing import Any, Dict, List


async def execute_fields_serially(
    execution_context: "ExecutionContext",
    fields: Dict[str, "ExecutableFieldNode"],
    type_condition: str,
):
    # print(
    #     ">> execute_fields_serially",
    #     {
    #         "type_condition": type_condition,
    #         "available_type_conditions": list(fields.keys()),
    #     }
    # )
    try:
        executable_fields = fields[type_condition]
    except KeyError:
        # print(f"No executable_fields for < {type_condition} >")
        return

    for response_name, field in executable_fields.items():
        await field(execution_context)


async def execute_fields(
    execution_context: "ExecutionContext",
    fields: Dict[str, "ExecutableFieldNode"],
    type_condition: str,
):
    # print(
    #     ">> execute_fields",
    #     {
    #         "type_condition": type_condition,
    #         "available_type_conditions": list(fields.keys()),
    #     }
    # )
    try:
        executable_fields = fields[type_condition]
    except KeyError:
        # print(f"No executable_fields for < {type_condition} >")
        return

    await asyncio.gather(
        *[
            field(execution_context, execution_context.context)
            for response_name, field in executable_fields.items()
        ],
        return_exceptions=False,
    )


# class Info:
#     """
#     TODO:
#     """
#
#     __slots__ = (
#         "field_name",
#         "field_nodes",
#         "return_type",
#         "parent_type",
#         "path",
#         "schema",
#         "fragments",
#         "root_value",
#         "operation",
#         "variable_values",
#         "extra",
#     )
#
#     def __init__(
#         self,
#         field_name: str,
#         field_nodes: List["FieldNode"],
#         return_type,
#         parent_type,
#         path,
#         schema: "GraphQLSchema",
#         fragments,
#         root_value: Any,
#         operation: "OperationDefinitionNode",
#         variable_values: Dict[str, Any],
#     ):
#         self.field_name = field_name
#         self.field_nodes = field_nodes
#         self.return_type = return_type
#         self.parent_type = parent_type
#         self.path = path
#         self.schema = schema
#         self.fragments = fragments
#         self.root_value = root_value
#         self.operation = operation
#         self.variable_values = variable_values
#         self.extra = {}  # TODO: spec it if useful
