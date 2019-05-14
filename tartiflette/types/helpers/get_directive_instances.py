from typing import Any, Dict, List, Optional

from tartiflette.types.helpers.transform_directive import transform_directive


def get_directive_instances(
    directives: Dict[str, Optional[dict]], schema: "GraphQLSchema"
) -> List[Dict[str, Any]]:
    try:
        computed_directives = []
        for directive_definition in directives:

            directive = schema.find_directive(directive_definition["name"])
            directive_dict = transform_directive(directive)

            if directive_definition["args"] is not None:
                directive_dict["args"].update(directive_definition["args"])

            computed_directives.append(directive_dict)

        return computed_directives
    except (AttributeError, KeyError, TypeError):
        pass
    return []
