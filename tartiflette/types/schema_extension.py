from typing import Any

from tartiflette.types.type import GraphQLExtension, GraphQLType


class GraphQLSchemaExtension(GraphQLType, GraphQLExtension):
    def __init__(self, directives, operations):
        self.directives = directives
        self.operations = operations or []

    # TODO Don't forget schema directives here when implementing them
    def bake(self, schema):
        schema.add_schema_directives(self.directives)
        for okind, otype in self.operations.items():
            setattr(schema, f"{okind}_operation_name", otype)

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if `other` instance is identical to `self`.
        :param other: object instance to compare to `self`
        :type other: Any
        :return: whether or not `other` is identical to `self`
        :rtype: bool
        """
        return self is other or (
            isinstance(other, GraphQLSchemaExtension)
            and other.directives == self.directives
            and other.operations == self.operations
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a GraphQLType instance.
        :return: the representation of a GraphQLType instance
        :rtype: str
        """
        return (
            f"GraphQLSchemaExtension("
            f"operations={repr(self.operations)}, "
            f"directives={repr(self.directives)})"
        )
