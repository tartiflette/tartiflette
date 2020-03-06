import pytest

from tartiflette import create_engine


@pytest.mark.asyncio
async def test_issue372():
    assert (
        await create_engine(
            """
            interface MediaMetadata {
                height: Int
                width : Int
            }

            interface Media {
                metadata: MediaMetadata
            }

            type VideoMetadata implements MediaMetadata {
                height: Int
                width : Int
                duration: Int
            }

            type Video implements Media {
                metadata: VideoMetadata
            }

            type Live implements Media {
                metadata: MediaMetadata
            }

            type Query {
                media: Media
            }
        """,
            schema_name="test_issue372",
        )
        is not None
    )
