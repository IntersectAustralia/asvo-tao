from tao.models import Job
from tao.tests.integration_tests.helper import LiveServerMGFTest, wait, interact
from tao.tests.support.factories import UserFactory, SimulationFactory, GalaxyModelFactory, DataSetFactory, DataSetPropertyFactory, JobFactory, StellarModelFactory, SnapshotFactory, BandPassFilterFactory

from taoui_light_cone.forms import Form as LightConeForm

class SubmitLightConeTests(LiveServerMGFTest):

    def setUp(self):
        super(SubmitLightConeTests, self).setUp()
        
        simulation = SimulationFactory.create()
        galaxy_model = GalaxyModelFactory.create()
        dataset = DataSetFactory.create(simulation=simulation, galaxy_model=galaxy_model)

        self.redshifts = [1, 2, 3]
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

    def test_submit_invalid_output_properties(self):
        self.visit('mock_galaxy_factory')

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

    def test_submit_valid_cone_job(self):
        self.visit('mock_galaxy_factory')
        
        ## fill in form (correctly)
        self.select(self.lc_id('catalogue_geometry'), 'Light-Cone')
        self.fill_in_fields({
            'ra_opening_angle': '2',
            'dec_opening_angle': '2',
            'redshift_min': '1',
            'redshift_max': '2',
        }, id_wrap=self.lc_id)
        self.click(self.lc_2select('op_add_all'))

        self.click('tao-tabs-2')
        self.click(self.sed_2select('op_add_all'))

        self.submit_mgf_form()
        self.assert_on_page('held_jobs')

    def test_submit_valid_box_job(self):
        self.visit('mock_galaxy_factory')
        
        ## fill in form (correctly)
        self.select(self.lc_id('catalogue_geometry'), 'Box')
        self.fill_in_fields({
            'box_size': '9',
            'snapshot': self.redshifts[0],
        }, id_wrap=self.lc_id)
        self.click(self.lc_2select('op_add_all'))

        self.click('tao-tabs-2')
        self.click(self.sed_2select('op_add_all'))

        self.submit_mgf_form()
        self.assert_on_page('held_jobs')
        

    def test_invalid_box_options_allow_light_cone_submit(self):
        self.visit('mock_galaxy_factory')

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

        ## fill in SED form correctly
        self.click('tao-tabs-2')
        self.click(self.sed_2select('op_add_all'))

        self.submit_mgf_form()
        self.assert_on_page('held_jobs')  # The form is valid because the invalid box size field is hidden

    def test_invalid_cone_options_allow_box_submit(self):
        self.visit('mock_galaxy_factory')

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
            'snapshot': self.redshifts[0],
        }, id_wrap=self.lc_id)
        self.click(self.lc_2select('op_add_all'))

        self.click('tao-tabs-2')
        self.click(self.sed_2select('op_add_all'))

        self.submit_mgf_form()
        self.assert_on_page('held_jobs')  # The form is valid because the invalid light cone fields hidden
