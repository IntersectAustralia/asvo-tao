from django.conf import settings
from django.test.testcases import TestCase

from tao.models import Job, User
#from tao.tests import helper
from tao.tests.support.factories import JobFactory

import os

class JobTestCase(TestCase):
    def setUp(self):
        super(JobTestCase, self).setUp()
        
        self.user = User()
        self.user.save()

    def tearDown(self):
        super(JobTestCase, self).tearDown()
        
    def test_not_available_unless_completed(self):
        self.jobs = dict((status, Job(status=status, user=self.user)) for (status, _) in Job.STATUS_CHOICES)

        for status, job in self.jobs.iteritems():
            job.save()


        for status, _ in Job.STATUS_CHOICES:
            if status != Job.COMPLETED:
                self.assertRaises(Exception, self.jobs[status].files)
            else:
                self.jobs[status].files()

    def test_files(self):
        output_path = 'job_dir'
        j = Job(user=self.user, status=Job.COMPLETED, output_path=output_path)
        j.save()
        
        dir_path = os.path.join(settings.FILES_BASE, output_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        output_path2 = 'job_dir/job_subdir'
        dir_path2 = os.path.join(settings.FILES_BASE, output_path2)
        if not os.path.exists(dir_path2):
            os.makedirs(dir_path2)
            
        file_names_to_contents = {
                                'file1': 'ksjhfewiu\n',
                                'filez2': 'faeowrfjieawmnc\n',
                                'file3': 'sdlkjfaeowijfiaowjef\n',
                                }
        file_names_to_contents2 = {
                                'job_subdir/fileA': 'aaaaahhhhhhh',
                                'job_subdir/fileB': 'baaaaaaaahhhhhh',
                                }
        from tao.tests import helper
        for file_name in file_names_to_contents.keys():
            helper.create_file(dir_path, file_name, file_names_to_contents)
        for file_name in file_names_to_contents2.keys():
            helper.create_file(dir_path, file_name, file_names_to_contents2)
            
        merged_file_names_to_contents = {}
        merged_file_names_to_contents.update(file_names_to_contents)
        merged_file_names_to_contents.update(file_names_to_contents2)
        self.assertEqual(sorted(merged_file_names_to_contents.keys()), sorted([job_file.file_name for job_file in j.files()]))

