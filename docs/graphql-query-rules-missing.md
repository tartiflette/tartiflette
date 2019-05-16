# GraphQL query rules

## OverlappingFieldsCanBeMerged (5.3.2)

> Specification section: **[Field Selection Merging](https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selection-Merging)**

> [GraphQL JS implementation](https://github.com/graphql/graphql-js/blob/master/src/validation/rules/OverlappingFieldsCanBeMerged.js#L63)

A selection set is only valid if all fields (including spreading any fragments) either correspond to distinct response names or can be merged without ambiguity.

* Requirements:
    - ... HF
