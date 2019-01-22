def get_directive_implem_list(directives, schema):
    try:
        _directives = {
            name: {
                "callables": schema.find_directive(name).implementation,
                "args": {
                    arg_name: schema.find_directive(name)
                    .arguments[arg_name]
                    .default_value
                    for arg_name in schema.find_directive(name).arguments
                },
            }
            for name in directives
        }

        for name, directive in _directives.items():
            if directives[name] is not None:
                directive["args"].update(directives[name])

        return [v for _, v in _directives.items()]

    except (AttributeError, KeyError, TypeError):
        return []
