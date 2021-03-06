from tao.models import Simulation, StellarModel, DustModel, BandPassFilter
from tao.settings import PROJECT_DIR
from tao.tests.integration_tests.helper import LiveServerTest
from tao.tests.support.factories import UserFactory, SimulationFactory, GalaxyModelFactory, DataSetFactory, JobFactory, DataSetPropertyFactory, DustModelFactory, StellarModelFactory, BandPassFilterFactory, GlobalParameterFactory, SnapshotFactory, SurveyPresetFactory

import os.path

class JobTypeFormTests(LiveServerTest):

    def setUp(self):
        super(JobTypeFormTests, self).setUp()

        GlobalParameterFactory.create(parameter_name='maximum-random-light-cones', parameter_value='10')
        box_sim = SimulationFactory.create(box_size=500, name='simulation_000')
        lc_sim = SimulationFactory.create(box_size=60,name='simulation_001')

        self.params_path = os.path.join(PROJECT_DIR, 'test_data', 'params.xml')
        params_string = open(self.params_path).read()

        for i in range(3):
            g = GalaxyModelFactory.create(name='galaxy_model_%03d' % i)
            ds = DataSetFactory.create(simulation=box_sim, galaxy_model=g, max_job_box_count=25)
            for j in range(10):
                SnapshotFactory.create(dataset=ds, redshift=str(j)+".0")
            for j in range(3):
                dsp = DataSetPropertyFactory.create(dataset=ds, label='parameter_%03d label' % j, name='name_%03d' % j, description='description_%03d' % j)
                ds.default_filter_field = dsp
                ds.save()


        for i in range(4,8):
            g = GalaxyModelFactory.create(name='galaxy_model_%03d' % i)
            ds = DataSetFactory.create(simulation=lc_sim, galaxy_model=g, max_job_box_count=25, id=i)
            for j in range(10):
                SnapshotFactory.create(dataset=ds, redshift=str(j)+".0")
            for j in range(4,7):
                dsp = DataSetPropertyFactory.create(dataset=ds, label='parameter_%03d label' % j, name='name_%03d' % j, description='description_%03d' % j)
                ds.default_filter_field = dsp
                ds.save()


        for i in range(3):
            StellarModelFactory.create(label='stellar_label_%03d' % i,
                                       name='model{0}/sspm.dat'.format(i),
                                       description='<p>Description %d </p>' % i)
            BandPassFilterFactory.create(label='Band pass filter %03d' % i, filter_id='%d' % i)
            DustModelFactory.create(name='Dust_model_%03d.dat' % i, label='Dust model %03d' % i, details='<p>Detail %d </p>' % i)
            SurveyPresetFactory.create(name='Preset %d' % i, parameters=params_string)

        username = "person"
        password = "funnyfish"
        self.user = UserFactory.create(username=username, password=password, is_staff=True, is_active=True, is_superuser=True)
        self.login(username, password)

        self.visit('mock_galaxy_factory')
        self.click('tao-tabs-job_type')


    def tearDown(self):
        super(JobTypeFormTests, self).tearDown()


    def test_light_cone_params(self):
        self.upload_params_file()

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
        self.assert_multi_selected_text_equals(self.lc_id('output_properties-right'), ['parameter_005 label'])
        rng_seeds_expected = [111111, 222222, 333333]
        rng_seeds_actual = self.selenium.execute_script('return catalogue.vm.light_cone.rng_seeds()')
        self.assertEqual(rng_seeds_expected, rng_seeds_actual)


    def test_sed_params(self):
        self.upload_params_file()

        self.click('tao-tabs-sed')

        sed_pop = self.get_selected_option_text(self.sed_id('single_stellar_population_model'))
        self.assertEqual('stellar_label_001', sed_pop)

        self.assert_multi_selected_text_equals(self.sed_id('band_pass_filters-right'), ['Band pass filter 000 (Apparent)','Band pass filter 002 (Apparent)'])

    def test_mock_image_params(self):
        self.upload_params_file()

        self.click('tao-tabs-mock_image')
        self.assertEqual([u'ALL', 0, 1, 2], self.get_ko_array('catalogue.vm.mock_image.sub_cone_options()', 'value'))
        self.assertEqual([u'1_apparent', u'3_apparent'],
            self.get_ko_array('catalogue.modules.mock_image.vm.image_settings()[0].mag_field_options()', 'pk'))
        self.assertEqual([u'FITS'], self.get_ko_array('catalogue.vm.mock_image.format_options', 'value'))

        self.assertEqual(1, self.get_image_setting_ko_field(0,'sub_cone'))
        self.assertEqual('3_apparent', self.get_image_setting_ko_field(0, 'mag_field', field='pk'))

        self.assertEqual('7', self.get_image_setting_ko_value(0, 'min_mag'))
        self.assertEqual('12', self.get_image_setting_ko_value(0, 'max_mag'))
        self.assertEqual('3', self.get_image_setting_ko_value(0, 'z_min'))
        self.assertEqual('4', self.get_image_setting_ko_value(0, 'z_max'))
        self.assertEqual('0.5', self.get_image_setting_ko_value(0, 'origin_ra'))
        self.assertEqual('1', self.get_image_setting_ko_value(0, 'origin_dec'))
        self.assertEqual('1', self.get_image_setting_ko_value(0, 'fov_ra'))
        self.assertEqual('2', self.get_image_setting_ko_value(0, 'fov_dec'))
        self.assertEqual('667', self.get_image_setting_ko_value(0, 'width'))
        self.assertEqual('666', self.get_image_setting_ko_value(0, 'height'))

        self.assertEqual(2, self.get_image_setting_ko_field(1,'sub_cone'))
        self.assertEqual('3_apparent', self.get_image_setting_ko_field(1, 'mag_field', field='pk'))

        self.assertEqual('', self.get_image_setting_ko_value(1, 'min_mag'))
        self.assertEqual('11', self.get_image_setting_ko_value(1, 'max_mag'))
        self.assertEqual('3', self.get_image_setting_ko_value(1, 'z_min'))
        self.assertEqual('4', self.get_image_setting_ko_value(1, 'z_max'))
        self.assertEqual('0.5', self.get_image_setting_ko_value(1, 'origin_ra'))
        self.assertEqual('1', self.get_image_setting_ko_value(1, 'origin_dec'))
        self.assertEqual('1', self.get_image_setting_ko_value(1, 'fov_ra'))
        self.assertEqual('2', self.get_image_setting_ko_value(1, 'fov_dec'))
        self.assertEqual('778', self.get_image_setting_ko_value(1, 'width'))
        self.assertEqual('777', self.get_image_setting_ko_value(1, 'height'))



    def test_rf_params(self):
        self.upload_params_file()

        self.click('tao-tabs-record_filter')
        rf_filter = self.get_selected_option_text(self.rf_id('filter'))
        self.assertEqual('parameter_005 label', rf_filter)
        rf_expected = {
            self.rf_id('min'): '',
            self.rf_id('max'): '12'
        }
        

    def test_output_params(self):
        self.upload_params_file()
        self.click('tao-tabs-output_format')
        out_format = self.get_selected_option_text('#id_output_format-supported_formats')
        self.assertEqual('FITS', out_format)
        

    def test_summary_params(self):
        self.upload_params_file()

        self.click('tao-tabs-summary_submit')
        self.assert_summary_field_correctly_shown('Light-Cone', 'light_cone', 'geometry_type')
        self.assert_summary_field_correctly_shown('simulation_001', 'light_cone', 'simulation')
        self.assert_summary_field_correctly_shown('galaxy_model_006', 'light_cone', 'galaxy_model')
        self.assert_summary_field_correctly_shown('1 properties selected', 'light_cone', 'output_properties')

        self.assert_summary_field_correctly_shown('stellar_label_001', 'sed', 'single_stellar_population_model')
        self.assert_summary_field_correctly_shown('2 properties selected', 'sed', 'band_pass_filters')
        self.assert_summary_field_correctly_shown('Not selected', 'sed', 'apply_dust')
        self.assert_summary_field_correctly_shown('2 images', 'mock_image', 'select_mock_image')

        self.assert_summary_field_correctly_shown(u'parameter_005 label \u2264 12.0', 'record_filter', 'record_filter')

        self.assert_summary_field_correctly_shown('FITS', 'output', 'output_format')


    def test_load_preset(self):
        self.click('presets_button')
        self.click('load_survey_preset_button')
        self.assert_page_has_content("Survey Preset 'Preset 0' loaded successfully.")
    
    def test_handles_malformed_xml(self):
        from selenium.webdriver.support.wait import WebDriverWait
        timeout = 2
        json_path = os.path.join(PROJECT_DIR, 'test_data', 'test_data.json')
        self.selenium.find_element_by_id('id_job_type-params_file').send_keys(json_path)
        WebDriverWait(self.selenium, timeout).until(lambda driver: driver.find_element_by_css_selector('.alert-error'))
        self.assert_page_has_content("Failed to process parameter file: 'test_data.json'.")

    def get_ko_array(self, vm_ko_array, field):
        js = 'return $.map(' + vm_ko_array + ', function(v, i) { return v.' + field + '; });'
        return self.selenium.execute_script(js)

    def get_image_setting_ko_field(self, index, setting, field='value'):
        js = 'return catalogue.modules.mock_image.vm.image_settings()[%d].%s().%s' % (index, setting, field)
        return self.selenium.execute_script(js)

    def get_image_setting_ko_value(self, index, setting):
        js = 'return catalogue.modules.mock_image.vm.image_settings()[%d].%s()' % (index, setting)
        return self.selenium.execute_script(js)

    def upload_params_file(self):
        self.selenium.find_element_by_id('id_job_type-params_file').send_keys(self.params_path)
