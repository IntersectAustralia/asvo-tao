from django.test.client import Client
from django.test.testcases import TestCase
from tao.models import TaoUser
from django.core import mail
from tao.tests.support.factories import GlobalParameterFactory

class RegisterUserTestCase(TestCase):
    """These tests are partly the reverse of how a real system is set up.
    TAO doesn't send an email if the txt template is empty.
    The tests here have an empty template for approval, and a populated template for rejection.
    In a typical production system the opposite will be true.
    However the functionality is still being tested correctly."""
    def setUp(self):
        self.client = Client()
        super_user = TaoUser(username='superman', email='email@super.com', first_name='super', last_name='man', is_active=True, is_staff=True)
        super_user.set_password('superman')
        super_user.save()
        GlobalParameterFactory(parameter_name='approve.html', parameter_value='')
        GlobalParameterFactory(parameter_name='approve.txt', parameter_value='')
        GlobalParameterFactory(parameter_name='registration.html', parameter_value='')
        GlobalParameterFactory(parameter_name='registration.txt', parameter_value='')
        GlobalParameterFactory(parameter_name='reject.html', parameter_value='{{ reason }}')
        GlobalParameterFactory(parameter_name='reject.txt', parameter_value='{{ reason }}')
        mail.outbox = []

    def testApproveUser(self):
        new_user = TaoUser(username='username', email='email@email.com', first_name='fname', last_name='lname', is_active=False, institution='Intersect', scientific_interests='', title='Mr')
        new_user.set_password('password')
        new_user.save()

        self.assertEquals(2, len(TaoUser.objects.all()))
        self.assertFalse(new_user.is_active)

        self.assertTrue(self.client.login(username='superman', password='superman'))

        outbox = mail.outbox #@UndefinedVariable
        self.assertEqual(0, len(outbox)) 

        response = self.client.post("/administration/approve_user/%d" % new_user.id)

        self.assertEqual(0, len(outbox))
        
        self.assertEqual(302, response.status_code)
        self.assertTrue(TaoUser.objects.get(pk=new_user.id).is_active)

    def testRejectUser(self):
        new_user = TaoUser(username='username', email='email@email.com', first_name='fname', last_name='lname', is_active=False, institution='Intersect', scientific_interests='', title='Mr')
        new_user.set_password('password')
        new_user.save()

        self.assertEquals(2, len(TaoUser.objects.all()))
        self.assertFalse(new_user.is_active)
        self.assertFalse(new_user.rejected)

        self.assertTrue(self.client.login(username='superman', password='superman'))

        outbox = mail.outbox #@UndefinedVariable
        self.assertEqual(0, len(outbox))

        reject_reason = 'Superman cannot use the system.'
        response = self.client.post("/administration/reject_user/%d" % new_user.id, {'reason':reject_reason})

        self.assertEqual(1, len(outbox))
        email_content = str(outbox[0].body)
        self.assertTrue(reject_reason in email_content)

        self.assertEqual(302, response.status_code)
        rejected_user = TaoUser.objects.get(pk=new_user.id)
        self.assertTrue(rejected_user.rejected)
        self.assertFalse(rejected_user.is_active)
