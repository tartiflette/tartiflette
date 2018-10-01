from .deprecated import Deprecated
from .non_introspectable import NonIntrospectable
from .directive import Directive
from .common import (
    OnExecutionDirective,
    OnBuildDirective,
    OnIntrospectionDirective,
    CommonDirective,
)

BUILT_IN_DIRECTIVES = {
    "deprecated": Deprecated,
    "non_introspectable": NonIntrospectable,
}
