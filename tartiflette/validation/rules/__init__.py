from .executable_definitions import ExecutableDefinitionsRule
from .fields_on_correct_type import FieldsOnCorrectTypeRule
from .fragments_on_composite_types import FragmentsOnCompositeTypesRule
from .has_enum_value_defined import HasEnumValueDefinedRule
from .has_field_defined import HasFieldDefinedRule
from .has_input_field_defined import HasInputFieldDefinedRule
from .has_member_defined import HasMemberDefinedRule
from .input_object_no_circular_ref import InputObjectNoCircularRefRule
from .known_argument_names import (
    KnownArgumentNamesOnDirectivesRule,
    KnownArgumentNamesRule,
)
from .known_directives import KnownDirectivesRule
from .known_fragment_names import KnownFragmentNamesRule
from .known_type_names import KnownTypeNamesRule
from .lone_anonymous_operation import LoneAnonymousOperationRule
from .lone_schema_definition import LoneSchemaDefinitionRule
from .no_fragment_cycles import NoFragmentCyclesRule
from .no_undefined_variables import NoUndefinedVariablesRule
from .no_unused_fragments import NoUnusedFragmentsRule
from .no_unused_variables import NoUnusedVariablesRule
from .overlapping_fields_can_be_merged import OverlappingFieldsCanBeMergedRule
from .possible_fragment_spreads import PossibleFragmentSpreadsRule
from .possible_type_extensions import PossibleTypeExtensionsRule
from .provided_required_arguments import (
    ProvidedRequiredArgumentsOnDirectivesRule,
    ProvidedRequiredArgumentsRule,
)
from .scalar_leafs import ScalarLeafsRule
from .single_field_subscriptions import SingleFieldSubscriptionsRule
from .unique_argument_names import UniqueArgumentNamesRule
from .unique_directive_names import UniqueDirectiveNamesRule
from .unique_directives_per_location import UniqueDirectivesPerLocationRule
from .unique_enum_value_names import UniqueEnumValueNamesRule
from .unique_field_definition_names import UniqueFieldDefinitionNamesRule
from .unique_fragment_names import UniqueFragmentNamesRule
from .unique_input_field_names import UniqueInputFieldNamesRule
from .unique_interface_implementation import UniqueInterfaceImplementationRule
from .unique_members import UniqueMembersRule
from .unique_operation_names import UniqueOperationNamesRule
from .unique_operation_types import UniqueOperationTypesRule
from .unique_type_names import UniqueTypeNamesRule
from .unique_variable_names import UniqueVariableNamesRule
from .valid_field_definition_types import ValidFieldDefinitionTypesRule
from .valid_implement_types import ValidImplementTypesRule
from .valid_input_value_types import ValidInputValueTypesRule
from .valid_member_types import ValidMemberTypesRule
from .valid_names import ValidNamesRule
from .valid_object_implements import ValidObjectImplementsRule
from .valid_operation_types import ValidOperationTypesRule
from .values_of_correct_type import ValuesOfCorrectTypeRule
from .variables_are_input_types import VariablesAreInputTypesRule
from .variables_in_allowed_position import VariablesInAllowedPositionRule

SPECIFIED_SDL_RULES = [
    LoneSchemaDefinitionRule,
    UniqueOperationTypesRule,
    UniqueTypeNamesRule,
    UniqueEnumValueNamesRule,
    UniqueFieldDefinitionNamesRule,
    UniqueDirectiveNamesRule,
    KnownTypeNamesRule,
    KnownDirectivesRule,
    UniqueDirectivesPerLocationRule,
    PossibleTypeExtensionsRule,
    KnownArgumentNamesOnDirectivesRule,
    UniqueArgumentNamesRule,
    UniqueInputFieldNamesRule,
    ProvidedRequiredArgumentsOnDirectivesRule,
    ValidOperationTypesRule,
    ValidNamesRule,
    ValidInputValueTypesRule,
    ValidFieldDefinitionTypesRule,
    HasFieldDefinedRule,
    HasInputFieldDefinedRule,
    HasEnumValueDefinedRule,
    HasMemberDefinedRule,
    UniqueMembersRule,
    ValidMemberTypesRule,
    UniqueInterfaceImplementationRule,
    ValidImplementTypesRule,
    ValidObjectImplementsRule,
    InputObjectNoCircularRefRule,
]

SPECIFIED_QUERY_RULES = [
    # ExecutableDefinitionsRule,  # Already checked through libgraphqlparser
    UniqueOperationNamesRule,
    LoneAnonymousOperationRule,
    SingleFieldSubscriptionsRule,
    KnownTypeNamesRule,
    FragmentsOnCompositeTypesRule,
    VariablesAreInputTypesRule,
    ScalarLeafsRule,
    FieldsOnCorrectTypeRule,
    UniqueFragmentNamesRule,
    KnownFragmentNamesRule,
    NoUnusedFragmentsRule,
    PossibleFragmentSpreadsRule,
    NoFragmentCyclesRule,
    UniqueVariableNamesRule,
    NoUndefinedVariablesRule,
    NoUnusedVariablesRule,
    KnownDirectivesRule,
    UniqueDirectivesPerLocationRule,
    KnownArgumentNamesRule,
    UniqueArgumentNamesRule,
    ValuesOfCorrectTypeRule,
    ProvidedRequiredArgumentsRule,
    VariablesInAllowedPositionRule,
    OverlappingFieldsCanBeMergedRule,
    UniqueInputFieldNamesRule,
]

__all__ = ("SPECIFIED_SDL_RULES", "SPECIFIED_QUERY_RULES")
