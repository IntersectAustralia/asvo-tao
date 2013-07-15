import json
from django.core.urlresolvers import reverse
from django.test import Client, TestCase
from django.test.utils import override_settings
from tao.tests.support.factories import JobFactory, UserFactory


class JobApiTest(TestCase):

    def setUp(self):
        super(JobApiTest, self).setUp()

        self.client = Client()
        self.client.defaults = {'REMOTE_ADDR': '123.2.3.4'}

        user = UserFactory.create()
        self.job = JobFactory.create(user=user, status='HELD')

        self.url_all_job = reverse('api_dispatch_list', kwargs={'resource_name': 'job', 'api_name': 'v1'})
        self.url_by_job_id = reverse('api_dispatch_detail', kwargs={'resource_name': 'job', 'api_name': 'v1', 'pk': self.job.id})
        self.url_by_status = self.url_all_job + '?status=HELD'
        self.data = {'format': 'json'}

    def tearDown(self):
        super(JobApiTest, self).tearDown()

    @override_settings(API_ALLOWED_IPS=['123.2.3.4'])
    def test_allowed_user_can_access_job_api(self):
        response = self.client.get(self.url_all_job, data=self.data)
        self.assertEqual(200, response.status_code)

        response = self.client.get(self.url_by_job_id, data=self.data)
        self.assertEqual(200, response.status_code)

        response = self.client.get(self.url_by_status, data=self.data)
        self.assertEqual(200, response.status_code)

    @override_settings(API_ALLOWED_IPS=['122.1.1.1'])
    def test_unauthorised_user_cannot_access_job_api(self):
        response = self.client.get(self.url_all_job, data=self.data)
        self.assertEqual(401, response.status_code)

        response = self.client.get(self.url_by_job_id, data=self.data)
        self.assertEqual(401, response.status_code)

        response = self.client.get(self.url_by_status, data=self.data)
        self.assertEqual(401, response.status_code)

    @override_settings(API_ALLOWED_IPS=['123.2.3.4'])
    def test_allowed_user_can_update_job_api(self):
        self.data = {'status': 'COMPLETED'}
        resp = self.client.put(self.url_by_job_id, data=json.dumps(self.data), content_type='application/json')
        self.assertEqual(204, resp.status_code)

    @override_settings(API_ALLOWED_IPS=['122.1.1.1'])
    def test_unauthorised_user_cannot_update_job_api(self):
        self.data = {'status': 'ERROR'}
        resp = self.client.put(self.url_by_job_id, data=json.dumps(self.data), content_type='application/json')
        self.assertEqual(401, resp.status_code)