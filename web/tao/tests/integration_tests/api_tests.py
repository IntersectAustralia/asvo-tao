from .helper import visit
from django.core.urlresolvers import reverse
from django.test import Client, TransactionTestCase
from django.test.utils import override_settings
from tao.tests.support.factories import JobFactory, UserFactory



class ApiTest(TransactionTestCase):
    
    def setUp(self):
        super(ApiTest, self).setUp()
        
        self.client = Client()
        self.client.defaults = {'REMOTE_ADDR': '123.2.3.4'}
        
        user = UserFactory.create()
        self.job = JobFactory.create(user=user)
        
    def tearDown(self):
        super(ApiTest, self).tearDown()
        
    @override_settings(API_ALLOWED_IPS=['123.2.3.4'])
    def test_allowed_user_can_access_API(self):
        response = visit(self.client, 'api_jobs')
        self.assertEqual(200, response.status_code)
    
        response = visit(self.client, 'api_jobs_by_id', self.job.id)
        self.assertEqual(200, response.status_code)
        
        response = visit(self.client, 'api_jobs_by_status', 'COMPLETED')
        self.assertEqual(200, response.status_code)
        
    @override_settings(API_ALLOWED_IPS=['122.1.1.1'])
    def test_unauthorised_user_cannot_access_API(self):
        response = visit(self.client, 'api_jobs') 
        self.assertEqual(403, response.status_code)
        
        response = visit(self.client, 'api_jobs_by_id', self.job.id)
        self.assertEqual(403, response.status_code)
        
        response = visit(self.client, 'api_jobs_by_status', 'COMPLETED')
        self.assertEqual(403, response.status_code)