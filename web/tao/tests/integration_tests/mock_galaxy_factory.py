from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

class MockGalaxyFactoryTest(LiveServerTestCase):

    def setUp(self):
        self.selenium = WebDriver()
        super(MockGalaxyFactoryTest, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(MockGalaxyFactoryTest, self).tearDown()

    def test_basic(self):
        self.selenium.get("%s%s" % (self.live_server_url, '/accounts/login/'))
