from django.test.testcases import TransactionTestCase
from django.test.utils import override_settings

from tao.forms import UserCreationForm
from tao.tests.support.factories import UserFactory
from tao.tests.helper import TaoModelsCleanUpMixin
from django.contrib.auth.models import AnonymousUser



class UserCreationFormTest(TransactionTestCase, TaoModelsCleanUpMixin):

    @override_settings(USE_CAPTCHA=False, MIN_PASSWORD_LENGTH=6)
    def test_create_user(self):
        user_form = UserCreationForm({'title': 'a',
            'first_name': 'b',
            'last_name': 'c',
            'institution': 'd',
            'email': 'u123@intersect.org.au',
            'recaptcha_response_field': 'PASSED',
            'username': 'e',
            'password1': '123456',
            'password2': '123456'}, user=AnonymousUser())
        self.assertTrue(user_form.is_valid())

    @override_settings(USE_CAPTCHA=False)
    def test_cannot_create_duplicate_email(self):
        # setup initial data or something
        # execute the behaviour you want to test
        # verify the output of the behaviour (sometimes mocks/stubs as well)
        
        """
        If I have a user with email "cindy@intersect.org.au"
        And I try to create a new user with the create user form with email "cindy@intersect.org.au"
        Then the form should be invalid
        """
        
        test_email = 'cindy@intersect.org.au'
        UserFactory.create(email=test_email)
        
        from tao.models import TaoUser
        self.assertEqual(1, TaoUser.objects.count())
        user_form = UserCreationForm({'title': 'a',
            'first_name': 'b', 
            'last_name': 'c', 
            'institution': 'd', 
            'email': test_email, 
            'recaptcha_response_field': 'PASSED',
            'username': 'e',
            'password1': 'funnyfish',
            'password2': 'funnyfish'}, user=AnonymousUser())
        self.assertFalse(user_form.is_valid())
        self.assertEqual(['That email is already taken.'], user_form.errors['email'])
