from tao.tests.support.factories import DataSetFactory, DataSetPropertyFactory, GalaxyModelFactory, GlobalParameterFactory, SimulationFactory, UserFactory, SnapshotFactory, StellarModelFactory, DustModelFactory, BandPassFilterFactory, SurveyPresetFactory
from tao.tests.integration_tests.helper import LiveServerTest

class DatasetTests(LiveServerTest):
    def setUp(self):
        super(DatasetTests, self).setUp()

        s1 = SimulationFactory.create()
        s2 = SimulationFactory.create()
        s3 = SimulationFactory.create()

        gm1 = GalaxyModelFactory.create()
        gm2 = GalaxyModelFactory.create()

        ds1 = DataSetFactory.create(simulation=s1, galaxy_model=gm1, max_job_box_count=25)
        ds2 = DataSetFactory.create(simulation=s2, galaxy_model=gm2, max_job_box_count=25)
        ds3 = DataSetFactory.create(simulation=s3, galaxy_model=gm2, max_job_box_count=25)
        self.default_dataset = ds2

        DataSetPropertyFactory.create(dataset=ds1, name='dataset property 1')
        DataSetPropertyFactory.create(dataset=ds2, name='dataset property 2')
        self.default_dataset.default_filter_field = DataSetPropertyFactory.create(dataset=ds3, name='dataset property 3')
        self.default_dataset.save()
        SnapshotFactory.create(dataset=self.default_dataset, redshift='0.33')
        self.survey_preset = SurveyPresetFactory.create(name='Preset 1', parameters='<xml></xml>')

        for i in range(3):
            StellarModelFactory.create(label='stellar_label_%03d' % i, name='stellar_name_%03d' % i, description='<p>Description %d </p>' % i)
            BandPassFilterFactory.create(label='Band pass filter %03d' % i, filter_id='%d' % i)
            DustModelFactory.create(name='Dust_model_%03d.dat' % i, label='Dust model %03d' % i, details='<p>Detail %d </p>' % i)
            SnapshotFactory.create(dataset_id=i);

        password = 'password'
        user = UserFactory.create(username='user', is_superuser=True)
        user.set_password(password)
        user.save()
        self.login(user.username, password)

    def test_default_dataset_loads_correctly(self):
        GlobalParameterFactory.create(parameter_name='default_dataset', parameter_value=self.default_dataset.pk)
        self.visit('mock_galaxy_factory')
        self.assert_on_page('mock_galaxy_factory')
        self.click('tao-tabs-light_cone')
        selected_simulation = self.get_selected_option_text(self.lc_id('dark_matter_simulation'))
        self.assertEqual(self.default_dataset.simulation.name, selected_simulation)
        selected_galaxy_model = self.get_selected_option_text(self.lc_id('galaxy_model'))
        self.assertEqual(self.default_dataset.galaxy_model.name, selected_galaxy_model)
        