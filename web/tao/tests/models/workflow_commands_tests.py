from datetime import datetime

from django.test.testcases import TestCase

from tao.models import Job, WorkflowCommand
from tao.tests.support.factories import JobFactory, UserFactory, WorkflowCommandFactory

import time

class WorkflowCommandsTests(TestCase):
    def setUp(self):
        super(WorkflowCommandsTests, self).setUp()
        user = UserFactory.create()
        job = JobFactory.create(user=user)
        self.jobID = job.id
        self.wfcommand = WorkflowCommandFactory.create(submitted_by=user, job_id=job, execution_comment='')

    def test_executed_time_initially_blank(self):
        self.assertEqual(None, self.wfcommand.executed)

    def test_executed_time_saved_on_complete(self):
        self.wfcommand.execution_status = Job.COMPLETED
        self.wfcommand.save()
        curr_time = datetime.now()
        self.assertNotEqual(None, self.wfcommand.executed)
        self.assert_date_time_equal(curr_time, self.wfcommand.executed)

    def test_executed_time_saved_on_error(self):
        self.wfcommand.execution_status = Job.ERROR
        self.wfcommand.save()
        curr_time = datetime.now()
        self.assertNotEqual(None, self.wfcommand.executed)
        self.assert_date_time_equal(curr_time, self.wfcommand.executed)

    def test_executed_time_updated_on_complete_after_resubmit(self):
        self.wfcommand.execution_status = Job.ERROR
        self.wfcommand.save()
        executed_error_time = datetime.now()

        self.wfcommand.execution_status = Job.SUBMITTED
        self.wfcommand.save()
        self.assert_date_time_equal(executed_error_time, self.wfcommand.executed)

        self.wfcommand.execution_status = Job.QUEUED
        self.wfcommand.save()
        self.assert_date_time_equal(executed_error_time, self.wfcommand.executed)

        self.wfcommand.execution_status = Job.IN_PROGRESS
        self.wfcommand.save()
        self.assert_date_time_equal(executed_error_time, self.wfcommand.executed)

        time.sleep(2)
        self.wfcommand.execution_status = Job.COMPLETED
        self.wfcommand.save()
        executed_completed_time = datetime.now()
        self.assert_date_time_equal(executed_completed_time, self.wfcommand.executed)

    def test_job_delete_command(self):
        self.wfcommand.command = WorkflowCommand.JOB_OUTPUT_DELETE
        self.wfcommand.execution_status = Job.COMPLETED
        self.wfcommand.save()

        jobs = Job.objects.all()
        self.assertEqual(0, len(jobs))

        self.wfcommand.execution_comment = 'Job %(id)s successfully deleted.' % {'id': self.jobID}

    def assert_date_time_equal(self, expected_datetime, actual_datetime):
        self.assertEqual(expected_datetime.date(), actual_datetime.date())
        self.assertEqual(expected_datetime.hour, actual_datetime.hour)
        self.assertEqual(expected_datetime.minute, actual_datetime.minute)
        self.assertEqual(expected_datetime.second, actual_datetime.second)