from unittest import TestCase

from class_registry.auto_import import AutoImport
from class_registry import Registry, AlreadyRegistered, NotRegistered


class FakeModule(object):

    def __init__(self, name):
        self.name = name

    @property
    def __name__(self):
        return self.name


class RegistryTests(TestCase):

    def get_test_class(self, key="ABC"):
        return type('TestClass', (object, ), {'key': key})

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
        self.assertNotIn(key, lc)

    def test_unregister_returns_none_when_class_isnt_already_registered(self):
        # as opposed to blowing up on a KeyError
        lc = Registry()
        TestClass = self.get_test_class("ABC")

        self.assertEqual(None, lc.unregister(TestClass))

    def test_raises_already_registered_when_key_has_already_been_registered(self):
        test_class_one = self.get_test_class("ABC")
        test_class_two = type('TestClassTwo', (object, ), {'key': "ABC"})
        lc = Registry()
        lc.register(test_class_one)

        with self.assertRaises(AlreadyRegistered) as e:
            lc.register(test_class_two)
        self.assertEqual("Key 'ABC' has already been registered as 'TestClass'.", str(e.exception))

    def test_raises_not_registered_when_trying_to_access_an_item_that_has_not_been_registered(self):
        lc = Registry()
        with self.assertRaises(NotRegistered) as e:
            lc['ABC']
        self.assertEqual('"Key \'ABC\' has not been registered."', str(e.exception))

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
        TestClass = type('TestClass', (object, ), {'obj_code': "code1"})
        lc.register(TestClass)
        self.assertEqual(lc["code1"], TestClass)


class AutoImportTests(TestCase):

    def test_will_replace_any_slash_in_the_path_with_a_dot_instead(self):
        fake_module = FakeModule(name='project')
        auto_import = AutoImport(fake_module)
        package_name = auto_import.get_package_name('foo/project')
        self.assertEqual(package_name, 'project')

    def test_will_replace_two_dots_in_the_module_name_when_running_south_migrations(self):
        fake_module = FakeModule(name='project..app')
        auto_import = AutoImport(fake_module)
        package_name = auto_import.get_package_name('foo/project/app')
        self.assertEqual(package_name, 'project.app')

    def test_when_demo_is_imported_registry_contains_all_classes_under_action_package(self):
        from class_registry.tests.demo.actions import action_registry as actions
        self.assertIn('one', actions)
        self.assertIn('two', actions)
        self.assertIn('three', actions)
