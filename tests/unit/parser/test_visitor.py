import pytest
from unittest.mock import Mock


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
    visi._current_node = Mock()
    return visi


def test_parser_visitor_create_node_name(a_visitor):
    assert a_visitor.create_node_name("a", "b") == "a(b)"
    assert a_visitor.create_node_name("a") == "a"


def test_parser_visitor(a_schema):
    from tartiflette.parser.visitor import TartifletteVisitor

    tv = TartifletteVisitor(a_schema)

    assert a_schema == tv.schema
    assert tv._vars == {}

    a_dict = {"A": "B"}

    tv = TartifletteVisitor(a_schema, a_dict)

    assert tv._vars == a_dict


def test_parser_visitor__on_argument(a_visitor, an_element):

    assert a_visitor._current_argument_name is None

    assert a_visitor._on_argument_in(an_element) is None
    assert a_visitor._current_argument_name == "a_name"

    assert a_visitor._on_argument_out(an_element) is None
    assert a_visitor._current_argument_name is None


def test_parser_visitor__on_value_in(a_visitor, an_element):

    a_visitor._current_node = Mock()
    del a_visitor._current_node.default_value
    a_visitor._current_node.arguments = {}
    a_visitor._current_argument_name = "an_argument_name"
    an_element.get_value = Mock(return_value="a_value")

    a_visitor._on_value_in(an_element)

    assert an_element.get_value.called
    assert a_visitor._current_node.arguments == {"an_argument_name": "a_value"}

    a_visitor._current_node.default_value = "a_default_value"

    a_visitor._on_value_in(an_element)

    assert a_visitor._current_node.default_value == "a_value"


def test_parser_visitor__on_variable_in(a_visitor, an_element):
    a_visitor._on_variable_in(an_element)
    assert a_visitor._current_node.var_name == "a_name"


def test_parser_visitor__on_variable_in_no_var_name_ukn_var(
    a_visitor, an_element
):
    from tartiflette.types.exceptions.tartiflette import (
        UnknownVariableException,
    )

    del a_visitor._current_node.var_name

    a_visitor._current_node.arguments = {}
    a_visitor._current_argument_name = "an_argument_name"
    a_visitor._vars = {}

    a_visitor._on_variable_in(an_element)

    assert a_visitor.continue_child == 0
    assert a_visitor.exception is not None
    assert isinstance(a_visitor.exception, UnknownVariableException)


def test_parser_visitor__on_variable_in_no_var_name(a_visitor, an_element):
    from tartiflette.types.exceptions.tartiflette import (
        UnknownVariableException,
    )

    del a_visitor._current_node.var_name

    a_visitor._current_node.arguments = {}
    a_visitor._current_argument_name = "an_argument_name"
    a_visitor._vars = {"a_name": "a_value"}

    a_visitor._on_variable_in(an_element)

    assert a_visitor._current_node.arguments == {"an_argument_name": "a_value"}


def test_parser_visitor__on_field_in_first_field(a_visitor, an_element):
    a_field = Mock()
    a_field.resolver = Mock()

    a_visitor._current_node = None
    a_visitor._operation_type = "an_operation_type"
    a_visitor.schema.get_operation_type = Mock(
        return_value="an_operation_type"
    )
    a_visitor.schema.find_type = Mock(return_value="an_operation_type")
    a_visitor.schema.get_field_by_name = Mock(return_value=a_field)

    a_visitor._on_field_in(an_element)

    assert a_visitor._depth == 1
    assert a_visitor.field_path == ["a_name"]
    assert a_visitor.schema.get_operation_type.call_args_list == [
        (("an_operation_type",),)
    ]
    assert a_visitor.schema.find_type.call_args_list == [
        (("an_operation_type",),)
    ]
    assert a_visitor.schema.get_field_by_name.call_args_list == [
        (("an_operation_type.a_name",),)
    ]
    assert a_visitor._current_node in a_visitor.root_nodes
    assert a_visitor._current_node.parent is None
    assert an_element.get_location.called == 1
    assert an_element.get_alias.called == 1


def test_parser_visitor__on_field_in_another_field(a_visitor, an_element):
    a_field = Mock()
    a_field.resolver = Mock()
    a_visitor._depth = 1
    a_visitor.field_path = ["a_parent_path_element"]
    a_visitor._current_node.field_executor = Mock()
    a_visitor._current_node.add_child = Mock()
    a_visitor._current_node.field_executor.schema_field = Mock()
    a_visitor._current_node.field_executor.schema_field.gql_type = "a_gql_type"
    current_node = a_visitor._current_node
    a_visitor.schema.get_field_by_name = Mock(return_value=a_field)

    a_visitor._on_field_in(an_element)

    assert a_visitor._depth == 2
    assert a_visitor.field_path == ["a_parent_path_element", "a_name"]
    assert a_visitor.schema.get_field_by_name.call_args_list == [
        (("a_gql_type.a_name",),)
    ]
    assert a_visitor._current_node not in a_visitor.root_nodes
    assert a_visitor._current_node.parent is current_node
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
    a_visitor._depth = 1
    a_visitor.field_path = ["a_parent_path_element"]
    a_visitor._current_node.field_executor = Mock()
    a_visitor._current_node.add_child = Mock()
    a_visitor._current_node.field_executor.schema_field = Mock()
    a_visitor._current_node.field_executor.schema_field.gql_type = "a_gql_type"
    a_visitor._inline_fragment_type = "an_inline_fragment_type"
    current_node = a_visitor._current_node

    class _get_field_by_name(MagicMock):
        def __call__(self, aname):
            super().__call__(aname)

            if aname == "a_gql_type.a_name":
                raise UnknownSchemaFieldResolver("a_message")

            return a_field

    a_visitor.schema.get_field_by_name = _get_field_by_name()

    a_visitor._on_field_in(an_element)

    assert a_visitor._depth == 2
    assert a_visitor.field_path == ["a_parent_path_element", "a_name"]
    assert a_visitor.schema.get_field_by_name.call_args_list == [
        (("a_gql_type.a_name",),),
        (("an_inline_fragment_type.a_name",),),
    ]
    assert a_visitor._current_node not in a_visitor.root_nodes
    assert a_visitor._current_node.parent is current_node
    assert an_element.get_location.called == 1
    assert an_element.get_alias.called == 1
    assert current_node.add_child.called == 1


def test_parser_visitor__on_field_unknow_schema_field(a_visitor, an_element):
    from tartiflette.types.exceptions.tartiflette import (
        UnknownSchemaFieldResolver,
    )
    from unittest.mock import MagicMock

    a_visitor._depth = 1
    a_visitor.field_path = ["a_parent_path_element"]
    a_visitor._current_node.field_executor = Mock()
    a_visitor._current_node.add_child = Mock()
    a_visitor._current_node.field_executor.schema_field = Mock()
    a_visitor._current_node.field_executor.schema_field.gql_type = "a_gql_type"
    a_visitor._inline_fragment_type = "an_inline_fragment_type"
    current_node = a_visitor._current_node

    an_exception = UnknownSchemaFieldResolver("a_message")

    class _get_field_by_name(MagicMock):
        def __call__(self, aname):
            super().__call__(aname)
            raise an_exception

    a_visitor.schema.get_field_by_name = _get_field_by_name()

    a_visitor._on_field_in(an_element)

    assert a_visitor._depth == 2
    assert a_visitor.field_path == ["a_parent_path_element", "a_name"]
    assert a_visitor.schema.get_field_by_name.call_args_list == [
        (("a_gql_type.a_name",),),
        (("an_inline_fragment_type.a_name",),),
    ]
    assert a_visitor._current_node not in a_visitor.root_nodes
    assert a_visitor.continue_child == 0
    assert a_visitor.exception == an_exception


def test_parser_visitor__on_field_out(a_visitor, an_element):
    a_visitor._depth = 2
    a_visitor.field_path = ["a", "b"]
    a_visitor._current_node.parent = "LOL"

    a_visitor._on_field_out(an_element)

    assert a_visitor._depth == 1
    assert a_visitor.field_path == ["a"]
    assert a_visitor._current_node == "LOL"


def test_parser_visitor__on_variable_definition_in(a_visitor, an_element):
    current_node = a_visitor._current_node

    a_visitor._on_variable_definition_in(an_element)

    assert a_visitor._current_node != current_node
    assert a_visitor._current_node.parent == current_node


def test_parser_visitor__validate_type(a_visitor, an_element):
    a_visitor._validate_type("ninja", "a", str)

    assert a_visitor.exception is None
    assert a_visitor.continue_child == 1

    a_visitor._validate_type("ntm", "a", int)
    assert a_visitor.exception is not None
    assert isinstance(a_visitor.exception, TypeError)
    assert a_visitor.continue_child == 0


def test_parser_visitor__validate_type_invalid_type_dont_care(
    a_visitor, an_element
):
    a_visitor._validate_type("ninja", "a", None)

    assert a_visitor.exception is None
    assert a_visitor.continue_child == 1


def test_parser_visitor__validate_vars_existing_okay_var(
    a_visitor, an_element
):
    a_visitor._current_node.var_name = "LOL"
    a_visitor._current_node.var_type = str
    a_visitor._current_node.is_list = False

    a_visitor._vars = {"LOL": "a_value"}

    a_visitor._validate_type = Mock()

    a_visitor._validates_vars()

    assert a_visitor._validate_type.call_args_list == [
        (("LOL", "a_value", str),)
    ]


def test_parser_visitor__validate_vars_existing_okay_var_is_list(
    a_visitor, an_element
):
    a_visitor._current_node.var_name = "LOL"
    a_visitor._current_node.var_type = str
    a_visitor._current_node.is_list = True

    a_visitor._vars = {"LOL": ["a_value_1", "a_value_2"]}

    a_visitor._validate_type = Mock()

    a_visitor._validates_vars()

    assert a_visitor._validate_type.call_args_list == [
        (("LOL", "a_value_1", str),),
        (("LOL", "a_value_2", str),),
    ]


def test_parser_visitor__validate_vars_existing_okay_var_is_list_nok(
    a_visitor, an_element
):
    a_visitor._current_node.var_name = "LOL"
    a_visitor._current_node.var_type = str
    a_visitor._current_node.is_list = True

    a_visitor._vars = {"LOL": "a_value_1"}

    a_visitor._validate_type = Mock()

    a_visitor._validates_vars()

    assert a_visitor.continue_child == 0
    assert a_visitor.exception is not None
    assert isinstance(a_visitor.exception, TypeError)


def test_parser_visitor__validate_vars_existing_okay_var_has_a_dfv(
    a_visitor, an_element
):
    a_visitor._current_node.var_name = "LOL"
    a_visitor._current_node.var_type = str
    a_visitor._current_node.default_value = "a_default_value"

    a_visitor._validate_type = Mock()

    a_visitor._validates_vars()

    assert a_visitor._vars == {"LOL": "a_default_value"}


def test_parser_visitor__validate_vars_existing_okay_var_no_dfv_but_nullable(
    a_visitor, an_element
):
    a_visitor._current_node.var_name = "LOL"
    a_visitor._current_node.var_type = str
    a_visitor._current_node.is_nullable = True
    a_visitor._current_node.default_value = None
    a_visitor._validate_type = Mock()

    a_visitor._validates_vars()

    assert a_visitor._vars == {"LOL": None}


def test_parser_visitor__validate_vars_existing_okay_var_no_dfv_non_nullable(
    a_visitor, an_element
):
    from tartiflette.types.exceptions.tartiflette import (
        UnknownVariableException,
    )

    a_visitor._current_node.var_name = "LOL"
    a_visitor._current_node.var_type = str
    a_visitor._current_node.is_nullable = False
    a_visitor._current_node.default_value = None
    a_visitor._validate_type = Mock()

    a_visitor._validates_vars()

    assert a_visitor.continue_child == 0
    assert a_visitor.exception is not None
    assert isinstance(a_visitor.exception, UnknownVariableException)


def test_parser_visitor__on_variable_definition_out(a_visitor, an_element):
    a_visitor._validates_vars = Mock()

    current_node = a_visitor._current_node
    a_visitor._current_node.parent = Mock()

    a_visitor._on_variable_definition_out(an_element)

    assert a_visitor._validates_vars.called
    assert a_visitor._current_node != current_node
    assert a_visitor._current_node == current_node.parent


def test_parser_visitor__on_named_type_in_ok(a_visitor, an_element):
    a_visitor._on_named_type_in(an_element)
    assert a_visitor._current_node.var_type == "a_name"


def test_parser_visitor__on_named_type_in_nok(a_visitor, an_element):
    del a_visitor._current_node

    assert a_visitor._on_named_type_in(an_element) is None


def test_parser_visitor__on_list_type_in_ok(a_visitor, an_element):
    a_visitor._on_list_type_in(an_element)
    assert a_visitor._current_node.is_list == True


def test_parser_visitor__on_list_type_in_nok(a_visitor, an_element):
    del a_visitor._current_node

    assert a_visitor._on_list_type_in(an_element) is None


def test_parser_visitor__on_non_null_type_in(a_visitor, an_element):
    a_visitor._on_non_null_type_in(an_element)
    assert a_visitor._current_node.is_nullable == False


def test_parser_visitor__on_fragment_definition_in(a_visitor, an_element):
    an_element.get_type_condition = Mock(return_value="a_type_condition")

    a_visitor._on_fragment_definition_in(an_element)

    assert a_visitor._current_fragment_definition is not None
    assert (
        a_visitor._fragments["a_name"]
        == a_visitor._current_fragment_definition
    )


def test_parser_visitor__on_fragment_definition_in_already_know_fragment(
    a_visitor, an_element
):
    from tartiflette.types.exceptions.tartiflette import TartifletteException

    an_element.get_type_condition = Mock(return_value="a_type_condition")

    a_visitor._fragments["a_name"] = Mock()
    a_visitor._on_fragment_definition_in(an_element)

    assert a_visitor.continue_child == 0
    assert a_visitor.exception is not None
    assert isinstance(a_visitor.exception, TartifletteException)


def test_parser_visitor__on_fragment_definition_out(a_visitor, an_element):
    a_visitor._on_fragment_definition_out(an_element)
    assert a_visitor._current_fragment_definition is None


def test_parser_visitor__on_fragment_spread_out(a_visitor, an_element):
    frag_def = Mock()
    frag_def.type_condition = Mock()
    frag_def.callbacks = [Mock(), Mock()]
    a_visitor._fragments["a_name"] = frag_def

    a_visitor._on_fragment_spread_out(an_element)

    assert a_visitor._current_type_condition is None
    for m in frag_def.callbacks:
        assert m.called


def test_parser_visitor__on_operation_definition_in(a_visitor, an_element):
    an_operation = Mock()
    an_element.get_operation = Mock(return_value=an_operation)

    assert a_visitor._operation_type is None
    a_visitor._on_operation_definition_in(an_element)
    assert a_visitor._operation_type == an_operation


def test_parser_visitor__on_operation_definition_out(a_visitor, an_element):
    a_visitor._operation_type = Mock()
    a_visitor._on_operation_definition_out(an_element)
    assert a_visitor._operation_type is None


def test_parser_visitor__on_inline_fragment_in(a_visitor, an_element):
    an_element.get_named_type = Mock(return_value="a_named_type")

    assert a_visitor._inline_fragment_type is None
    assert a_visitor._current_type_condition is None

    a_visitor._on_inline_fragment_in(an_element)

    assert a_visitor._inline_fragment_type == "a_named_type"
    assert a_visitor._current_type_condition == "a_named_type"


def test_parser_visitor__on_inline_fragment_out(a_visitor, an_element):
    a_visitor._inline_fragment_type = Mock()
    a_visitor._current_type_condition = Mock()

    a_visitor._on_inline_fragment_out(an_element)

    assert a_visitor._inline_fragment_type is None
    assert a_visitor._current_type_condition is None


def test_parser_visitor__in(a_visitor, an_element):
    a_visitor.path = "/NTM"
    an_element.libgraphql_type = "LOL"
    a_callback = Mock()
    a_visitor._events[a_visitor.IN]["LOL"] = a_callback

    a_visitor._in(an_element)

    assert a_visitor.path == "/NTM/LOL(a_name)"
    assert a_callback.called


def test_parser_visitor__in_no_callback(a_visitor, an_element):
    a_visitor.path = "/NTM"
    an_element.libgraphql_type = "LOL"

    assert a_visitor._in(an_element) is None
    assert a_visitor.path == "/NTM/LOL(a_name)"


def test_parser_visitor__out(a_visitor, an_element):
    a_visitor.path = "/NTM/LOL(a_name)"
    an_element.libgraphql_type = "LOL"
    a_callback = Mock()
    a_visitor._events[a_visitor.OUT]["LOL"] = a_callback

    a_visitor._out(an_element)

    assert a_visitor.path == "/NTM"
    assert a_callback.called


def test_parser_visitor__out_no_callback(a_visitor, an_element):
    a_visitor.path = "/NTM/LOL(a_name)"
    an_element.libgraphql_type = "LOL"

    assert a_visitor._out(an_element) is None
    assert a_visitor.path == "/NTM"


def test_parser_visitor_update_dont_care(a_visitor, an_element):
    a_visitor.continue_child = 0
    an_element.libgraphql_type = "SelectionSet"
    a_callback = Mock()
    a_visitor._events[a_visitor.IN]["default"] = a_callback

    a_visitor.update(a_visitor.IN, an_element)

    assert a_callback.called is False
    assert a_visitor.continue_child == 1
    assert a_visitor.event == a_visitor.IN


def test_parser_visitor_update(a_visitor, an_element):
    a_visitor.continue_child = 0
    a_visitor.event = None
    a_visitor._current_fragment_definition = None

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
    a_visitor._current_fragment_definition = Mock()
    a_visitor._current_fragment_definition.callbacks = []

    an_element.libgraphql_type = "LOL"
    a_callback = Mock()
    a_visitor._events[a_visitor.IN]["default"] = a_callback

    a_visitor.update(a_visitor.IN, an_element)

    assert a_callback.called is False
    assert a_visitor.continue_child == 1
    assert a_visitor.event == a_visitor.IN
    assert len(a_visitor._current_fragment_definition.callbacks) == 1
