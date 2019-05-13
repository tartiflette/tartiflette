from functools import partial
from typing import Any, Callable, Dict, List, Optional, Union

from tartiflette.types.exceptions.tartiflette import InvalidValue, NullError
from tartiflette.types.helpers import has_typename, reduce_type

from .coercer_way import CoercerWay


def _set_typename(result: Any, typename: Optional[str]) -> None:
    if result is None or typename is None or has_typename(result):
        return

    try:
        result["_typename"] = typename
        return
    except TypeError:
        pass

    try:
        setattr(result, "_typename", typename)
    except AttributeError:
        pass  # Res is unmutable


async def _scalar_coercer(
    func: Callable, val: Optional[Any], *_args, **_kwargs
):
    if val is None:
        return val

    return func(val)


async def _object_coercer(
    raw_type: Optional[str], val: Optional[Any], *_args, **_kwargs
) -> Optional[dict]:
    if val is None:
        return None

    _set_typename(val, raw_type)
    return {}


async def _list_coercer(
    func: Callable, val: Optional[Any], *args, **kwargs
) -> Optional[list]:
    if val is None:
        return val

    if isinstance(val, list):
        # TODO maybe gather them
        return [await func(v, *args, **kwargs) for v in val]

    return [await func(val, *args, **kwargs)]


async def _not_null_coercer(
    func: Callable,
    val: Optional[Any],
    field_definition: "GraphQLField",
    ctx: Dict[Any, Any],
    info: "Info",
) -> Any:
    if val is None:
        raise NullError(val, info)
    return await func(val, field_definition, ctx, info)


def _get_type_coercers(field_type: "GraphQLType") -> List[Callable]:
    coercer_list = []
    current_type = field_type
    while hasattr(current_type, "gql_type"):
        if current_type.is_list:
            coercer_list.append(_list_coercer)
        if current_type.is_not_null:
            coercer_list.append(_not_null_coercer)
        current_type = current_type.gql_type
    return coercer_list


def _list_and_null_coercer(
    field_type: Union["GraphQLList", "GraphQLNonNull"], coercer: Callable
) -> Callable:
    field_type_coercers = _get_type_coercers(field_type)
    for field_type_coercer in reversed(field_type_coercers):
        coercer = partial(field_type_coercer, coercer)
    return coercer


async def _enum_coercer(
    enum_valid_values: List[str],
    func: Callable,
    val: Optional[str],
    field_definion: "GraphQLField",
    ctx: Dict[Any, Any],
    info: "Info",
) -> Optional[str]:
    if val is None:
        return val

    if val not in enum_valid_values:
        raise InvalidValue(val, info)
    return await func(val, field_definion, ctx, info)


def _is_an_enum(
    reduced_type: str, schema: "GraphQLSchema", way
) -> Optional[Callable]:
    enum = schema.find_enum(reduced_type)
    if enum:
        scalar = schema.find_scalar("String")
        return partial(
            _enum_coercer,
            [x.value for x in enum.values],
            partial(
                _scalar_coercer,
                scalar.coerce_output
                if way == CoercerWay.OUTPUT
                else scalar.coerce_input,
            ),
        )
    return None


def _is_a_scalar(
    reduced_type: str, schema: "GraphQLSchema", way
) -> Optional[Callable]:
    scalar = schema.find_scalar(reduced_type)
    if scalar:
        return partial(
            _scalar_coercer,
            scalar.coerce_output
            if way == CoercerWay.OUTPUT
            else scalar.coerce_input,
        )
    return None


def _is_union(reduced_type: str, schema: "GraphQLSchema") -> bool:
    try:
        return schema.find_type(reduced_type).is_union
    except (AttributeError, KeyError):
        pass
    return False


async def _input_object_coercer(
    input_field_coercers: Dict[str, "GraphQLArgument"],
    values: Dict[Any, Any],
    field_definition: "GraphQLField",
    ctx: Dict[Any, Any],
    info: "Info",
):
    if values is None:
        return None

    coerced = {}

    for field_name, coercer in input_field_coercers.items():
        coerced[field_name] = await coercer(
            values.get(field_name), field_definition, ctx, info
        )
    return coerced


def _get_input_object_coercer(fields, schema) -> Callable:
    return partial(
        _input_object_coercer,
        {
            x.name: get_coercer(x, schema=schema, way=CoercerWay.INPUT)
            for x in fields
        },
    )


def _is_an_input_object(reduced_type, schema):
    try:
        return _get_input_object_coercer(
            schema.find_type(reduced_type).input_fields, schema
        )
    except (AttributeError, KeyError):
        pass

    return None


async def _directive_endpoint(val, *_args, **_kwargs):
    return val


async def _input_directive_runner(directives, coercers, val, *args, **kwargs):
    return await directives(
        await coercers(val, *args, **kwargs), *args, **kwargs
    )


async def _output_directive_runner(directives, coercers, val, *args, **kwargs):
    return await coercers(
        await directives(val, *args, **kwargs), *args, **kwargs
    )


def _add_directive_runner_partial(func, reduce_type_name, schema, way):
    try:
        rtype = schema.find_type(reduce_type_name)
    except KeyError:
        return func

    if hasattr(rtype, "directives"):
        directives = rtype.directives.get(way)
        if way == CoercerWay.OUTPUT:
            return partial(_output_directive_runner, directives, func)
        return partial(_input_directive_runner, directives, func)

    return func


def get_coercer(
    field: Union["GraphQLField", "GraphQLArgument"],
    schema=None,
    way=CoercerWay.OUTPUT,
) -> Optional[Callable]:

    schema = schema or field.schema
    if not schema:
        return None

    field_type = field.gql_type
    reduced_type = reduce_type(field_type)
    is_union = _is_union(reduced_type, schema)
    default_coercer = partial(
        _object_coercer, reduced_type if not is_union else None
    )

    # TODO We can do better here.
    try:
        coercer = _is_an_enum(reduced_type, schema, way)
        if not coercer:
            coercer = _is_a_scalar(reduced_type, schema, way)
            if not coercer:
                coercer = _is_an_input_object(reduced_type, schema)
                if not coercer:
                    # per default you're an object
                    coercer = default_coercer
    except AttributeError:
        coercer = default_coercer

    # Manage List and NonNull
    coercer = _list_and_null_coercer(field_type, coercer)

    # Manage directives
    return _add_directive_runner_partial(coercer, reduced_type, schema, way)
