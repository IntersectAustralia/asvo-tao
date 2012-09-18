from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

class MockGalaxyFactoryTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(MockGalaxyFactoryTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(MockGalaxyFactoryTest, cls).tearDownClass()
        cls.selenium.quit()

    def test_basic(self):
        self.selenium.get("%s%s" % (self.live_server_url, '/accounts/login/'))
