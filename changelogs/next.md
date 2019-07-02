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
from tartiflette.subscription import Subscription
```

After:
```python
from tartiflette import (
    Directive, Resolver, Scalar, Subscription
)
```

- `GrapQLError` is marked as deprecated in favor of `TartifletteError`, importable through `from tartiflette import TartifletteError`

## Fixed

- ISSUE-245 - Fix a bug in SDL tokenization that was corrupting Unicode.
