from unittest.mock import Mock

import pytest

from tartiflette.parser.nodes.definition import NodeDefinition
from tartiflette.parser.nodes.fragment_definition import NodeFragmentDefinition
from tartiflette.types.exceptions.tartiflette import (
    AlreadyDefined,
    MissingRequiredArgument,
    MultipleRootNodeOnSubscriptionOperation,
    NotLoneAnonymousOperation,
    NotUniqueOperationName,
    TartifletteError,
    UndefinedDirectiveArgument,
    UndefinedFieldArgument,
    UniqueArgumentNames,
    UnusedFragment,
)
from tartiflette.types.location import Location
from tartiflette.utils.arguments import UNDEFINED_VALUE


@pytest.fixture
def a_schema():
    return Mock()


@pytest.fixture
def an_element():
    el = Mock()
    el.name = "a_name"
    el.get_location = Mock(return_value="a_location")
    el.get_alias = Mock(return_value="an_alias")
    return el


@pytest.fixture
def a_visitor(a_schema):
    from tartiflette.parser.visitor import TartifletteVisitor

    visi = TartifletteVisitor(a_schema)
    visi._internal_ctx.node = Mock()
    return visi


def test_parser_visitor(a_schema):
    from tartiflette.parser.visitor import TartifletteVisitor

    tv = TartifletteVisitor(a_schema)

    assert a_schema == tv.schema
    assert tv._vars == {}

    a_dict = {"A": "B"}

    tv = TartifletteVisitor(a_schema, a_dict)

    assert tv._vars == a_dict


def test_parser_visitor__on_argument(a_visitor, an_element):
    field_def_mock = Mock(arguments={"a_name": Mock()})
    field_node_mock = Mock(arguments={})

    a_visitor._get_parent_type = Mock(return_value="Query")
    a_visitor._internal_ctx.field_path = ["field", "path"]
    a_visitor._internal_ctx._fields = {"field/path": field_def_mock}
    a_visitor._internal_ctx.node = field_node_mock
    a_visitor._internal_ctx.node.name = "dog"

    assert a_visitor._internal_ctx.argument is None

    assert a_visitor._on_argument_in(an_element) is None
    assert a_visitor._internal_ctx.argument.name == "a_name"

    assert a_visitor._on_argument_out(an_element) is None
    assert a_visitor._internal_ctx.argument is None


def test_parser_visitor__on_argument_undefined_field_argument(
    a_visitor, an_element
):
    field_def_mock = Mock(arguments={"an_argument": Mock()})
    field_node_mock = Mock(arguments={})

    a_visitor._internal_ctx.directive = None
    a_visitor._get_parent_type = Mock(return_value="Query")
    a_visitor._internal_ctx.field_path = ["field", "path"]
    a_visitor._internal_ctx._fields = {"field/path": field_def_mock}
    a_visitor._internal_ctx.node = field_node_mock
    a_visitor._internal_ctx.node.name = "dog"

    an_element.name = "undefinedArgument"

    assert a_visitor._internal_ctx.argument is None
    assert a_visitor.exceptions == []

    assert a_visitor._on_argument_in(an_element) is None
    assert a_visitor._internal_ctx.argument is None

    assert a_visitor._on_argument_out(an_element) is None
    assert a_visitor._internal_ctx.argument is None

    assert len(a_visitor.exceptions) == 1
    assert isinstance(a_visitor.exceptions[0], UndefinedFieldArgument)
    assert (
        str(a_visitor.exceptions[0])
        == "Undefined argument < undefinedArgument > on field < dog > of type < Query >."
    )


def test_parser_visitor__on_argument_undefined_directive_argument(
    a_visitor, an_element
):
    directive_mock = Mock(arguments={"an_argument": Mock()})
    directive_mock.name = "myDirective"

    a_visitor._internal_ctx.directive = Mock()
    a_visitor._internal_ctx.directive.name = "myDirective"
    a_visitor._internal_ctx.directive.arguments = {}
    a_visitor.schema.find_directive = Mock(return_value=directive_mock)

    an_element.name = "undefinedArgument"

    assert a_visitor._internal_ctx.argument is None
    assert a_visitor.exceptions == []

    assert a_visitor._on_argument_in(an_element) is None
    assert a_visitor._internal_ctx.argument is None

    assert a_visitor._on_argument_out(an_element) is None
    assert a_visitor._internal_ctx.argument is None

    assert len(a_visitor.exceptions) == 1
    assert isinstance(a_visitor.exceptions[0], UndefinedDirectiveArgument)
    assert (
        str(a_visitor.exceptions[0])
        == "Undefined argument < undefinedArgument > on directive < @myDirective >."
    )


def test_parser_visitor__on_argument_non_unique_field_argument(
    a_visitor, an_element
):
    field_def_mock = Mock(arguments={"an_argument": Mock()})
    field_node_mock = Mock(arguments={"an_argument": Mock()})

    a_visitor._internal_ctx.directive = None
    a_visitor._get_parent_type = Mock(return_value="Query")
    a_visitor._internal_ctx.field_path = ["field", "path"]
    a_visitor._internal_ctx._fields = {"field/path": field_def_mock}
    a_visitor._internal_ctx.node = field_node_mock
    a_visitor._internal_ctx.node.name = "dog"

    an_element.name = "an_argument"

    assert a_visitor._internal_ctx.argument is None
    assert a_visitor.exceptions == []

    assert a_visitor._on_argument_in(an_element) is None
    assert a_visitor._internal_ctx.argument is None

    assert a_visitor._on_argument_out(an_element) is None
    assert a_visitor._internal_ctx.argument is None

    assert len(a_visitor.exceptions) == 1
    assert isinstance(a_visitor.exceptions[0], UniqueArgumentNames)
    assert (
        str(a_visitor.exceptions[0])
        == "There can be only one argument named < an_argument >."
    )


def test_parser_visitor__on_argument_non_unique_directive_argument(
    a_visitor, an_element
):
    directive_def_mock = Mock(arguments={"an_argument": Mock()})
    directive_def_mock.name = "myDirective"
    directive_node_mock = Mock(arguments={"an_argument": Mock()})
    directive_node_mock.name = "myDirective"

    a_visitor.schema.find_directive = Mock(return_value=directive_def_mock)
    a_visitor._internal_ctx.directive = directive_node_mock

    an_element.name = "an_argument"

    assert a_visitor._internal_ctx.argument is None
    assert a_visitor.exceptions == []

    assert a_visitor._on_argument_in(an_element) is None
    assert a_visitor._internal_ctx.argument is None

    assert a_visitor._on_argument_out(an_element) is None
    assert a_visitor._internal_ctx.argument is None

    assert len(a_visitor.exceptions) == 1
    assert isinstance(a_visitor.exceptions[0], UniqueArgumentNames)
    assert (
        str(a_visitor.exceptions[0])
        == "There can be only one argument named < an_argument >."
    )


def test_parser_visitor__on_directive(a_visitor, an_element):
    directive_mock = Mock()
    directive_mock.arguments = {}

    a_visitor.schema.find_directive = Mock(return_value=directive_mock)

    assert a_visitor._internal_ctx.directive is None

    assert a_visitor._on_directive_in(an_element) is None
    assert a_visitor._internal_ctx.directive.name == "a_name"

    assert a_visitor._on_directive_out(an_element) is None
    assert a_visitor._internal_ctx.directive is None


def test_parser_visitor__on_directive_out_missing_required_argument(
    a_visitor, an_element
):
    not_required_arg_mock = Mock(is_required=False)
    not_required_arg_mock.name = "not_required"

    required_arg_mock = Mock(is_required=True)
    required_arg_mock.name = "required"

    directive_def_mock = Mock()
    directive_def_mock.name = "myDirective"
    directive_def_mock.arguments = {
        "not_required": not_required_arg_mock,
        "required": required_arg_mock,
    }

    directive_node_mock = Mock()
    directive_node_mock.name = "myDirective"
    directive_node_mock.arguments = {}

    a_visitor.schema.find_directive = Mock(return_value=directive_def_mock)
    a_visitor._internal_ctx.directive = directive_node_mock

    assert a_visitor._internal_ctx.directive.name == "myDirective"
    assert a_visitor.exceptions == []

    assert a_visitor._on_directive_out(an_element) is None

    assert len(a_visitor.exceptions) == 1
    assert isinstance(a_visitor.exceptions[0], MissingRequiredArgument)
    assert (
        str(a_visitor.exceptions[0])
        == "Missing required < required > argument on < @myDirective > directive."
    )


def test_parser_visitor__on_value_in(a_visitor, an_element):

    a_visitor._internal_ctx.node = Mock()
    del a_visitor._internal_ctx.node.default_value
    a_visitor._internal_ctx.node.arguments = {}
    a_visitor._internal_ctx.argument = Mock()
    a_visitor._internal_ctx.argument.name = "an_argument_name"
    an_element.get_value = Mock(return_value="a_value")

    a_visitor._on_value_in(an_element)

    assert an_element.get_value.called
    assert a_visitor._internal_ctx.node.arguments == {
        "an_argument_name": a_visitor._internal_ctx.argument
    }

    a_visitor._internal_ctx.node.default_value = "a_default_value"

    a_visitor._on_value_in(an_element)

    assert a_visitor._internal_ctx.node.default_value == "a_value"


def test_parser_visitor__on_variable_in(a_visitor, an_element):
    a_visitor._on_variable_in(an_element)
    assert a_visitor._internal_ctx.node.var_name == "a_name"


def test_parser_visitor__on_variable_in_no_var_name_ukn_var(
    a_visitor, an_element
):
    from tartiflette.types.exceptions.tartiflette import (
        UnknownVariableException,
    )

    del a_visitor._internal_ctx.node.var_name

    a_visitor._internal_ctx.node.arguments = {}
    a_visitor._internal_ctx.argument = Mock()
    a_visitor._internal_ctx.argument.name = "an_argument_name"
    a_visitor._vars = {}

    a_visitor._on_variable_in(an_element)

    assert a_visitor.continue_child == 0
    assert a_visitor.exceptions is not None
    assert isinstance(a_visitor.exceptions[0], UnknownVariableException)


def test_parser_visitor__on_variable_in_no_var_name(a_visitor, an_element):
    del a_visitor._internal_ctx.node.var_name

    a_visitor._internal_ctx.directive = None
    a_visitor._internal_ctx.node.arguments = {}
    a_visitor._internal_ctx.argument = Mock()
    a_visitor._internal_ctx.argument.name = "a_name"
    a_visitor._vars = {"a_name": "a_value"}

    a_visitor._on_variable_in(an_element)

    assert a_visitor._internal_ctx.node.arguments == {
        "a_name": a_visitor._internal_ctx.argument
    }


def test_parser_visitor__on_field_in_first_field(a_visitor, an_element):
    a_field = Mock()
    a_field.resolver = Mock()
    a_field.is_leaf = False

    a_visitor._internal_ctx.node = None
    a_visitor._internal_ctx.operation = Mock()
    a_visitor._internal_ctx.operation.name = "Yo"
    a_visitor._internal_ctx.operation.type = "an_operation_type"
    a_visitor._internal_ctx.operation.children = []
    a_visitor.operations = {"Yo": a_visitor._internal_ctx.operation}
    a_visitor.schema.get_operation_type = Mock(
        return_value="an_operation_type"
    )
    a_visitor.schema.find_type = Mock(return_value="an_operation_type")
    a_visitor.schema.get_field_by_name = Mock(return_value=a_field)
    an_element.get_selection_set_size = Mock(return_value=1)

    a_visitor._on_field_in(an_element)

    assert a_visitor._internal_ctx.depth == 1
    assert a_visitor._internal_ctx.field_path == ["a_name"]
    assert a_visitor.schema.get_operation_type.call_args_list == [
        (("an_operation_type",),)
    ]
    assert a_visitor.schema.find_type.call_args_list == [
        (("an_operation_type",),)
    ]
    assert a_visitor.schema.get_field_by_name.call_args_list == [
        (("an_operation_type.a_name",),)
    ]
    assert a_visitor._internal_ctx.node in a_visitor.operations["Yo"].children
    assert a_visitor._internal_ctx.node.parent is None
    assert an_element.get_location.called == 1
    assert an_element.get_alias.called == 1


def test_parser_visitor__on_field_in_another_field(a_visitor, an_element):
    a_field = Mock()
    a_field.resolver = Mock()
    a_field.is_leaf = False

    an_element.get_selection_set_size = Mock(return_value=1)

    a_visitor._internal_ctx.field_path = ["a_parent_path_element"]
    a_visitor._internal_ctx.node.field_executor = Mock()
    a_visitor._internal_ctx.node.add_child = Mock()
    a_visitor._internal_ctx.node.field_executor.schema_field = Mock()
    a_visitor._internal_ctx.node.field_executor.schema_field.gql_type = (
        "a_gql_type"
    )
    current_node = a_visitor._internal_ctx.node
    a_visitor.schema.get_field_by_name = Mock(return_value=a_field)

    a_visitor._internal_ctx.operation = Mock()
    a_visitor._internal_ctx.operation.name = "Yo"
    a_visitor._internal_ctx.operation.type = "Query"
    a_visitor._internal_ctx.operation.children = []
    a_visitor.operations = {"Yo": a_visitor._internal_ctx.operation}

    a_visitor._on_field_in(an_element)

    assert a_visitor._internal_ctx.depth == 2
    assert a_visitor._internal_ctx.field_path == [
        "a_parent_path_element",
        "a_name",
    ]
    assert a_visitor.schema.get_field_by_name.call_args_list == [
        (("a_gql_type.a_name",),)
    ]
    assert (
        a_visitor._internal_ctx.node not in a_visitor.operations["Yo"].children
    )
    assert a_visitor._internal_ctx.node.parent is current_node
    assert an_element.get_location.called == 1
    assert an_element.get_alias.called == 1
    assert current_node.add_child.called == 1


def test_parser_visitor__on_field_in_a_fragment(a_visitor, an_element):
    from tartiflette.types.exceptions.tartiflette import (
        UnknownSchemaFieldResolver,
    )
    from unittest.mock import MagicMock

    a_field = Mock()
    a_field.resolver = Mock()
    a_field.is_leaf = False

    an_element.get_selection_set_size = Mock(return_value=1)
    a_visitor._internal_ctx.field_path = ["a_parent_path_element"]
    a_visitor._internal_ctx.node.field_executor = Mock()
    a_visitor._internal_ctx.node.add_child = Mock()
    a_visitor._internal_ctx.node.field_executor.schema_field = Mock()
    a_visitor._internal_ctx.node.field_executor.schema_field.gql_type = (
        "a_gql_type"
    )
    a_visitor._internal_ctx.inline_fragment_info = Mock()
    a_visitor._internal_ctx.inline_fragment_info.type = (
        "an_inline_fragment_type"
    )
    a_visitor._internal_ctx.inline_fragment_info.depth = 2
    a_visitor._internal_ctx.inline_fragment_info.directives = []
    a_visitor._internal_ctx.type_condition = (
        a_visitor._internal_ctx.inline_fragment_info.type
    )
    current_node = a_visitor._internal_ctx.node

    a_visitor._internal_ctx.operation = Mock()
    a_visitor._internal_ctx.operation.name = "Yo"
    a_visitor._internal_ctx.operation.type = "Query"
    a_visitor._internal_ctx.operation.children = []
    a_visitor.operations = {"Yo": a_visitor._internal_ctx.operation}

    class _get_field_by_name(MagicMock):
        def __call__(self, aname):
            super().__call__(aname)

            if aname == "a_gql_type.a_name":
                raise UnknownSchemaFieldResolver("a_message")

            return a_field

    a_visitor.schema.get_field_by_name = _get_field_by_name()

    a_visitor._on_field_in(an_element, type_cond_depth=1)

    assert a_visitor._internal_ctx.depth == 2
    assert a_visitor._internal_ctx.field_path == [
        "a_parent_path_element",
        "a_name",
    ]
    assert a_visitor.schema.get_field_by_name.call_args_list == [
        (("a_gql_type.a_name",),),
        (("an_inline_fragment_type.a_name",),),
    ]
    assert (
        a_visitor._internal_ctx.node not in a_visitor.operations["Yo"].children
    )
    assert a_visitor._internal_ctx.node.parent is current_node
    assert an_element.get_location.called == 1
    assert an_element.get_alias.called == 1
    assert current_node.add_child.called == 1


def test_parser_visitor__on_field_unknow_schema_field(a_visitor, an_element):
    from tartiflette.types.exceptions.tartiflette import (
        UnknownSchemaFieldResolver,
    )
    from unittest.mock import MagicMock

    a_visitor._internal_ctx.field_path = ["a_parent_path_element"]
    a_visitor._internal_ctx.node.field_executor = Mock()
    a_visitor._internal_ctx.node.add_child = Mock()
    a_visitor._internal_ctx.node.field_executor.schema_field = Mock()
    a_visitor._internal_ctx.node.field_executor.schema_field.gql_type = (
        "a_gql_type"
    )
    a_visitor._internal_ctx.inline_fragment_info = Mock()
    a_visitor._internal_ctx.inline_fragment_info.type = (
        "an_inline_fragment_type"
    )
    a_visitor._internal_ctx.type_condition = (
        a_visitor._internal_ctx.inline_fragment_info.type
    )
    a_visitor._internal_ctx.inline_fragment_info.depth = 2

    a_visitor._internal_ctx.operation = Mock()
    a_visitor._internal_ctx.operation.name = "Yo"
    a_visitor._internal_ctx.operation.type = "Query"
    a_visitor._internal_ctx.operation.children = []
    a_visitor.operations = {"Yo": a_visitor._internal_ctx.operation}

    an_exception = UnknownSchemaFieldResolver("a_message")

    class _get_field_by_name(MagicMock):
        def __call__(self, aname):
            super().__call__(aname)
            raise an_exception

    a_visitor.schema.get_field_by_name = _get_field_by_name()

    a_visitor._on_field_in(an_element)

    assert a_visitor._internal_ctx.depth == 1
    assert a_visitor._internal_ctx.field_path == ["a_parent_path_element"]
    assert (
        a_visitor._internal_ctx.node not in a_visitor.operations["Yo"].children
    )
    assert a_visitor.continue_child == 0
    assert a_visitor.exceptions[0] == an_exception


def test_parser_visitor__on_field_out(a_visitor, an_element):
    field_mock = Mock()
    field_mock.arguments = {}

    a_visitor._internal_ctx.field_path = ["field", "path"]
    a_visitor._internal_ctx._fields = {"field/path": field_mock}
    a_visitor._internal_ctx.operation = Mock()
    a_visitor._internal_ctx.operation.type = "Query"
    a_visitor._internal_ctx.node = Mock()
    a_visitor._internal_ctx.node.name = "field"
    a_visitor._internal_ctx.node.parent = "LOL"
    a_visitor._internal_ctx.move_out_field = Mock(
        wraps=a_visitor._internal_ctx.move_out_field
    )

    a_visitor._on_field_out(an_element)

    assert a_visitor._internal_ctx.depth == 1
    assert a_visitor._internal_ctx.field_path == ["field"]
    assert a_visitor._internal_ctx.node == "LOL"
    a_visitor._internal_ctx.move_out_field.assert_called_once()


def test_parser_visitor__on_field_out_missing_required_argument(
    a_visitor, an_element
):
    not_required_arg_mock = Mock(is_required=False)
    not_required_arg_mock.name = "not_required"

    required_arg_mock = Mock(is_required=True)
    required_arg_mock.name = "required"

    field_mock = Mock()
    field_mock.name = "fieldName"
    field_mock.arguments = {
        "not_required": not_required_arg_mock,
        "required": required_arg_mock,
    }

    a_visitor._internal_ctx.field_path = ["fieldName"]
    a_visitor._internal_ctx._fields = {"fieldName": field_mock}
    a_visitor._internal_ctx.operation = Mock()
    a_visitor._internal_ctx.operation.type = "Query"

    a_visitor._internal_ctx.node = Mock()
    a_visitor._internal_ctx.node.name = "fieldName"
    a_visitor._internal_ctx.node.parent = "Query"
    a_visitor._internal_ctx.node.arguments = {}

    assert a_visitor.exceptions == []

    a_visitor._on_field_out(an_element)

    assert len(a_visitor.exceptions) == 1
    assert isinstance(a_visitor.exceptions[0], MissingRequiredArgument)
    assert (
        str(a_visitor.exceptions[0])
        == "Missing required < required > argument on < fieldName > field."
    )


def test_parser_visitor__on_variable_definition_in(a_visitor, an_element):
    a_visitor._internal_ctx.node = Mock()
    current_node = a_visitor._internal_ctx.node

    a_visitor._on_variable_definition_in(an_element)

    assert a_visitor._internal_ctx.node != current_node
    assert a_visitor._internal_ctx.node.parent == current_node


def test_parser_visitor__validate_type(a_visitor, an_element):
    a_visitor._validate_type("ninja", "a", str, False)

    assert a_visitor.exceptions == []
    assert a_visitor.continue_child == 1

    a_visitor._validate_type("ntm", "a", int, False)
    assert a_visitor.exceptions is not None
    assert isinstance(a_visitor.exceptions[0], TartifletteError)
    assert a_visitor.continue_child == 0


def test_parser_visitor__validate_type_invalid_type_dont_care(
    a_visitor, an_element
):
    a_visitor._validate_type("ninja", "a", None, False)

    assert a_visitor.exceptions == []
    assert a_visitor.continue_child == 1


def test_parser_visitor__validate_vars_existing_okay_var(
    a_visitor, an_element
):
    a_visitor._internal_ctx.node = Mock()
    a_visitor._internal_ctx.node.var_name = "LOL"
    a_visitor._internal_ctx.node.var_type = str
    a_visitor._internal_ctx.node.is_list = False
    a_visitor._internal_ctx.node.is_nullable = False

    a_visitor._vars = {"LOL": "a_value"}

    a_visitor._validate_type = Mock()

    a_visitor._validates_vars()

    assert a_visitor._validate_type.call_args_list == [
        (("LOL", "a_value", str, False),)
    ]


def test_parser_visitor__validate_vars_existing_okay_var_is_list(
    a_visitor, an_element
):
    a_visitor._internal_ctx.node = Mock()
    a_visitor._internal_ctx.node.var_name = "LOL"
    a_visitor._internal_ctx.node.var_type = str
    a_visitor._internal_ctx.node.is_list = True
    a_visitor._internal_ctx.node.is_nullable = True

    a_visitor._vars = {"LOL": ["a_value_1", "a_value_2"]}

    a_visitor._validate_type = Mock()

    a_visitor._validates_vars()

    assert a_visitor._validate_type.call_args_list == [
        (("LOL", "a_value_1", str, True),),
        (("LOL", "a_value_2", str, True),),
    ]


def test_parser_visitor__validate_vars_existing_okay_var_is_list_nok(
    a_visitor, an_element
):
    a_visitor._internal_ctx.node = Mock()
    a_visitor._internal_ctx.node.var_name = "LOL"
    a_visitor._internal_ctx.node.var_type = str
    a_visitor._internal_ctx.node.is_list = True

    a_visitor._vars = {"LOL": "a_value_1"}

    a_visitor._validate_type = Mock()

    a_visitor._validates_vars()

    assert a_visitor.continue_child == 0
    assert a_visitor.exceptions is not None
    assert isinstance(a_visitor.exceptions[0], TartifletteError)


def test_parser_visitor__validate_vars_existing_okay_var_has_a_dfv(
    a_visitor, an_element
):
    a_visitor._internal_ctx.node = Mock()
    a_visitor._internal_ctx.node.var_name = "LOL"
    a_visitor._internal_ctx.node.var_type = str
    a_visitor._internal_ctx.node.default_value = "a_default_value"

    a_visitor._validate_type = Mock()

    a_visitor._validates_vars()

    assert a_visitor._vars == {"LOL": "a_default_value"}


def test_parser_visitor__validate_vars_existing_okay_var_no_dfv_but_nullable(
    a_visitor, an_element
):
    a_visitor._internal_ctx.node = Mock()
    a_visitor._internal_ctx.node.var_name = "LOL"
    a_visitor._internal_ctx.node.var_type = str
    a_visitor._internal_ctx.node.is_nullable = True
    a_visitor._internal_ctx.node.default_value = UNDEFINED_VALUE
    a_visitor._validate_type = Mock()

    a_visitor._validates_vars()

    assert a_visitor._vars == {"LOL": UNDEFINED_VALUE}


def test_parser_visitor__validate_vars_existing_okay_var_no_dfv_non_nullable(
    a_visitor, an_element
):
    from tartiflette.types.exceptions.tartiflette import (
        UnknownVariableException,
    )

    a_visitor._internal_ctx.node = Mock()
    a_visitor._internal_ctx.node.var_name = "LOL"
    a_visitor._internal_ctx.node.var_type = str
    a_visitor._internal_ctx.node.is_nullable = False
    a_visitor._internal_ctx.node.default_value = None
    a_visitor._validate_type = Mock()

    a_visitor._validates_vars()

    assert a_visitor.continue_child == 0
    assert a_visitor.exceptions is not None
    assert isinstance(a_visitor.exceptions[0], UnknownVariableException)


def test_parser_visitor__on_variable_definition_out(a_visitor, an_element):
    a_visitor._validates_vars = Mock()
    a_visitor._internal_ctx.node = Mock()
    current_node = a_visitor._internal_ctx.node
    a_visitor._internal_ctx.node.parent = Mock()

    a_visitor._on_variable_definition_out(an_element)

    assert a_visitor._validates_vars.called
    assert a_visitor._internal_ctx.node != current_node
    assert a_visitor._internal_ctx.node == current_node.parent


def test_parser_visitor__on_named_type_in_ok(a_visitor, an_element):
    a_visitor._internal_ctx.node = Mock()
    a_visitor._on_named_type_in(an_element)
    assert a_visitor._internal_ctx.node.var_type == "a_name"


def test_parser_visitor__on_named_type_in_nok(a_visitor, an_element):
    a_visitor._internal_ctx.node = "A"

    assert a_visitor._on_named_type_in(an_element) is None


def test_parser_visitor__on_list_type_in_ok(a_visitor, an_element):
    a_visitor._internal_ctx.node = Mock()
    a_visitor._on_list_type_in(an_element)
    assert a_visitor._internal_ctx.node.is_list == True


def test_parser_visitor__on_list_type_in_nok(a_visitor, an_element):
    a_visitor._internal_ctx.node = "A"

    assert a_visitor._on_list_type_in(an_element) is None


def test_parser_visitor__on_non_null_type_in(a_visitor, an_element):
    a_visitor._internal_ctx.node = Mock()
    a_visitor._on_non_null_type_in(an_element)
    assert a_visitor._internal_ctx.node.is_nullable == False


def test_parser_visitor__on_fragment_definition_in(a_visitor, an_element):
    an_element.get_type_condition = Mock(return_value="a_type_condition")

    a_visitor._on_fragment_definition_in(an_element)

    assert a_visitor._internal_ctx.fragment_definition is not None
    assert (
        a_visitor._fragments["a_name"]
        == a_visitor._internal_ctx.fragment_definition
    )


def test_parser_visitor__on_fragment_definition_in_already_know_fragment(
    a_visitor, an_element
):
    an_element.get_type_condition = Mock(return_value="a_type_condition")

    a_visitor._fragments["a_name"] = Mock()
    a_visitor._on_fragment_definition_in(an_element)

    assert a_visitor.continue_child == 0
    assert a_visitor.exceptions is not None
    assert isinstance(a_visitor.exceptions[0], AlreadyDefined)


def test_parser_visitor__on_fragment_definition_out(a_visitor, an_element):
    a_visitor._on_fragment_definition_out(an_element)
    assert a_visitor._internal_ctx.fragment_definition is None


def test_parser_visitor__on_fragment_spread_out(a_visitor, an_element):
    a_visitor._to_call_later = []

    a_visitor._internal_ctx = Mock()
    a_visitor._internal_ctx.fragment_spread = Mock()
    a_visitor._internal_ctx.fragment_spread.directives = []

    a_visitor._on_fragment_spread_out(an_element)

    assert len(a_visitor._to_call_later) == 1


def test_parser_visitor__on_operation_definition_out(a_visitor, an_element):
    a_visitor._internal_ctx.operation = Mock()
    a_visitor._internal_ctx.operation.type = Mock()
    a_visitor._on_operation_definition_out(an_element)
    assert a_visitor._internal_ctx.operation is None


def test_parser_visitor__on_inline_fragment_in(a_visitor, an_element):
    an_element.get_named_type = Mock(return_value="a_named_type")

    assert a_visitor._internal_ctx.inline_fragment_info is None
    assert a_visitor._internal_ctx.type_condition is None

    a_visitor._on_inline_fragment_in(an_element)

    assert a_visitor._internal_ctx.inline_fragment_info.type == "a_named_type"
    assert a_visitor._internal_ctx.type_condition == "a_named_type"


def test_parser_visitor__on_inline_fragment_out(a_visitor, an_element):
    a_visitor._internal_ctx.inline_fragment_info = Mock()
    a_visitor._internal_ctx.type_condition = Mock()

    a_visitor._on_inline_fragment_out(an_element)

    assert a_visitor._internal_ctx.inline_fragment_info is None
    assert a_visitor._internal_ctx.type_condition is None


@pytest.mark.parametrize(
    (
        "curr_path",
        "continue_child",
        "error_path",
        "in_fragment_spread_context",
        "event_callback_called",
        "reset_error_called",
        "expected_path",
        "expected_continue_child",
        "expected_error_path",
    ),
    [
        # Cases without any errors
        (
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
            1,
            None,
            False,
            True,
            False,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)/FakeType(a_name)",
            1,
            None,
        ),
        (
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
            1,
            None,
            True,
            True,
            False,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)/FakeType(a_name)",
            1,
            None,
        ),
        # Cases with error on current node
        (
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
            0,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
            False,
            True,
            False,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)/FakeType(a_name)",
            0,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
        ),
        (
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
            0,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
            True,
            False,
            False,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)/FakeType(a_name)",
            0,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
        ),
        # Cases with error on parent node
        (
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)/SelectionSet/Field(doesKnowCommand)",
            0,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
            False,
            True,
            False,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)/SelectionSet/Field(doesKnowCommand)/FakeType(a_name)",
            0,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
        ),
        (
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)/SelectionSet/Field(doesKnowCommand)",
            0,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
            True,
            False,
            False,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)/SelectionSet/Field(doesKnowCommand)/FakeType(a_name)",
            0,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
        ),
        # Cases with error on siblings
        (
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(human)",
            0,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
            False,
            True,
            False,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(human)/FakeType(a_name)",
            0,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
        ),
        (
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(human)",
            0,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
            True,
            True,
            True,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(human)/FakeType(a_name)",
            1,
            None,
        ),
        # Cases with error on child
        (
            "/Doc/OpeDef(Yolo)/SelectionSet",
            0,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
            False,
            True,
            False,
            "/Doc/OpeDef(Yolo)/SelectionSet/FakeType(a_name)",
            0,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
        ),
        (
            "/Doc/OpeDef(Yolo)/SelectionSet",
            0,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
            True,
            True,
            True,
            "/Doc/OpeDef(Yolo)/SelectionSet/FakeType(a_name)",
            1,
            None,
        ),
    ],
)
def test_parser_visitor_in_v2(
    a_visitor,
    an_element,
    curr_path,
    continue_child,
    error_path,
    in_fragment_spread_context,
    event_callback_called,
    reset_error_called,
    expected_path,
    expected_continue_child,
    expected_error_path,
):
    node_gql_type = "FakeType"
    node_event_callback = Mock()

    # Init visitor instance
    a_visitor._internal_ctx.path = curr_path
    a_visitor.continue_child = continue_child
    a_visitor._error_path = error_path
    a_visitor._in_fragment_spread_context = in_fragment_spread_context

    # Mock visitor callable
    a_visitor._reset_error_path_and_continue_child = Mock(
        wraps=a_visitor._reset_error_path_and_continue_child
    )
    a_visitor._internal_ctx.move_in = Mock(
        wraps=a_visitor._internal_ctx.move_in
    )
    a_visitor._events[a_visitor.IN][node_gql_type] = node_event_callback

    # Init element instance
    an_element.libgraphql_type = node_gql_type

    assert a_visitor._in(an_element) is None

    a_visitor._internal_ctx.move_in.assert_called_once_with(an_element)
    assert a_visitor._internal_ctx.path == expected_path
    assert a_visitor.continue_child == expected_continue_child
    assert a_visitor._error_path == expected_error_path

    if event_callback_called:
        node_event_callback.assert_called_once()
    else:
        node_event_callback.assert_not_called()

    if reset_error_called:
        a_visitor._reset_error_path_and_continue_child.assert_called_once()
    else:
        a_visitor._reset_error_path_and_continue_child.assert_not_called()


@pytest.mark.parametrize(
    (
        "curr_path",
        "continue_child",
        "error_path",
        "in_fragment_spread_context",
        "event_callback_called",
        "reset_error_called",
        "expected_path",
        "expected_continue_child",
        "expected_error_path",
    ),
    [
        # Cases without any errors
        (
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
            1,
            None,
            False,
            True,
            False,
            "/Doc/OpeDef(Yolo)/SelectionSet",
            1,
            None,
        ),
        (
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
            1,
            None,
            True,
            True,
            False,
            "/Doc/OpeDef(Yolo)/SelectionSet",
            1,
            None,
        ),
        # Cases with error on current node
        (
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
            0,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
            False,
            True,
            False,
            "/Doc/OpeDef(Yolo)/SelectionSet",
            0,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
        ),
        (
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
            0,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
            True,
            False,
            False,
            "/Doc/OpeDef(Yolo)/SelectionSet",
            0,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
        ),
        # Cases with error on parent node
        (
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)/SelectionSet/Field(doesKnowCommand)",
            0,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
            False,
            True,
            False,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)/SelectionSet",
            0,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
        ),
        (
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)/SelectionSet/Field(doesKnowCommand)",
            0,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
            True,
            False,
            False,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)/SelectionSet",
            0,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
        ),
        # Cases with error on siblings
        (
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(human)",
            0,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
            False,
            True,
            False,
            "/Doc/OpeDef(Yolo)/SelectionSet",
            0,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
        ),
        (
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(human)",
            0,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
            True,
            True,
            True,
            "/Doc/OpeDef(Yolo)/SelectionSet",
            1,
            None,
        ),
        # Cases with error on child
        (
            "/Doc/OpeDef(Yolo)/SelectionSet",
            0,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
            False,
            True,
            False,
            "/Doc/OpeDef(Yolo)",
            0,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
        ),
        (
            "/Doc/OpeDef(Yolo)/SelectionSet",
            0,
            "/Doc/OpeDef(Yolo)/SelectionSet/Field(dog)",
            True,
            True,
            True,
            "/Doc/OpeDef(Yolo)",
            1,
            None,
        ),
    ],
)
def test_parser_visitor_out(
    a_visitor,
    an_element,
    curr_path,
    continue_child,
    error_path,
    in_fragment_spread_context,
    event_callback_called,
    reset_error_called,
    expected_path,
    expected_continue_child,
    expected_error_path,
):
    node_gql_type = "FakeType"
    node_event_callback = Mock()

    # Init visitor instance
    a_visitor._internal_ctx.path = curr_path
    a_visitor.continue_child = continue_child
    a_visitor._error_path = error_path
    a_visitor._in_fragment_spread_context = in_fragment_spread_context

    # Mock visitor callable
    a_visitor._reset_error_path_and_continue_child = Mock(
        wraps=a_visitor._reset_error_path_and_continue_child
    )
    a_visitor._internal_ctx.move_out = Mock(
        wraps=a_visitor._internal_ctx.move_out
    )
    a_visitor._events[a_visitor.OUT][node_gql_type] = node_event_callback

    # Init element instance
    an_element.libgraphql_type = node_gql_type

    assert a_visitor._out(an_element) is None

    a_visitor._internal_ctx.move_out.assert_called_once()
    assert a_visitor._internal_ctx.path == expected_path
    assert a_visitor.continue_child == expected_continue_child
    assert a_visitor._error_path == expected_error_path

    if event_callback_called:
        node_event_callback.assert_called_once()
    else:
        node_event_callback.assert_not_called()

    if reset_error_called:
        a_visitor._reset_error_path_and_continue_child.assert_called_once()
    else:
        a_visitor._reset_error_path_and_continue_child.assert_not_called()


def test_parser_visitor_update_subscription_selection_set(
    a_visitor, an_element
):
    a_visitor.continue_child = 0
    a_visitor._internal_ctx.operation = Mock()
    a_visitor._internal_ctx.operation.type = "Subscription"
    an_element.libgraphql_type = "SelectionSet"

    a_callback = Mock()
    a_visitor._events[a_visitor.IN]["default"] = a_callback

    a_visitor.update(a_visitor.IN, an_element)

    assert a_callback.called is True
    assert a_visitor.continue_child == 1
    assert a_visitor.event == a_visitor.IN


def test_parser_visitor_update(a_visitor, an_element):
    a_visitor.continue_child = 0
    a_visitor.event = None
    a_visitor._internal_ctx.fragment_definition = None

    an_element.libgraphql_type = "LOL"
    a_callback = Mock()
    a_visitor._events[a_visitor.IN]["default"] = a_callback

    a_visitor.update(a_visitor.IN, an_element)

    assert a_callback.called is True
    assert a_visitor.continue_child == 1
    assert a_visitor.event == a_visitor.IN


def test_parser_visitor_update_in_fragment(a_visitor, an_element):
    from functools import partial

    a_visitor.continue_child = 0
    a_visitor.event = None
    a_visitor._internal_ctx.fragment_definition = Mock()
    a_visitor._internal_ctx.fragment_definition.callbacks = []

    an_element.libgraphql_type = "LOL"
    a_callback = Mock()
    a_visitor._events[a_visitor.IN]["default"] = a_callback

    a_visitor.update(a_visitor.IN, an_element)

    assert a_callback.called is False
    assert a_visitor.continue_child == 1
    assert a_visitor.event == a_visitor.IN
    assert len(a_visitor._internal_ctx.fragment_definition.callbacks) == 1


@pytest.mark.parametrize(
    "defined_fragments,used_fragments,unused",
    [
        (
            {
                "FragmentA": NodeFragmentDefinition(
                    "path", None, "FragmentA", "A"
                )
            },
            {"FragmentA"},
            [],
        ),
        (
            {
                "FragmentA": NodeFragmentDefinition(
                    "path", None, "FragmentA", "A"
                ),
                "FragmentB": NodeFragmentDefinition(
                    "path", None, "FragmentB", "B"
                ),
            },
            {"FragmentA"},
            ["FragmentB"],
        ),
        (
            {
                "FragmentA": NodeFragmentDefinition(
                    "path", None, "FragmentA", "A"
                ),
                "FragmentB": NodeFragmentDefinition(
                    "path", None, "FragmentB", "B"
                ),
            },
            set(),
            ["FragmentA", "FragmentB"],
        ),
    ],
)
def test_on_document_out_unused_fragment(
    a_visitor, defined_fragments, used_fragments, unused
):
    a_visitor._fragments = defined_fragments
    a_visitor._used_fragments = used_fragments

    a_visitor._on_document_out()

    assert len(a_visitor.exceptions) == len(unused)
    for exception, unused_fragment in zip(a_visitor.exceptions, unused):
        assert isinstance(exception, UnusedFragment)


def test_parser_visitor__on_operation_definition_in_not_unique(
    a_visitor, an_element
):
    an_element.name = "getName"
    an_element.get_location = Mock(return_value=Location(2, 1, 2, 2))

    a_visitor._named_operations = {
        "getName": NodeDefinition(None, None, Location(1, 1, 1, 2), "getName")
    }

    a_visitor._on_operation_definition_in(an_element)

    assert len(a_visitor.exceptions) == 1
    assert isinstance(a_visitor.exceptions[0], NotUniqueOperationName)
    assert (
        str(a_visitor.exceptions[0])
        == "Operation name < getName > should be unique."
    )
    assert a_visitor.exceptions[0].locations == [
        Location(1, 1, 1, 2),
        Location(2, 1, 2, 2),
    ]


@pytest.mark.parametrize(
    "named_operations,anonymous_operations,nb_errors",
    [
        (
            {
                "getName": NodeDefinition(
                    None, None, Location(1, 1, 1, 2), "getName"
                )
            },
            [],
            0,
        ),
        (
            {
                "getName": NodeDefinition(
                    None, None, Location(1, 1, 1, 2), "getName"
                )
            },
            [NodeDefinition(None, None, Location(2, 1, 2, 2), None)],
            1,
        ),
        (
            {},
            [
                NodeDefinition(None, None, Location(2, 1, 2, 2), None),
                NodeDefinition(None, None, Location(2, 1, 2, 2), None),
            ],
            2,
        ),
    ],
)
def test_on_document_out_unused_fragment(
    a_visitor, named_operations, anonymous_operations, nb_errors
):
    a_visitor._named_operations = named_operations
    a_visitor._anonymous_operations = anonymous_operations

    a_visitor._on_document_out()

    assert len(a_visitor.exceptions) == nb_errors
    for exception, operation in zip(
        a_visitor.exceptions, anonymous_operations
    ):
        assert isinstance(exception, NotLoneAnonymousOperation)
        assert (
            str(exception)
            == "Anonymous operation must be the only defined operation."
        )
        assert exception.locations == [operation.location]


@pytest.mark.parametrize(
    "operation_type,selections_size,depth,has_error",
    [
        ("Query", 4, 0, False),
        ("Mutation", 4, 0, False),
        ("Subscription", 1, 0, False),
        ("Subscription", 2, 1, False),
        ("Subscription", 2, 0, True),
    ],
)
def test_on_selection_set_in(
    a_visitor, an_element, operation_type, selections_size, depth, has_error
):
    location = Location(1, 1, 1, 2)
    a_visitor._internal_ctx.field_path = []
    for i in range(0, depth):
        a_visitor._internal_ctx.field_path.append(str(i))

    a_visitor._internal_ctx.operation = Mock(location=location)
    a_visitor._internal_ctx.operation.type = operation_type
    an_element.get_selections_size = Mock(return_value=selections_size)

    a_visitor._on_selection_set_in(an_element)

    if not has_error:
        assert a_visitor.exceptions == []
    else:
        assert len(a_visitor.exceptions) == 1
        assert isinstance(
            a_visitor.exceptions[0], MultipleRootNodeOnSubscriptionOperation
        )
        assert (
            str(a_visitor.exceptions[0])
            == "Subscription operations must have exactly one root field."
        )
        assert a_visitor.exceptions[0].locations == [location]
