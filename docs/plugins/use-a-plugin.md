---
id: use-a-plugin
title: Use a plugin
sidebar_label: Use a plugin
---

## Using a plugin

1. Simply install it. Best method is using `pip install tartiflette-plugin-time-it`
2. Then ask the `create_engine` api to load it like this:
```python
engine = await create_engine(
    sdl,
    modules=[
        "tartiflette_plugin_a_plugin",
        {
            "name": "tartiflette_plugin_time_it",
            "config": {
                "foo": "bar",
            },
        },
    ],
)
```

> Some plugins need configuration, some don't. Be sure to have a look at their respective documentation.
