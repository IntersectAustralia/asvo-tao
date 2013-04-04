from django.utils.html import strip_tags

from tao.tests.integration_tests.helper import LiveServerTest, wait

from tao.tests.support.factories import UserFactory, SimulationFactory, GalaxyModelFactory, DataSetFactory, JobFactory, DataSetPropertyFactory, DustModelFactory, StellarModelFactory, BandPassFilterFactory
from tao.models import Simulation, StellarModel, DustModel, BandPassFilter
from tao.settings import MODULE_INDICES

class MockGalaxyFactoryTest(LiveServerTest):

    def setUp(self):
        super(MockGalaxyFactoryTest, self).setUp()

        simulation = SimulationFactory.create()
        simulation2 = SimulationFactory.create()

        for unused in range(3):
            g = GalaxyModelFactory.create()
            ds = DataSetFactory.create(simulation=simulation, galaxy_model=g)
            DataSetPropertyFactory.create(dataset=ds)
            DataSetPropertyFactory.create(dataset=ds)

        for unused in range(4):
            g = GalaxyModelFactory.create()
            ds = DataSetFactory.create(simulation=simulation2, galaxy_model=g)
            dsp = DataSetPropertyFactory.create(dataset=ds)
            ds.default_filter_field = dsp
            ds.save()

        for unused in range(3):
            StellarModelFactory.create()
            BandPassFilterFactory.create()
            DustModelFactory.create()

        username = "person"
        password = "funnyfish"
        self.user = UserFactory.create(username=username, password=password)
        self.login(username, password)
        
        self.visit('mock_galaxy_factory')

    def tearDown(self):
        super(MockGalaxyFactoryTest, self).tearDown()

    def test_box_size_field_on_initial_load(self):
        initial_selection = self.get_selected_option_text(self.lc_id('catalogue_geometry'))
        self.assertEqual('Light-Cone', initial_selection)
        self.assert_not_displayed(self.lc_id('box_size'))
    
    def test_box_size_field_on_catalogue_geometry_change(self):
        self.select(self.lc_id('catalogue_geometry'), 'Box')
        self.assert_is_displayed(self.lc_id('box_size'))
        
        self.select(self.lc_id('catalogue_geometry'), 'Light-Cone')
        self.assert_not_displayed(self.lc_id('box_size'))
        
    def test_sidebar_text_on_initial_load(self):    
        first_simulation = Simulation.objects.all()[0]
        first_galaxy_model = first_simulation.galaxymodel_set.all()[0]
        
        self.assert_galaxy_model_info_shown(first_galaxy_model)
        self.assert_galaxy_model_options_correct_for_a_simulation(first_simulation)
        self.assert_simulation_info_shown(first_simulation)

        self.click('tao-tabs-' + MODULE_INDICES['sed'])
        self.assert_sidebar_info_not_shown('stellar-model')
        self.assert_sidebar_info_not_shown('band-pass')
        self.assert_sidebar_info_not_shown('dust-model')
    
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

    def test_sed_sidebar_text_on_apply_sed(self):
        self.click('tao-tabs-' + MODULE_INDICES['sed'])
        self.click(self.sed('apply_sed'))
        initial_stellar_model = StellarModel.objects.all()[0]
        self.assert_stellar_model_info_shown(initial_stellar_model)
        self.assert_sidebar_info_not_shown('dust')

        self.click(self.sed('apply_sed'))
        self.assert_sidebar_info_not_shown('stellar-model')
        self.assert_sidebar_info_not_shown('band-pass')
        self.assert_sidebar_info_not_shown('dust-model')

    def test_sed_sidebar_text_on_apply_dust(self):
        self.click('tao-tabs-' + MODULE_INDICES['sed'])
        self.click(self.sed('apply_sed'))
        self.click(self.sed('apply_dust'))
        initial_dust_model = DustModel.objects.all()[0]
        self.assert_dust_model_info_shown(initial_dust_model)

        self.click(self.sed('apply_dust'))
        self.assert_sidebar_info_not_shown('dust')

    def test_sed_sidebar_text_on_stellar_model_change(self):
        self.click('tao-tabs-' + MODULE_INDICES['sed'])
        self.click(self.sed('apply_sed'))
        third_stellar_model = StellarModel.objects.all()[2]

        self.select_stellar_model(third_stellar_model)
        self.assert_stellar_model_info_shown(third_stellar_model)

    def test_output_property_details(self):
        simulation = Simulation.objects.all()[0]
        self.select_dark_matter_simulation(simulation)
        init_galaxy_model_of_simulation = simulation.galaxymodel_set.all()[0]
        dataset = init_galaxy_model_of_simulation.dataset_set.all()[0]
        for i in [1,0]:
            output_property = dataset.datasetproperty_set.all()[i]
            self.click_by_css(self.lc_id('output_properties_from') + " option[value='"+str(output_property.id)+"']")
            name_displayed = self.get_info_field('output-property', 'name')
            self.assertEquals(output_property.label, name_displayed)
        self.click(self.lc_2select('op_add_all'))
        output_property = dataset.datasetproperty_set.all()[i]
        self.click_by_css(self.lc_id('output_properties') + " option[value='"+str(output_property.id)+"']")
        name_displayed = self.get_info_field('output-property', 'name')
        self.assertEquals(output_property.label, name_displayed)

    def test_bandpass_filter_details(self):
        self.click('tao-tabs-' + MODULE_INDICES['sed'])
        self.click(self.sed('apply_sed'))
        for i in [1,0]:
            bandpass_filter = BandPassFilter.objects.all()[i]
            self.click_by_css(self.sed_id('band_pass_filters_from') + " option[value='"+str(bandpass_filter.id)+"']")
            name_displayed = self.get_info_field('band-pass', 'name')
            self.assertEquals(bandpass_filter.label, name_displayed)
        self.click(self.sed_2select('op_add_all'))
        bandpass_filter = BandPassFilter.objects.all()[i]
        self.click_by_css(self.sed_id('band_pass_filters') + " option[value='"+str(bandpass_filter.id)+"']")
        name_displayed = self.get_info_field('band-pass', 'name')
        self.assertEquals(bandpass_filter.label, name_displayed)

    def test_summary_on_initial_load(self):
        self.click('tao-tabs-' + LiveServerTest.SUMMARY_INDEX)
        geometry_displayed = self.get_summary_field_text('light_cone', 'geometry_type')
        init_simulation = Simulation.objects.all()[0]
        simulation_displayed = self.get_summary_field_text('light_cone', 'simulation')
        init_galaxy_model = init_simulation.galaxymodel_set.all()[0]
        galaxy_model_displayed = self.get_summary_field_text('light_cone', 'galaxy_model')
        output_properties_displayed = self.get_summary_field_text('light_cone', 'output_properties')
        sed_displayed = self.get_summary_field_text('sed', 'select_sed')
        filter_displayed = self.get_summary_field_text('record_filter', 'record_filter')

        self.assertEqual('Light-Cone', geometry_displayed)
        self.assertEqual(init_simulation.name, simulation_displayed)
        self.assertEqual(init_galaxy_model.name, galaxy_model_displayed)
        self.assertEqual('0 properties selected', output_properties_displayed)
        self.assertEqual('Not selected', sed_displayed)
        self.assertEqual('No Filter', filter_displayed)
        self.assert_not_displayed('div.summary_light_cone .box_fields')
        self.assert_not_displayed('div.summary_sed .apply_sed')

    def test_summary_on_geometry_change(self):
        self.select(self.lc_id('catalogue_geometry'), 'Box')
        self.click('tao-tabs-' + LiveServerTest.SUMMARY_INDEX)
        geometry_displayed = self.get_summary_field_text('light_cone', 'geometry_type')

        self.assertEqual('Box', geometry_displayed)
        self.assert_is_displayed('div.summary_light_cone .box_fields')
        self.assert_not_displayed('div.summary_light_cone .light_cone_fields')

    def test_summary_on_simulation_change(self):
        second_simulation = Simulation.objects.all()[1]
        self.select_dark_matter_simulation(second_simulation)
        init_galaxy_model_of_second_simulation = second_simulation.galaxymodel_set.all()[0]
        dataset = init_galaxy_model_of_second_simulation.dataset_set.all()[0]
        filter = dataset.datasetproperty_set.all()[0]
        self.click('tao-tabs-' + MODULE_INDICES['record_filter'])
        self.select_record_filter(filter)
        max_input = "99"
        min_input = "9"
        self.fill_in_fields({'max': max_input, 'min': min_input}, id_wrap=self.rf_id)
        self.click('tao-tabs-' + LiveServerTest.SUMMARY_INDEX)
        wait(1)
        import HTMLParser
        h = HTMLParser.HTMLParser()
        if filter.units != '':
            expected_filter_display = min_input + h.unescape(' &le; ') + filter.label + ' (' + filter.units + ') '+ h.unescape(' &le; ') + max_input
        else:
            expected_filter_display = min_input + h.unescape(' &le; ') + filter.label + h.unescape(' &le; ') + max_input
        simulation_displayed = self.get_summary_field_text('light_cone', 'simulation')
        galaxy_model_displayed = self.get_summary_field_text('light_cone', 'galaxy_model')
        filter_displayed = self.get_summary_field_text('record_filter', 'record_filter')

        self.assertEqual(second_simulation.name, simulation_displayed)
        self.assertEqual(init_galaxy_model_of_second_simulation.name, galaxy_model_displayed)
        self.assertEqual(expected_filter_display, filter_displayed)

    def test_summary_on_dataset_description_expand(self):
        # in dataset, stellar model, and dust model, clicking on ">>" expands to show the description
        # ">>" rotates to show the current state: expanded or not
        init_simulation = Simulation.objects.all()[0];
        init_galaxy_model = init_simulation.galaxymodel_set.all()[0]
        self.click('tao-tabs-' + LiveServerTest.SUMMARY_INDEX)
        self.assertEqual('>>', self.selenium.find_element_by_id('expand_dataset').text)
        self.click('expand_dataset')
        expected_simulation_details = init_simulation.name + ':\n' + strip_tags(init_simulation.details)
        expected_galaxy_model_details = init_galaxy_model.name + ':\n' + strip_tags(init_galaxy_model.details)
        simulation_details_displayed = strip_tags(self.get_summary_field_text('light_cone', 'simulation_description'))
        galaxy_model_details_displayed = strip_tags(self.get_summary_field_text('light_cone', 'galaxy_model_description'))
        self.assertEqual(expected_simulation_details, simulation_details_displayed)
        self.assertEqual(expected_galaxy_model_details, galaxy_model_details_displayed)
        self.assertEqual('<<', self.selenium.find_element_by_id('expand_dataset').text)

    def test_summary_on_light_cone_dimensions_change(self):
        #range displays should be intelligent, i.e. if the min or max is blank, it isn't displayed
        pass

    def test_summary_on_filter_expand(self):
        # Clicking on ">>" in output properties or bandpass filters expands the div and lists the properties in an unordered list
        pass

    def get_field_by_value_in_control_group(self, value, name):
        control_group = self.selenium.find_elements_by_name(name)
        for field in control_group:
            if field.get_attribute('value') == value:
                return field
        raise ValueError(value + 'not in ' + name + '_list')

    def test_unique_light_cone_selected_on_initial_load(self):
        initial_selection = self.get_selected_option_text(self.lc_id('catalogue_geometry'))
        self.assertEqual('Light-Cone', initial_selection)
        self.assert_are_displayed('light_cone-light_cone_type')
        self.assertTrue(self.get_field_by_value_in_control_group('unique', 'light_cone-light_cone_type').is_selected())

    def test_unique_random_display_on_geometry_change(self):
        self.select(self.lc_id('catalogue_geometry'), 'Box')
        self.assert_are_not_displayed('light_cone-light_cone_type')

        self.select(self.lc_id('catalogue_geometry'), 'Light-Cone')
        self.assert_are_displayed('light_cone-light_cone_type')

    def test_description_displayed_in_listing(self):
        job = JobFactory.create(user=self.user)
        wait(1)
        self.visit('job_index')
        self.assert_page_has_content(job.description)

    def test_sed_elements_disabled_on_initial_load(self):
        self.click('tao-tabs-' + MODULE_INDICES['sed'])
        self.assert_is_unchecked(self.sed_id('apply_sed'))
        self.assert_is_disabled(self.sed_id('single_stellar_population_model'))
        self.assert_is_disabled(self.sed_id('band_pass_filters_filter'))
        self.assert_is_disabled(self.sed_id('band_pass_filters_from'))
        self.assert_is_disabled(self.sed_id('band_pass_filters'))

    def test_sed_module_enabled_on_check_apply(self):
        self.click('tao-tabs-' + MODULE_INDICES['sed'])
        self.click(self.sed('apply_sed'))
        self.assert_is_checked(self.sed_id('apply_sed'))
        self.assert_is_enabled(self.sed_id('single_stellar_population_model'))
        self.assert_is_enabled(self.sed_id('band_pass_filters_filter'))
        self.assert_is_enabled(self.sed_id('band_pass_filters_from'))
        self.assert_is_enabled(self.sed_id('band_pass_filters'))

        self.click(self.sed('apply_sed'))
        self.assert_is_unchecked(self.sed_id('apply_sed'))
        self.assert_is_disabled(self.sed_id('single_stellar_population_model'))
        self.assert_is_disabled(self.sed_id('band_pass_filters_filter'))
        self.assert_is_disabled(self.sed_id('band_pass_filters_from'))
        self.assert_is_disabled(self.sed_id('band_pass_filters'))

    def test_dust_model_disabled_on_initial_load(self):
        self.click('tao-tabs-' + MODULE_INDICES['sed'])
        self.assert_is_unchecked(self.sed_id('apply_dust'))
        self.assert_is_disabled(self.sed_id('select_dust_model'))

    def test_dust_model_enabled_on_check_apply(self):
        self.click('tao-tabs-' + MODULE_INDICES['sed'])
        self.click(self.sed('apply_sed'))
        self.click(self.sed('apply_dust'))
        self.assert_is_checked(self.sed_id('apply_dust'))
        self.assert_is_enabled(self.sed_id('select_dust_model'))

        self.click(self.sed('apply_dust'))
        self.assert_is_unchecked(self.sed_id('apply_dust'))
        self.assert_is_disabled(self.sed_id('select_dust_model'))

    def assert_simulation_info_shown(self, simulation):
        """  check the name of the simulation in the sidebar is the same as simulation_name
             check the values in the side bar correspond to that simulation
        """
        simulation_selector_value = {
                            '.simulation-info .name': simulation.name,
                            '.simulation-info .details': strip_tags(simulation.details),
                            }
        self.assert_selector_texts_equals_expected_values(simulation_selector_value)
        
    def assert_galaxy_model_info_shown(self, galaxy_model):
        galaxy_model_selector_value = {
                             '.galaxy-model-info .name': galaxy_model.name,
                             '.galaxy-model-info .details': strip_tags(galaxy_model.details),
                             }
        self.assert_selector_texts_equals_expected_values(galaxy_model_selector_value)
        
    def assert_galaxy_model_options_correct_for_a_simulation(self, simulation):
        expected_galaxy_model_names = [x[0] for x in simulation.galaxymodel_set.values_list('name')]
        selector = '%s option' % self.lc_id('galaxy_model')
        actual_galaxy_model_names = [x.text for x in self.selenium.find_elements_by_css_selector(selector)]
        
        self.assertEqual(expected_galaxy_model_names, actual_galaxy_model_names)

    def assert_stellar_model_info_shown(self, stellar_model):
        stellar_model_selector_value = {
                            '.stellar-model-info .name': stellar_model.name,
                            '.stellar-model-info .details': strip_tags(stellar_model.description),
                            }
        self.assert_selector_texts_equals_expected_values(stellar_model_selector_value)

    def assert_dust_model_info_shown(self, dust_model):
        dust_model_selector_value = {
                            '.dust-model-info .name': dust_model.name,
                            '.dust-model-info .details': strip_tags(dust_model.details),
                            }
        self.assert_selector_texts_equals_expected_values(dust_model_selector_value)

    def assert_sidebar_info_not_shown(self, field_name):
        self.assertEqual([], self.find_visible_elements('.' + field_name + '-info .name'))
        self.assertEqual([], self.find_visible_elements('.' + field_name + '-info .details'))