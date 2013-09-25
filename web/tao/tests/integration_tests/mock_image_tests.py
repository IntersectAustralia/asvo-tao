from tao.models import Job
from tao.tests.integration_tests.helper import LiveServerMGFTest
from tao.tests.support.factories import UserFactory, SimulationFactory, GalaxyModelFactory, DataSetFactory, \
    DataSetPropertyFactory, JobFactory, StellarModelFactory, SnapshotFactory, BandPassFilterFactory, \
    GlobalParameterFactory, SurveyPresetFactory, DustModelFactory

from taoui_light_cone.forms import Form as LightConeForm


class MockImageTests(LiveServerMGFTest):

    def setUp(self):
        super(MockImageTests, self).setUp()

        GlobalParameterFactory.create(parameter_name='maximum-random-light-cones', parameter_value='10')
        GlobalParameterFactory(parameter_name='INITIAL_JOB_STATUS', parameter_value='HELD')
        GlobalParameterFactory(parameter_name='job_too_large_warning', parameter_value='JOB_WARNING')
        simulation = SimulationFactory.create(box_size=500)
        galaxy_model = GalaxyModelFactory.create()
        dataset = DataSetFactory.create(simulation=simulation, galaxy_model=galaxy_model, max_job_box_count=15)
        DustModelFactory.create()

        self.redshifts = ['1.23456789', '2.987654321', '3.69154927', '4.567890123']
        for redshift in self.redshifts:
            SnapshotFactory.create(dataset=dataset, redshift=redshift)

        DataSetPropertyFactory.create(dataset=dataset)
        StellarModelFactory.create()
        BandPassFilterFactory.create()
        self.survey_preset = SurveyPresetFactory.create(name='Preset 1', parameters='<xml></xml>')

        self.username = "user"
        password = "password"
        self.user = UserFactory.create(username=self.username, password=password, is_staff=True, is_superuser=True)

        
        self.parameters = """<lightcone>
                        <database_type>sqlite</database_type>
                        <database_name>random.db</database_name>
                        <catalogue_geometry>cone</catalogue_geometry>
                        </lightcone>
                    """
        
        self.login(self.username, password)
        self.visit('mock_galaxy_factory')
        self.click('tao-tabs-' + 'light_cone')
        ## fill in ligght-cone and sed (correctly)
        self.select(self.lc_id('catalogue_geometry'), 'Light-Cone')
        self.fill_in_fields({
            'ra_opening_angle': '2',
            'dec_opening_angle': '2',
            'redshift_min': '1',
            'redshift_max': '2',
        }, id_wrap=self.lc_id)
        self.click(self.lc_2select('op_add_all'))
        self.click('tao-tabs-sed')
        self.click(self.sed('apply_sed'))
        self.click(self.sed_2select('op_add_all'))
        self.click('tao-tabs-record_filter')
        self.fill_in_fields({
            'min': '1\n',
            'max': '10\n',
        }, id_wrap=self.rf_id)
        self.click('tao-tabs-mock_image')

    def tearDown(self):
        super(MockImageTests, self).tearDown()

    def mi_image_id(self, number):
        return lambda bare_name: '.single-form:nth-child(%d) #id_mock_image-__prefix__-%s' % (number, bare_name)

    def test_no_mock_image_ok(self):
        self.submit_mgf_form()
        self.assert_on_page('job_index')

    def test_valid_min_max_equal(self):
        self.click(self.mi_id('apply_mock_image'))
        self.fill_in_fields({
            'z_min': '1',
            'z_max': '1',
        }, id_wrap=self.mi_image_id(1), clear=True)
        self.submit_mgf_form()
        self.assert_on_page('job_index')

    def test_two_images_ok(self):
        self.click(self.mi_id('apply_mock_image'))
        self.fill_in_fields({
            'z_min': '1',
            'z_max': '1.5',
        }, id_wrap=self.mi_image_id(1), clear=True)
        self.click(self.mi_id('add_image_button'))
        self.fill_in_fields({
            'z_min': '1.5',
            'z_max': '2',
        }, id_wrap=self.mi_image_id(2), clear=True)
        self.submit_mgf_form()
        self.assert_on_page('job_index')
        job = Job.objects.latest('created_time')
        self.assertTrue(job.user.username == self.user.username, 'Job created does not belong to user!')
        self.visit('view_job', job.id)
        # from code import interact
        # interact(local=locals())
        self.assert_page_has_content('2 images')
