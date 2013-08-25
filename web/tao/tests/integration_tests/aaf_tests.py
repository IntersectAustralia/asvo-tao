from django.contrib.sites.models import Site
from django.core import mail

from tao.models import TaoUser
from tao.tests.integration_tests import helper
from tao.tests.support.factories import UserFactory

import os

class AAFTests(helper.LiveServerTest):

    def setUp(self):
        os.environ['SHIB_auEdupersonSharedToken'] = "aafsharedtokenthingy"
        os.environ['SHIB_givenName'] = "Bob"
        os.environ['SHIB_surname'] = "Blog"
        os.environ['SHIB_email'] = "test@intersect.org.au"
        super(AAFTests, self).setUp()
        self.selenium.add_cookie({'_shibsession_': True})

    def tearDown(self):
        super(AAFTests, self).tearDown()
        del os.environ['SHIB_auEdupersonSharedToken']

    def test_aaf_registered(self):
        ## go to home
        ## check that TaoUser with username = aafsharedtokenthingy exists
        self.visit('home')
        aaf_user = TaoUser.objects.get(username="aafsharedtokenthingy")
        pass
        # self.assertNotEqual(None, aaf_user)
        # self.assertEqual(os.environ['SHIB_givenName'], aaf_user.givenName)
