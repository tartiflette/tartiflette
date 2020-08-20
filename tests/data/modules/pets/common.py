from typing import Any, Callable, Dict, Optional, Union

from tartiflette import Directive, Resolver, Scalar
from tartiflette.scalar.builtins.boolean import ScalarBoolean
from tartiflette.scalar.builtins.float import ScalarFloat
from tartiflette.scalar.builtins.int import ScalarInt
from tartiflette.scalar.builtins.string import ScalarString


class BooleanScalar(ScalarBoolean):
    pass


class FloatScalar(ScalarFloat):
    pass


class IntScalar(ScalarInt):
    pass


class StringScalar(ScalarString):
    pass


class DebugDirective:
    async def on_argument_execution(
        self,
        directive_args: Dict[str, Any],
        next_directive: Callable,
        parent_node: Union["FieldNode", "DirectiveNode"],
        argument_definition_node: "InputValueDefinitionNode",
        argument_node: Optional["ArgumentNode"],
        value: Any,
        ctx: Optional[Any],
    ):
        return await next_directive(
            parent_node, argument_definition_node, argument_node, value, ctx
        )

    async def on_post_input_coercion(
        self,
        directive_args: Dict[str, Any],
        next_directive: Callable,
        parent_node,
        value: Any,
        ctx: Optional[Any],
    ):
        return await next_directive(parent_node, value, ctx)


class LowercaseDirective:
    async def on_argument_execution(
        self,
        directive_args: Dict[str, Any],
        next_directive: Callable,
        parent_node: Union["FieldNode", "DirectiveNode"],
        argument_definition_node: "InputValueDefinitionNode",
        argument_node: Optional["ArgumentNode"],
        value: Any,
        ctx: Optional[Any],
    ):
        result = await next_directive(
            parent_node, argument_definition_node, argument_node, value, ctx
        )
        if isinstance(result, str):
            return result.lower()
        if isinstance(result, list):
            return [
                value.lower() if isinstance(value, str) else value
                for value in result
            ]
        return result

    async def on_post_input_coercion(
        self,
        directive_args: Dict[str, Any],
        next_directive: Callable,
        parent_node,
        value: Any,
        ctx: Optional[Any],
    ):
        result = await next_directive(parent_node, value, ctx)
        if isinstance(result, str):
            return result.lower()
        if isinstance(result, list):
            return [
                value.lower() if isinstance(value, str) else value
                for value in result
            ]
        return result


class IncrementDirective:
    async def on_argument_execution(
        self,
        directive_args: Dict[str, Any],
        next_directive: Callable,
        parent_node: Union["FieldNode", "DirectiveNode"],
        argument_definition_node: "InputValueDefinitionNode",
        argument_node: Optional["ArgumentNode"],
        value: Any,
        ctx: Optional[Any],
    ):
        result = await next_directive(
            parent_node, argument_definition_node, argument_node, value, ctx
        )
        if isinstance(result, (int, float)):
            return result + directive_args["step"]
        if isinstance(result, list):
            return [
                value + directive_args["step"]
                if isinstance(value, (int, float))
                else value
                for value in result
            ]
        return result

    async def on_post_input_coercion(
        self,
        directive_args: Dict[str, Any],
        next_directive: Callable,
        parent_node,
        value: Any,
        ctx: Optional[Any],
    ):
        result = await next_directive(parent_node, value, ctx)
        if isinstance(result, (int, float)):
            return result + directive_args["step"]
        if isinstance(result, list):
            return [
                value + directive_args["step"]
                if isinstance(value, (int, float))
                else value
                for value in result
            ]
        return result


class ConcatenateDirective:
    async def on_argument_execution(
        self,
        directive_args: Dict[str, Any],
        next_directive: Callable,
        parent_node: Union["FieldNode", "DirectiveNode"],
        argument_definition_node: "InputValueDefinitionNode",
        argument_node: Optional["ArgumentNode"],
        value: Any,
        ctx: Optional[Any],
    ):
        result = await next_directive(
            parent_node, argument_definition_node, argument_node, value, ctx
        )
        return (
            result + directive_args["with"]
            if isinstance(result, str)
            else result
        )

    async def on_post_input_coercion(
        self,
        directive_args: Dict[str, Any],
        next_directive: Callable,
        parent_node,
        value: Any,
        ctx: Optional[Any],
    ):
        result = await next_directive(parent_node, value, ctx)
        return (
            result + directive_args["with"]
            if isinstance(result, str)
            else result
        )


class MapToValueDirective:
    async def on_argument_execution(
        self,
        directive_args: Dict[str, Any],
        next_directive: Callable,
        parent_node: Union["FieldNode", "DirectiveNode"],
        argument_definition_node: "InputValueDefinitionNode",
        argument_node: Optional["ArgumentNode"],
        value: Any,
        ctx: Optional[Any],
    ):
        await next_directive(
            parent_node, argument_definition_node, argument_node, value, ctx
        )
        return directive_args["newValue"]

    async def on_post_input_coercion(
        self,
        directive_args: Dict[str, Any],
        next_directive: Callable,
        parent_node,
        value: Any,
        ctx: Optional[Any],
    ):
        await next_directive(parent_node, value, ctx)
        return directive_args["newValue"]


async def resolve_unwrapped_field(parent, args, ctx, info):
    if "param" in args:
        return f"SUCCESS-{args['param']}"
    return "SUCCESS"


async def resolve_list_field(parent, args, ctx, info):
    if "param" in args:
        return "SUCCESS-[{}]".format(
            str(args["param"])
            if not isinstance(args["param"], list)
            else "-".join([str(item) for item in args["param"]])
        )
    return "SUCCESS"


async def resolve_input_object_field(parent, args, ctx, info):
    if "param" in args:
        if args["param"] is None:
            return "SUCCESS-None"
        if isinstance(args["param"], dict):
            if not args["param"]:
                return "SUCCESS-{}"
            return "SUCCESS-{}".format(
                "-".join(
                    [
                        "[{}:{}]".format(
                            str(arg_name),
                            str(
                                arg_values
                                if not isinstance(arg_values, list)
                                else "-".join([str(arg) for arg in arg_values])
                            ),
                        )
                        for arg_name, arg_values in args["param"].items()
                    ]
                )
            )
    return "SUCCESS"


def bake(schema_name, config):
    Scalar("DefaultRawInt", schema_name=schema_name)(IntScalar())
    Scalar("DefaultRawString", schema_name=schema_name)(StringScalar())
    Scalar("Boolean", schema_name=schema_name)(BooleanScalar())
    Scalar("Float", schema_name=schema_name)(FloatScalar())
    Scalar("Int", schema_name=schema_name)(IntScalar())
    Scalar("String", schema_name=schema_name)(StringScalar())
    Directive("debug", schema_name=schema_name)(DebugDirective())
    Directive("lowercase", schema_name=schema_name)(LowercaseDirective())
    Directive("increment", schema_name=schema_name)(IncrementDirective())
    Directive("concatenate", schema_name=schema_name)(ConcatenateDirective())
    Directive("mapToValue", schema_name=schema_name)(MapToValueDirective())
    Resolver("Query.booleanField", schema_name=schema_name)(
        resolve_unwrapped_field
    )
    Resolver("Query.enumField", schema_name=schema_name)(
        resolve_unwrapped_field
    )
    Resolver("Query.floatField", schema_name=schema_name)(
        resolve_unwrapped_field
    )
    Resolver("Query.intField", schema_name=schema_name)(
        resolve_unwrapped_field
    )
    Resolver("Query.stringField", schema_name=schema_name)(
        resolve_unwrapped_field
    )
    Resolver("Query.booleanWithDefaultField", schema_name=schema_name)(
        resolve_unwrapped_field
    )
    Resolver("Query.enumWithDefaultField", schema_name=schema_name)(
        resolve_unwrapped_field
    )
    Resolver("Query.floatWithDefaultField", schema_name=schema_name)(
        resolve_unwrapped_field
    )
    Resolver("Query.intWithDefaultField", schema_name=schema_name)(
        resolve_unwrapped_field
    )
    Resolver("Query.stringWithDefaultField", schema_name=schema_name)(
        resolve_unwrapped_field
    )
    Resolver("Query.nonNullBooleanField", schema_name=schema_name)(
        resolve_unwrapped_field
    )
    Resolver("Query.nonNullEnumField", schema_name=schema_name)(
        resolve_unwrapped_field
    )
    Resolver("Query.nonNullFloatField", schema_name=schema_name)(
        resolve_unwrapped_field
    )
    Resolver("Query.nonNullIntField", schema_name=schema_name)(
        resolve_unwrapped_field
    )
    Resolver("Query.nonNullStringField", schema_name=schema_name)(
        resolve_unwrapped_field
    )
    Resolver("Query.nonNullBooleanWithDefaultField", schema_name=schema_name)(
        resolve_unwrapped_field
    )
    Resolver("Query.nonNullEnumWithDefaultField", schema_name=schema_name)(
        resolve_unwrapped_field
    )
    Resolver("Query.nonNullFloatWithDefaultField", schema_name=schema_name)(
        resolve_unwrapped_field
    )
    Resolver("Query.nonNullIntWithDefaultField", schema_name=schema_name)(
        resolve_unwrapped_field
    )
    Resolver("Query.nonNullStringWithDefaultField", schema_name=schema_name)(
        resolve_unwrapped_field
    )
    Resolver("Query.listBooleanField", schema_name=schema_name)(
        resolve_list_field
    )
    Resolver("Query.listEnumField", schema_name=schema_name)(
        resolve_list_field
    )
    Resolver("Query.listFloatField", schema_name=schema_name)(
        resolve_list_field
    )
    Resolver("Query.listIntField", schema_name=schema_name)(resolve_list_field)
    Resolver("Query.listStringField", schema_name=schema_name)(
        resolve_list_field
    )
    Resolver("Query.listWithDefaultBooleanField", schema_name=schema_name)(
        resolve_list_field
    )
    Resolver("Query.listWithDefaultEnumField", schema_name=schema_name)(
        resolve_list_field
    )
    Resolver("Query.listWithDefaultFloatField", schema_name=schema_name)(
        resolve_list_field
    )
    Resolver("Query.listWithDefaultIntField", schema_name=schema_name)(
        resolve_list_field
    )
    Resolver("Query.listWithDefaultStringField", schema_name=schema_name)(
        resolve_list_field
    )
    Resolver("Query.nonNullListBooleanField", schema_name=schema_name)(
        resolve_list_field
    )
    Resolver("Query.nonNullListEnumField", schema_name=schema_name)(
        resolve_list_field
    )
    Resolver("Query.nonNullListFloatField", schema_name=schema_name)(
        resolve_list_field
    )
    Resolver("Query.nonNullListIntField", schema_name=schema_name)(
        resolve_list_field
    )
    Resolver("Query.nonNullListStringField", schema_name=schema_name)(
        resolve_list_field
    )
    Resolver(
        "Query.nonNullListWithDefaultBooleanField", schema_name=schema_name
    )(resolve_list_field)
    Resolver("Query.nonNullListWithDefaultEnumField", schema_name=schema_name)(
        resolve_list_field
    )
    Resolver(
        "Query.nonNullListWithDefaultFloatField", schema_name=schema_name
    )(resolve_list_field)
    Resolver("Query.nonNullListWithDefaultIntField", schema_name=schema_name)(
        resolve_list_field
    )
    Resolver(
        "Query.nonNullListWithDefaultStringField", schema_name=schema_name
    )(resolve_list_field)
    Resolver("Query.listNonNullBooleanField", schema_name=schema_name)(
        resolve_list_field
    )
    Resolver("Query.listNonNullEnumField", schema_name=schema_name)(
        resolve_list_field
    )
    Resolver("Query.listNonNullFloatField", schema_name=schema_name)(
        resolve_list_field
    )
    Resolver("Query.listNonNullIntField", schema_name=schema_name)(
        resolve_list_field
    )
    Resolver("Query.listNonNullStringField", schema_name=schema_name)(
        resolve_list_field
    )
    Resolver(
        "Query.listWithDefaultNonNullBooleanField", schema_name=schema_name
    )(resolve_list_field)
    Resolver("Query.listWithDefaultNonNullEnumField", schema_name=schema_name)(
        resolve_list_field
    )
    Resolver(
        "Query.listWithDefaultNonNullFloatField", schema_name=schema_name
    )(resolve_list_field)
    Resolver("Query.listWithDefaultNonNullIntField", schema_name=schema_name)(
        resolve_list_field
    )
    Resolver(
        "Query.listWithDefaultNonNullStringField", schema_name=schema_name
    )(resolve_list_field)
    Resolver("Query.inputObjectField", schema_name=schema_name)(
        resolve_input_object_field
    )
    Resolver("Query.inputObjectWithDefaultField", schema_name=schema_name)(
        resolve_input_object_field
    )
    Resolver("Query.nonNullInputObjectField", schema_name=schema_name)(
        resolve_input_object_field
    )
    Resolver(
        "Query.nonNullInputObjectWithDefaultField", schema_name=schema_name
    )(resolve_input_object_field)
    Resolver("Query.withDefaultInputObjectField", schema_name=schema_name)(
        resolve_input_object_field
    )
    Resolver(
        "Query.withDefaultInputObjectWithDefaultField", schema_name=schema_name
    )(resolve_input_object_field)
    Resolver(
        "Query.nonNullWithDefaultInputObjectField", schema_name=schema_name
    )(resolve_input_object_field)
    Resolver(
        "Query.nonNullWithDefaultInputObjectWithDefaultField",
        schema_name=schema_name,
    )(resolve_input_object_field)
    Resolver("Query.wrapperNonNullInputObjectField", schema_name=schema_name)(
        resolve_input_object_field
    )
    Resolver(
        "Query.wrapperNonNullInputObjectWithDefaultField",
        schema_name=schema_name,
    )(resolve_input_object_field)
    Resolver(
        "Query.nonNullWrapperNonNullInputObjectField", schema_name=schema_name
    )(resolve_input_object_field)
    Resolver(
        "Query.nonNullWrapperNonNullInputObjectWithDefaultField",
        schema_name=schema_name,
    )(resolve_input_object_field)
    Resolver(
        "Query.wrapperNonNullWithDefaultInputObjectField",
        schema_name=schema_name,
    )(resolve_input_object_field)
    Resolver(
        "Query.wrapperNonNullWithDefaultInputObjectWithDefaultField",
        schema_name=schema_name,
    )(resolve_input_object_field)
    Resolver(
        "Query.nonNullWrapperNonNullWithDefaultInputObjectField",
        schema_name=schema_name,
    )(resolve_input_object_field)
    Resolver(
        "Query.nonNullWrapperNonNullWithDefaultInputObjectWithDefaultField",
        schema_name=schema_name,
    )(resolve_input_object_field)
    Resolver("Query.innerNonNullInputObjectField", schema_name=schema_name)(
        resolve_input_object_field
    )
    Resolver(
        "Query.innerNonNullInputObjectWithDefaultField",
        schema_name=schema_name,
    )(resolve_input_object_field)
    Resolver(
        "Query.nonNullInnerNonNullInputObjectField", schema_name=schema_name
    )(resolve_input_object_field)
    Resolver(
        "Query.nonNullInnerNonNullInputObjectWithDefaultField",
        schema_name=schema_name,
    )(resolve_input_object_field)
    Resolver(
        "Query.innerNonNullWithDefaultInputObjectField",
        schema_name=schema_name,
    )(resolve_input_object_field)
    Resolver(
        "Query.innerNonNullWithDefaultInputObjectWithDefaultField",
        schema_name=schema_name,
    )(resolve_input_object_field)
    Resolver(
        "Query.nonNullInnerNonNullWithDefaultInputObjectField",
        schema_name=schema_name,
    )(resolve_input_object_field)
    Resolver(
        "Query.nonNullInnerNonNullWithDefaultInputObjectWithDefaultField",
        schema_name=schema_name,
    )(resolve_input_object_field)
