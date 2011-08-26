__all__ = ('site',)


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class Registry(object):

    def __init__(self):
        self._registry = {}

    def register(self, site_class):
        if site_class.key in self._registry:
            err_msg = "Key %s has already been registered as %s." % (site_class.key, self._registry[site_class.key])
            raise AlreadyRegistered(err_msg)

        self._registry[site_class.key] = site_class

        return site_class

    def unregister(self, site_class):
        self._registry.pop(site_class.key, None)

    def get_registered_class(self, key):
        if key not in self._registry:
            raise NotRegistered("Key %s has not been registered." % key)
        return self._registry[key]

    @property
    def classes(self):
        return self._registry

site = Registry()