from tao.models import Job
from tao.tests.integration_tests.helper import LiveServerMGFTest
from tao.tests.support.factories import UserFactory, SimulationFactory, GalaxyModelFactory, DataSetFactory, DataSetParameterFactory, JobFactory, StellarModelFactory, SnapshotFactory

from tao.forms import LightConeForm

class SubmitLightConeTests(LiveServerMGFTest):
    def setUp(self):
        super(SubmitLightConeTests, self).setUp()
        
        simulation = SimulationFactory.create()
        galaxy_model = GalaxyModelFactory.create()
        dataset = DataSetFactory.create(simulation=simulation, galaxy_model=galaxy_model)

        self.redshifts = [1, 2, 3]
        for redshift in self.redshifts:
            SnapshotFactory.create(dataset=dataset, redshift=redshift)

        DataSetParameterFactory.create(dataset=dataset)
        StellarModelFactory.create()
        
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
        
    def test_submit_valid_cone_job(self):
        self.visit('mock_galaxy_factory')
        
        ## fill in form (correctly)
        self.select('#id_catalogue_geometry', 'Light-Cone')
        self.fill_in_fields({
            'id_ra_opening_angle': '2',
            'id_dec_opening_angle': '2',
            'id_redshift_min': '1',
            'id_redshift_max': '2',
        })
        self.submit_mgf_form()

        self.assert_on_page('submitted_jobs')

    def test_submit_valid_box_job(self):
        self.visit('mock_galaxy_factory')
        
        ## fill in form (correctly)
        self.select('#id_catalogue_geometry', 'Box')
        self.fill_in_fields({
            'id_box_size': '234',
            'id_snapshot': self.redshifts[0],
        })
        self.submit_mgf_form()

        self.assert_on_page('submitted_jobs')
        

    def test_invalid_box_options_allow_light_cone_submit(self):
        self.visit('mock_galaxy_factory')

        ## fill in box fields (incorrectly)
        self.select('#id_catalogue_geometry', 'Box')
        self.fill_in_fields({
            'id_box_size': 'bad_input',
        })

        ## fill in light-cone fields (correctly)
        self.select('#id_catalogue_geometry', 'Light-Cone')
        self.fill_in_fields({
            'id_ra_opening_angle': '2',
            'id_dec_opening_angle': '2',
            'id_redshift_min': '1',
            'id_redshift_max': '2',
        })

        self.submit_mgf_form()

        self.assert_on_page('submitted_jobs')  # The form is valid because the invalid box size field is hidden

    def test_invalid_cone_options_allow_box_submit(self):
        self.visit('mock_galaxy_factory')

        ## fill in light-cone fields (incorrectly)
        self.select('#id_catalogue_geometry', 'Light-Cone')
        self.fill_in_fields({
            'id_ra_opening_angle': 'not_valid',
            'id_dec_opening_angle': 'not_valid',
            'id_redshift_min': 'not_valid',
            'id_redshift_max': 'not_valid',
        })

        ## fill in box fields (correctly)
        self.select('#id_catalogue_geometry', 'Box')
        self.fill_in_fields({
            'id_box_size': '1',
            'id_snapshot': self.redshifts[0],
        })


        self.submit_mgf_form()

        self.assert_on_page('submitted_jobs')  # The form is valid because the invalid light cone fields hidden
