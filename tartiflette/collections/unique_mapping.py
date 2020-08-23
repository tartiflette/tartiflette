try:
    from collections import MutableMapping
except ImportError:
    from collections.abc import MutableMapping
from typing import Any, Iterator

__all__ = ("AlreadyDefinedException", "UniqueMapping")


class AlreadyDefinedException(Exception):
    pass


class UniqueMapping(MutableMapping):
    """Mapping which doesn't allow to redefine an existing key."""

    def __setitem__(self, key: Any, value: Any) -> None:
        """Store a key / value pair to the mapping.

        If the key is already defined, an AlreadyDefinedException will
        be raised.

        :param key: the key of the value to store
        :param value: the value related to the key to store
        :type key: Any
        :type value: Any
        """
        if key in self.__dict__:
            raise AlreadyDefinedException()
        self.__dict__[key] = value

    def __getitem__(self, key: Any) -> Any:
        """Return the value defined by the key.

        :param key: the key to fetch
        :type key: Any
        :return: the value defined by the key
        :rtype: Any
        """
        return self.__dict__[key]

    def __delitem__(self, key: Any) -> None:
        """Delete a key / value pair from the mapping.

        :param key: the key to delete
        :type key: Any
        """
        del self.__dict__[key]

    def __iter__(self) -> Iterator:
        """Return an iterator over the mapping.

        :return: an iterator over the mapping
        :rtype: Iterator
        """
        return iter(self.__dict__)

    def __len__(self) -> int:
        """Return the length of the mapping.

        :return: the length of the mapping
        :rtype: int
        """
        return len(self.__dict__)
