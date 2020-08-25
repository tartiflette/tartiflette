import os

from glob import glob

_BASE_PATH = os.path.dirname(os.path.abspath(__file__))

__all__ = ("get_path_to_query", "get_path_to_sdl", "read_sdl_file", "load_sdl")


def get_path_to_query(*paths):
    return os.path.join(_BASE_PATH, "queries", *paths)


def get_path_to_sdl(*paths):
    return os.path.join(_BASE_PATH, "sdls", *paths)


def read_sdl_file(*paths):
    with open(get_path_to_sdl(*paths)) as sdl_file:
        return sdl_file.read()


def load_sdl(sdl):
    full_sdl = ""

    file_paths = []
    if isinstance(sdl, list):
        file_paths += sdl
    elif os.path.isfile(sdl):
        file_paths.append(sdl)
    elif os.path.isdir(sdl):
        file_paths.extend(
            glob(os.path.join(sdl, "**/*.graphql"), recursive=True)
        )
        file_paths.extend(glob(os.path.join(sdl, "**/*.sdl"), recursive=True))
    else:
        full_sdl = sdl

    for file_path in file_paths:
        with open(file_path, mode="r") as sdl_file:
            full_sdl = f"{full_sdl} {sdl_file.read()}"

    return full_sdl
