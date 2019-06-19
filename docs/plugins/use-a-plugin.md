---
id: use-a-plugin
title: Use a plugin
sidebar_label: Plugins
---

## Using a plugin.

  1. Simply install it. Best method is using `pip`.
  2. Then ask the `create_engine` api to load it like this:

```python
engine = await create_engine(
    sdl,
    modules=[
        "tartiflette_plugin_a_plugin",
        {
            "name": "tartiflette_plugin_another_plugin",
            "config": {
                "foo": "bar"
            }
        }
    ]
)
```

Some plugins need config, some don't. Be sure to have a look at their respective documentation.
