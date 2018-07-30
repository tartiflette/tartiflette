from collections import namedtuple
from typing import List, Any

Info = namedtuple("Info",
                  ["query_field", "schema_field", "schema", "path", "location"])

# on build/bake
# on resolve
# on introspect


class CoercedValue:
# CoercedValue = namedtuple('CoercedValue', ["name", "error"])

    def __init__(self, value: Any = None, error: Exception = None):
        self.value = value
        self.error = error

    def __repr__(self):
        return "{}(value={!r}, error={!r})".format(
            self.__class__.__name__, self.value, self.error
        )
