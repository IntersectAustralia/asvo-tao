
from django.conf import settings
from tao.models import Job
from tao.tests import helper
from tao.tests.integration_tests.helper import LiveServerTest
from tao.tests.support.factories import JobFactory, UserFactory
import os


class JobTest(LiveServerTest):
    
    fixtures = ['rules.json']

    def setUp(self):
        super(JobTest, self).setUp()
        
        self.username = 'user'
        self.password = 'password'

        self.user = UserFactory.create(username=self.username)
        self.user.set_password(self.password)
        self.user.save()

        self.job = JobFactory.create(user=self.user)
        
        self.output_path = 'job1'
        self.dir_path = os.path.join(settings.FILES_BASE, self.output_path)
        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)
        self.output_path2 = 'job1/job2'
        self.dir_path2 = os.path.join(settings.FILES_BASE, self.output_path2)
        if not os.path.exists(self.dir_path2):
            os.makedirs(self.dir_path2)
            
        self.file_names_to_contents = {
                                  'file1': 'abc\n', 
                                  'filez2': 'pqr\n', 
                                  'file3': 'xyz\n',
                                  }
        self.file_names_to_contents2 = {
                                        'job2/fileA': 'aaaahhhh',
                                        'job2/fileB': 'baaaaaa',
                                        }
        
        
    def tearDown(self):
        super(JobTest, self).tearDown()
        for root, dirs, files in os.walk(self.dir_path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
                
    def test_view_job_with_files(self):
        self.login(self.username, self.password)
        
        completed_job = JobFactory.create(user=self.user, status=Job.COMPLETED, output_path='job1')
        
        # give the job some directory tree of files
        for file_name in self.file_names_to_contents.keys():
            helper.create_file(self.dir_path, file_name, self.file_names_to_contents)
        for file_name in self.file_names_to_contents2.keys():
            helper.create_file(self.dir_path, file_name, self.file_names_to_contents2)
        
        self.visit('view_job', completed_job.id)

        merged_file_names_to_contents = {}
        merged_file_names_to_contents.update(self.file_names_to_contents)
        merged_file_names_to_contents.update(self.file_names_to_contents2)
        self.assert_page_has_content(completed_job.parameters)
        li_elements = self.selenium.find_elements_by_css_selector('#id_completed_jobs li')
        self.assertEqual(sorted(merged_file_names_to_contents.keys()), [li.text for li in li_elements])
        
        # test files download 
        for li in li_elements:
            li.find_element_by_css_selector('a').click()
            
            split_name = li.text.split('/')
            file_name = split_name[-1]
            download_path = os.path.join(self.DOWNLOAD_DIRECTORY, file_name)
            self.assertTrue(os.path.exists(download_path))
            f = open(download_path)
            self.assertEqual(merged_file_names_to_contents[li.text], f.read())
            f.close()
            
    # test that anonymous user cannot view job or download files
    def test_anonymous_user_cannot_view_or_download(self):
        completed_job = JobFactory.create(user=self.user, status=Job.COMPLETED, output_path='job1')
        self.visit('view_job', completed_job.id)
        
        self.assert_on_page('login', ignore_query_string=True)
        
        helper.create_file(self.dir_path, 'file1', self.file_names_to_contents)

        self.visit('get_file', completed_job.id, 'file1') #file_path)
        
        self.assert_on_page('login', ignore_query_string=True)
        
        download_path = os.path.join(self.DOWNLOAD_DIRECTORY, 'file1')
        self.assertFalse(os.path.exists(download_path))
        
    # test that another logged-in user cannot view job or download files created by the original user
    def test_other_user_cannot_view_or_download(self):
        username = 'user2'
        password = 'password2'

        user2 = UserFactory.create(username=username)
        user2.set_password(password)
        user2.save()
                
        completed_job = JobFactory.create(user=self.user, status=Job.COMPLETED, output_path='job1')
        
        helper.create_file(self.dir_path, 'file1', self.file_names_to_contents)
        
        self.login(username, password)
        self.visit('view_job', completed_job.id)
        self.assert_page_has_content('Forbidden')
        
        self.visit('get_file', completed_job.id, 'file1')
        self.assert_page_has_content('Forbidden')
        
        download_path = os.path.join(self.DOWNLOAD_DIRECTORY, 'file1')
        self.assertFalse(os.path.exists(download_path))
        
    def test_view_job_without_files(self):
        self.login(self.username, self.password)
        
        self.visit('submitted_jobs')
        self._click_view_job(self.job)
        self.assert_page_has_content("This job has not completed (and hence has no output).")

    def _click_view_job(self, job):
        job_id = job.id
        job_link = self.selenium.find_element_by_id("view_job_%s" % job_id)
        job_link.click()

