from django.test import TestCase

from django.test.client import Client
from django.conf import settings
from tao.models import User
from django.test.utils import override_settings


class CreateUserTest (TestCase):

    def setUp(self):
        self.client = Client()

    def testCreateUser(self):  
        self.assertTrue(True, "we is crazy")

    @override_settings(DEBUG=True)
    def testSuccessful(self):
        response = self.client.post('/accounts/register/', { 'title' : 'MyTit', 'first_name' : 'MyFirstName', 'last_name' : 'MyLastName',
                                                            'username' : 'myUserName', 'email' : 'myEmail@email.com', 'password1' : "password1",
                                                            'password2' : 'password1', 'institution' : 'Intersect', 'scientific_interests' : 'Black Holes',
                                                            'recaptcha_response_field' : 'PASSED' })
        self.assertEquals(302, response.status_code)
        print(response.content)
        print(settings.DEBUG)
        self.assertEquals(1, len(User.objects.all()))
        # TODO test fields are saved properly
        
class MyTestTwo(TestCase):
    def testFirst(self):
        self.assertTrue(False, "This is the create_user one")