import pytest

from tartiflette import create_schema
from tests.data.utils import get_path_to_sdl


@pytest.mark.asyncio
async def test_issue201():
    assert (
        await create_schema(
            [get_path_to_sdl("issue201.sdl")], name="test_issue201",
        )
        is not None
    )
