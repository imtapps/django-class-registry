from class_registry.tests.demo.actions import action_registry


@action_registry.register
class Two(object):
    key = 'two'
