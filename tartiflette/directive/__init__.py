from .common import (
    OnExecutionDirective,
    OnBuildDirective,
    OnIntrospectionDirective,
    CommonDirective,
)
from .deprecated import Deprecated
from .directive import Directive
from .non_introspectable import NonIntrospectable


BUILT_IN_DIRECTIVES = {
    "deprecated": Deprecated,
    "non_introspectable": NonIntrospectable,
}
