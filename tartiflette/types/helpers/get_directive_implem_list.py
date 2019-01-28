from typing import Any, Dict, List, Optional


def get_directive_implem_list(
    directives: Dict[str, Optional[dict]], schema: "GraphQLSchema"
) -> List[Dict[str, Any]]:
    try:
        computed_directives = {}
        for directive_name, directive_args in directives.items():
            directive = schema.find_directive(directive_name)
            computed_directives[directive_name] = {
                "callables": directive.implementation,
                "args": {
                    arg_name: directive.arguments[arg_name].default_value
                    for arg_name in directive.arguments
                },
            }

            if directive_args is not None:
                computed_directives[directive_name]["args"].update(
                    directive_args
                )

        return list(computed_directives.values())
    except (AttributeError, KeyError, TypeError):
        pass
    return []
