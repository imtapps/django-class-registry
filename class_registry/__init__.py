VERSION = '0.0.3'


import warnings

__all__ = ('Registry',)

class AlreadyRegistered(Exception):
    pass


class NotRegistered(KeyError):
    pass


class Registry(dict):
    """
    Dictionary like object representing a collection of objects.

    To add items to the registry, decorate the class with the ``register``
    method.

    my_registry  = Registry()

    @my_registry.register
    class Example(object):
        key = 'HDR0'


    Then when you'll be able to get the registered class back out of the
    registry by accessing it like a dictionary with the key
    >>> my_registry['HDR0']
    <class 'path.to.module.Example'>

    """
    def __init__(self, key_name='key', *args, **kwargs):
        self.key_name = key_name
        super(Registry, self).__init__(*args, **kwargs)

    def register(self, klass):
        key = self._get_key_from_class(klass)
        if key in self:
            msg = "Key '{key}' has already been registered as '{name}'.".format(key=key, name=self[key].__name__)
            raise AlreadyRegistered(msg)

        self.__setitem__(key, klass)
        return klass

    def unregister(self, klass):
        key = self._get_key_from_class(klass)
        if key in self:
            self.__delitem__(key)

    def _get_key_from_class(self, klass):
        return getattr(klass, self.key_name)

    def __getitem__(self, key):
        """
        The registry is a dictionary. Raising `NotRegistered` instead of
        a `KeyError` seems more appropriate.
        """
        if self.has_key(key):
            return super(Registry, self).__getitem__(key)

        raise NotRegistered("Key '{key}' has not been registered.".format(key=key))

    def get_registered_class(self, key):
        warnings.warn(
            "The 'get_registered_class' method will be removed soon. Just access your registry like a dictionary.",
            PendingDeprecationWarning,
        )
        return self[key]

    @property
    def classes(self):
        warnings.warn(
            "The 'classes' property will be removed soon. Just access your registry like a dictionary.",
            PendingDeprecationWarning,
        )
        return self