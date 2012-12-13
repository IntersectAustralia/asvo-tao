from tao.tests.integration_tests.helper import LiveServerTest
from tao.tests.support.factories import UserFactory, SimulationFactory, GalaxyModelFactory
from tao.models import Simulation

class MockGalaxyFactoryTest(LiveServerTest):

    def setUp(self):
        super(MockGalaxyFactoryTest, self).setUp()
        
        simulation = SimulationFactory.create()
        simulation2 = SimulationFactory.create()

        for unused in range(3):
            GalaxyModelFactory.create(simulation=simulation)
            
        for unused in range(4):
            GalaxyModelFactory.create(simulation=simulation2)
        
        username = "person"
        password = "funnyfish"
        UserFactory.create(username=username, password=password)
        self.login(username, password)
        
        self.visit('mock_galaxy_factory')
        
    def test_box_size_field_on_initial_load(self):
        initial_selection = self.get_selected_option_text('#id_catalogue_geometry')
        self.assertEqual('Light-Cone', initial_selection)
        self.assert_not_displayed('#id_box_size')
    
    def test_box_size_field_on_catalogue_geometry_change(self):
        self.select('#id_catalogue_geometry', 'Box')
        self.assert_is_displayed('#id_box_size')
        
        self.select('#id_catalogue_geometry', 'Light-Cone')
        self.assert_not_displayed('#id_box_size')
        
    def test_sidebar_text_on_initial_load(self):    
        first_simulation = Simulation.objects.all()[0]
        first_galaxy_model = first_simulation.galaxymodel_set.all()[0]
        
        self.assert_galaxy_model_info_shown(first_galaxy_model)
        self.assert_galaxy_model_options_correct_for_a_simulation(first_simulation)
        self.assert_simulation_info_shown(first_simulation)
    
    def test_sidebar_text_on_simulation_change(self):      
        second_simulation = Simulation.objects.all()[1]
        
        self.select_dark_matter_simulation(second_simulation)
        
        self.assert_galaxy_model_info_shown(second_simulation.galaxymodel_set.all()[0])
        self.assert_galaxy_model_options_correct_for_a_simulation(second_simulation)
        self.assert_simulation_info_shown(second_simulation)
        
    def test_sidebar_text_on_galaxy_model_change(self):
        first_simulation = Simulation.objects.all()[0]
        second_galaxy_model = first_simulation.galaxymodel_set.all()[1]
        
        self.select_galaxy_model(second_galaxy_model)
        
        self.assert_galaxy_model_info_shown(second_galaxy_model)
            
    def assert_simulation_info_shown(self, simulation):
        """  check the name of the simulation in the sidebar is the same as simulation_name
             check the values in the side bar correspond to that simulation
        """
        self.assert_selector_texts_equals_expected_values({
                                                           '.simulation-info .simulation-name': simulation.name,
                                                           '.simulation-info .simulation-paper': simulation.paper_title,
                                                           '.simulation-info .simulation-cosmology': simulation.cosmology,
                                                           '.simulation-info .simulation-cosmological-parameters': simulation.cosmological_parameters,
                                                           '.simulation-info .simulation-box-size': simulation.box_size,
                                                           })
        self.assert_attribute_equals('href', {
                                              '.simulation-info .simulation-paper': simulation.paper_url,
                                              '.simulation-info .simulation-link': simulation.external_link_url,
                                              '.simulation-info .simulation-web-site': simulation.web_site,
                                              })
        
    def assert_galaxy_model_info_shown(self, galaxy_model):
        galaxy_model_selector_value = {
                             '.galaxy-model-info .galaxy-model-name': galaxy_model.name,
                             '.galaxy-model-info .galaxy-model-kind': galaxy_model.kind,
                             '.galaxy-model-info .galaxy-model-paper': galaxy_model.paper_title
                             }
        self.assert_selector_texts_equals_expected_values(galaxy_model_selector_value)
        
        galaxy_model_paper_url = self.find_visible_element('.galaxy-model-info .galaxy-model-paper').get_attribute('href')
        
        self.assertEqual(galaxy_model.paper_url, galaxy_model_paper_url)
        
    def assert_galaxy_model_options_correct_for_a_simulation(self, simulation):
        expected_galaxy_model_names = [x[0] for x in simulation.galaxymodel_set.values_list('name')]
        actual_galaxy_model_names = [x.text for x in self.selenium.find_elements_by_css_selector('#id_galaxy_model option')]
        
        self.assertEqual(expected_galaxy_model_names, actual_galaxy_model_names)
