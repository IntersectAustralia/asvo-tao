from django.conf import settings

from tao.models import Job
from tao.tests import helper
from tao.tests.integration_tests.helper import LiveServerTest
from tao.tests.support.factories import UserFactory, JobFactory, GlobalParameterFactory, SimulationFactory, GalaxyModelFactory, DataSetFactory, DataSetPropertyFactory, SnapshotFactory, SurveyPresetFactory

import os


class DiskStorageTests(LiveServerTest):
    fixtures = ['rules.json']

    def setUp(self):
        super(DiskStorageTests, self).setUp()

        username = 'user'
        password = 'password'

        self.user = UserFactory.create(username=username, is_superuser=True)
        self.user.set_password(password)
        self.user.save()
        self.login(username, password)

        output_path = 'job_output'
        self.job = JobFactory.create(user=self.user, status=Job.COMPLETED, output_path=output_path)
        file_content = 'abc' * 2000000
        file_name_to_content = {'file_name': file_content}
        helper.create_file(os.path.join(settings.FILES_BASE, output_path), 'file_name', file_name_to_content)
        self.job.save()

        self.simulation = SimulationFactory.create()
        self.galaxy = GalaxyModelFactory.create()
        self.dataset = DataSetFactory.create(simulation=self.simulation, galaxy_model=self.galaxy)
        self.output_prop = DataSetPropertyFactory.create(dataset=self.dataset, name='Central op', is_filter=False)
        self.filter = DataSetPropertyFactory.create(name='CentralMvir rf', units="Msun/h", dataset=self.dataset)
        self.computed_filter = DataSetPropertyFactory.create(name='Computed Property', dataset=self.dataset, is_computed=True)
        self.snapshot = SnapshotFactory.create(dataset=self.dataset, redshift='0.33')
        self.survey_preset = SurveyPresetFactory.create(name='Preset 1', parameters='<xml></xml>')

        self.default_disk_quota = GlobalParameterFactory.create(parameter_name='default_disk_quota', parameter_value='6')

    def tearDown(self):
        super(DiskStorageTests, self).tearDown()
        for root, dirs, files in os.walk(settings.FILES_BASE, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    def test_under_disk_quota_can_get_new_catalogue(self):
        # check for both default_disk_quota and disk_quota allocated to the user
        self.visit('mock_galaxy_factory')


        self.assert_on_page('mock_galaxy_factory')

        self.visit('job_index')
        self.default_disk_quota.parameter_value = 5  # lower default_disk_quota for testing user's allocated disk_quota
        self.default_disk_quota.save()
        self.user.disk_quota = 6
        self.user.save()
        self.visit('mock_galaxy_factory')
        self.assert_on_page('mock_galaxy_factory')

        # test user with unlimited disk quota
        self.user.disk_quota = -1
        self.user.save()
        self.visit('mock_galaxy_factory')
        self.assert_on_page('mock_galaxy_factory')

    def test_above_disk_quota_cannot_get_new_catalogue(self):
        self.default_disk_quota.parameter_value = 5
        self.default_disk_quota.save()
        self.visit('mock_galaxy_factory')
        self.assert_on_page('job_index')

        self.default_disk_quota.parameter_value = 6  # reset default_disk_quota for testing user's allocated disk_quota
        self.default_disk_quota.save()
        self.user.disk_quota = 5
        self.user.save()
        self.visit('mock_galaxy_factory')
        self.assert_on_page('job_index')

    def test_current_disk_usage_displayed_on_history_page(self):
        self.visit('job_index')
        usage_str = self.user.display_current_disk_usage().strip() + ' of ' + self.user.display_user_disk_quota().strip()
        self.assert_element_text_equals('#id_current_disk_usage', usage_str)