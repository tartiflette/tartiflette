from typing import Any, Callable, Dict, Optional

from tartiflette import Directive


class DeprecatedDirective:
    """
    Built-in directive to indicate deprecated portions of a GraphQL service’s
    schema, such as deprecated fields on a type or deprecated enum values.
    """

    async def on_post_bake(
        self,
        directive_args: Dict[str, Any],
        next_directive: Callable,
        element: "GraphQLType",
    ) -> "GraphQLType":
        """
        Marks the baked element as deprecated.
        :param directive_args: arguments passed to the directive
        :param next_directive: next directive to call
        :param element: current baked element
        :type directive_args: Dict[str, Any]
        :type next_directive: Callable
        :type element: Any
        :return: the deprecated baked element
        :rtype: Any
        """
        element = await next_directive(element)
        setattr(element, "isDeprecated", True)
        setattr(element, "deprecationReason", directive_args["reason"])
        return element


def bake(schema_name: str, config: Optional[Dict[str, Any]] = None) -> str:
    """
    Links the directive to the appropriate schema and returns the SDL related
    to the directive.
    :param schema_name: schema name to link with
    :param config: configuration of the directive
    :type schema_name: str
    :type config: Optional[Dict[str, Any]]
    :return: the SDL related to the directive
    :rtype: str
    """
    # pylint: disable=unused-argument
    Directive("deprecated", schema_name=schema_name)(DeprecatedDirective())
    return '''
    """Marks an element of a GraphQL schema as no longer supported."""
    directive @deprecated(
        """Explains why this element was deprecated, usually also including a suggestion for how to access supported similar data. Formatted using the Markdown syntax (as specified by [CommonMark](https://commonmark.org/)."""
        reason: String = "No longer supported"
    ) on FIELD_DEFINITION | ENUM_VALUE
    '''
