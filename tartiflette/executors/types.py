from collections import namedtuple

ExecutionData = namedtuple(
    'ExecutionData', ['parent_result', 'path', 'arguments', 'name', 'field',
                      'location', 'schema']
)

CoercedValue = namedtuple(
    'CoercedValue',  ["value", "errors"]
)
