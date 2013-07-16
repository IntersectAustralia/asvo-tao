import json
from django.core.urlresolvers import reverse
from django.test import Client, TestCase
from django.test.utils import override_settings
from tao.tests.support.factories import JobFactory, UserFactory, WorkflowCommandFactory

class WorkflowApiTest(TestCase):
    def setUp(self):
        super(WorkflowApiTest, self).setUp()

        self.client = Client()
        self.client.defaults = {'REMOTE_ADDR': '123.2.3.4'}

        user = UserFactory.create()
        self.job = JobFactory.create(user=user)
        self.wfcommand = WorkflowCommandFactory.create(job_id=self.job, submitted_by=user, execution_status='QUEUED')

        self.url_all_wfcommand = reverse('api_dispatch_list', kwargs={'resource_name': 'workflowcommand', 'api_name': 'v1'})
        # print self.url_all_wfcommand
        self.url_by_wf_id = reverse('api_dispatch_detail', kwargs={'resource_name': 'workflowcommand', 'api_name': 'v1', 'pk': self.wfcommand.id})
        # self.url_by_job_id = reverse('api_dipatch_detail', kwargs={'resource_name': 'workflowcommand', 'api_name': 'v1'}, job_id = job.id)
        # print self.url_by_job_id
        self.data = {'format': 'json'}

    def tearDown(self):
        super(WorkflowApiTest, self).tearDown()

    @override_settings(API_ALLOWED_IPS=['123.2.3.4'])
    def test_allowed_user_can_read_api(self):
        resp = self.client.get(self.url_all_wfcommand, data=self.data)
        self.assertEqual(200, resp.status_code)

        resp = self.client.get(self.url_by_wf_id, data=self.data)
        self.assertEqual(200, resp.status_code)

        url_by_job_id = self.url_all_wfcommand + '?job_id=' + str(self.job.id)
        resp = self.client.get(url_by_job_id, data=self.data)
        self.assertEqual(200, resp.status_code)

        url_by_status = self.url_all_wfcommand + '?execution_status=QUEUED'
        resp = self.client.get(url_by_status, data=self.data)
        self.assertEqual(200, resp.status_code)

    @override_settings(API_ALLOWED_IPS=['122.1.1.1'])
    def test_unauthorised_user_cannot_access_api(self):
        resp = self.client.get(self.url_all_wfcommand, data=self.data)
        self.assertEqual(401, resp.status_code)

        resp = self.client.get(self.url_by_wf_id, data=self.data)
        self.assertEqual(401, resp.status_code)

        url_by_job_id = self.url_all_wfcommand + '?job_id=' + str(self.job.id)
        resp = self.client.get(url_by_job_id, data=self.data)
        self.assertEqual(401, resp.status_code)

        url_by_status = self.url_all_wfcommand + '?execution_status=QUEUED'
        resp = self.client.get(url_by_status, data=self.data)
        self.assertEqual(401, resp.status_code)

    @override_settings(API_ALLOWED_IPS=['123.2.3.4'])
    def test_allowed_user_can_update_api(self):
        self.data = {'execution_comment': 'unit testing PUT'}
        resp = self.client.put(self.url_by_wf_id, data=json.dumps(self.data), content_type='application/json')
        self.assertEqual(204, resp.status_code)

    @override_settings(API_ALLOWED_IPS=['122.1.1.1'])
    def test_unauthorised_user_cannot_update_api(self):
        self.data = {'execution_comment': 'unit testing PUT'}
        resp = self.client.put(self.url_by_wf_id, data=json.dumps(self.data), content_type='application/json')
        self.assertEqual(401, resp.status_code)