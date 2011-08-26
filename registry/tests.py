from unittest import TestCase

from registry import sites

__all__ = ('RegistryTests',)

class RegisteredObjectOne(object):
    key = "rule_one"


class RegisteredObjectTwo(object):
    key = "rule_two"


class RegistryTests(TestCase):

    def setUp(self):
        self.registry = sites.Registry()
        self.rule = RegisteredObjectOne
        self.registry.register(self.rule)

    def test_register_adds_rules_by_key(self):
        self.assertEqual(self.rule, self.registry._registry[self.rule.key])

    def test_raises_already_registered_exception_when_rule_already_registered(self):
        with self.assertRaises(sites.AlreadyRegistered) as msg:
            self.registry.register(self.rule)
        self.assertEqual("Key %s has already been registered as %s." % (self.rule.key, self.rule),
                         msg.exception.message)

    def test_returns_rule_class_for_key_in_get_rule_class(self):
        rule_class = self.registry.get_registered_class(self.rule.key)
        self.assertEqual(self.rule, rule_class)

    def test_raises_not_registered_exception_when_getting_rule_class_that_doesnt_exist(self):
        rule_key = "bad_key"
        with self.assertRaises(sites.NotRegistered) as msg:
            self.registry.get_registered_class(rule_key)
        self.assertEqual("Key %s has not been registered." % rule_key,
                         msg.exception.message)

    def test_returns_all_registered_rules_from_rules_property(self):
        self.assertEqual({self.rule.key: self.rule}, self.registry.classes)

    def test_sites_site_is_registry_instance(self):
        self.assertIsInstance(sites.site, sites.Registry)

    def test_register_returns_class_so_that_it_can_be_used_as_a_decorator(self):
        registered_rule = self.registry.register(RegisteredObjectTwo)
        self.assertEqual(RegisteredObjectTwo, registered_rule)

    def test_unregister_removes_class_from_registry(self):
        self.registry.unregister(self.rule)
        self.assertEqual({}, self.registry._registry)

    def test_unregister_does_not_remove_what_is_not_there(self):
        self.registry.unregister(RegisteredObjectTwo)
        self.assertEqual({self.rule.key: self.rule}, self.registry._registry)
