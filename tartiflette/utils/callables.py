from inspect import (
    isasyncgenfunction,
    iscoroutinefunction,
    isfunction,
    ismethod,
)
from typing import AsyncGenerator, Coroutine


def is_valid_coroutine(coroutine: Coroutine) -> bool:
    """
    Determines whether or not the filled in parameter is a valid coroutine
    callable.
    :param coroutine: object to check
    :type coroutine: Coroutine
    :return: whether or not the filled in parameter is a valid coroutine
    callable
    :rtype: bool
    """
    return iscoroutinefunction(
        coroutine
        if isfunction(coroutine) or ismethod(coroutine)
        else coroutine.__call__
    )


def is_valid_async_generator(generator: AsyncGenerator) -> bool:
    """
    Determines whether or not the filled in parameter is a valid asynchronous
    generator.
    :param generator: object to check
    :type generator: AsyncGenerator
    :return: whether or not the filled in parameter is a valid asynchronous
    generator
    :rtype: bool
    """
    return isasyncgenfunction(
        generator if isfunction(generator) else generator.__call__
    )
