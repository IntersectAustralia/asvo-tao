from django.core import mail
from django.test.utils import override_settings

from tao.tests.integration_tests import helper
from tao.tests.support.factories import UserFactory, GlobalParameterFactory
from tao.models import GlobalParameter, User

class UserRegisterTest(helper.LiveServerTest):

    def setUp(self):
        super(UserRegisterTest, self).setUp()
        self.admin_emails = []
        for unused in range(10):
            u = UserFactory.create(is_staff=True)
            self.admin_emails.append(u.email)
        UserFactory.create(username="someone", email="normal@test.com")
        GlobalParameterFactory(parameter_name='registration.html', parameter_value='{{ pending_requests_url }}')
        GlobalParameterFactory(parameter_name='registration.txt', parameter_value='{{ pending_requests_url }}')
        mail.outbox = []

    def tearDown(self):
        for o in User.objects.all(): o.delete()
        super(UserRegisterTest, self).tearDown()
    
    @override_settings(USE_CAPTCHA=False)    
    def test_email_admin(self):
        self.visit('register')

        field_data = {'#id_title': 'a',
                      '#id_first_name': 'b',
                      '#id_last_name': 'c',
                      '#id_username': 'd',
                      '#id_email': 'me@meeee.com',
                      '#id_password1': 'funnyfish',
                      '#id_password2': 'funnyfish',
                      '#id_institution': 'g'}
        self.fill_in_fields(field_data)
      
        submit_button = self.selenium.find_element_by_tag_name('button')
        submit_button.submit()
        
        self.assertEqual(1, len(mail.outbox)) #@UndefinedVariable
        email = mail.outbox[0] #@UndefinedVariable
        self.assertEqual('Registration submitted', email.subject)
        self.assertEqual(self.admin_emails, email.to)
        
        expected_url = self.get_full_url('access_requests')
        self.assert_email_body_contains(email, expected_url)
