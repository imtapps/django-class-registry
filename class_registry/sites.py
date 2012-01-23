
__all__ = ('Registry',)

import warnings

warnings.warn(
    "Registry has moved. Change your imports to 'from class_registry import Registry'",
    PendingDeprecationWarning,
)

from class_registry import Registry
