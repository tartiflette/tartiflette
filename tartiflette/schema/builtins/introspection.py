import os


def bake(_schema_name, _config):
    with open(
        os.path.join(os.path.dirname(__file__), "introspection.sdl")
    ) as file:
        return file.read()
