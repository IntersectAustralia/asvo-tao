from django.conf import settings
from django.test.utils import override_settings

from tao.models import Job
from tao.tests import helper
from tao.tests.integration_tests.helper import LiveServerTest
from tao.tests.support.factories import JobFactory, UserFactory

import os, zipfile


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
        
        self.output_paths = ['job1', 'large_job']
        self.dir_paths = [os.path.join(settings.FILES_BASE, output_path) for output_path in self.output_paths]

        self.file_names_to_contents = {
                                       'file1': 'abc\n', 
                                       'filez2.txt': 'pqr\n', 
                                       'file3': 'xyz\n',
                                       'job2/fileA': 'aaaahhhh',
                                       'job2/fileB': 'baaaaaa',
                                       }
        self.file_names_to_contents2 = {
                                       'waybigfile1': 'xnfaihnehrawlrwerajelrjxmjaeimrjwmrejlxaljrxm;kjmrlakjemrajlejrljrljaereirje;rjmriarie;rirjijeaim;jea;ljmxirjwra;ojer',
                                       'waybigfile2': 'xnfaihnehrawlrwerajelrjxmjaeimrjwmrejlxaljrxm;kjmrlakjemrajlejrljrljaereirje;rjmriarie;rirjijeaim;jea;ljmxirjwra;ojer',
                                       'waybigfile3': 'xnfaihnehrawlrwerajelrjxmjaeimrjwmrejlxaljrxm;kjmrlakjemrajlejrljrljaereirje;rjmriarie;rirjijeaim;jea;ljmxirjwra;ojer',
                                       'waybigfile4': 'xnfaihnehrawlrwerajelrjxmjaeimrjwmrejlxaljrxm;kjmrlakjemrajlejrljrljaereirje;rjmriarie;rirjijeaim;jea;ljmxirjwra;ojer',
                                       'waybigfile5': 'xnfaihnehrawlrwerajelrjxmjaeimrjwmrejlxaljrxm;kjmrlakjemrajlejrljrljaereirje;rjmriarie;rirjijeaim;jea;ljmxirjwra;ojer',
                                       }
        
        for file_name in self.file_names_to_contents.keys():
            helper.create_file(self.dir_paths[0], file_name, self.file_names_to_contents)
        for file_name in self.file_names_to_contents2.keys():
            helper.create_file(self.dir_paths[1], file_name, self.file_names_to_contents2)    
            
    def tearDown(self):
        super(JobTest, self).tearDown()
        for root, dirs, files in os.walk(settings.FILES_BASE, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
                
    def test_view_job_with_files(self):
        self.login(self.username, self.password)
        
        completed_job = JobFactory.create(user=self.user, status=Job.COMPLETED, output_path=self.output_paths[0])
        
        self.visit('view_job', completed_job.id)

        self.assert_page_has_content(completed_job.parameters)
        li_elements = self.selenium.find_elements_by_css_selector('#id_completed_jobs li')
        self.assertEqual(sorted(self.file_names_to_contents.keys()), sorted([li.text for li in li_elements]))
        
        # test files download 
        for li in li_elements:
            li.find_element_by_css_selector('a').click()
            
            split_name = li.text.split('/')
            file_name = split_name[-1]
            download_path = os.path.join(self.DOWNLOAD_DIRECTORY, file_name)
            self.assertTrue(os.path.exists(download_path))
            f = open(download_path)
            self.assertEqual(self.file_names_to_contents[li.text], f.read())
            f.close()
            
    # test that anonymous user cannot view job or download files
    def test_anonymous_user_cannot_view_or_download(self):
        completed_job = JobFactory.create(user=self.user, status=Job.COMPLETED, output_path=self.output_paths[0])
        self.visit('view_job', completed_job.id)
        
        self.assert_on_page('login', ignore_query_string=True)
        
        first_filename = self.file_names_to_contents.keys()[0]

        self.visit('get_file', completed_job.id, first_filename) 
        
        self.assert_on_page('login', ignore_query_string=True)
        
        download_path = os.path.join(self.DOWNLOAD_DIRECTORY, first_filename)
        self.assertFalse(os.path.exists(download_path))
        
    # test that another logged-in user cannot view job or download files created by the original user
    def test_other_user_cannot_view_or_download(self):
        username = 'user2'
        password = 'password2'

        user2 = UserFactory.create(username=username)
        user2.set_password(password)
        user2.save()
                
        completed_job = JobFactory.create(user=self.user, status=Job.COMPLETED, output_path=self.output_paths[0])
        
        helper.create_file(self.dir_paths[0], 'file1', self.file_names_to_contents)
        
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

    def test_zip_file_download(self):
        completed_job = JobFactory.create(user=self.user, status=Job.COMPLETED, output_path=self.output_paths[0])

        self.login(self.username, self.password)
        self.visit('view_job', completed_job.id)
            
        download_link = self.selenium.find_element_by_id('id_download_as_zip')
        download_link.click()
        
        download_path = os.path.join(self.DOWNLOAD_DIRECTORY, 'tao_output.zip')

        self.assertTrue(os.path.exists(download_path))
        
        # extract the files
        extract_path = os.path.join(self.DOWNLOAD_DIRECTORY, 'tao_output')
        self._extract_zipfile_to_dir(download_path, extract_path)
        
        self._assert_directories_match(self.dir_paths[0], extract_path)
                
    def test_zip_file_displayed(self):
        self.login(self.username, self.password)
        completed_job = JobFactory.create(user=self.user, status=Job.COMPLETED, output_path=self.output_paths[0])
        self.visit('view_job', completed_job.id)
        
        self.assert_page_has_content('Download zip file')
        
    @override_settings(MAX_DOWNLOAD_SIZE=40)
    def test_large_zip_file_not_displayed(self):
        self.login(self.username, self.password)
        completed_job = JobFactory.create(user=self.user, status=Job.COMPLETED, output_path=self.output_paths[1])
        self.visit('view_job', completed_job.id)
        
        self.assert_page_does_not_contain('Download zip file')
        self.assert_page_has_content('Zip file exceeds maximum download size.')
    
    @override_settings(MAX_DOWNLOAD_SIZE=10)
    def test_large_file_not_downloadable(self):
        """ Job output files larger than the download limit gets displayed, but are not downloadable.
        """
        self.login(self.username, self.password)
        large_completed_job = JobFactory.create(user=self.user, status=Job.COMPLETED, output_path=self.output_paths[1])
        self.visit('view_job', large_completed_job.id)
        
        for file_name in self.file_names_to_contents2.keys():
            self.assert_page_has_content(file_name + " (File size exceeds download limit.)")
            
        for file_name in self.file_names_to_contents2.keys():
            self.visit('get_file', large_completed_job.id, file_name)
            self.assert_page_has_content('Forbidden')

    @override_settings(MAX_DOWNLOAD_SIZE=10)
    def test_small_file_downloads(self):
        self.login(self.username, self.password)
        small_completed_job = JobFactory.create(user=self.user, status=Job.COMPLETED, output_path=self.output_paths[0])
        self.visit('view_job', small_completed_job.id)
        
        for file_name in self.file_names_to_contents.keys():
            self.assert_page_has_content(file_name)
            self.assert_page_does_not_contain("(File size exceeds download limit.)")
        
        for file_name in self.file_names_to_contents.keys():
            self.visit('get_file', small_completed_job.id, file_name)
            download_path = os.path.join(self.DOWNLOAD_DIRECTORY, os.path.basename(file_name))
            self.assertTrue(os.path.exists(download_path))
        
    def _extract_zipfile_to_dir(self, download_path, dirname):
        fullpathhandle = open(download_path, 'r')
        zipfile_obj = zipfile.ZipFile(fullpathhandle)
        for filename in zipfile_obj.namelist(): 
            fullpath = os.path.join(dirname, filename)
            helper.mkdir_p(os.path.dirname(fullpath))
            helper.write_file_from_zip(zipfile_obj, filename, fullpath)
            
    def _assert_directories_match(self, expected_dir_path, actual_dir_path):
        expected_dir_list = self._list_all_files(expected_dir_path)
        actual_dir_list = self._list_all_files(actual_dir_path)
        self.assertEqual(len(expected_dir_list), len(actual_dir_list))
        
        expected_dir_list.sort()
        actual_dir_list.sort()
        self.assertEqual(expected_dir_list, actual_dir_list)
        
        for first, second in zip(expected_dir_list, actual_dir_list):
            first_path = os.path.join(expected_dir_path, first)
            second_path = os.path.join(actual_dir_path, second)
            with open(first_path, 'r') as f1:
                with open(second_path, 'r') as f2:
                    self.assertEqual(f1.read(), f2.read())
            
    def _click_view_job(self, job):
        job_id = job.id
        job_link = self.selenium.find_element_by_id("view_job_%s" % job_id)
        job_link.click()

    def _list_all_files(self, dir):
        list_of_files = []
        for root, dirnames, filenames in os.walk(dir):
            for name in filenames:
                list_of_files.append(os.path.join(root[len(dir)+1:], name))
        return list_of_files
