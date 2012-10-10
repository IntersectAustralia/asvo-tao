from django.test.testcases import TestCase

from tao.datasets import dark_matter_simulation_choices, galaxy_model_choices
from tao.models import Job, User


class JobTestCase(TestCase):
    def setUp(self):
        self.user = User()
        self.user.save()

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
        output_dir = 'something'
        j = Job(user=self.user, status=Job.COMPLETED)
        j.save()

        j.files()
