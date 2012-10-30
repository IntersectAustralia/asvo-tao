from tao.tests.integration_tests.helper import LiveServerTest
from tao.tests.support.factories import SimulationFactory, GalaxyModelFactory, UserFactory, DataSetFactory, DataSetParameterFactory
from tao.models import Simulation, DataSet, DataSetParameter

class FilterTests(LiveServerTest):
    
    def setUp(self):
        super(FilterTests, self).setUp()
        
        simulation1 = SimulationFactory.create()
        simulation2 = SimulationFactory.create()
        
        for unused in range(4):
            galaxy_model = GalaxyModelFactory.create(simulation=simulation1)
            dataset = DataSetFactory.create(simulation=simulation1, galaxy_model=galaxy_model)
            DataSetParameterFactory.create(dataset=dataset)
            
        for unused in range(5):
            galaxy_model = GalaxyModelFactory.create(simulation=simulation2)
            dataset = DataSetFactory.create(simulation=simulation2, galaxy_model=galaxy_model)
            DataSetParameterFactory.create(dataset=dataset)
            
        username = "user"
        password = "password"
        UserFactory.create(username=username, password=password)
        self.login(username, password)
        
        self.visit('mock_galaxy_factory')
        
    def test_filter_options(self):
        # check drop-down list correspond to properties of the currently selected simulation and galaxy model
        initial_simulation = Simulation.objects.all()[0]
        initial_galaxy_model = initial_simulation.galaxymodel_set.all()[0]
        dataset = DataSet.objects.get(simulation=initial_simulation, galaxy_model=initial_galaxy_model)
        dataset_parameters = dataset.datasetparameter_set.all()
        
        expected_filter_options = self.get_expected_filter_options(dataset_parameters)
        actual_filter_options = self.get_actual_filter_options()
        
        self.assertEqual(expected_filter_options, actual_filter_options)
        
    def test_filter_updates(self):
        # check drop-down list updates when simulation or galaxy model is changed
        simulation = Simulation.objects.all()[1]
        galaxy_model = simulation.galaxymodel_set.all()[4]
        dataset = DataSet.objects.get(simulation=simulation, galaxy_model=galaxy_model)
        dataset_parameters = dataset.datasetparameter_set.all()
        expected_filter_options = self.get_expected_filter_options(dataset_parameters)
        
        self.select_dark_matter_simulation(simulation)
        self.select_galaxy_model(galaxy_model)
        
        actual_filter_options = self.get_actual_filter_options()
        self.assertEqual(expected_filter_options, actual_filter_options)

    def test_max_min_fields(self):
        self.assert_is_disabled('#id_max') 
        self.assert_is_disabled('#id_min')
        
        simulation = Simulation.objects.all()[1]
        galaxy_model = simulation.galaxymodel_set.all()[4]
        dataset = DataSet.objects.get(simulation=simulation, galaxy_model=galaxy_model)
        dataset_parameter = dataset.datasetparameter_set.all()[0]
        
        self.select_dark_matter_simulation(simulation)
        self.select_galaxy_model(galaxy_model)
        self.select('#id_filter', dataset_parameter.name)

        self.assert_is_enabled('#id_max')
        self.assert_is_enabled('#id_min')
        
    def test_max_min_fields_after_failed_submit(self):
        simulation = Simulation.objects.all()[1]
        self.select_dark_matter_simulation(simulation)
        galaxy_model = simulation.galaxymodel_set.all()[4]
        self.select_galaxy_model(galaxy_model)
        dataset = DataSet.objects.get(simulation=simulation, galaxy_model=galaxy_model)
        dataset_parameter = dataset.datasetparameter_set.all()[0]
        self.select('#id_filter', dataset_parameter.name)
        
        max_input = "bad number"
        min_input = "73"
        self.fill_in_fields({'id_max': max_input, 'id_min': min_input})
        
        self.submit_form()
        
        # check after failed submit, max/min fields are both still enabled
        self.assert_is_enabled('#id_max')
        self.assert_is_enabled('#id_min')

        # check values are the same in the form as user previously selected      
        self.assertEqual(simulation.name, self.get_selected_option_text('#id_dark_matter_simulation'))
        self.assertEqual(galaxy_model.name, self.get_selected_option_text('#id_galaxy_model'))
        self.assertEqual(dataset_parameter.name, self.get_selected_option_text('#id_filter'))
        self.assertEqual(max_input, self.get_selector_value('#id_max'))
        self.assertEqual(min_input, self.get_selector_value('#id_min'))
        
    def submit_form(self):
        submit_button = self.selenium.find_element_by_css_selector('#mgf-form input[type="submit"]')
        submit_button.submit()