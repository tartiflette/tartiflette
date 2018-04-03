from unittest.mock import MagicMock


class AsyncMock(MagicMock):
    """ Fix to be able to use MagicMock with async context"""

    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)
