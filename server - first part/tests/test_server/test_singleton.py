from unittest import TestCase
from utilities.singleton import Singleton


class SimpleSingleton(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.simple_attr = "SimpleSingleton"


class TestSingleton(TestCase):
    def test_unique_instance(self):
        instance1 = SimpleSingleton()
        instance2 = SimpleSingleton()

        self.assertEquals(instance1, instance2, "Error, two different "
                                                "instances")
