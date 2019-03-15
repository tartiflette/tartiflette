import pytest


async def _resolver(*args, **kwargs):
    return {"name": "a", "nickname": "n", "barkVolume": 25}


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(resolvers={"Query.dog": _resolver})
async def test_issue158(engine):
    print(
        await engine.execute(
            """
        fragment lol on Dog {
            nickname: Int
        }
        query {
            dog {
                name @skip(if: true)
                nickname @include(if: true)
                barkVolume
                ...lol @skip(if: false)
                ... @include(if: true) {
                    name
                }
            }
        }
        """
        )
    )
