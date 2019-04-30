def _get_callables(implementation):
    return {
        "on_field_execution": implementation.on_field_execution,
        "on_argument_execution": implementation.on_argument_execution,
        "on_enum_value_field_execution": implementation.on_enum_value_field_execution,
        "on_enum_value_argument_execution": implementation.on_enum_value_argument_execution,
        "on_introspection": implementation.on_introspection,
        "on_build": implementation.on_build,
    }


def transform_directive(directive, args=None):
    return {
        "callables": _get_callables(directive.implementation),
        "args": {
            arg_name: directive.arguments[arg_name].default_value
            for arg_name in directive.arguments
        }
        if not args
        else args,
    }
