from typing import Any, Callable, Dict, Optional, Union

from tartiflette import Directive
from tartiflette.types.exceptions.tartiflette import SkipCollection


def include_selection(
    directive_args: Dict[str, Any],
    selection: Union["FragmentSpreadNode", "FieldNode", "InlineFragmentNode"],
    ctx: Optional[Any],
) -> Union["FragmentSpreadNode", "FieldNode", "InlineFragmentNode"]:
    """
    Determines whether or not the selection should be collected or skipped.
    :param directive_args: arguments passed to the directive
    :param selection: the selection node to collect or skip
    :param ctx: context passed to the query execution
    :type directive_args: Dict[str, Any]
    :type selection: Union[FragmentSpreadNode, FieldNode, InlineFragmentNode]
    :type ctx: Optional[Any]
    :return: the selection node to collect
    :rtype: Union[FragmentSpreadNode, FieldNode, InlineFragmentNode]
    """
    # pylint: disable=unused-argument
    if not directive_args["if"]:
        raise SkipCollection()
    return selection


class IncludeDirective:
    """
    Built-in directive which allows for conditional inclusion of fields,
    fragment spreads, and inline fragments at execution time.
    """

    async def on_field_collection(
        self,
        directive_args: Dict[str, Any],
        next_directive: Callable,
        field_node: "FieldNode",
        ctx: Optional[Any],
    ) -> "FieldNode":
        """
        Determines whether or not the field should be collected or skipped at
        execution time.
        :param directive_args: arguments passed to the directive
        :param next_directive: next directive to call
        :param field_node: the field to collect or skip
        :param ctx: context passed to the query execution
        :type directive_args: Dict[str, Any]
        :type next_directive: Callable
        :type field_node: FieldNode
        :type ctx: Optional[Any]
        :return: the field node to collect
        :rtype: FieldNode
        """
        return include_selection(
            directive_args, await next_directive(field_node, ctx), ctx
        )

    async def on_fragment_spread_collection(
        self,
        directive_args: Dict[str, Any],
        next_directive: Callable,
        fragment_spread_node: "FragmentSpreadNode",
        ctx: Optional[Any],
    ) -> "FragmentSpreadNode":
        """
        Determines whether or not the fragment spread should be collected or
        skipped at execution time.
        :param directive_args: arguments passed to the directive
        :param next_directive: next directive to call
        :param fragment_spread_node: the fragment spread to collect or skip
        :param ctx: context passed to the query execution
        :type directive_args: Dict[str, Any]
        :type next_directive: Callable
        :type fragment_spread_node: FragmentSpreadNode
        :type ctx: Optional[Any]
        :return: the fragment spread node to collect
        :rtype: FragmentSpreadNode
        """
        return include_selection(
            directive_args,
            await next_directive(fragment_spread_node, ctx),
            ctx,
        )

    async def on_inline_fragment_collection(
        self,
        directive_args: Dict[str, Any],
        next_directive: Callable,
        inline_fragment_node: "InlineFragmentNode",
        ctx: Optional[Any],
    ) -> "InlineFragmentNode":
        """
        Determines whether or not the inline fragment should be collected or
        skipped at execution time.
        :param directive_args: arguments passed to the directive
        :param next_directive: next directive to call
        :param inline_fragment_node: the inline fragment to collect or skip
        :param ctx: context passed to the query execution
        :type directive_args: Dict[str, Any]
        :type next_directive: Callable
        :type inline_fragment_node: InlineFragmentNode
        :type ctx: Optional[Any]
        :return: the inline fragment node to collect
        :rtype: InlineFragmentNode
        """
        return include_selection(
            directive_args,
            await next_directive(inline_fragment_node, ctx),
            ctx,
        )


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
    Directive("include", schema_name=schema_name)(IncludeDirective())
    return '''
    """Directs the executor to include this field or fragment only when the `if` argument is true."""
    directive @include(
      """Included when true."""
      if: Boolean!
    ) on FIELD | FRAGMENT_SPREAD | INLINE_FRAGMENT
    '''
