from typing import Any, Dict, Optional

from tartiflette import Scalar

from .string import ScalarString


class ScalarID(ScalarString):
    """
    Built-in scalar which handle ID values.
    """

    # TODO: :-), with @relay I think.


def bake(schema_name: str, config: Optional[Dict[str, Any]] = None) -> str:
    """
    Links the scalar to the appropriate schema and returns the SDL related
    to the scalar.
    :param schema_name: schema name to link with
    :param config: configuration of the scalar
    :type schema_name: str
    :type config: Optional[Dict[str, Any]]
    :return: the SDL related to the scalar
    :rtype: str
    """
    # pylint: disable=unused-argument
    Scalar("ID", schema_name=schema_name)(ScalarID())
    return '''
    """The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID."""
    scalar ID
    '''
