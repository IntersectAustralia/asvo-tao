from django.utils.timezone import get_default_timezone

from tao.models import Job
from tao.tests.integration_tests.helper import LiveServerMGFTest
from tao.tests.support.factories import UserFactory, JobFactory

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
        self.submitted_job = JobFactory.create(user=self.user, parameters=parameters, status=Job.SUBMITTED)
        self.queued_job = JobFactory.create(user=self.user, parameters=parameters, status=Job.QUEUED)
        self.in_progress_job = JobFactory.create(user=self.user, parameters=parameters, status=Job.IN_PROGRESS)
        self.completed_job = JobFactory.create(user=self.user, parameters=parameters, status=Job.COMPLETED)
        self.error_job = JobFactory.create(user=self.user, parameters=parameters, status=Job.ERROR, error_message=error_message[0])
        self.error_job2 =  JobFactory.create(user=self.user, parameters=parameters, status=Job.ERROR, error_message=error_message[1])

        self.visit('job_index')

    def tearDown(self):
        super(ListJobsTests, self).tearDown()

    def test_all_jobs_in_a_single_table(self):
        expected_jobs = [self.held_job, self.submitted_job, self.queued_job, self.in_progress_job, self.completed_job, self.error_job, self.error_job2]
        self.assert_job_table_equals(expected_jobs)

    def test_error_message_displayed_in_popup(self):
        self.assert_are_displayed_by_class_name('openPopUp')
        buttons = self.selenium.find_elements_by_class_name('openPopUp')

        buttons[0].click()
        self.assert_page_has_content(self.error_job.error_message)
        self.click_by_class_name('ui-button-text')

        buttons[1].click()
        self.assert_page_has_content(self.error_job2.error_message)

    def test_completed_job_viewed_via_link(self):
        completed_id = self.completed_job.id
        self.assert_is_displayed('#view_job_' + str(completed_id))
        
        self.click('view_job_' + str(completed_id))
        self.assert_page_has_content('Viewing Job ' + str(completed_id))

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
            return [str(job.id) + ' (View)', job.created_time.astimezone(get_default_timezone()).strftime('%a %d %b %Y %H:%M'), job.description, job.status]
        else:
            return body + [job.status]

    def _clean_parameter_lines(self, job):
        parameter_lines = job.parameters.split("\n")
        stripped_lines = [line.strip() for line in parameter_lines]
        return "\n".join(stripped_lines).strip()
