from django.utils import unittest
from selenium.webdriver.firefox.webdriver import WebDriver
from os import path as opath
import time


class JavaScriptTestCase(unittest.TestCase):

    def setUp(self):
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(1) # wait one second before failing to find

    def tearDown(self):
        self.selenium.quit()

    def test_catalogue_extender_required(self):
        self.selenium.get(self._load('test_catalogue_extender_required'))
        self.assert_zero_failures()

    def _load(self, page):
        return 'file://' + opath.join(opath.dirname(__file__), 'qunit', page+'.html')

    def assert_zero_failures(self):
        elem = self.selenium.find_element_by_css_selector('#qunit-testresult span.failed')
        self.assertTrue(int(elem.text) == 0, "Failures found: " + elem.text)


