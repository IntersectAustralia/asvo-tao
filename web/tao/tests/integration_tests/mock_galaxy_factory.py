from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

class MockGalaxyFactoryTest(LiveServerTestCase):

    def setUp(self):
        super(MockGalaxyFactoryTest, self).setUp()
        self.selenium = WebDriver()

    def tearDown(self):
        super(MockGalaxyFactoryTest, self).tearDownClass()
        self.selenium.quit()

    def test_basic(self):
        self.selenium.get("%s%s" % (self.live_server_url, '/accounts/login/'))
