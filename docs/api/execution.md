---
id: execution
title: Execution
sidebar_label: Execution
---

Aside from building the `Engine`, the `execute` method is responsible for executing the GraphQL query coming from the client.

Its parameters are:
* `query` _(Union[str, bytes])_: the GraphQL request/query as UTF8-encoded string
* `operation_name` _(Optional[str])_: the operation name to execute
* `context` _(Optional[Any])_: value containing anything you could need and which will be available during all the execution process
* `variables` _(Optional[Dict[str, Any]])_: the variables provided in the GraphQL request
* `initial_value` _(Optional[Any])_: an initial value which will be forwarded to the resolver of root type (Query/Mutation/Subscription) fields

```python
from tartiflette import create_engine


engine = await create_engine(
    "myDsl.graphql"
)

result = await engine.execute(
    query="query MyVideo($id: String!) { video(id: $id) { id title } }",
    operation_name="MyVideo",
    context={
        "mysql_client": MySQLClient(),
        "auth_info": AuthInfo(),
    },
    variables={
        "id": "1234",
    },
    initial_value={},
)

# `result` will contains something like
# {
#     "data": {
#         "video": {
#             "id": "1234",
#             "title": "My fabulous title"
#         }
#     }
# }
```
