from django.core import mail
from django.conf import settings
from django.test.testcases import TestCase

from tao import models
from tao.models import Job, TaoUser
from tao.tests.support.factories import GlobalParameterFactory

import os

class JobTestCase(TestCase):
    def setUp(self):
        super(JobTestCase, self).setUp()
        GlobalParameterFactory(parameter_name='job-status.html', parameter_value='{{ job.id }} {{ user.username }}')
        GlobalParameterFactory(parameter_name='job-status.txt', parameter_value='{{ job.id }} {{ user.username }}')

        self.user = TaoUser()
        self.user.save()
        mail.outbox = []

    def tearDown(self):
        super(JobTestCase, self).tearDown()

    def test_initial_job_status(self):
        GlobalParameterFactory(parameter_name='INITIAL_JOB_STATUS', parameter_value='SUBMITTED')
        job = Job(user=self.user)
        self.assertEquals('SUBMITTED', job.status)

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

    def test_email_sent_only_when_completed(self):
        mail.outbox = []
        job = Job(user=self.user, status=Job.IN_PROGRESS, output_path='job_dir')
        job.save()
        self.assertEqual(0, len(mail.outbox))
        job.status = Job.COMPLETED
        job.save()
        self.assertEqual(1, len(mail.outbox))
        self.assertEquals('[ASVO-TAO] Catalogue status update',
                          mail.outbox[0].subject)
        mail_content = str(mail.outbox[0].body)
        self.assertTrue((str(job.id) in mail_content) and (self.user.username in mail_content))
