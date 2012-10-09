from tao.tests import create_user
from tao.tests import dataset_tests
from tao.tests import forms
from tao.tests import models
from tao.tests import pagination_test
from tao.tests import register_user
from tao.tests import widget_tests

from tao.tests.integration_tests import ALL_INTEGRATION_TEST_CASES

import unittest


def suite():
    suite = unittest.TestSuite()
    test_modules = [create_user, forms, register_user, pagination_test, dataset_tests, widget_tests, models]
    for module in test_modules:
        suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(module))
    for test_case in ALL_INTEGRATION_TEST_CASES:
        suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_case))
    return suite
