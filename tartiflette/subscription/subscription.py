from typing import Callable, Optional

from tartiflette.schema.registry import SchemaRegistry
from tartiflette.types.exceptions.tartiflette import (
    MissingImplementation,
    NonAsyncGeneratorSubscription,
    NotSubscriptionField,
    UnknownFieldDefinition,
)
from tartiflette.utils.callables import is_valid_async_generator

__all__ = ("Subscription",)


class Subscription:
    """
    This decorator allows you to link a GraphQL Schema subscription field to a
    subscription generator.

    For example, for the following SDL:

        type Subscription {
            countdown(startAt: Int!): Int!
        }

    Use the Subscription decorator the following way:

        @Subscription("Subscription.countdown")
        async def countdown_subscription(parent, arguments, request_ctx, info):
            countdown = arguments["startAt"]
            while countdown > 0:
                yield countdown
                countdown -= 1
                await asyncio.sleep(1)
            yield 0
    """

    def __init__(
        self,
        name: str,
        schema_name: str = "default",
        arguments_coercer: Optional[Callable] = None,
        concurrently: Optional[bool] = None,
    ) -> None:
        """
        :param name: name of the subscription field
        :param schema_name: name of the schema to which link the subscription
        :param arguments_coercer: callable to use to coerce field arguments
        :param concurrently: whether list should be coerced concurrently
        :type name: str
        :type schema_name: str
        :type arguments_coercer: Optional[Callable]
        :type concurrently: Optional[bool]
        """
        self.name = name
        self._implementation = None
        self._schema_name = schema_name
        self._arguments_coercer = arguments_coercer
        self._concurrently = concurrently

    def bake(self, schema: "GraphQLSchema") -> None:
        """
        Sets the subscription generator into the schema subscription
        definition.
        :param schema: the GraphQLSchema instance linked to the subscription
        :type schema: GraphQLSchema
        """
        if not self._implementation:
            raise MissingImplementation(
                f"No implementation given for subscription < {self.name} >"
            )

        try:
            field = schema.get_field_by_name(self.name)
        except KeyError:
            raise UnknownFieldDefinition(
                f"Unknown Field Definition {self.name}"
            )

        parent_type_name = self.name.split(".")[0]
        if parent_type_name != schema.subscription_operation_name:
            raise NotSubscriptionField(
                "Field < %s > isn't a subscription field." % self.name
            )

        field.subscribe = self._implementation
        field.subscription_arguments_coercer = self._arguments_coercer
        field.subscription_concurrently = self._concurrently

    def __call__(self, implementation: Callable) -> Callable:
        """
        Registers the subscription generator into the schema.
        :param implementation: implementation of the subscription generator
        :type implementation: Callable
        :return: the implementation of the subscription generator
        :rtype: Callable
        """
        if not is_valid_async_generator(implementation):
            raise NonAsyncGeneratorSubscription(
                "The subscription < {} > given is not an awaitable "
                "generator.".format(repr(implementation))
            )

        SchemaRegistry.register_subscription(self._schema_name, self)
        self._implementation = implementation
        return implementation
