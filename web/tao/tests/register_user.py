from django.test.client import Client
from django.test.testcases import TestCase
from tao.models import User, UserProfile
from django.core import mail


class RegisterUserTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        super_user = User(username='superman', email='email@super.com', first_name='super', last_name='man', is_active=True, is_staff=True)
        super_user.set_password('superman')
        super_user.save()
        mail.outbox = []

    def testApproveUser(self):
        new_user = User(username='username', email='email@email.com', first_name='fname', last_name='lname', is_active=False)
        new_user.set_password('password')
        new_user.save()
        new_user_profile = UserProfile(user=new_user, institution='Intersect', scientific_interests='', title='Mr')
        new_user_profile.save()

        self.assertEquals(2, len(User.objects.all()))
        self.assertFalse(new_user.is_active)

        self.assertTrue(self.client.login(username='superman', password='superman'))

        self.assertEqual(0, len(mail.outbox))

        response = self.client.post("/admininistration/approve_user/%d" % new_user.id)

        self.assertEqual(1, len(mail.outbox))
        
        self.assertEqual(302, response.status_code)
        self.assertTrue(User.objects.get(pk=new_user.id).is_active)

    def testRejectUser(self):
        new_user = User(username='username', email='email@email.com', first_name='fname', last_name='lname', is_active=False)
        new_user.set_password('password')
        new_user.save()
        new_user_profile = UserProfile(user=new_user, institution='Intersect', scientific_interests='', title='Mr')
        new_user_profile.save()

        self.assertEquals(2, len(User.objects.all()))
        self.assertFalse(new_user.is_active)
        self.assertFalse(new_user.get_profile().rejected)

        self.assertTrue(self.client.login(username='superman', password='superman'))

        self.assertEqual(0, len(mail.outbox))

        reject_reason = 'Superman cannot use the system.'
        response = self.client.post("/admininistration/reject_user/%d" % new_user.id, {'reason':reject_reason})

        self.assertEqual(1, len(mail.outbox))
        email_content = str(mail.outbox[0].body)
        self.assertTrue(reject_reason in email_content)

        self.assertEqual(302, response.status_code)
        rejected_user = User.objects.get(pk=new_user.id)
        self.assertTrue(rejected_user.get_profile().rejected)
        self.assertFalse(rejected_user.is_active)
