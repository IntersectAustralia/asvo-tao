from tao.tests import create_user
from tao.tests import forms
from tao.tests import register_user
from tao.tests import pagination_test
from tao.tests import dataset_tests
from tao.tests import widget_tests

#from .integration_tests import *

import unittest


def suite():
    suite = unittest.TestSuite()
    test_modules = [create_user, forms, register_user, pagination_test, dataset_tests, widget_tests]
    for module in test_modules:
        suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(module))
    return suite
