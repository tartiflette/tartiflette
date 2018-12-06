import os
from functools import partial

from cffi import FFI

from tartiflette.types.location import Location

## TODO automatize read from headers files

CDEFS_LIBGRAPHQL = """
/**
 * This file provides C wrappers for ../GraphQLParser.h.
 */

struct GraphQLAstNode;

/**
 * Parse the given GraphQL source string, returning an AST. Returns
 * NULL on error. Return value must be freed with
 * graphql_node_free(). If NULL is returned and error is not NULL, an
 * error message is placed in error and must be freed with
 * graphql_error_free().
 */
struct GraphQLAstNode *graphql_parse_string(
    const char *text, const char **error);

struct GraphQLAstNode *graphql_parse_string_with_experimental_schema_support(
    const char *text, const char **error);

/**
 * Read and parse GraphQL source from the given file, returning an
 * AST. Returns nullptr on error. Return value must be freed with
 * graphql_node_free(). If NULL is returned and error is not NULL, an
 * error message is placed in error and must be freed with
 * graphql_error_free().
 */
struct GraphQLAstNode *graphql_parse_file(FILE *file, const char **error);

struct GraphQLAstNode *graphql_parse_file_with_experimental_schema_support(
    FILE *file, const char **error);

/**
 * Frees an error.
 */
void graphql_error_free(const char *error);

/* A location in the AST. */
struct GraphQLAstLocation {
  unsigned int beginLine;
  unsigned int beginColumn;
  unsigned int endLine;
  unsigned int endColumn;
};

/* Fills location with location information for the given node. */
void graphql_node_get_location(const struct GraphQLAstNode *node,
                               struct GraphQLAstLocation *location);

void graphql_node_free(struct GraphQLAstNode *node);



struct GraphQLAstDefinition;

struct GraphQLAstDocument;
int GraphQLAstDocument_get_definitions_size(const struct GraphQLAstDocument *node);

struct GraphQLAstOperationDefinition;
const char * GraphQLAstOperationDefinition_get_operation(const struct GraphQLAstOperationDefinition *node);
const struct GraphQLAstName * GraphQLAstOperationDefinition_get_name(const struct GraphQLAstOperationDefinition *node);
int GraphQLAstOperationDefinition_get_variable_definitions_size(const struct GraphQLAstOperationDefinition *node);
int GraphQLAstOperationDefinition_get_directives_size(const struct GraphQLAstOperationDefinition *node);
const struct GraphQLAstSelectionSet * GraphQLAstOperationDefinition_get_selection_set(const struct GraphQLAstOperationDefinition *node);

struct GraphQLAstVariableDefinition;
const struct GraphQLAstVariable * GraphQLAstVariableDefinition_get_variable(const struct GraphQLAstVariableDefinition *node);
const struct GraphQLAstType * GraphQLAstVariableDefinition_get_type(const struct GraphQLAstVariableDefinition *node);
const struct GraphQLAstValue * GraphQLAstVariableDefinition_get_default_value(const struct GraphQLAstVariableDefinition *node);

struct GraphQLAstSelectionSet;
int GraphQLAstSelectionSet_get_selections_size(const struct GraphQLAstSelectionSet *node);

struct GraphQLAstSelection;

struct GraphQLAstField;
const struct GraphQLAstName * GraphQLAstField_get_alias(const struct GraphQLAstField *node);
const struct GraphQLAstName * GraphQLAstField_get_name(const struct GraphQLAstField *node);
int GraphQLAstField_get_arguments_size(const struct GraphQLAstField *node);
int GraphQLAstField_get_directives_size(const struct GraphQLAstField *node);
const struct GraphQLAstSelectionSet * GraphQLAstField_get_selection_set(const struct GraphQLAstField *node);

struct GraphQLAstArgument;
const struct GraphQLAstName * GraphQLAstArgument_get_name(const struct GraphQLAstArgument *node);
const struct GraphQLAstValue * GraphQLAstArgument_get_value(const struct GraphQLAstArgument *node);

struct GraphQLAstFragmentSpread;
const struct GraphQLAstName * GraphQLAstFragmentSpread_get_name(const struct GraphQLAstFragmentSpread *node);
int GraphQLAstFragmentSpread_get_directives_size(const struct GraphQLAstFragmentSpread *node);

struct GraphQLAstInlineFragment;
const struct GraphQLAstNamedType * GraphQLAstInlineFragment_get_type_condition(const struct GraphQLAstInlineFragment *node);
int GraphQLAstInlineFragment_get_directives_size(const struct GraphQLAstInlineFragment *node);
const struct GraphQLAstSelectionSet * GraphQLAstInlineFragment_get_selection_set(const struct GraphQLAstInlineFragment *node);

struct GraphQLAstFragmentDefinition;
const struct GraphQLAstName * GraphQLAstFragmentDefinition_get_name(const struct GraphQLAstFragmentDefinition *node);
const struct GraphQLAstNamedType * GraphQLAstFragmentDefinition_get_type_condition(const struct GraphQLAstFragmentDefinition *node);
int GraphQLAstFragmentDefinition_get_directives_size(const struct GraphQLAstFragmentDefinition *node);
const struct GraphQLAstSelectionSet * GraphQLAstFragmentDefinition_get_selection_set(const struct GraphQLAstFragmentDefinition *node);

struct GraphQLAstValue;

struct GraphQLAstVariable;
const struct GraphQLAstName * GraphQLAstVariable_get_name(const struct GraphQLAstVariable *node);

struct GraphQLAstIntValue;
const char * GraphQLAstIntValue_get_value(const struct GraphQLAstIntValue *node);

struct GraphQLAstFloatValue;
const char * GraphQLAstFloatValue_get_value(const struct GraphQLAstFloatValue *node);

struct GraphQLAstStringValue;
const char * GraphQLAstStringValue_get_value(const struct GraphQLAstStringValue *node);

struct GraphQLAstBooleanValue;
int GraphQLAstBooleanValue_get_value(const struct GraphQLAstBooleanValue *node);

struct GraphQLAstNullValue;

struct GraphQLAstEnumValue;
const char * GraphQLAstEnumValue_get_value(const struct GraphQLAstEnumValue *node);

struct GraphQLAstListValue;
int GraphQLAstListValue_get_values_size(const struct GraphQLAstListValue *node);

struct GraphQLAstObjectValue;
int GraphQLAstObjectValue_get_fields_size(const struct GraphQLAstObjectValue *node);

struct GraphQLAstObjectField;
const struct GraphQLAstName * GraphQLAstObjectField_get_name(const struct GraphQLAstObjectField *node);
const struct GraphQLAstValue * GraphQLAstObjectField_get_value(const struct GraphQLAstObjectField *node);

struct GraphQLAstDirective;
const struct GraphQLAstName * GraphQLAstDirective_get_name(const struct GraphQLAstDirective *node);
int GraphQLAstDirective_get_arguments_size(const struct GraphQLAstDirective *node);

struct GraphQLAstType;

struct GraphQLAstNamedType;
const struct GraphQLAstName * GraphQLAstNamedType_get_name(const struct GraphQLAstNamedType *node);

struct GraphQLAstListType;
const struct GraphQLAstType * GraphQLAstListType_get_type(const struct GraphQLAstListType *node);

struct GraphQLAstNonNullType;
const struct GraphQLAstType * GraphQLAstNonNullType_get_type(const struct GraphQLAstNonNullType *node);

struct GraphQLAstName;
const char * GraphQLAstName_get_value(const struct GraphQLAstName *node);

struct GraphQLAstSchemaDefinition;
int GraphQLAstSchemaDefinition_get_directives_size(const struct GraphQLAstSchemaDefinition *node);
int GraphQLAstSchemaDefinition_get_operation_types_size(const struct GraphQLAstSchemaDefinition *node);

struct GraphQLAstOperationTypeDefinition;
const char * GraphQLAstOperationTypeDefinition_get_operation(const struct GraphQLAstOperationTypeDefinition *node);
const struct GraphQLAstNamedType * GraphQLAstOperationTypeDefinition_get_type(const struct GraphQLAstOperationTypeDefinition *node);

struct GraphQLAstScalarTypeDefinition;
const struct GraphQLAstName * GraphQLAstScalarTypeDefinition_get_name(const struct GraphQLAstScalarTypeDefinition *node);
int GraphQLAstScalarTypeDefinition_get_directives_size(const struct GraphQLAstScalarTypeDefinition *node);

struct GraphQLAstObjectTypeDefinition;
const struct GraphQLAstName * GraphQLAstObjectTypeDefinition_get_name(const struct GraphQLAstObjectTypeDefinition *node);
int GraphQLAstObjectTypeDefinition_get_interfaces_size(const struct GraphQLAstObjectTypeDefinition *node);
int GraphQLAstObjectTypeDefinition_get_directives_size(const struct GraphQLAstObjectTypeDefinition *node);
int GraphQLAstObjectTypeDefinition_get_fields_size(const struct GraphQLAstObjectTypeDefinition *node);

struct GraphQLAstFieldDefinition;
const struct GraphQLAstName * GraphQLAstFieldDefinition_get_name(const struct GraphQLAstFieldDefinition *node);
int GraphQLAstFieldDefinition_get_arguments_size(const struct GraphQLAstFieldDefinition *node);
const struct GraphQLAstType * GraphQLAstFieldDefinition_get_type(const struct GraphQLAstFieldDefinition *node);
int GraphQLAstFieldDefinition_get_directives_size(const struct GraphQLAstFieldDefinition *node);

struct GraphQLAstInputValueDefinition;
const struct GraphQLAstName * GraphQLAstInputValueDefinition_get_name(const struct GraphQLAstInputValueDefinition *node);
const struct GraphQLAstType * GraphQLAstInputValueDefinition_get_type(const struct GraphQLAstInputValueDefinition *node);
const struct GraphQLAstValue * GraphQLAstInputValueDefinition_get_default_value(const struct GraphQLAstInputValueDefinition *node);
int GraphQLAstInputValueDefinition_get_directives_size(const struct GraphQLAstInputValueDefinition *node);

struct GraphQLAstInterfaceTypeDefinition;
const struct GraphQLAstName * GraphQLAstInterfaceTypeDefinition_get_name(const struct GraphQLAstInterfaceTypeDefinition *node);
int GraphQLAstInterfaceTypeDefinition_get_directives_size(const struct GraphQLAstInterfaceTypeDefinition *node);
int GraphQLAstInterfaceTypeDefinition_get_fields_size(const struct GraphQLAstInterfaceTypeDefinition *node);

struct GraphQLAstUnionTypeDefinition;
const struct GraphQLAstName * GraphQLAstUnionTypeDefinition_get_name(const struct GraphQLAstUnionTypeDefinition *node);
int GraphQLAstUnionTypeDefinition_get_directives_size(const struct GraphQLAstUnionTypeDefinition *node);
int GraphQLAstUnionTypeDefinition_get_types_size(const struct GraphQLAstUnionTypeDefinition *node);

struct GraphQLAstEnumTypeDefinition;
const struct GraphQLAstName * GraphQLAstEnumTypeDefinition_get_name(const struct GraphQLAstEnumTypeDefinition *node);
int GraphQLAstEnumTypeDefinition_get_directives_size(const struct GraphQLAstEnumTypeDefinition *node);
int GraphQLAstEnumTypeDefinition_get_values_size(const struct GraphQLAstEnumTypeDefinition *node);

struct GraphQLAstEnumValueDefinition;
const struct GraphQLAstName * GraphQLAstEnumValueDefinition_get_name(const struct GraphQLAstEnumValueDefinition *node);
int GraphQLAstEnumValueDefinition_get_directives_size(const struct GraphQLAstEnumValueDefinition *node);

struct GraphQLAstInputObjectTypeDefinition;
const struct GraphQLAstName * GraphQLAstInputObjectTypeDefinition_get_name(const struct GraphQLAstInputObjectTypeDefinition *node);
int GraphQLAstInputObjectTypeDefinition_get_directives_size(const struct GraphQLAstInputObjectTypeDefinition *node);
int GraphQLAstInputObjectTypeDefinition_get_fields_size(const struct GraphQLAstInputObjectTypeDefinition *node);

struct GraphQLAstTypeExtensionDefinition;
const struct GraphQLAstObjectTypeDefinition * GraphQLAstTypeExtensionDefinition_get_definition(const struct GraphQLAstTypeExtensionDefinition *node);

struct GraphQLAstDirectiveDefinition;
const struct GraphQLAstName * GraphQLAstDirectiveDefinition_get_name(const struct GraphQLAstDirectiveDefinition *node);
int GraphQLAstDirectiveDefinition_get_arguments_size(const struct GraphQLAstDirectiveDefinition *node);
int GraphQLAstDirectiveDefinition_get_locations_size(const struct GraphQLAstDirectiveDefinition *node);

struct GraphQLAstVisitorCallbacks;

/**
 * Walk the AST rooted at the given node, issuing callbacks from the given
 * callbacks struct as appropriate. userData will be passed as the userData
 * argument to each callback.
 */
void graphql_node_visit(const struct GraphQLAstNode *node,
                        const struct GraphQLAstVisitorCallbacks *callbacks,
                        void *userData);



const char *graphql_ast_to_json(const struct GraphQLAstNode *node);
"""

TYPES_LIBGRAPHQL = [
    ["Document", "document"],
    ["OperationDefinition", "operation_definition"],
    ["VariableDefinition", "variable_definition"],
    ["SelectionSet", "selection_set"],
    ["Field", "field"],
    ["Argument", "argument"],
    ["FragmentSpread", "fragment_spread"],
    ["InlineFragment", "inline_fragment"],
    ["FragmentDefinition", "fragment_definition"],
    ["Variable", "variable"],
    ["IntValue", "int_value"],
    ["FloatValue", "float_value"],
    ["StringValue", "string_value"],
    ["BooleanValue", "boolean_value"],
    ["NullValue", "null_value"],
    ["EnumValue", "enum_value"],
    ["ListValue", "list_value"],
    ["ObjectValue", "object_value"],
    ["ObjectField", "object_field"],
    ["Directive", "directive"],
    ["NamedType", "named_type"],
    ["ListType", "list_type"],
    ["NonNullType", "non_null_type"],
    ["Name", "name"],
    ["SchemaDefinition", "schema_definition"],
    ["OperationTypeDefinition", "operation_type_definition"],
    ["ScalarTypeDefinition", "scalar_type_definition"],
    ["ObjectTypeDefinition", "object_type_definition"],
    ["FieldDefinition", "field_definition"],
    ["InputValueDefinition", "input_value_definition"],
    ["InterfaceTypeDefinition", "interface_type_definition"],
    ["UnionTypeDefinition", "union_type_definition"],
    ["EnumTypeDefinition", "enum_type_definition"],
    ["EnumValueDefinition", "enum_value_definition"],
    ["InputObjectTypeDefinition", "input_object_type_definition"],
    ["TypeExtensionDefinition", "type_extension_definition"],
    ["DirectiveDefinition", "directive_definition"],
]

## Doing all this cause the macro definitions directly in cffi doesn't works
_CDEF_LIBGRAPHQL_CALLBACK_STRUCTS = ""

for typ in TYPES_LIBGRAPHQL:
    CDEFS_LIBGRAPHQL = (
        CDEFS_LIBGRAPHQL + "\ntypedef int (*visit_{st}_func)(const struct "
        "GraphQLAst{t} *{st}, void *user_data);".format(st=typ[1], t=typ[0])
    )
    CDEFS_LIBGRAPHQL = (
        CDEFS_LIBGRAPHQL
        + "\ntypedef void (*end_visit_{st}_func)(const struct "
        "GraphQLAst{t} *{st}, void *user_data);".format(st=typ[1], t=typ[0])
    )

    _CDEF_LIBGRAPHQL_CALLBACK_STRUCTS = (
        _CDEF_LIBGRAPHQL_CALLBACK_STRUCTS
        + "visit_{st}_func visit_{st}; \n".format(st=typ[1])
    )
    _CDEF_LIBGRAPHQL_CALLBACK_STRUCTS = (
        _CDEF_LIBGRAPHQL_CALLBACK_STRUCTS
        + "end_visit_{st}_func end_visit_{st}; \n".format(st=typ[1])
    )

_CDEF_LIBGRAPHQL_CALLBACK_STRUCTS = (
    """
struct GraphQLAstVisitorCallbacks {
%s
};
"""
    % _CDEF_LIBGRAPHQL_CALLBACK_STRUCTS
)

CDEFS_LIBGRAPHQL = CDEFS_LIBGRAPHQL + _CDEF_LIBGRAPHQL_CALLBACK_STRUCTS


class _ParsedData:
    def __init__(self, c_parsed, destroy_cb):
        self._c_parsed = c_parsed
        self._destroy_cb = destroy_cb

    def __enter__(self):
        return self._c_parsed

    def __exit__(self, exc_type, exc_value, traceback):
        self._destroy_cb(self._c_parsed)


class Visitor:
    IN = 0
    OUT = 1
    UKN = 2

    def __init__(self):
        self.event = self.UKN
        self.continue_child = 1


class _VisitorElement:
    def __init__(self, lib, ffi, libgraphql_type, internal_element):
        self._lib = lib
        self._ffi = ffi
        self._internal_element = internal_element
        self.libgraphql_type = libgraphql_type
        self.name = None
        try:
            self.name = self._get_name()
        except AttributeError:
            pass

    def _get_name_object(self):
        if self._internal_element != self._ffi.NULL:
            return self._lib.__getattr__(
                "GraphQLAst%s_get_name" % self.libgraphql_type
            )(self._internal_element)
        return self._ffi.NULL

    def _get_name_string(self, name_object):
        if self._ffi.NULL != name_object:
            return self._from_char_to_string(
                self._lib.GraphQLAstName_get_value(name_object)
            )
        return None

    def _from_char_to_string(self, val):
        return self._ffi.string(val).decode("UTF-8", "replace")

    def _get_name(self):
        element = self._internal_element
        if self.libgraphql_type != "Name":
            element = self._get_name_object()

        return self._get_name_string(element)

    def get_location(self):
        location = self._ffi.new("struct GraphQLAstLocation *")
        self._lib.graphql_node_get_location(
            self._ffi.cast("struct GraphQLAstNode *", self._internal_element),
            location,
        )
        return Location(
            location.beginLine,
            location.beginColumn,
            location.endLine,
            location.endColumn,
        )


class _VisitorElementIntValue(_VisitorElement):
    def __init__(self, lib, ffi, internal_element):
        super().__init__(lib, ffi, "IntValue", internal_element)

    def get_value(self):
        val = self._from_char_to_string(
            self._lib.GraphQLAstIntValue_get_value(self._internal_element)
        )
        return int(val)


class _VisitorElementStringValue(_VisitorElement):
    def __init__(self, lib, ffi, internal_element):
        super().__init__(lib, ffi, "StringValue", internal_element)

    def get_value(self):
        val = self._lib.GraphQLAstStringValue_get_value(self._internal_element)
        return self._from_char_to_string(val)


class _VisitorElementFloatValue(_VisitorElement):
    def __init__(self, lib, ffi, internal_element):
        super().__init__(lib, ffi, "FloatValue", internal_element)

    def get_value(self):
        val = self._from_char_to_string(
            self._lib.GraphQLAstFloatValue_get_value(self._internal_element)
        )
        return float(val)


class _VisitorElementBooleanValue(_VisitorElement):
    def __init__(self, lib, ffi, internal_element):
        super().__init__(lib, ffi, "BooleanValue", internal_element)
        self._values = [False, True]

    def get_value(self):
        val = self._lib.GraphQLAstBooleanValue_get_value(
            self._internal_element
        )
        return self._values[val]


class _VisitorElementFragmentDefinition(_VisitorElement):
    def __init__(self, lib, ffi, internal_element):
        super().__init__(lib, ffi, "FragmentDefinition", internal_element)

    def get_type_condition(self):
        name_type = self._lib.GraphQLAstFragmentDefinition_get_type_condition(
            self._internal_element
        )
        if name_type != self._ffi.NULL:
            return self._get_name_string(
                self._lib.GraphQLAstNamedType_get_name(name_type)
            )

        return None


class _VisitorElementOperationDefinition(_VisitorElement):
    def __init__(self, lib, ffi, internal_element):
        super().__init__(lib, ffi, "OperationDefinition", internal_element)

    def get_operation(self):
        return self._from_char_to_string(
            self._lib.GraphQLAstOperationDefinition_get_operation(
                self._internal_element
            )
        ).capitalize()


class _VisitorElementField(_VisitorElement):
    def __init__(self, lib, ffi, internal_element):
        super().__init__(lib, ffi, "Field", internal_element)

    def get_alias(self):
        return self._get_name_string(
            self._lib.GraphQLAstField_get_alias(self._internal_element)
        )


class _VisitorElementInlineFragment(_VisitorElement):
    def __init__(self, lib, ffi, internal_element):
        super().__init__(lib, ffi, "InlineFragment", internal_element)

    def get_named_type(self):
        return self._get_name_string(
            self._lib.GraphQLAstNamedType_get_name(
                self._lib.GraphQLAstInlineFragment_get_type_condition(
                    self._internal_element
                )
            )
        )


_LIBGRAPHQL_TYPE_TO_CLASS = {
    "IntValue": _VisitorElementIntValue,
    "StringValue": _VisitorElementStringValue,
    "FloatValue": _VisitorElementFloatValue,
    "BooleanValue": _VisitorElementBooleanValue,
    "FragmentDefinition": _VisitorElementFragmentDefinition,
    "OperationDefinition": _VisitorElementOperationDefinition,
    "Field": _VisitorElementField,
    "InlineFragment": _VisitorElementInlineFragment,
}


class LibGraphqlParser:
    def __init__(self):
        self._ffi = FFI()
        self._ffi.cdef(CDEFS_LIBGRAPHQL)

        # TODO use importlib.resource in Python3.7
        self._lib_dir = os.path.dirname(__file__)
        try:
            self._lib = self._ffi.dlopen(
                "%s/libgraphqlparser.so" % self._lib_dir
            )
        except OSError:
            self._lib = self._ffi.dlopen(
                "%s/libgraphqlparser.dylib" % self._lib_dir
            )
        self._lib_callbacks = self._ffi.new(
            "struct GraphQLAstVisitorCallbacks *"
        )
        self._errors = self._ffi.new("char **")
        self._callbacks = []
        self._interested_by = {}
        self._default_visitor_cls = Visitor
        self._creates_callbacks()

    def _create_visitor_element(self, libgraphql_type, element):
        try:
            return _LIBGRAPHQL_TYPE_TO_CLASS[libgraphql_type](
                self._lib, self._ffi, element
            )
        except KeyError:
            pass

        return _VisitorElement(self._lib, self._ffi, libgraphql_type, element)

    def _callback_enter(self, libgraphql_type, element, udata):
        context = self._ffi.from_handle(udata)
        context.update(
            Visitor.IN, self._create_visitor_element(libgraphql_type, element)
        )
        return context.continue_child

    def _callback_exit(self, libgraphql_type, element, udata):
        context = self._ffi.from_handle(udata)
        if context.continue_child:
            context.update(
                Visitor.OUT,
                self._create_visitor_element(libgraphql_type, element),
            )

    def _set_callback(self, proto, func, attr):
        c_func = self._ffi.callback(proto)(func)
        # Keep the callbacks alive in this list
        # to keep the underlying cdata alive.
        # because we do it with reflexion and
        # not with decoration
        self._callbacks.append(c_func)
        setattr(self._lib_callbacks, attr, c_func)

    def _set_exit_callback(self, typee):
        self._set_callback(
            "void(struct GraphQLAst%s *, void *)" % typee[0],
            partial(self._callback_exit, typee[0]),
            "end_visit_%s" % typee[1],
        )

    def _set_enter_callback(self, typee):
        self._set_callback(
            "int(struct GraphQLAst%s *, void *)" % typee[0],
            partial(self._callback_enter, typee[0]),
            "visit_%s" % typee[1],
        )

    def _creates_callbacks(self):
        for typee in TYPES_LIBGRAPHQL:
            if typee[0] not in ["Name"]:
                self._set_enter_callback(typee)
                self._set_exit_callback(typee)

    def _parse(self, query):
        if isinstance(query, str):
            # TODO don't replace here.
            query = query.replace("\n", " ").encode("UTF-8")

        c_query = self._ffi.new("char[]", query)
        parsed_data = _ParsedData(
            self._lib.graphql_parse_string(c_query, self._errors),
            self._lib.graphql_node_free,
        )

        if self._errors[0] != self._ffi.NULL:
            # TODO specialize Exception here
            e = Exception(
                self._ffi.string(self._errors[0]).decode("UTF-8", "replace")
            )
            self._lib.graphql_error_free(self._errors[0])
            raise e

        return parsed_data

    def parse_and_visit(self, query, ctx=None):
        if not ctx:
            ctx = self._default_visitor_cls()

        with self._parse(query) as parsed:
            self._lib.graphql_node_visit(
                parsed, self._lib_callbacks, self._ffi.new_handle(ctx)
            )

    def parse_and_jsonify(self, query):
        with self._parse(query) as parsed:
            return self._ffi.string(self._lib.graphql_ast_to_json(parsed))
