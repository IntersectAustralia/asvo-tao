from tao.models import Simulation, StellarModel, DustModel, BandPassFilter
from tao.settings import MODULE_INDICES, PROJECT_DIR
from tao.tests.integration_tests.helper import LiveServerTest
from tao.tests.support.factories import UserFactory, SimulationFactory, GalaxyModelFactory, DataSetFactory, JobFactory, DataSetPropertyFactory, DustModelFactory, StellarModelFactory, BandPassFilterFactory, GlobalParameterFactory

import os.path

class JobTypeFormTests(LiveServerTest):

    def setUp(self):
        super(JobTypeFormTests, self).setUp()

        GlobalParameterFactory.create(parameter_name='maximum-random-light-cones', parameter_value='10')
        box_sim = SimulationFactory.create(box_size=500, name='simulation_000')
        lc_sim = SimulationFactory.create(box_size=60,name='simulation_001')

        for i in range(3):
            g = GalaxyModelFactory.create(name='galaxy_model_%03d' % i)
            ds = DataSetFactory.create(simulation=box_sim, galaxy_model=g, max_job_box_count=25)
            for j in range(3):
                DataSetPropertyFactory.create(dataset=ds, label='parameter_%03d label' % j, name='name_%03d' % j, description='description_%03d' % j)


        for i in range(4,8):
            g = GalaxyModelFactory.create(name='galaxy_model_%03d' % i)
            ds = DataSetFactory.create(simulation=lc_sim, galaxy_model=g, max_job_box_count=25)
            for j in range(4,7):
                dsp = DataSetPropertyFactory.create(dataset=ds, label='parameter_%03d label' % j, name='name_%03d' % j, description='description_%03d' % j)
                ds.default_filter_field = dsp
                ds.save()


        for i in range(3):
            StellarModelFactory.create(label='stellar_label_%03d' % i, name='stellar_name_%03d' % i, description='<p>Description %d </p>' % i)
            BandPassFilterFactory.create(label='Band pass filter %03d' % i, filter_id='Band_pass_filter_%03d.txt' % i)
            DustModelFactory.create(name='Dust_model_%03d.dat' % i, label='Dust model %03d' % i, details='<p>Detail %d </p>' % i)

        username = "person"
        password = "funnyfish"
        self.user = UserFactory.create(username=username, password=password, is_staff=True, is_active=True, is_superuser=True)
        self.login(username, password)

        self.visit('mock_galaxy_factory')
        self.click('tao-tabs-' + MODULE_INDICES['job_type'])

        params_path = os.path.join(PROJECT_DIR, 'test_data', 'params.xml')
        params_file = open(params_path)
        self.selenium.find_element_by_id('id_job_type-params_file').send_keys(params_path)


    def tearDown(self):
        super(JobTypeFormTests, self).tearDown()


    def test_light_cone_params(self):

        # from code import interact
        # interact(local=locals())
        
        self.click('tao-tabs-' + MODULE_INDICES['light_cone'])

        lc_geometry = self.get_selected_option_text(self.lc_id('catalogue_geometry'))
        self.assertEqual('Light-Cone', lc_geometry)

        lc_sim = self.get_selected_option_text(self.lc_id('dark_matter_simulation'))
        self.assertEqual('simulation_001', lc_sim)

        lc_galaxy = self.get_selected_option_text(self.lc_id('galaxy_model'))
        self.assertEqual('galaxy_model_006', lc_galaxy)

        lc_expected = { 
            self.lc_id('ra_opening_angle'): '1',
            self.lc_id('dec_opening_angle'): '2',
            self.lc_id('redshift_min'): '3',
            self.lc_id('redshift_max'): '4',

            self.lc_id('number_of_light_cones'): '3'
        }

        self.assert_attribute_equals('value', lc_expected)

        self.assert_is_checked(self.lc_id('light_cone_type_1'))

        self.assert_multi_selected_text_equals(self.lc_id('output_properties'), ['name_005'])


    def test_sed_params(self):
        self.click('tao-tabs-' + MODULE_INDICES['sed'])

        sed_pop = self.get_selected_option_text(self.sed_id('single_stellar_population_model'))
        self.assertEqual('stellar_label_001', sed_pop)

        self.assert_multi_selected_text_equals(self.sed_id('band_pass_filters'), ['Band pass filter 000 (Absolute)','Band pass filter 002 (Apparent)'])


    def test_rf_params(self):
        self.click('tao-tabs-' + MODULE_INDICES['record_filter'])

        rf_filter = self.get_selected_option_text(self.rf_id('filter'))
        self.assertEqual('Band pass filter 000', rf_filter)
        rf_expected = {
            self.rf_id('min'): '1',
            self.rf_id('max'): '12'
        }
        

    def test_output_params(self):
        self.click('tao-tabs-' + MODULE_INDICES['output_format'])
        out_format = self.get_selected_option_text('#id_output_format-supported_formats')
        self.assertEqual('FITS', out_format)
        

    def test_summary_params(self):
        self.click('tao-tabs-' + MODULE_INDICES['summary'])

        self.assert_summary_field_correctly_shown('Light-Cone', 'light_cone', 'geometry_type')
        self.assert_summary_field_correctly_shown('simulation_001', 'light_cone', 'simulation')
        self.assert_summary_field_correctly_shown('galaxy_model_006', 'light_cone', 'galaxy_model')
        self.assert_summary_field_correctly_shown('1 property selected', 'light_cone', 'output_properties')

        self.assert_summary_field_correctly_shown('stellar_label_001', 'sed', 'single_stellar_population_model')
        self.assert_summary_field_correctly_shown('2 filters selected', 'sed', 'band_pass_filters')
        self.assert_summary_field_correctly_shown('None', 'sed', 'dust_model')

        self.assert_summary_field_correctly_shown(u'1 \u2264 Band pass filter 000 (Absolute) \u2264 12', 'record_filter', 'record_filter')

        self.assert_summary_field_correctly_shown('FITS', 'output', 'output_format')
