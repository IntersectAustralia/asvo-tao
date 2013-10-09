from django.contrib.auth.forms import PasswordChangeForm
from django.test import TransactionTestCase

from tao.forms import PasswordResetForm
from tao.models import TaoUser
from tao.tests.support.factories import UserFactory
from tao.tests.helper import TaoModelsCleanUpMixin


class PasswordChangeFormTests(TransactionTestCase, TaoModelsCleanUpMixin):

    def setUp(self):
        super(PasswordChangeFormTests, self).setUp()
        username = "user"
        password = "password"
        email = "abc@example.com"
        self.user1 = UserFactory.create(username=username+"1", password=password+"1", email=email+"1")
        self.user2 = UserFactory.create(username=username+"2", password=password+"2", email=email+"2")

    def tearDown(self):
        for o in TaoUser.objects.all(): o.delete()
        super(PasswordChangeFormTests, self).tearDown()

    def test_verify_old_password_on_change(self):
        password_change_form = PasswordChangeForm({
            'old_password': 'wrong_password',
            'new_password1': 'blah',
            'new_password2': 'blah',
        })
        self.assertFalse(password_change_form.is_valid())

    def test_new_passwords_match_on_change(self):
        password_change_form = PasswordChangeForm({
            'old_password': 'password',
            'new_password1': 'blahblah',
            'new_password2': 'somethingelse',
        })
        self.assertFalse(password_change_form.is_valid())

    def test_username_on_reset(self):
        valid_password_reset_form = PasswordResetForm({
            'username': self.user1.username,
            'email': self.user1.email,
        })
        self.assertTrue(valid_password_reset_form.is_valid())
        # a non-existent username will throw a KeyError and disrupt the test

    def test_email_matches_user_on_reset(self):
        non_existant_email_form = PasswordResetForm({
            'username': self.user1.username,
            'email': 'nonexistant@email.com',
        })
        self.assertFalse(non_existant_email_form.is_valid())
        email_stored_for_different_user_form = PasswordResetForm({
            'username': self.user1.username,
            'email': self.user2.email,
        })
        self.assertFalse(email_stored_for_different_user_form.is_valid())
        valid_password_reset_form = PasswordResetForm({
            'username': self.user2.username,
            'email': self.user2.email,
        })
        self.assertTrue(valid_password_reset_form.is_valid())