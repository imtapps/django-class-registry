Allows you to create any Registry, similar to how django's admin
has you register classes, or their template library has you register tags.


Usage
======

::

    from class_registry import Registry

    site = Registry()

    @site.register
    class MyCoolClass(object):
      """
      My class that should be registered.
      """
      key = "ABC"


    >>> site["ABC"]
    <class 'MyCoolClass'>

Alternate use
-------------

Or, if you want your own key name, specify it when you register the class.::

    container = Registry(key_name="other_key")

    @container.register
    class MyCoolClass(object):
      other_key = "POL-COOL-CLS"

