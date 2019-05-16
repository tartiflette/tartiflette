from typing import Dict, List, Union

from tartiflette.types.exceptions.tartiflette import TartifletteError
from tartiflette.types.helpers.reduce_type import reduce_type


def find_field_by_name(
    field_name: str, schema: "GraphQLSchema"
) -> Union[None, "GraphQLField"]:
    """
    Find a field in the schema using it's FQFN (Type.field_name).

    This absorbs schema method errors and return None if the
    field isn't found instead of raising errors.

    :param field_name: the Fully Qualified Field Name to search.
    :type field_name: str
    :param schema: The schema instance to look through.
    :type schema: GraphQLSchema

    :return: A GraphQLField or None if field is not found
    :rtype: Union[None, GraphQLField]
    """

    try:
        return schema.get_field_by_name(field_name)
    except (AttributeError, KeyError, TartifletteError):
        return None


def find_field(
    parent_type_name: str, field_name: str, schema: "GraphQLSchema"
) -> Union[None, "GraphQLField"]:
    """
    Find a field in the schema using it's Parent type name and the field name.

    This absorbs schema method errors and return None if the
    field isn't found instead of raising errors.

    :param parent_type_name: The Parent type name of the field to search for.
    :type parent_type_name: str
    :param field_name: the Field Name to search for.
    :type field_name: str
    :param schema: The schema instance to look through.
    :type schema: GraphQLSchema

    :return: A GraphQLField or None if field is not found
    :rtype: Union[None, GraphQLField]
    """
    return find_field_by_name(f"{parent_type_name}.{field_name}", schema)


def find_field_reduced_type(
    parent_type_name: str, field_name: str, schema: "GraphQLSchema"
) -> Union[None, "GraphQLType"]:
    """
    Find the reduced type (completly unwrapped type) Object of a field using
    it's parent type name and the field name.

    :param parent_type_name: The Parent type name of the field to search for.
    :type parent_type_name: str
    :param field_name: the Field Name to search for.
    :type field_name: str
    :param schema: The schema instance to look through.
    :type schema: GraphQLSchema

    :return: A GraphQLType or None if field is not found.
    :rtype: Union[None, "GraphQLType"]
    """

    schema_field = find_field(parent_type_name, field_name, schema)

    if not schema_field:
        return None

    return schema.type_definitions[reduce_type(schema_field.gql_type)]


def get_schema_field_type_name(
    parent_type_name: str, field_name: str, schema: "GraphQLSchema"
) -> Union[None, str]:
    """
    Find the reduced type (completly unwrapped type) name of a field using
    it's parent type name and the field name.

    :param parent_type_name: The Parent type name of the field to search for.
    :type parent_type_name: str
    :param field_name: the Field Name to search for.
    :type field_name: str
    :param schema: The schema instance to look through.
    :type schema: GraphQLSchema

    :return: A string or None if field is not found.
    :rtype: Union[None, str]
    """

    try:
        return reduce_type(
            find_field(parent_type_name, field_name, schema).gql_type
        )
    except (AttributeError, KeyError):
        return None


def find_nodes_by_name(nodes: List["Node"], name: str) -> List["Node"]:
    """
    Retrive a list of nodes named `name` inside a given `nodes` list

    :param nodes: The node list to look through.
    :type nodes: List["Node"]
    :param name: The name to search for.
    :type name: str

    :return: A list of Node object named `name`.
    :rtype: List["Node"]
    """
    return [x for x in nodes if x.name and x.name.value == name]


def _find_var_usage_in_spread(spreads, per_fragment, used_vars=None):
    if not used_vars:
        used_vars = []

    for spread in spreads:
        used_vars = _find_var_usage_in_spread(
            per_fragment.get(spread.name.value, {}).get("spreads", []),
            per_fragment,
            used_vars,
        )
        used_vars.extend(
            per_fragment.get(spread.name.value, {}).get("used_vars", [])
        )

    return used_vars


def get_used_vars(
    operation: "OperationDefinitionNode",
    per_operation: Dict[
        str,
        Dict[str, Union[List["VaribalbeNode"], List["FragmentSpreadNode"]]],
    ],
    per_fragment: Dict[
        str,
        Dict[str, Union[List["VaribalbeNode"], List["FragmentSpreadNode"]]],
    ],
) -> List["VariableNode"]:
    """
    Retrive which varibles are use in the context of an operation.

    Per_operation : { "operation_name" : { "used_vars": [VariableNode], "spreads": [FragmentSpreadNode] }}
    Per_fragment : { "fragment_name": { "used_vars": [VariableNode], "spreads": [FragmentSpreadNode] }}

    This method will walk these two dicts and collect the the variable nodes that are used in a given "operation_name"

    :param operation: The operation to look through
    :type operation: OperationDefinitionNode
    :param per_operation: A dict with var and spread used sorted by operation name
    :type per_operation: Dict[str, Dict[str, Union[List["VaribalbeNode"], List["FragmentSpreadNode"]]]]
    :param per_fragment: A dict with var and spread used sorted by fragment name
    :type per_fragment: Dict[str, Dict[str, Union[List["VaribalbeNode"], List["FragmentSpreadNode"]]]]

    :return: a list of Variable Node used in a operation context.
    :rtype: List["VariableNode"]
    """

    operation_key = operation.name.value if operation.name else "None"

    used_vars = per_operation.get(operation_key, {}).get("used_vars", [])

    used_vars.extend(
        _find_var_usage_in_spread(
            per_operation.get(operation_key, {}).get("spreads", []),
            per_fragment,
        )
    )
    return used_vars


def get_defined_vars(
    operation: "OperationDefinitionNode"
) -> List["VariableNode"]:
    """
    Retrieve a list of VariableNode defined inside the variableDefinitionNode list of an OperationDefinitionNode

    :param operation: the operation definition node to look through
    :type operation: "OperationDefinitionNode"

    :return: The List of VariableNode that was buried in the list of VariableDefinitionNode of the given OperationDefinitionNode
    :rtype: List["VariableNode"]
    """

    return [x.variable for x in operation.variable_definitions]
