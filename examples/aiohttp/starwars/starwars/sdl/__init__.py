import os
from tartiflette import Engine


def _starwars_schema():
    my_path = os.path.dirname(__file__)
    with open("%s/starwars.sdl" % my_path, "r") as sdl_file:
        return sdl_file.read()


STARWARSTIFLETTE = Engine(schema=_starwars_schema())

__all__ = ["STARWARSTIFLETTE"]
