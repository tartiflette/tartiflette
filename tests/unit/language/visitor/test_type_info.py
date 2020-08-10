import os

import pytest

from tartiflette import create_engine
from tartiflette.language.ast import (
    FieldNode,
    NameNode,
    OperationDefinitionNode,
    SelectionSetNode,
)
from tartiflette.language.parsers.libgraphqlparser import parse_to_document
from tartiflette.language.visitor.type_info import (
    TypeInfo,
    WithTypeInfoVisitor,
)
from tartiflette.language.visitor.visit import visit
from tartiflette.language.visitor.visitor import Visitor
from tartiflette.types.helpers.definition import (
    get_wrapped_type,
    is_composite_type,
)

_BASE_DIR = os.path.dirname(__file__)


@pytest.mark.asyncio
async def test_allow_all_methods_to_be_called_before_entering_any_node():
    engine = await create_engine(
        os.path.join(_BASE_DIR, "fixtures", "harness.graphql"),
        schema_name="allow_all_methods_to_be_called_before_entering_any_node",
    )
    type_info = TypeInfo(engine._schema)

    assert type_info.get_type() is None
    assert type_info.get_parent_type() is None
    assert type_info.get_input_type() is None
    assert type_info.get_parent_input_type() is None
    assert type_info.get_field_def() is None
    assert type_info.get_default_value() is None
    assert type_info.get_directive() is None
    assert type_info.get_argument() is None
    assert type_info.get_enum_value() is None


@pytest.mark.asyncio
async def test_visit_with_type_info_supports_different_operation_types():
    engine = await create_engine(
        """
        schema {
          query: QueryRoot
          mutation: MutationRoot
          subscription: SubscriptionRoot
        }
        
        type QueryRoot {
          foo: String
        }
        
        type MutationRoot {
          bar: String
        }
        
        type SubscriptionRoot {
          baz: String
        }
        """,
        schema_name="supports_different_operation_types",
    )

    ast = parse_to_document(
        """
        query { foo }
        mutation { bar }
        subscription { baz }
        """,
        engine._schema,
    )

    class MyVisitor(Visitor):
        def __init__(self, type_info):
            self.type_info = type_info
            self.root_types = {}

        def enter_OperationDefinition(
            self, node, key, parent, path, ancestors
        ):
            self.root_types[node.operation_type] = str(
                self.type_info.get_type()
            )

    type_info = TypeInfo(engine._schema)
    visitor = MyVisitor(type_info)
    visit(ast, WithTypeInfoVisitor(type_info, visitor))
    assert visitor.root_types == {
        "query": "QueryRoot",
        "mutation": "MutationRoot",
        "subscription": "SubscriptionRoot",
    }


@pytest.mark.asyncio
async def test_visit_with_type_info_provide_exact_same_arguments_to_wrapped_visitor():
    class MyVisitor(Visitor):
        def __init__(self):
            self.visitor_args = []

        def enter(self, node, key, parent, path, ancestors):
            self.visitor_args.append(
                ("enter", node, key, parent, path, ancestors)
            )

        def leave(self, node, key, parent, path, ancestors):
            self.visitor_args.append(
                ("leave", node, key, parent, path, ancestors)
            )

    engine = await create_engine(
        os.path.join(_BASE_DIR, "fixtures", "harness.graphql"),
        schema_name="provide_exact_same_arguments_to_wrapped_visitor",
    )

    ast = parse_to_document(
        "{ human(id: 4) { name, pets { ... { name } }, unknown } }",
        engine._schema,
    )

    visitor = MyVisitor()
    wrapped_visitor = MyVisitor()
    visit(ast, visitor)
    visit(ast, WithTypeInfoVisitor(TypeInfo(engine._schema), wrapped_visitor))
    assert visitor.visitor_args == wrapped_visitor.visitor_args


@pytest.mark.asyncio
async def test_visit_with_type_info_maintains_type_info_during_visit():
    engine = await create_engine(
        os.path.join(_BASE_DIR, "fixtures", "harness.graphql"),
        schema_name="maintains_type_info_during_visit",
    )

    class MyVisitor(Visitor):
        def __init__(self, type_info):
            self.type_info = type_info
            self.visited = []

        def enter(self, node, key, parent, path, ancestors):
            parent_type = self.type_info.get_parent_type()
            gql_type = self.type_info.get_type()
            input_type = self.type_info.get_input_type()
            self.visited.append(
                (
                    "enter",
                    node.__class__.__name__,
                    (node.value if isinstance(node, NameNode) else None),
                    str(parent_type) if parent_type else None,
                    str(gql_type) if gql_type else None,
                    str(input_type) if input_type else None,
                )
            )

        def leave(self, node, key, parent, path, ancestors):
            parent_type = self.type_info.get_parent_type()
            gql_type = self.type_info.get_type()
            input_type = self.type_info.get_input_type()
            self.visited.append(
                (
                    "leave",
                    node.__class__.__name__,
                    (node.value if isinstance(node, NameNode) else None),
                    str(parent_type) if parent_type else None,
                    str(gql_type) if gql_type else None,
                    str(input_type) if input_type else None,
                )
            )

    type_info = TypeInfo(engine._schema)
    visitor = MyVisitor(type_info)

    ast = parse_to_document(
        "{ human(id: 4) { name, pets { ... { name } }, unknown } }",
        engine._schema,
    )

    visit(ast, WithTypeInfoVisitor(type_info, visitor))

    assert visitor.visited == [
        ("enter", "DocumentNode", None, None, None, None),
        ("enter", "OperationDefinitionNode", None, None, "QueryRoot", None),
        ("enter", "SelectionSetNode", None, "QueryRoot", "QueryRoot", None),
        ("enter", "FieldNode", None, "QueryRoot", "Human", None),
        ("enter", "NameNode", "human", "QueryRoot", "Human", None),
        ("leave", "NameNode", "human", "QueryRoot", "Human", None),
        ("enter", "ArgumentNode", None, "QueryRoot", "Human", "ID"),
        ("enter", "NameNode", "id", "QueryRoot", "Human", "ID"),
        ("leave", "NameNode", "id", "QueryRoot", "Human", "ID"),
        ("enter", "IntValueNode", None, "QueryRoot", "Human", "ID"),
        ("leave", "IntValueNode", None, "QueryRoot", "Human", "ID"),
        ("leave", "ArgumentNode", None, "QueryRoot", "Human", "ID"),
        ("enter", "SelectionSetNode", None, "Human", "Human", None),
        ("enter", "FieldNode", None, "Human", "String", None),
        ("enter", "NameNode", "name", "Human", "String", None),
        ("leave", "NameNode", "name", "Human", "String", None),
        ("leave", "FieldNode", None, "Human", "String", None),
        ("enter", "FieldNode", None, "Human", "[Pet]", None),
        ("enter", "NameNode", "pets", "Human", "[Pet]", None),
        ("leave", "NameNode", "pets", "Human", "[Pet]", None),
        ("enter", "SelectionSetNode", None, "Pet", "[Pet]", None),
        ("enter", "InlineFragmentNode", None, "Pet", "Pet", None),
        ("enter", "SelectionSetNode", None, "Pet", "Pet", None),
        ("enter", "FieldNode", None, "Pet", "String", None),
        ("enter", "NameNode", "name", "Pet", "String", None),
        ("leave", "NameNode", "name", "Pet", "String", None),
        ("leave", "FieldNode", None, "Pet", "String", None),
        ("leave", "SelectionSetNode", None, "Pet", "Pet", None),
        ("leave", "InlineFragmentNode", None, "Pet", "Pet", None),
        ("leave", "SelectionSetNode", None, "Pet", "[Pet]", None),
        ("leave", "FieldNode", None, "Human", "[Pet]", None),
        ("enter", "FieldNode", None, "Human", None, None),
        ("enter", "NameNode", "unknown", "Human", None, None),
        ("leave", "NameNode", "unknown", "Human", None, None),
        ("leave", "FieldNode", None, "Human", None, None),
        ("leave", "SelectionSetNode", None, "Human", "Human", None),
        ("leave", "FieldNode", None, "QueryRoot", "Human", None),
        ("leave", "SelectionSetNode", None, "QueryRoot", "QueryRoot", None),
        ("leave", "OperationDefinitionNode", None, None, "QueryRoot", None),
        ("leave", "DocumentNode", None, None, None, None),
    ]


@pytest.mark.asyncio
async def test_visit_with_type_info_maintains_type_info_during_edit():
    engine = await create_engine(
        os.path.join(_BASE_DIR, "fixtures", "harness.graphql"),
        schema_name="maintains_type_info_during_edit",
    )

    class MyVisitor(Visitor):
        def __init__(self, type_info):
            self.type_info = type_info
            self.visited = []

        def enter(self, node, key, parent, path, ancestors):
            parent_type = self.type_info.get_parent_type()
            gql_type = self.type_info.get_type()
            input_type = self.type_info.get_input_type()
            self.visited.append(
                (
                    "enter",
                    node.__class__.__name__,
                    (node.value if isinstance(node, NameNode) else None),
                    str(parent_type) if parent_type else None,
                    str(gql_type) if gql_type else None,
                    str(input_type) if input_type else None,
                )
            )

            if isinstance(node, FieldNode):
                if not node.selection_set and is_composite_type(
                    get_wrapped_type(gql_type)
                ):
                    return FieldNode(
                        alias=node.alias,
                        name=node.name,
                        arguments=node.arguments,
                        directives=node.directives,
                        selection_set=SelectionSetNode(
                            selections=[
                                FieldNode(name=NameNode(value="__typename"))
                            ],
                        ),
                    )

        def leave(self, node, key, parent, path, ancestors):
            parent_type = self.type_info.get_parent_type()
            gql_type = self.type_info.get_type()
            input_type = self.type_info.get_input_type()
            self.visited.append(
                (
                    "leave",
                    node.__class__.__name__,
                    (node.value if isinstance(node, NameNode) else None),
                    str(parent_type) if parent_type else None,
                    str(gql_type) if gql_type else None,
                    str(input_type) if input_type else None,
                )
            )

    type_info = TypeInfo(engine._schema)
    visitor = MyVisitor(type_info)

    ast = parse_to_document(
        "{ human(id: 4) { name, pets }, alien }", engine._schema,
    )

    edited_ast = visit(ast, WithTypeInfoVisitor(type_info, visitor))

    assert ast == parse_to_document(
        "{ human(id: 4) { name, pets }, alien }", engine._schema,
    )
    assert (
        len(
            edited_ast.definitions[0]
            .selection_set.selections[0]
            .selection_set.selections[1]
            .selection_set.selections
        )
        == 1
    )
    assert (
        len(
            edited_ast.definitions[0]
            .selection_set.selections[1]
            .selection_set.selections
        )
        == 1
    )
    assert (
        edited_ast.definitions[0]
        .selection_set.selections[0]
        .selection_set.selections[1]
        .selection_set.selections[0]
        .name.value
        == "__typename"
    )
    assert (
        edited_ast.definitions[0]
        .selection_set.selections[1]
        .selection_set.selections[0]
        .name.value
        == "__typename"
    )
    assert visitor.visited == [
        ("enter", "DocumentNode", None, None, None, None),
        ("enter", "OperationDefinitionNode", None, None, "QueryRoot", None),
        ("enter", "SelectionSetNode", None, "QueryRoot", "QueryRoot", None),
        ("enter", "FieldNode", None, "QueryRoot", "Human", None),
        ("enter", "NameNode", "human", "QueryRoot", "Human", None),
        ("leave", "NameNode", "human", "QueryRoot", "Human", None),
        ("enter", "ArgumentNode", None, "QueryRoot", "Human", "ID"),
        ("enter", "NameNode", "id", "QueryRoot", "Human", "ID"),
        ("leave", "NameNode", "id", "QueryRoot", "Human", "ID"),
        ("enter", "IntValueNode", None, "QueryRoot", "Human", "ID"),
        ("leave", "IntValueNode", None, "QueryRoot", "Human", "ID"),
        ("leave", "ArgumentNode", None, "QueryRoot", "Human", "ID"),
        ("enter", "SelectionSetNode", None, "Human", "Human", None),
        ("enter", "FieldNode", None, "Human", "String", None),
        ("enter", "NameNode", "name", "Human", "String", None),
        ("leave", "NameNode", "name", "Human", "String", None),
        ("leave", "FieldNode", None, "Human", "String", None),
        ("enter", "FieldNode", None, "Human", "[Pet]", None),
        ("enter", "NameNode", "pets", "Human", "[Pet]", None),
        ("leave", "NameNode", "pets", "Human", "[Pet]", None),
        ("enter", "SelectionSetNode", None, "Pet", "[Pet]", None),
        ("enter", "FieldNode", None, "Pet", "String!", None),
        ("enter", "NameNode", "__typename", "Pet", "String!", None),
        ("leave", "NameNode", "__typename", "Pet", "String!", None),
        ("leave", "FieldNode", None, "Pet", "String!", None),
        ("leave", "SelectionSetNode", None, "Pet", "[Pet]", None),
        ("leave", "FieldNode", None, "Human", "[Pet]", None),
        ("leave", "SelectionSetNode", None, "Human", "Human", None),
        ("leave", "FieldNode", None, "QueryRoot", "Human", None),
        ("enter", "FieldNode", None, "QueryRoot", "Alien", None),
        ("enter", "NameNode", "alien", "QueryRoot", "Alien", None),
        ("leave", "NameNode", "alien", "QueryRoot", "Alien", None),
        ("enter", "SelectionSetNode", None, "Alien", "Alien", None),
        ("enter", "FieldNode", None, "Alien", "String!", None),
        ("enter", "NameNode", "__typename", "Alien", "String!", None),
        ("leave", "NameNode", "__typename", "Alien", "String!", None),
        ("leave", "FieldNode", None, "Alien", "String!", None),
        ("leave", "SelectionSetNode", None, "Alien", "Alien", None),
        ("leave", "FieldNode", None, "QueryRoot", "Alien", None),
        ("leave", "SelectionSetNode", None, "QueryRoot", "QueryRoot", None),
        ("leave", "OperationDefinitionNode", None, None, "QueryRoot", None),
        ("leave", "DocumentNode", None, None, None, None),
    ]


@pytest.mark.asyncio
async def test_visit_with_type_info_supports_traversals_of_selection_sets():
    engine = await create_engine(
        os.path.join(_BASE_DIR, "fixtures", "harness.graphql"),
        schema_name="supports_traversals_of_selection_sets",
    )

    class MyVisitor(Visitor):
        def __init__(self, type_info):
            self.type_info = type_info
            self.visited = []

        def enter(self, node, key, parent, path, ancestors):
            parent_type = self.type_info.get_parent_type()
            gql_type = self.type_info.get_type()
            self.visited.append(
                (
                    "enter",
                    node.__class__.__name__,
                    (node.value if isinstance(node, NameNode) else None),
                    str(parent_type) if parent_type else None,
                    str(gql_type) if gql_type else None,
                )
            )

        def leave(self, node, key, parent, path, ancestors):
            parent_type = self.type_info.get_parent_type()
            gql_type = self.type_info.get_type()
            self.visited.append(
                (
                    "leave",
                    node.__class__.__name__,
                    (node.value if isinstance(node, NameNode) else None),
                    str(parent_type) if parent_type else None,
                    str(gql_type) if gql_type else None,
                )
            )

    human_type = engine._schema.find_type("Human")
    type_info = TypeInfo(engine._schema, initial_type=human_type)
    visitor = MyVisitor(type_info)

    ast = parse_to_document("{ name, pets { name } }", engine._schema)

    assert len(ast.definitions) == 1
    operation_node = ast.definitions[0]
    assert isinstance(operation_node, OperationDefinitionNode)
    assert visitor.visited == []

    visit(
        operation_node.selection_set, WithTypeInfoVisitor(type_info, visitor)
    )

    assert visitor.visited == [
        ("enter", "SelectionSetNode", None, "Human", "Human"),
        ("enter", "FieldNode", None, "Human", "String"),
        ("enter", "NameNode", "name", "Human", "String"),
        ("leave", "NameNode", "name", "Human", "String"),
        ("leave", "FieldNode", None, "Human", "String"),
        ("enter", "FieldNode", None, "Human", "[Pet]"),
        ("enter", "NameNode", "pets", "Human", "[Pet]"),
        ("leave", "NameNode", "pets", "Human", "[Pet]"),
        ("enter", "SelectionSetNode", None, "Pet", "[Pet]"),
        ("enter", "FieldNode", None, "Pet", "String"),
        ("enter", "NameNode", "name", "Pet", "String"),
        ("leave", "NameNode", "name", "Pet", "String"),
        ("leave", "FieldNode", None, "Pet", "String"),
        ("leave", "SelectionSetNode", None, "Pet", "[Pet]"),
        ("leave", "FieldNode", None, "Human", "[Pet]"),
        ("leave", "SelectionSetNode", None, "Human", "Human"),
    ]
