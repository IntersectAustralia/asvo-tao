from datetime import datetime

from django.test.testcases import TestCase

from tao.models import Job
from tao.tests.support.factories import UserFactory, WorkflowCommandFactory

import time

class WorkflowCommandsTests(TestCase):
    def setUp(self):
        super(WorkflowCommandsTests, self).setUp()
        user = UserFactory.create()
        self.wfcommand = WorkflowCommandFactory.create(submitted_by=user)

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

    def assert_date_time_equal(self, expected_datetime, actual_datetime):
        self.assertEqual(expected_datetime.date(), actual_datetime.date())
        self.assertEqual(expected_datetime.hour, actual_datetime.hour)
        self.assertEqual(expected_datetime.minute, actual_datetime.minute)
        self.assertEqual(expected_datetime.second, actual_datetime.second)