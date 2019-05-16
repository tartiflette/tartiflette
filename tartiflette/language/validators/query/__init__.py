from .all_variable_usages_are_allowed import AllVariableUsagesAreAllowed
from .all_variable_uses_defined import AllVariableUsesDefined
from .all_variables_used import AllVariablesUsed
from .argument_names import ArgumentNames
from .argument_uniqueness import ArgumentUniqueness
from .directives_are_defined import DirectivesAreDefined
from .directives_are_in_valid_locations import DirectivesAreInValidLocations
from .directives_are_unique_per_location import DirectivesAreUniquePerLocation
from .executable_definitions import ExecutableDefinition
from .field_selections_on_objects_interfaces_and_unions_types import (
    FieldSelectionsOnObjectsInterfacesAndUnionsTypes,
)
from .fragment_must_be_used import FragmentMustBeUsed
from .fragment_name_uniqueness import FragmentNameUniqueness
from .fragment_spread_is_possible import FragmentSpreadIsPossible
from .fragment_spread_target_defined import FragmentSpreadTargetDefined
from .fragment_spread_type_existence import FragmentSpreadTypeExistence
from .fragment_spreads_must_not_form_cycles import (
    FragmentSpreadsMustNotFormCycles,
)
from .fragments_on_composite_types import FragmentsOnCompositeTypes
from .input_object_field_uniqueness import InputObjectFieldUniqueness
from .leaf_field_selections import LeafFieldSelections
from .lone_anonymous_operation import LoneAnonymousOperation
from .operation_name_uniqueness import OperationNameUniqueness
from .required_arguments import RequiredArguments
from .single_root_field import SingleRootField
from .values_of_correct_type import ValuesOfCorrectType
from .variable_uniqueness import VariableUniqueness
from .variables_are_input_types import VariablesAreInputTypes

# TODO make this automatically via reflection

RULE_SET = {
    AllVariableUsagesAreAllowed.RULE_NAME: AllVariableUsagesAreAllowed(),
    AllVariablesUsed.RULE_NAME: AllVariablesUsed(),
    AllVariableUsesDefined.RULE_NAME: AllVariableUsesDefined(),
    ArgumentNames.RULE_NAME: ArgumentNames(),
    ArgumentUniqueness.RULE_NAME: ArgumentUniqueness(),
    DirectivesAreDefined.RULE_NAME: DirectivesAreDefined(),
    DirectivesAreInValidLocations.RULE_NAME: DirectivesAreInValidLocations(),
    DirectivesAreUniquePerLocation.RULE_NAME: DirectivesAreUniquePerLocation(),
    ExecutableDefinition.RULE_NAME: ExecutableDefinition(),
    FieldSelectionsOnObjectsInterfacesAndUnionsTypes.RULE_NAME: FieldSelectionsOnObjectsInterfacesAndUnionsTypes(),
    FragmentMustBeUsed.RULE_NAME: FragmentMustBeUsed(),
    FragmentNameUniqueness.RULE_NAME: FragmentNameUniqueness(),
    FragmentsOnCompositeTypes.RULE_NAME: FragmentsOnCompositeTypes(),
    FragmentSpreadIsPossible.RULE_NAME: FragmentSpreadIsPossible(),
    FragmentSpreadsMustNotFormCycles.RULE_NAME: FragmentSpreadsMustNotFormCycles(
        True
    ),
    FragmentSpreadTargetDefined.RULE_NAME: FragmentSpreadTargetDefined(),
    FragmentSpreadTypeExistence.RULE_NAME: FragmentSpreadTypeExistence(),
    InputObjectFieldUniqueness.RULE_NAME: InputObjectFieldUniqueness(),
    LeafFieldSelections.RULE_NAME: LeafFieldSelections(),
    LoneAnonymousOperation.RULE_NAME: LoneAnonymousOperation(),
    RequiredArguments.RULE_NAME: RequiredArguments(),
    SingleRootField.RULE_NAME: SingleRootField(),
    OperationNameUniqueness.RULE_NAME: OperationNameUniqueness(),
    ValuesOfCorrectType.RULE_NAME: ValuesOfCorrectType(),
    VariablesAreInputTypes.RULE_NAME: VariablesAreInputTypes(),
    VariableUniqueness.RULE_NAME: VariableUniqueness(),
}
