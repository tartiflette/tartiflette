import os
from tartiflette.tartiflette import Tartiflette


def _starwars_schema():
    my_path = os.path.dirname(__file__)
    with open("%s/starwars.sdl" % my_path, "r") as sdl_file:
        return sdl_file.read()


STARWARSTIFLETTE = Tartiflette(sdl=_starwars_schema())

__all__ = ["STARWARSTIFLETTE"]
