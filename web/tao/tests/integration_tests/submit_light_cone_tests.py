from tao.models import Snapshot
from tao.settings import MODULE_INDICES
from tao.tests.integration_tests.helper import LiveServerMGFTest, wait, interact
from tao.tests.support.factories import UserFactory, SimulationFactory, GalaxyModelFactory, DataSetFactory, DataSetPropertyFactory, JobFactory, StellarModelFactory, SnapshotFactory, BandPassFilterFactory

from taoui_light_cone.forms import Form as LightConeForm

class SubmitLightConeTests(LiveServerMGFTest):

    def setUp(self):
        super(SubmitLightConeTests, self).setUp()
        
        simulation = SimulationFactory.create()
        galaxy_model = GalaxyModelFactory.create()
        dataset = DataSetFactory.create(simulation=simulation, galaxy_model=galaxy_model)

        self.redshifts = ['1.23456789', '2.987654321', '3.69154927', '4.567890123']
        for redshift in self.redshifts:
            SnapshotFactory.create(dataset=dataset, redshift=redshift)

        DataSetPropertyFactory.create(dataset=dataset)
        StellarModelFactory.create()
        BandPassFilterFactory.create()

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

    def test_submit_invalid_output_properties(self):
        ## fill in form (correctly)
        self.select(self.lc_id('catalogue_geometry'), 'Light-Cone')
        self.fill_in_fields({
            'ra_opening_angle': '2',
            'dec_opening_angle': '2',
            'redshift_min': '1',
            'redshift_max': '2',
            }, id_wrap=self.lc_id)
        self.submit_mgf_form()

        self.assert_on_page('mock_galaxy_factory')

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
        self.clear(self.lc_id('number_of_light_cones'))
        self.fill_in_fields({
            'number_of_light_cones': '3', # this is actually the calculated maximum for parameters above
        }, id_wrap=self.lc_id)
        self.submit_mgf_form()

        self.assert_on_page('job_index')

    def test_submit_valid_random_cone_job(self):
        self.select(self.lc_id('catalogue_geometry'), 'Light-Cone')
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
        self.click_by_css(self.lc_id('light_cone_type_1')) # select "random"
        self.submit_mgf_form()

        self.assert_on_page('job_index')

    def test_submit_invalid_unique_cone_job(self):
        self.select(self.lc_id('catalogue_geometry'), 'Light-Cone')
        self.fill_in_fields({
            'ra_opening_angle': '2',
            'dec_opening_angle': '2',
            'redshift_min': '1',
            'redshift_max': '2',
        }, id_wrap=self.lc_id)
        self.click(self.lc_2select('op_add_all'))
        self.clear(self.lc_id('number_of_light_cones'))
        self.fill_in_fields({
            'number_of_light_cones': '4', # this exceeds the calculated maximum for parameters above
        }, id_wrap=self.lc_id)
        wait(1);
        self.submit_mgf_form()

        self.assert_on_page('mock_galaxy_factory')

    def test_submit_valid_box_job(self):
        ## fill in form (correctly)
        self.select(self.lc_id('catalogue_geometry'), 'Box')
        self.fill_in_fields({
            'box_size': '9',
            'snapshot': "%.5g" % float(self.redshifts[0]),
        }, id_wrap=self.lc_id)
        self.click(self.lc_2select('op_add_all'))
        self.submit_mgf_form()

        self.assert_on_page('job_index')
        

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
        self.fill_in_fields({
            'box_size': '1',
            'snapshot': "%.5g" % float(self.redshifts[0]),
        }, id_wrap=self.lc_id)
        self.click(self.lc_2select('op_add_all'))

        self.submit_mgf_form()
        self.assert_on_page('job_index') # The form is valid because the invalid light cone fields hidden

    def test_redshift_stays_selected_after_failed_submit(self):
        self.select(self.lc_id('catalogue_geometry'), 'Box')
        self.fill_in_fields({
            'box_size': 'bad_number',
        }, id_wrap=self.lc_id)
        third_snapshot_text = "%.5g" % float(Snapshot.objects.all()[2].redshift)
        self.select(self.lc_id('snapshot'), third_snapshot_text)

        self.submit_mgf_form()
        self.assert_on_page('mock_galaxy_factory')
        self.assertEqual(third_snapshot_text, self.get_selected_option_text(self.lc_id('snapshot')))

    def test_number_of_cones_stays_the_same_after_failed_submit(self):
        number_of_light_cones = '3'
        self.select(self.lc_id('catalogue_geometry'), 'Light-Cone')
        self.fill_in_fields({
            'ra_opening_angle': '2',
            'dec_opening_angle': '2',
            'redshift_min': '1',
            'redshift_max': '2',
        }, id_wrap=self.lc_id)
        self.click_by_css(self.lc_id('light_cone_type_0'))
        self.clear(self.lc_id('number_of_light_cones'))
        self.fill_in_fields({
            'number_of_light_cones': number_of_light_cones, # this is actually the calculated maximum for parameters above
        }, id_wrap=self.lc_id)

        self.submit_mgf_form()
        self.assert_on_page('mock_galaxy_factory')
        self.assertEqual(number_of_light_cones, self.selenium.find_element_by_css_selector(self.lc_id('number_of_light_cones')).get_attribute('value'))