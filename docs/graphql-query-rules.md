# GraphQL query rules

## ExecutableDefinitions

> Specification section: **[Executable Definitions](https://graphql.github.io/graphql-spec/June2018/#sec-Executable-Definitions)**

> [GraphQL JS implementation](https://github.com/graphql/graphql-js/blob/master/src/validation/rules/ExecutableDefinitions.js#L19)

A GraphQL document is only valid for execution if all definitions are either operation or fragment definitions (document containing **TypeSystemDefinition** is invalid for execution).

* Requirements:
    - list of document definitions


## UniqueOperationNames

> Specification section: **[Operation Name Uniqueness](https://graphql.github.io/graphql-spec/June2018/#sec-Operation-Name-Uniqueness)**

> [GraphQL JS implementation](https://github.com/graphql/graphql-js/blob/master/src/validation/rules/UniqueOperationNames.js#L16)

A GraphQL document is only valid if all defined operations have unique names.

* Requirements:
    - list of operation definitions


## LoneAnonymousOperation

> Specification section: **[Lone Anonymous Operation](https://graphql.github.io/graphql-spec/June2018/#sec-Lone-Anonymous-Operation)**

> [GraphQL JS implementation](https://github.com/graphql/graphql-js/blob/master/src/validation/rules/LoneAnonymousOperation.js#L18)

A GraphQL document is only valid if when it contains an anonymous operation (the query short-hand) that it contains only that one operation definition.

* Requirements:
    - number of operation definitions
    - anonymous operation definition


## SingleFieldSubscriptions

> Specification section: **[Subscriptions with Single Root Field](https://graphql.github.io/graphql-spec/June2018/#sec-Single-root-field)**

> [GraphQL JS implementation](https://github.com/graphql/graphql-js/blob/master/src/validation/rules/SingleFieldSubscriptions.js#L19)

A GraphQL subscription is valid only if it contains a single root field (introspection fields are counted).

* Requirements:
    - number of root fields of the subscription operation


## KnownTypeNames

> Specification section: **[Fragment Spread Type Existence](https://graphql.github.io/graphql-spec/June2018/#sec-Fragment-Spread-Type-Existence)**

> [GraphQL JS implementation](https://github.com/graphql/graphql-js/blob/master/src/validation/rules/KnownTypeNames.js#L35)

A GraphQL document is only valid if fragments must be specified on types that exist in the schema. This applies for both named and inline fragments. If they are not defined in the schema, the query does not validate.

* Requirements:
    - list of fragment definitions/inline fragments with their named type
    - a baked GraphQLSchema instance in order to be able to retrieve and check types


## FragmentsOnCompositeTypes

> Specification section: **[Fragments on Composite Types](https://graphql.github.io/graphql-spec/June2018/#sec-Fragments-On-Composite-Types)**

> [GraphQL JS implementation](https://github.com/graphql/graphql-js/blob/master/src/validation/rules/FragmentsOnCompositeTypes.js#L28)

Fragments can only be declared on unions, interfaces, and objects. They are invalid on scalars. They can only be applied on non‐leaf fields. This rule applies to both inline and named fragments.

* Requirements:
    - list of fragment definitions/inline fragments with their named type
    - a baked GraphQLSchema instance in order to be able to retrieve and check types


## VariablesAreInputTypes

> Specification section: **[Variables are Input Types](https://graphql.github.io/graphql-spec/June2018/#sec-Variables-Are-Input-Types)**

> [GraphQL JS implementation](https://github.com/graphql/graphql-js/blob/master/src/validation/rules/VariablesAreInputTypes.js#L24)

A GraphQL operation is only valid if all the variables it defines are of input types (scalar, enum, or input object).

* Requirements:
    - list of variable definitions of each operation
    - a baked GraphQLSchema instance in order to be able to retrieve and check input types


## ScalarLeafs

> Specification section: **[Leaf Field Selections](https://graphql.github.io/graphql-spec/June2018/#sec-Leaf-Field-Selections)**

> [GraphQL JS implementation](https://github.com/graphql/graphql-js/blob/master/src/validation/rules/ScalarLeafs.js#L30)

A GraphQL document is valid only if all leaf fields (fields without sub selections) are of scalar or enum types. Conversely leaf selections on objects, interfaces, and unions without subfields are disallowed.

* Requirements:
    - list of fields

## FieldsOnCorrectType

> Specification section: **[Field Selections on Objects, Interfaces, and Unions Types](https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types)**

> [GraphQL JS implementation](https://github.com/graphql/graphql-js/blob/master/src/validation/rules/FieldsOnCorrectType.js#L38)

A GraphQL document is only valid if all fields selected are defined by the parent type, or are an allowed meta field such as \_\_typename.

* Requirements:
    - list of fields with their parent types
    - a baked GraphQLSchema instance in order to be able to check if fields exists


## UniqueFragmentNames

> Specification section: **[Fragment Name Uniqueness](https://graphql.github.io/graphql-spec/June2018/#sec-Fragment-Name-Uniqueness)**

> [GraphQL JS implementation](https://github.com/graphql/graphql-js/blob/master/src/validation/rules/UniqueFragmentNames.js#L16)

A GraphQL document is only valid if all defined fragments have unique names.

* Requirements:
    - list of fragment definitions


## KnownFragmentNames

> Specification section: **[Fragment spread target defined](https://graphql.github.io/graphql-spec/June2018/#sec-Fragment-spread-target-defined)**

> [GraphQL JS implementation](https://github.com/graphql/graphql-js/blob/master/src/validation/rules/KnownFragmentNames.js#L17)

A GraphQL document is only valid if all `...Fragment` fragment spreads refer to fragments defined in the same document.

* Requirements:
    - list of fragment spreads
    - list of fragment definitions


## NoUnusedFragments

> Specification section: **[Fragments must be used](https://graphql.github.io/graphql-spec/June2018/#sec-Fragments-Must-Be-Used)**

> [GraphQL JS implementation](https://github.com/graphql/graphql-js/blob/master/src/validation/rules/NoUnusedFragments.js#L17)

A GraphQL document is only valid if all fragment definitions are spread within operations, or spread within other fragments spread within operations.

* Requirements:
    - list of fragment spreads
    - list of fragment definitions


## PossibleFragmentSpreads

> Specification section: **[Fragment spread is possible](https://graphql.github.io/graphql-spec/June2018/#sec-Fragment-spread-is-possible)**

> [GraphQL JS implementation](https://github.com/graphql/graphql-js/blob/master/src/validation/rules/PossibleFragmentSpreads.js#L33)

Fragments are declared on a type and will only apply when the runtime object type matches the type condition. They also are spread within the context of a parent type. A fragment spread is only valid if its type condition could ever apply within the parent type.

* Requirements:
    - list of inline fragments/fragment spreads with their parent types
    - a baked GraphQLSchema instance in order to be able to check fragments

## NoFragmentCycles

> Specification section: **[Fragments must not form cycles](https://graphql.github.io/graphql-spec/June2018/#sec-Fragment-spreads-must-not-form-cycles)**

> [GraphQL JS implementation](https://github.com/graphql/graphql-js/blob/master/src/validation/rules/NoFragmentCycles.js#L16)

The graph of fragment spreads must not form any cycles including spreading itself. Otherwise an operation could infinitely spread or infinitely execute on cycles in the underlying data.

* Requirements:
    - list of fragment definitions
    - list of fragment spreads


## UniqueVariableNames

> Specification section: **[Variable Uniqueness](https://graphql.github.io/graphql-spec/June2018/#sec-Variable-Uniqueness)**

> [GraphQL JS implementation](https://github.com/graphql/graphql-js/blob/master/src/validation/rules/UniqueVariableNames.js#L17)

A GraphQL operation is only valid if all its variables are uniquely named.

* Requirements:
    - list of variable definitions of each operation


## NoUndefinedVariables

> Specification section: **[All Variable Used Defined](https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Uses-Defined)**

> [GraphQL JS implementation](https://github.com/graphql/graphql-js/blob/master/src/validation/rules/NoUndefinedVariables.js#L19)

A GraphQL operation is only valid if all variables encountered, both directly and via fragment spreads, are defined by that operation.

* Requirements:
    - list of variable definitions of each operation
    - list of variable used by each operation (have to look on fragment used in operations)


## NoUnusedVariables

> Specification section: **[All Variables Used](https://graphql.github.io/graphql-spec/June2018/#sec-All-Variables-Used)**

> [GraphQL JS implementation](https://github.com/graphql/graphql-js/blob/master/src/validation/rules/NoUnusedVariables.js#L22)

A GraphQL operation is only valid if all variables defined by an operation are used, either directly or within a spread fragment.

* Requirements:
    - list of variable definitions of each operation
    - list of variable used by each operation (have to look on fragment used in operations)


## KnownDirectives

> Specification section: **[Directives Are Defined](https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-Defined)**

> [GraphQL JS implementation](https://github.com/graphql/graphql-js/blob/master/src/validation/rules/KnownDirectives.js#L30)

A GraphQL document is only valid if all `@directives` are known by the schema and legally positioned.

* Requirements:
    - list of used directives with their location
    - a baked GraphQLSchema instance in order to be able to check directive and their locations


## UniqueDirectivesPerLocation

> Specification section: **[Directives Are Unique Per Location](https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-Unique-Per-Location)**

> [GraphQL JS implementation](https://github.com/graphql/graphql-js/blob/master/src/validation/rules/UniqueDirectivesPerLocation.js#L23)

A GraphQL document is only valid if all directives at a given location are uniquely named. When more than one directive of the same name is used, the expected metadata or behavior becomes ambiguous, therefore only one of each directive is allowed per location.

* Requirements:
    - list of used directives at each location


## KnownArgumentNames

> Specification section: **[Argument Names](https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Names)**

> [GraphQL JS implementation](https://github.com/graphql/graphql-js/blob/master/src/validation/rules/KnownArgumentNames.js#L43)

Every argument provided to a field or directive must be defined in the set of possible arguments of that field or directive.

* Requirements:
    - list of arguments of each fields/directives
    - a baked GraphQLSchema instance in order to be able to check arguments are defined


## UniqueArgumentNames

> Specification section: **[Argument Uniqueness](https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Uniqueness)**

> [GraphQL JS implementation](https://github.com/graphql/graphql-js/blob/master/src/validation/rules/UniqueArgumentNames.js#L17)

A GraphQL field or directive is only valid if all supplied arguments are uniquely named.

* Requirements:
    - list of arguments of each fields/directives


## ValuesOfCorrectType

> Specification section: **[Value Type Correctness](https://graphql.github.io/graphql-spec/June2018/#sec-Values-of-Correct-Type)**

> [GraphQL JS implementation](https://github.com/graphql/graphql-js/blob/master/src/validation/rules/ValuesOfCorrectType.js#L72)

A GraphQL document is only valid if all value literals are of the type expected at their position.

* Requirements:
    - list of literal values and their parent type


## ProvidedRequiredArguments

> Specification section: **[Argument Optionality](https://graphql.github.io/graphql-spec/June2018/#sec-Required-Arguments)**

> [GraphQL JS implementation](https://github.com/graphql/graphql-js/blob/master/src/validation/rules/ProvidedRequiredArguments.js#L74)

A field or directive is only valid if all required (non-null without a default value) field arguments have been provided.

* Requirements:
    - list of arguments of each fields/directives
    - a baked GraphQLSchema instance in order to be able to check required arguments


## VariablesInAllowedPosition

> Specification section: **[All Variable Usages Are Allowed](https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed)**

> [GraphQL JS implementation](https://github.com/graphql/graphql-js/blob/master/src/validation/rules/VariablesInAllowedPosition.js#L25)

Variable usages must be compatible with the arguments they are passed to.

Validation failures occur when variables are used in the context of types that are complete mismatches, or if a nullable type in a variable is passed to a non‐null argument type.

* Requirements:
    - list of variable definitions of each operation
    - list of variable used by each operation (have to look on fragment used in operations) with the expected type


## OverlappingFieldsCanBeMerged

> Specification section: **[Field Selection Merging](https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selection-Merging)**

> [GraphQL JS implementation](https://github.com/graphql/graphql-js/blob/master/src/validation/rules/OverlappingFieldsCanBeMerged.js#L63)

A selection set is only valid if all fields (including spreading any fragments) either correspond to distinct response names or can be merged without ambiguity.

* Requirements:
    - ... HF


## UniqueInputFieldNames

> Specification section: **[Input Object Field Uniqueness](https://graphql.github.io/graphql-spec/June2018/#sec-Input-Object-Field-Uniqueness)**

> [GraphQL JS implementation](https://github.com/graphql/graphql-js/blob/master/src/validation/rules/UniqueInputFieldNames.js#L17)

A GraphQL input object value is only valid if all supplied fields are uniquely named.

* Requirements:
    - list of object field of each input object value
