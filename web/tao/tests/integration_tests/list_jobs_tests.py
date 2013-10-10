from django.utils.timezone import get_default_timezone
from django.conf import settings

from tao.models import Job, GlobalParameter

from tao.tests import helper
from tao.tests.integration_tests.helper import LiveServerMGFTest
from tao.tests.support.factories import UserFactory, JobFactory

import os

class ListJobsTests(LiveServerMGFTest):

    fixtures = ['rules.json']

    def setUp(self):
        super(ListJobsTests, self).setUp()

        username = "user"
        password = "password"
        self.user = UserFactory.create(username=username, password=password)
        self.user.save()
        self.login(username, password)

        parameters = """<lightcone>
                        <database_type>sqlite</database_type>
                        <database_name>random.db</database_name>
                        <catalogue_geometry>cone</catalogue_geometry>
                        </lightcone>
                    """
        error_message = ['blah blah', 'wah wah', 'lah lah']

        self.held_job = JobFactory.create(user=self.user, parameters=parameters, status=Job.HELD)
        self.error_job = JobFactory.create(user=self.user, parameters=parameters, status=Job.ERROR, error_message=error_message[0])
        self.in_progress_job = JobFactory.create(user=self.user, parameters=parameters, status=Job.IN_PROGRESS)
        self.submitted_job = JobFactory.create(user=self.user, parameters=parameters, status=Job.SUBMITTED)
        self.completed_job = JobFactory.create(user=self.user, parameters=parameters, status=Job.COMPLETED)
        self.queued_job = JobFactory.create(user=self.user, parameters=parameters, status=Job.QUEUED)
        self.error_job2 = JobFactory.create(user=self.user, parameters=parameters, status=Job.ERROR, error_message=error_message[1])

        self.visit('job_index')

    def tearDown(self):
        super(ListJobsTests, self).tearDown()

    def _test_all_jobs_in_a_single_table(self):
        expected_jobs = [self.held_job, self.submitted_job, self.queued_job, self.in_progress_job, self.completed_job, self.error_job2, self.error_job]
        self.assert_job_table_equals(expected_jobs)

    def _test_completed_job_viewed_via_link(self):
        completed_id = self.completed_job.id
        self.assert_is_displayed('#view_job_' + str(completed_id))
        
        self.click('view_job_' + str(completed_id))
        self.assert_page_has_content('Viewing Job ' + str(completed_id))

    def _test_history_table_job_order(self):
        in_progress_job2 = JobFactory.create(user=self.user, status=Job.IN_PROGRESS)
        held_job2 = JobFactory.create(user=self.user, status=Job.HELD, description='2nd held job (should appear first in list)')
        in_progress_job3 = JobFactory.create(user=self.user, status=Job.IN_PROGRESS)
        in_progress_job4 = JobFactory.create(user=self.user, status=Job.IN_PROGRESS, description='most recent in progress job (should appear before other in_progress jobs)')
        self.visit('job_index')

        expected_jobs = [held_job2, self.held_job, self.submitted_job, self.queued_job, in_progress_job4, in_progress_job3, in_progress_job2, self.in_progress_job, self.completed_job, self.error_job2, self.error_job]
        self.assert_job_table_equals(expected_jobs)

    def assert_job_table_equals(self, expected_jobs):
        header_row = ['Id', 'Submitted Timestamp', 'Description', 'Status/Error Message']
        body = [self._get_job_tablebody(job) for job in expected_jobs]

        expected_table = [header_row] + body
        actual_table = self.table_as_text_rows('#jobs_table')
        self.assertEqual(expected_table, actual_table)

    def _get_job_tablebody(self, job):
        body = [str(job.id), job.created_time.astimezone(get_default_timezone()).strftime('%a %d %b %Y %H:%M'), job.description]
        if job.status == Job.ERROR:
            return body + [job.status+ ' ?']
        elif job.status == Job.COMPLETED:
            return [str(job.id), job.created_time.astimezone(get_default_timezone()).strftime('%a %d %b %Y %H:%M'), job.description, job.status]
        else:
            return body + [job.status]

    def _clean_parameter_lines(self, job):
        parameter_lines = job.parameters.split("\n")
        stripped_lines = [line.strip() for line in parameter_lines]
        return "\n".join(stripped_lines).strip()

    def test_user_disk_quota_no_limit(self):
        try:
            param = GlobalParameter.objects.get(parameter_name='default_disk_quota')
            param.delete()
        except (GlobalParameter.DoesNotExist, ValueError):
            pass
        
        quota = self.user.user_disk_quota()
        self.assertEqual(quota, -1)
        
        self.visit('job_index')
        
        disk_usage = self.user.display_current_disk_usage()
        self.assert_page_has_content(disk_usage)
        
        disk_quota = "of %s" % self.user.display_user_disk_quota()
        self.assert_page_does_not_contain(disk_quota)
        
    def test_user_disk_quota_default(self):
        try:
            param = GlobalParameter.objects.get(parameter_name='default_disk_quota')
            param.parameter_value = 100
            param.save()
        except (GlobalParameter.DoesNotExist, ValueError):
            param = GlobalParameter(parameter_name='default_disk_quota', parameter_value=100)
            param.save()
        
        self.user.disk_quota = 0
        self.user.save()
        
        self.visit('job_index')
            
        disk_usage = self.user.display_current_disk_usage()
        disk_quota = self.user.display_user_disk_quota()
        usage_text = "%s  of %s" % (disk_usage, disk_quota)
        self.assert_page_has_content(usage_text)
            
    def test_user_disk_quota_limit(self):
        self.user.disk_quota = 10
        self.user.save()
        self.visit('job_index')
        
        disk_usage = self.user.display_current_disk_usage()
        disk_quota = self.user.display_user_disk_quota()
        usage_text = "%s  of %s" % (disk_usage, disk_quota)
        self.assert_page_has_content(usage_text)
    
    
    def test_user_disk_usage_displays_correctly(self):
        output_path = 'job_output'
        file_content = 'abc' * 2000000
        file_name_to_content = {'file_name': file_content}
        helper.create_file(os.path.join(settings.FILES_BASE, output_path), 'file_name', file_name_to_content)
        self.user.disk_quota = 10
        self.user.save()
        self.visit('job_index')
        usage_text = "%s  of  %s" % ('6MB', '10MB')
        self.assert_page_has_content(usage_text)

