from django.conf import settings
from tao.models import Snapshot
from tao.settings import MODULE_INDICES
from tao.tests.integration_tests.helper import LiveServerMGFTest
from tao.tests.support.factories import UserFactory, SimulationFactory, GalaxyModelFactory, DataSetFactory, DataSetPropertyFactory, JobFactory, StellarModelFactory, SnapshotFactory, BandPassFilterFactory, GlobalParameterFactory, SurveyPresetFactory

from taoui_light_cone.forms import Form as LightConeForm

class SubmitLightConeTests(LiveServerMGFTest):

    def setUp(self):
        super(SubmitLightConeTests, self).setUp()

        GlobalParameterFactory.create(parameter_name='maximum-random-light-cones', parameter_value='10')
        GlobalParameterFactory(parameter_name='INITIAL_JOB_STATUS', parameter_value='HELD')
        GlobalParameterFactory(parameter_name='job_too_large_warning', parameter_value='JOB_WARNING')
        simulation = SimulationFactory.create(box_size=500)
        galaxy_model = GalaxyModelFactory.create()
        dataset = DataSetFactory.create(simulation=simulation, galaxy_model=galaxy_model, max_job_box_count=15)

        self.redshifts = ['1.23456789', '2.987654321', '3.69154927', '4.567890123']
        for redshift in self.redshifts:
            SnapshotFactory.create(dataset=dataset, redshift=redshift)

        DataSetPropertyFactory.create(dataset=dataset)
        StellarModelFactory.create()
        BandPassFilterFactory.create()
        self.survey_preset = SurveyPresetFactory.create(name='Preset 1', parameters='<xml></xml>')

        self.username = "user"
        password = "password"
        self.user = UserFactory.create(username=self.username, password=password)

        
        self.parameters = """<lightcone>
                        <database_type>sqlite</database_type>
                        <database_name>random.db</database_name>
                        <catalogue_geometry>cone</catalogue_geometry>
                        </lightcone>
                    """
        
        self.login(self.username, password)
        self.visit('mock_galaxy_factory')
        self.click('tao-tabs-' + 'light_cone')

    def tearDown(self):
        super(SubmitLightConeTests, self).tearDown()

    def test_display_job_estimate_on_cone_only(self):
        self.assert_not_displayed('#max_job_size') # box is selected on initial load

        self.select(self.lc_id('catalogue_geometry'), 'Light-Cone')
        self.assert_is_displayed('#max_job_size')

    def test_job_estimate_displayed_correctly(self):
        self.select(self.lc_id('catalogue_geometry'), 'Light-Cone')
        # the box count calculated from these parameters is 15, within the max_job_box_count set for this dataset, 15
        self.fill_in_fields({
            'ra_opening_angle': '1\n',
            'dec_opening_angle': '2\n',
            'redshift_min': '3\n',
            'redshift_max': '4\n',
        }, id_wrap=self.lc_id)
        self.assert_page_has_content('Estimated job size: 3%')
        self.assert_page_does_not_contain("job tool argue earning")

    def test_job_estimated_too_large(self):
        self.select(self.lc_id('catalogue_geometry'), 'Light-Cone')
        # the box count calculated from these parameters is 16, exceeding the max_job_box_count set for this dataset, 15
        self.fill_in_fields({
            'ra_opening_angle': '1\n',
            'dec_opening_angle': '2\n',
            'redshift_min': '3\n',
            'redshift_max': '5\n',
        }, id_wrap=self.lc_id)
        self.assert_page_has_content("JOB_WARNING")

    def test_job_estimate_with_invalid_parameters(self):
        self.select(self.lc_id('catalogue_geometry'), 'Light-Cone')
        self.fill_in_fields({
            'ra_opening_angle': 'zero\n',
            'dec_opening_angle': '0\n',
            'redshift_min': '0\n',
            'redshift_max': '5\n',
        }, id_wrap=self.lc_id)
        self.assert_page_has_content("waiting for valid cone parameters")

    def test_submit_invalid_output_properties(self):
        ## fill in form (correctly)
        self.select(self.lc_id('catalogue_geometry'), 'Light-Cone')
        self.fill_in_fields({
            'ra_opening_angle': '2',
            'dec_opening_angle': '2',
            'redshift_min': '1',
            'redshift_max': '2',
            }, id_wrap=self.lc_id)
        self.assert_required_on_field(True, self.lc_id('output_properties'))
        #self.submit_mgf_form()
        #self.assert_required_on_field(True, self.lc_id('output_properties'))

    def test_submit_valid_unique_cone_job(self):
        ## fill in form (correctly)
        self.select(self.lc_id('catalogue_geometry'), 'Light-Cone')
        self.fill_in_fields({
            'ra_opening_angle': '2',
            'dec_opening_angle': '2',
            'redshift_min': '1',
            'redshift_max': '2',
        }, id_wrap=self.lc_id)
        self.click(self.lc_2select('op_add_all'))
        self.click('tao-tabs-record_filter')
        self.fill_in_fields({
            'min': '1\n',
            'max': '10\n',
        }, id_wrap=self.rf_id)
        self.submit_mgf_form()
        self.assert_on_page('job_index')

    def test_submit_valid_random_cone_job(self):
        self.select(self.lc_id('catalogue_geometry'), 'Light-Cone')
        self.click_by_css(self.lc_id('light_cone_type_1')) # select "random"
        self.fill_in_fields({
            'ra_opening_angle': '2',
            'dec_opening_angle': '2',
            'redshift_min': '1',
            'redshift_max': '2',
        }, id_wrap=self.lc_id)
        self.click(self.lc_2select('op_add_all'))
        self.clear(self.lc_id('number_of_light_cones'))
        self.fill_in_fields({
            'number_of_light_cones': '10', # this is greater than the maximum for "unique" for the parameters above
        }, id_wrap=self.lc_id)
        self.click('tao-tabs-record_filter')
        self.fill_in_fields({
            'min': '1\n',
            'max': '10\n',
        }, id_wrap=self.rf_id)
        self.submit_mgf_form()
        self.assert_on_page('job_index')

    def _test_submit_invalid_random_cone_job(self):
        self.wait(1)
        self.select(self.lc_id('catalogue_geometry'), 'Light-Cone')
        self.click_by_css(self.lc_id('light_cone_type_1')) # select "random"
        self.fill_in_fields({
            'ra_opening_angle': '2',
            'dec_opening_angle': '2',
            'redshift_min': '1',
            'redshift_max': '2',
        }, id_wrap=self.lc_id)
        self.click(self.lc_2select('op_add_all'))
        self.wait(1)
        self.clear(self.lc_id('number_of_light_cones'))
        self.fill_in_fields({
            'number_of_light_cones': '11', # this exceeds the maximum in db, 10
        }, id_wrap=self.lc_id)
        self.click(self.lc_2select('op_add_all')) # click somewhere else to shift focus out of the number of cones field (this shouldn't affect the current selection, as they are already all selected)
        self.assertEqual('10', self.get_selector_value(self.lc_id('number_of_light_cones'))) # resets to the maximum valid value
        self.submit_mgf_form()

        self.assert_on_page('job_index') # used to return to the mock_galaxy_factory page, as previously used to keep the invalid input and fail validation

    def test_submit_valid_box_job(self):
        from tao import models
        ## fill in form (correctly)
        self.select(self.lc_id('catalogue_geometry'), 'Box')
        self.clear(self.lc_id('box_size'))
        self.fill_in_fields({
            'box_size': '9',
            'snapshot': "%.5g" % float(self.redshifts[0]),
        }, id_wrap=self.lc_id)
        self.click(self.lc_2select('op_add_all'))
        self.click('tao-tabs-record_filter')
        self.fill_in_fields({
            'min': '1\n',
            'max': '10\n',
        }, id_wrap=self.rf_id)
        self.submit_mgf_form()
        self.assert_on_page('job_index')
        self.assert_page_has_content(settings.INITIAL_JOB_MESSAGE % models.initial_job_status().lower())

    def test_invalid_box_options_allow_light_cone_submit(self):
        ## fill in box fields (incorrectly)
        self.select(self.lc_id('catalogue_geometry'), 'Box')
        self.fill_in_fields({
            'box_size': 'bad_input',
        }, id_wrap=self.lc_id)

        ## fill in light-cone fields (correctly)
        self.select(self.lc_id('catalogue_geometry'), 'Light-Cone')
        self.fill_in_fields({
            'ra_opening_angle': '2',
            'dec_opening_angle': '2',
            'redshift_min': '1',
            'redshift_max': '2',
        }, id_wrap=self.lc_id)
        self.click(self.lc_2select('op_add_all'))
        self.click('tao-tabs-record_filter')
        self.fill_in_fields({
            'min': '1\n',
            'max': '10\n',
        }, id_wrap=self.rf_id)
        self.submit_mgf_form()
        self.assert_on_page('job_index') # The form is valid because the invalid box size field is hidden

    def test_invalid_cone_options_allow_box_submit(self):
        ## fill in light-cone fields (incorrectly)
        self.select(self.lc_id('catalogue_geometry'), 'Light-Cone')
        self.fill_in_fields({
            'ra_opening_angle': 'not_valid',
            'dec_opening_angle': 'not_valid',
            'redshift_min': 'not_valid',
            'redshift_max': 'not_valid',
        }, id_wrap=self.lc_id)

        ## fill in box fields (correctly)
        self.select(self.lc_id('catalogue_geometry'), 'Box')
        self.clear(self.lc_id('box_size'))
        self.fill_in_fields({
            'box_size': '1',
            'snapshot': "%.5g" % float(self.redshifts[0]),
        }, id_wrap=self.lc_id)
        self.click(self.lc_2select('op_add_all'))
        self.click('tao-tabs-record_filter')
        self.fill_in_fields({
            'min': '1\n',
            'max': '10\n',
        }, id_wrap=self.rf_id)
        self.submit_mgf_form()
        self.assert_on_page('job_index') # The form is valid because the invalid light cone fields hidden

    def _test_redshift_stays_selected_after_failed_submit(self):
        self.select(self.lc_id('catalogue_geometry'), 'Box')
        self.fill_in_fields({
            'box_size': 'bad_number',
        }, id_wrap=self.lc_id)
        third_snapshot_text = "%.5g" % float(Snapshot.objects.all()[2].redshift)
        self.select(self.lc_id('snapshot'), third_snapshot_text)

        self.submit_mgf_form()
        self.assert_on_page('mock_galaxy_factory')
        self.assertEqual(third_snapshot_text, self.get_selected_option_text(self.lc_id('snapshot')))

    def _test_number_of_cones_stays_the_same_after_failed_submit(self):
        number_of_light_cones = '10'
        self.select(self.lc_id('catalogue_geometry'), 'Light-Cone')
        self.fill_in_fields({
            'ra_opening_angle': '2',
            'dec_opening_angle': '2',
            'redshift_min': '1',
            'redshift_max': '2',
        }, id_wrap=self.lc_id)
        self.click_by_css(self.lc_id('light_cone_type_1'))
        self.clear(self.lc_id('number_of_light_cones'))
        self.fill_in_fields({
            'number_of_light_cones': number_of_light_cones, # this is the maximum stored for random light-cones in db
        }, id_wrap=self.lc_id)

        self.submit_mgf_form()
        self.assert_on_page('mock_galaxy_factory')
        self.assertEqual(number_of_light_cones, self.selenium.find_element_by_css_selector(self.lc_id('number_of_light_cones')).get_attribute('value'))
