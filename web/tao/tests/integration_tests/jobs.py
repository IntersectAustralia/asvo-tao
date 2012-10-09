from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

from tao.tests.support.factories import JobFactory, UserFactory
from tao.models import Job

def wait():
    import time
    time.sleep(1)

def interact(locals):
    """
        drop into an interactive shell - can be helpful for debugging
        call like interact(locals())
    """
    import code
    code.interact(local=locals)



class JobTest(LiveServerTestCase):


    def setUp(self):
        super(JobTest, self).setUp()
        self.selenium = WebDriver()

        username = 'user'
        password = 'password'

        self.user = UserFactory.create(username=username)
        self.user.set_password(password)
        self.user.save()

        self.job = JobFactory.create(user=self.user)
        self._login(username, password)

    def tearDown(self):
        super(JobTest, self).tearDown()
        self.selenium.quit()

    def test_view_job_without_files(self):
        self._visit('submitted_jobs')
        self._view_job(self.job)
        self._assert_page_has_content("This job has not completed (and hence has no output).")


    def _login(self, username, password):
        self._visit('login')

        username_input = self.selenium.find_element_by_id('id_username')
        password_input = self.selenium.find_element_by_id('id_password')
        submit_button = self.selenium.find_element_by_tag_name('button')  # TODO make this more specific

        username_input.send_keys(username)
        password_input.send_keys(password)

        submit_button.submit()

    def _visit(self, url_name):
        """ self._visit(name_of_url_as_defined_in_your_urlconf) """
        from django.core.urlresolvers import reverse
        self.selenium.get("%s%s" % (self.live_server_url, reverse(url_name)))

    def _view_job(self, job):
        job_id = job.id
        job_link = self.selenium.find_element_by_id("view_job_%s" % job_id)
        job_link.click()

    def _assert_page_has_content(self, string):
        import re

        page_source = self.selenium.page_source

        pattern = re.escape(string)
        self.assertTrue(re.search(pattern, page_source), "page source did not contain %s" % pattern)
