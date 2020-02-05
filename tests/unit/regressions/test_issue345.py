import pytest

from tartiflette.utils.callables import is_valid_async_generator


async def a_func():
    pass


def s_func():
    pass


async def an_async_gen(alist):
    async for an_elem in alist:
        yield an_elem


class Ninja:
    @staticmethod
    async def st_a_func():
        pass

    @staticmethod
    def st_s_func():
        pass

    async def a_func(self):
        pass

    def s_func(self):
        pass

    @staticmethod
    async def st_an_async_gen(alist):
        async for an_elem in alist:
            yield an_elem

    async def an_async_gen(self, alist):
        async for an_elem in alist:
            yield an_elem


_A_NINJA = Ninja()


@pytest.mark.parametrize(
    "obj,expected",
    [
        (a_func, False),
        (s_func, False),
        (an_async_gen, True),
        (_A_NINJA.an_async_gen, True),
        (_A_NINJA.st_an_async_gen, True),
        (_A_NINJA.st_s_func, False),
        (_A_NINJA.st_a_func, False),
        (_A_NINJA.s_func, False),
        (_A_NINJA.a_func, False),
    ],
)
def test_is_valid_async_generator(obj, expected):
    assert is_valid_async_generator(obj) == expected
