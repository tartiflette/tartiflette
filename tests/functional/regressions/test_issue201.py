import os

import pytest

from tartiflette import create_engine


@pytest.mark.asyncio
async def test_issue201():
    assert (
        await create_engine(
            [f"{os.path.dirname(__file__)}/sdl/issue201.sdl"],
            schema_name="test_issue201",
        )
        is not None
    )
