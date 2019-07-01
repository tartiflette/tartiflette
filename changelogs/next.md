# [Next]

## Added

## Changed

- Updated dev dependancies
- Update import using isort.
- Public classes should be import through `from tartiflette import <>`

> Beware that you'll may have to change your imports

Before:
```python
from tartiflette.directive import Directive
from tartiflette.resolver import Resolver
from tartiflette.scalar import Scalar
```

After:
```python
from tartiflette import (
    Directive, Resolver, Scalar
)
```

## Fixed
