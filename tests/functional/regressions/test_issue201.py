import os
from tartiflette import Engine


def test_issue201():
    assert (
        Engine(
            [f"{os.path.dirname(__file__)}/sdl/issue201.sdl"],
            schema_name="test_issue201",
        )
        is not None
    )
