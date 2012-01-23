
from unittest import TestCase


from class_registry import Registry, AlreadyRegistered, NotRegistered

__all__ = (
    'RegistryTests',
)

class RegistryTests(TestCase):

    def get_test_class(self, key="ABC"):
        return type('TestClass', (object,), {'key': key})

    def test_register_adds_item_to_collection(self):
        lc = Registry()
        TestClass = self.get_test_class("ABC")

        lc.register(TestClass)

        self.assertEqual(lc["ABC"], TestClass)

    def test_unregister_removes_item_from_collection(self):
        key = "ABC"
        lc = Registry()
        TestClass = self.get_test_class(key)

        lc[key] = TestClass
        lc.unregister(TestClass)

        self.assertFalse(lc.has_key(key))

    def test_unregister_returns_none_when_class_isnt_already_registered(self):
        # as opposed to blowing up on a KeyError
        lc = Registry()
        TestClass = self.get_test_class("ABC")

        self.assertEqual(None, lc.unregister(TestClass))

    def test_raises_already_registered_when_key_has_already_been_registered(self):
        test_class_one = self.get_test_class("ABC")
        test_class_two = type('TestClassTwo', (object,), {'key': "ABC"})

        lc = Registry()
        lc.register(test_class_one)

        with self.assertRaises(AlreadyRegistered) as e:
            lc.register(test_class_two)
        self.assertEqual("Key 'ABC' has already been registered as 'TestClass'.", e.exception.message)

    def test_raises_not_registered_when_trying_to_access_an_item_that_has_not_been_registered(self):
        lc = Registry()

        with self.assertRaises(NotRegistered) as e:
            lc['ABC']
        self.assertEqual("Key 'ABC' has not been registered.", e.exception.message)

    def test_classes_property_returns_same_object(self):
        # for backwards compatibility. Now that registry is a dict, the old
        # classes property has no purpose.
        lc = Registry()
        classes = lc.classes

        self.assertEqual(lc, classes)

    def test_get_registered_class_returns_registered_class(self):
        # for backwards compatibility. You can (and should) just access
        # your registry like a normal dictionary.
        lc = Registry()
        TestClass = self.get_test_class("ABC")

        lc.register(TestClass)

        self.assertEqual(lc.get_registered_class("ABC"), TestClass)

    def test_registry_allows_customizable_key_name(self):
        lc = Registry(key_name='obj_code')
        TestClass = type('TestClass', (object,), {'obj_code': "code1"})

        lc.register(TestClass)

        self.assertEqual(lc["code1"], TestClass)

