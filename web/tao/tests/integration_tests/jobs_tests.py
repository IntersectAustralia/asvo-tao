
from tao.tests.support.factories import JobFactory, UserFactory
from tao.tests.integration_tests import helper

class JobTest(helper.LiveServerTest):

    def setUp(self):
        super(JobTest, self).setUp()
        
        username = 'user'
        password = 'password'

        self.user = UserFactory.create(username=username)
        self.user.set_password(password)
        self.user.save()

        self.job = JobFactory.create(user=self.user)
        self.login(username, password)

    def test_view_job_without_files(self):
        self.visit('submitted_jobs')
        self._view_job(self.job)
        self.assert_page_has_content("This job has not completed (and hence has no output).")


    def _view_job(self, job):
        job_id = job.id
        job_link = self.selenium.find_element_by_id("view_job_%s" % job_id)
        job_link.click()

