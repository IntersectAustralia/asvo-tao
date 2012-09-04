from django.test.client import Client
from django.test.testcases import TestCase

class AccessingPagesTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def testAccessingPagesWithoutLoggingIn(self):
        response = self.client.get('/mock_galaxy_factory/', follow=True)
        self.assertContains(response, 'Login', count=None, status_code=200)