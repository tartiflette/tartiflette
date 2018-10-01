from .boolean import ScalarBoolean
from .float import ScalarFloat
from .id import ScalarId
from .int import ScalarInt
from .string import ScalarString
from .date import ScalarDate
from .time import ScalarTime
from .datetime import ScalarDateTime
from .custom_scalar import Scalar

CUSTOM_SCALARS = {
    "Int": ScalarInt,
    "ID": ScalarId,
    "String": ScalarString,
    "Float": ScalarFloat,
    "Boolean": ScalarBoolean,
    "Date": ScalarDate,
    "Time": ScalarTime,
    "DateTime": ScalarDateTime,
}

__all__ = ["Scalar", "CUSTOM_SCALARS"]
