from django.contrib.sites.models import Site
from django.core import mail

from tao.models import TaoUser
from tao.tests.integration_tests import helper
from tao.tests.support.factories import UserFactory


class PasswordResetTests(helper.LiveServerTest):

    def setUp(self):
        super(PasswordResetTests, self).setUp()
        self.username = "username"
        self.first_name = "Bob"
        self.userpass = "password"
        self.email = "abc@example.com"
        self.user = UserFactory.create(username=self.username, first_name=self.first_name, email=self.email)
        self.user.set_password(self.userpass)
        self.user.save()

    def tearDown(self):
        for o in TaoUser.objects.all():
            o.delete()
        super(PasswordResetTests, self).tearDown()

    def test_password_change_requires_login(self):
        self.visit('password_change')
        self.assert_on_page('login', ignore_query_string=True)

    def test_password_change_form(self):
        self.login(self.username, self.userpass)
        self.click('id-account_settings_menu')
        self.click('id-change_your_password')
        self.assert_on_page('password_change')

        self.assert_is_displayed('#id_old_password')
        self.assert_is_displayed('#id_new_password1')
        self.assert_is_displayed('#id_new_password2')
        self.assert_is_displayed('button[type="submit"]')

    def test_change_current_password(self):
        self.login(self.username, self.userpass)
        self.visit('password_change')

        field_data = {
            '#id_old_password': "password",
            '#id_new_password1': 'newPassword',
            '#id_new_password2': 'newPassword',
        }
        self.fill_in_fields(field_data)
        self.click_by_css('button[type="submit"]')

        self.click('id-account_settings_menu')
        self.click('id-logout')
        self.login(self.username, password='newPassword')
        self.assert_on_page('home')

    def test_reset_password(self):
        self.visit('login')
        self.click('id_password_reset')
        self.assert_on_page('password_reset')

        field_data = {
            '#id_username': self.username,
            '#id_email': self.email,
        }
        self.fill_in_fields(field_data)
        self.click_by_css('button[type="submit"]')
        self.assert_on_page('password_reset_done')
        self.assertEqual(1, len(mail.outbox))

        email = mail.outbox[0]
        mail_content = str(email.body)
        site_name = Site.objects.get(id=1).name
        self.assertTrue(self.user.email in email.to)
        self.assertEqual("Password reset on " + site_name, email.subject)
        self.assertTrue(self.first_name in mail_content)
        self.assertTrue(self.username in mail_content)
        self.assertTrue("You're receiving this e-mail because you requested a password reset for your user account at " + site_name in mail_content)