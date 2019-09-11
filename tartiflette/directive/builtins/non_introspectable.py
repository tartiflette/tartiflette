from typing import Any, Callable, Dict, Optional

from tartiflette import Directive


class NonIntrospectableDirective:
    """
    Built-in directive to skip the introspection of the portions of a GraphQL
    service's schema.
    """

    async def on_introspection(
        self,
        directive_args: Dict[str, Any],
        next_directive: Callable,
        introspected_element: Any,
        ctx: Optional[Any],
        info: "ResolveInfo",
    ) -> None:
        """
        Skips the treatment and returns None instead of the introspected
        element.
        :param directive_args: arguments passed to the directive
        :param next_directive: next directive to call
        :param introspected_element: current introspected element
        :param ctx: context passed to the query execution
        :param info: information related to the execution
        :type directive_args: Dict[str, Any]
        :type next_directive: Callable
        :type introspected_element: Any
        :type ctx: Optional[Any]
        :type info: ResolveInfo
        :return: the deprecated introspected element
        :rtype: Any
        """
        # pylint: disable=unused-argument
        return None


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
    Directive("nonIntrospectable", schema_name=schema_name)(
        NonIntrospectableDirective()
    )
    return '''
    """Directs the executor to hide the element on introspection queries."""
    directive @nonIntrospectable on FIELD_DEFINITION
    '''
