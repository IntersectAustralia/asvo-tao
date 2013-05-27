from django.core import mail
from django.test.utils import override_settings

from tao.tests.integration_tests import helper
from tao.tests.support.factories import UserFactory, GlobalParameterFactory
from tao.models import GlobalParameter, User


class SupportTests(helper.LiveServerTest):

    def setUp(self):
        super(SupportTests, self).setUp()
        self.username = 'someone'
        self.userpass = 'password'
        self.user = UserFactory.create(username=self.username, email="normal@test.com")
        self.user.set_password(self.userpass)
        self.user.save()
        GlobalParameterFactory(parameter_name='support-template.html', parameter_value='{{ user.email }} {{ message }}')
        GlobalParameterFactory(parameter_name='support-template.txt', parameter_value='{{ user.email }} {{ message }}')
        GlobalParameterFactory(parameter_name='support-recipients', parameter_value='test1@example.org, test2@example.org')
        mail.outbox = []

    def tearDown(self):
        for o in User.objects.all(): o.delete()
        super(SupportTests, self).tearDown()

    def test_support_requires_login(self):
        "Tests that the support link requires authenticated user"
        self.visit('support_page')
        self.assert_on_page('login', ignore_query_string=True)

    def test_support_form(self):
        "Test that the form is shown for registered user and has message field"
        self.login(self.username, self.userpass)
        self.visit('support_page')
        self.assert_on_page('support_page')
        self.assert_is_displayed('#id_message')
        self.assert_is_displayed('#id_subject')
        self.assert_is_displayed('button[type="submit"]')

    def test_support_email(self):
        "Test that the submit button in the form triggers an email to configured emails and it contains the message"
        subject = 'A'
        message = 'Some message for support.'
        self.login(self.username, self.userpass)
        self.visit('support_page')
        self.fill_in_fields({'#id_subject': subject, '#id_message': message})
        self.submit_support_form()
        self.assertEqual(1, len(mail.outbox))
        email = mail.outbox[0]
        mail_content = str(email.body)
        self.assertEqual('TAO Support: ' + subject, email.subject)
        self.assertTrue(message in mail_content)
        self.assertTrue(self.user.email in mail_content)
        self.assertTrue(self.user.email in email.to)
        self.assertTrue('test1@example.org' in email.bcc)
        self.assertTrue('test2@example.org' in email.bcc)
        self.assertTrue(len(email.to) == 1)
        self.assertTrue(len(email.bcc) == 2)
        self.assert_page_has_content("Thank you -- your email has been sent")

    def test_support_message_not_empty(self):
        "Test that the form is not submitted if there is no message (i.e. all is whitespace)"
        self.login(self.username, self.userpass)
        self.visit('support_page')
        self.fill_in_fields({'#id_subject': '   ', '#id_message': '   \n   \t'})
        self.submit_support_form()
        self.assertEqual(0, len(mail.outbox))
        self.assert_on_page('support_page')
        self.assert_page_does_not_contain("Thank you -- your email has been sent")
        self.assert_page_has_content('Enter a valid value')

    def test_link_to_support_page(self):
        "Test that clicking the Support link on the top banner takes the user to the support page"
        self.login(self.username, self.userpass)
        self.selenium.maximize_window()
        self.click('id-support')
        self.assert_on_page('support_page')