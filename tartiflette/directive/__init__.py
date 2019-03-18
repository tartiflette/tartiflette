from .common import (
    OnExecutionDirective,
    OnBuildDirective,
    OnIntrospectionDirective,
    CommonDirective,
)
from .deprecated import Deprecated
from .directive import Directive
from .non_introspectable import NonIntrospectable
from .skip import Skip
from .include import Include

BUILT_IN_DIRECTIVES = {
    "deprecated": Deprecated,
    "non_introspectable": NonIntrospectable,
    "skip": Skip,
    "include": Include,
}
