import HTMLParser

from django.utils.html import strip_tags
from selenium.webdriver.common.keys import Keys

from tao.models import Simulation, StellarModel, DustModel, BandPassFilter, DataSetProperty
from tao.settings import MODULE_INDICES
from tao.tests.integration_tests.helper import LiveServerTest
from tao.tests.support.factories import UserFactory, SimulationFactory, GalaxyModelFactory, DataSetFactory, JobFactory, DataSetPropertyFactory, DustModelFactory, StellarModelFactory, BandPassFilterFactory, GlobalParameterFactory, SurveyPresetFactory, SnapshotFactory

class MockGalaxyFactoryTest(LiveServerTest):

    def setUp(self):
        super(MockGalaxyFactoryTest, self).setUp()

        GlobalParameterFactory.create(parameter_name='maximum-random-light-cones', parameter_value='10')
        simulation = SimulationFactory.create(box_size=500)
        simulation2 = SimulationFactory.create()

        for unused in range(3):
            g = GalaxyModelFactory.create()
            ds = DataSetFactory.create(simulation=simulation, galaxy_model=g)
            for unused in range(5):
                DataSetPropertyFactory.create(dataset=ds)
            SnapshotFactory.create(dataset=ds)

        for unused in range(4):
            g = GalaxyModelFactory.create()
            ds = DataSetFactory.create(simulation=simulation2, galaxy_model=g)
            dsp = DataSetPropertyFactory.create(dataset=ds)
            ds.default_filter_field = dsp
            ds.save()

        for i in range(3):
            StellarModelFactory.create()
            BandPassFilterFactory.create(description='<p>BPF Description %s</p>' % i)
            DustModelFactory.create()

        self.survey_preset = SurveyPresetFactory.create(name='Preset 1', parameters='<xml></xml>')
        
        username = "person"
        password = "funnyfish"
        self.user = UserFactory.create(username=username, password=password)
        self.login(username, password)

        self.visit('mock_galaxy_factory')
        self.click('tao-tabs-' + 'light_cone')
        self.select(self.lc_id('catalogue_geometry'), 'Light-Cone')
        

    def tearDown(self):
        super(MockGalaxyFactoryTest, self).tearDown()

    def _test_box_size_field_on_initial_load(self):
        initial_selection = self.get_selected_option_text(self.lc_id('catalogue_geometry'))
        self.assertEqual('Light-Cone', initial_selection)
        self.assert_not_displayed(self.lc_id('box_size'))

    def _test_box_size_field_on_catalogue_geometry_change(self):
        self.select(self.lc_id('catalogue_geometry'), 'Box')
        self.assert_is_displayed(self.lc_id('box_size'))

        self.select(self.lc_id('catalogue_geometry'), 'Light-Cone')
        self.assert_not_displayed(self.lc_id('box_size'))

    def test_max_number_light_cones_displayed(self):
        self.assert_element_text_equals(unicode("label[for='id_light_cone-number_of_light_cones']"), unicode('Select the number of light-cones:  *'))

        ra_open = '1'
        dec_open = '2'
        rmin = '3'
        rmax = '4'
        self.fill_in_fields({'ra_opening_angle': ra_open, 'dec_opening_angle': dec_open, 'redshift_min': rmin, 'redshift_max': rmax}, id_wrap=self.lc_id)

        self.click_by_css(self.lc_id('light_cone_type_1')) # select "random"

        self.assert_element_text_equals(unicode("span.spinner-message"), 'maximum is 10')

        self.click_by_css(self.lc_id('light_cone_type_0')) # select "unique"
        self.assert_element_text_equals(unicode("span.spinner-message"), 'maximum is 8')

        self.clear(self.lc_id('redshift_max'))
        self.assert_element_text_equals(unicode("label[for='id_light_cone-number_of_light_cones']"), unicode('Select the number of light-cones:  *'))

        self.fill_in_fields({'redshift_max': rmin}, id_wrap=self.lc_id)
        self.assert_element_text_equals(unicode("label[for='id_light_cone-number_of_light_cones']"), unicode('Select the number of light-cones:  *' ))


    def test_spinner_arrows_disabled_out_of_range(self):
        self.assertEqual('1', self.get_selector_value(self.lc_id('number_of_light_cones')))
        self.click_by_class_name('ui-spinner-down')
        self.assertEqual('1', self.get_selector_value(self.lc_id('number_of_light_cones')))

        self.click_by_css(self.lc_id('light_cone_type_1')) # select "random", whose maximum is 10
        for unused in range(15):
            self.click_by_class_name('ui-spinner-up')
        self.assertEqual('10', self.get_selector_value(self.lc_id('number_of_light_cones')))

    def _test_sidebar_text_on_initial_load(self):
        first_simulation = Simulation.objects.all()[0]
        first_galaxy_model = first_simulation.galaxymodel_set.all()[0]

        self.assert_galaxy_model_info_shown(first_galaxy_model)
        self.assert_galaxy_model_options_correct_for_a_simulation(first_simulation)
        self.assert_simulation_info_shown(first_simulation)

        self.click('tao-tabs-' + 'sed')
        self.assert_sidebar_info_not_shown('stellar-model')
        self.assert_sidebar_info_not_shown('band-pass')
        self.assert_sidebar_info_not_shown('dust-model')

    def _test_sidebar_text_on_simulation_change(self):
        second_simulation = Simulation.objects.all()[1]

        self.select_dark_matter_simulation(second_simulation)

        self.assert_galaxy_model_info_shown(second_simulation.galaxymodel_set.all()[0])
        self.assert_galaxy_model_options_correct_for_a_simulation(second_simulation)
        self.assert_simulation_info_shown(second_simulation)

    def _test_sidebar_text_on_galaxy_model_change(self):
        first_simulation = Simulation.objects.all()[0]
        second_galaxy_model = first_simulation.galaxymodel_set.all()[1]

        self.select_galaxy_model(second_galaxy_model)

        self.assert_galaxy_model_info_shown(second_galaxy_model)

    # ASVO-464
    def test_sidebar_text_on_output_property_change(self):
        properties = list(DataSetProperty.objects.all())
        op_left = self.selenium.find_element_by_css_selector(self.lc_id('output_properties-left select'))
        # check mouse click updates the sidebar text
        self.click_by_css(self.lc_id('output_properties-left') + " option[value='"+str(properties[0].id)+"']")
        self.assert_output_property_info_shown(properties[0])
        # check arrow up and down keys update the sidebar text
        op_left.send_keys(Keys.ARROW_DOWN)
        self.assert_output_property_info_shown(properties[1])
        for i in range(2, 5):
            op_left.send_keys(Keys.ARROW_DOWN)
            self.assert_output_property_info_shown(properties[i])
        for i in range(2, 5):
            op_left.send_keys(Keys.ARROW_UP)
            self.assert_output_property_info_shown(properties[5-i])
        op_left.send_keys(Keys.ARROW_UP)
        self.assert_output_property_info_shown(properties[0])
        # select multiple options by clicking shift and arrow keys
        for i in range(1, 4):
            op_left.send_keys(Keys.SHIFT + Keys.ARROW_DOWN)
            self.assert_output_property_info_shown(properties[i])
        op_left.send_keys(Keys.META + Keys.ARROW_UP)
        self.assert_output_property_info_shown(properties[3])
        # select multiple options by holding down command key and click different options
        op_left.send_keys(Keys.DOWN + Keys.META)
        self.click_by_css(self.lc_id('output_properties-left') + " option[value='"+str(properties[4].id)+"']")
        self.assert_output_property_info_shown(properties[4])
        self.click_by_css(self.lc_id('output_properties-left') + " option[value='"+str(properties[0].id)+"']")
        self.assert_output_property_info_shown(properties[0])
        self.click_by_css(self.lc_id('output_properties-left') + " option[value='"+str(properties[2].id)+"']")
        self.assert_output_property_info_shown(properties[2])

    def _test_sed_sidebar_text_on_apply_sed(self):
        self.click('tao-tabs-' + 'sed')
        self.click(self.sed('apply_sed'))
        initial_stellar_model = StellarModel.objects.all()[0]
        self.assert_stellar_model_info_shown(initial_stellar_model)
        self.assert_sidebar_info_not_shown('dust')

        self.click(self.sed('apply_sed'))
        self.assert_sidebar_info_not_shown('stellar-model')
        self.assert_sidebar_info_not_shown('band-pass')
        self.assert_sidebar_info_not_shown('dust-model')

    # ASVO-464
    def test_sed_sidebar_text_on_band_pass_filter_change(self):
        filters = list(BandPassFilter.objects.all())
        self.click('tao-tabs-sed')
        self.click(self.sed('apply_sed'))
        bp_left = self.selenium.find_element_by_css_selector(self.sed_id('band_pass_filters-left select'))
        # check mouse click updates the sidebar text
        self.click_by_css(self.sed_id('band_pass_filters-left') + " option[value='"+str(filters[0].id)+"_absolute']")
        self.assert_band_pass_filter_info_shown(filters[0])
        # check arrow up and down keys update the sidebar text
        bp_left.send_keys(Keys.ARROW_DOWN)
        self.assert_band_pass_filter_info_shown(filters[0])  # Band pass filter 000 apparent
        bp_left.send_keys(Keys.ARROW_DOWN)
        self.assert_band_pass_filter_info_shown(filters[1])  # Band pass filter 001 absolute
        bp_left.send_keys(Keys.ARROW_DOWN)
        self.assert_band_pass_filter_info_shown(filters[1])  # Band pass filter 001 apparent
        bp_left.send_keys(Keys.ARROW_DOWN)
        self.assert_band_pass_filter_info_shown(filters[2])  # Band pass filter 002 absolute
        bp_left.send_keys(Keys.ARROW_UP)
        self.assert_band_pass_filter_info_shown(filters[1])  # Band pass filter 001 apparent
        bp_left.send_keys(Keys.ARROW_UP)
        self.assert_band_pass_filter_info_shown(filters[1])  # Band pass filter 001 absolute
        bp_left.send_keys(Keys.ARROW_UP)
        self.assert_band_pass_filter_info_shown(filters[0])  # Band pass filter 000 apparent
        bp_left.send_keys(Keys.ARROW_UP)
        self.assert_band_pass_filter_info_shown(filters[0])  # Band pass filter 000 absolute
        # select multiple options by clicking shift and arrow keys
        bp_left.send_keys(Keys.SHIFT + Keys.ARROW_DOWN)
        self.assert_band_pass_filter_info_shown(filters[0])  # Band pass filter 000 apparent
        bp_left.send_keys(Keys.SHIFT + Keys.ARROW_DOWN)
        self.assert_band_pass_filter_info_shown(filters[1])  # Band pass filter 001 absolute
        bp_left.send_keys(Keys.SHIFT + Keys.ARROW_DOWN)
        self.assert_band_pass_filter_info_shown(filters[1])  # Band pass filter 001 apparent
        bp_left.send_keys(Keys.META + Keys.ARROW_UP)
        self.assert_band_pass_filter_info_shown(filters[1])  # Band pass filter 001 absolute
        # # select multiple options by holding down command key and click different options
        bp_left.send_keys(Keys.DOWN + Keys.META)
        self.click_by_css(self.sed_id('band_pass_filters-left') + " option[value='"+str(filters[2].id)+"_apparent']")
        self.assert_band_pass_filter_info_shown(filters[2])
        self.click_by_css(self.sed_id('band_pass_filters-left') + " option[value='"+str(filters[0].id)+"_absolute']")
        self.assert_band_pass_filter_info_shown(filters[0])
        self.click_by_css(self.sed_id('band_pass_filters-left') + " option[value='"+str(filters[2].id)+"_absolute']")
        self.assert_band_pass_filter_info_shown(filters[2])

    def _test_sed_sidebar_text_on_apply_dust(self):
        self.click('tao-tabs-' + 'sed')
        self.click(self.sed('apply_sed'))
        self.click(self.sed('apply_dust'))
        initial_dust_model = DustModel.objects.all()[0]
        self.assert_dust_model_info_shown(initial_dust_model)

        self.click(self.sed('apply_dust'))
        self.assert_sidebar_info_not_shown('dust')

    def _test_sed_sidebar_text_on_stellar_model_change(self):
        self.click('tao-tabs-' + 'sed')
        self.click(self.sed('apply_sed'))
        third_stellar_model = StellarModel.objects.all()[2]

        self.select_stellar_model(third_stellar_model)
        self.assert_stellar_model_info_shown(third_stellar_model)

    def _test_output_property_details(self):
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

    def _test_bandpass_filter_details(self):
        extension = 'apparent'
        self.click('tao-tabs-' + 'sed')
        self.click(self.sed('apply_sed'))
        for i in [1,0]:
            bandpass_filter = BandPassFilter.objects.all()[i]
            self.click_by_css(self.sed_id('band_pass_filters_from') + " option[value='"+str(bandpass_filter.id)+"_" + extension + "']")
            name_displayed = self.get_info_field('band-pass', 'name')
            self.assertEquals(bandpass_filter.label + ' (' + extension.capitalize() + ')', name_displayed)
        self.click(self.sed_2select('op_add_all'))
        bandpass_filter = BandPassFilter.objects.all()[i]
        self.click_by_css(self.sed_id('band_pass_filters') + " option[value='"+str(bandpass_filter.id)+"_" + extension + "']")
        name_displayed = self.get_info_field('band-pass', 'name')
        self.assertEquals(bandpass_filter.label + ' (' + extension.capitalize() + ')', name_displayed)

    def _test_summary_on_initial_load(self):
        self.click('tao-tabs-' + 'summary')
        init_simulation = Simulation.objects.all()[0]
        init_galaxy_model = init_simulation.galaxymodel_set.all()[0]

        self.assert_summary_field_correctly_shown('Light-Cone', 'light_cone', 'geometry_type')
        self.assert_summary_field_correctly_shown(init_simulation.name, 'light_cone', 'simulation')
        self.assert_summary_field_correctly_shown(init_galaxy_model.name, 'light_cone', 'galaxy_model')
        self.assert_summary_field_correctly_shown('0 properties selected', 'light_cone', 'output_properties')
        self.assert_summary_field_correctly_shown('Not selected', 'sed', 'select_sed')
        self.assert_summary_field_correctly_shown('No Filter', 'record_filter', 'record_filter')
        self.assert_not_displayed(self.get_summary_selector('light_cone', 'box_fields'))
        self.assert_not_displayed(self.get_summary_selector('sed', 'apply_sed'))

    def _test_summary_on_geometry_change(self):
        self.select(self.lc_id('catalogue_geometry'), 'Box')
        self.click('tao-tabs-' + 'summary')

        self.assert_summary_field_correctly_shown('Box', 'light_cone', 'geometry_type')
        self.assert_is_displayed(self.get_summary_selector('light_cone', 'box_fields'))
        self.assert_not_displayed(self.get_summary_selector('light_cone', 'light_cone_fields'))

    def _test_summary_on_simulation_change(self):
        second_simulation = Simulation.objects.all()[1]
        self.select_dark_matter_simulation(second_simulation)
        init_galaxy_model_of_second_simulation = second_simulation.galaxymodel_set.all()[0]
        dataset = init_galaxy_model_of_second_simulation.dataset_set.all()[0]
        filter = dataset.datasetproperty_set.all()[0]
        self.click('tao-tabs-' + 'record_filter')
        self.select_record_filter(filter)
        max_input = "99"
        min_input = "9"
        self.fill_in_fields({'max': max_input, 'min': min_input}, id_wrap=self.rf_id)
        self.click('tao-tabs-' + 'summary')
        self.wait(2)
        h = HTMLParser.HTMLParser()
        if filter.units != '':
            expected_filter_display = min_input + h.unescape(' &le; ') + filter.label + ' (' + filter.units + ') '+ h.unescape(' &le; ') + max_input
        else:
            expected_filter_display = min_input + h.unescape(' &le; ') + filter.label + h.unescape(' &le; ') + max_input

        self.assert_summary_field_correctly_shown(second_simulation.name, 'light_cone', 'simulation')
        self.assert_summary_field_correctly_shown(init_galaxy_model_of_second_simulation.name, 'light_cone', 'galaxy_model')
        self.assert_summary_field_correctly_shown(expected_filter_display, 'record_filter', 'record_filter')

    def _test_summary_on_dataset_description_expand(self):
        # in dataset, stellar model, and dust model, clicking on ">>" expands to show the description
        # ">>" rotates to show the current state: expanded or not
        init_simulation = Simulation.objects.all()[0];
        init_galaxy_model = init_simulation.galaxymodel_set.all()[0]

        self.click('tao-tabs-' + 'summary')
        self.assert_not_displayed(self.get_summary_selector('light_cone', 'simulation_description'))
        self.assert_not_displayed(self.get_summary_selector('light_cone', 'galaxy_model_description'))
        self.assertEqual('>>', self.selenium.find_element_by_id('expand_dataset').text)
        self.click('expand_dataset')
        self.assertEqual('<<', self.selenium.find_element_by_id('expand_dataset').text)
        expected_simulation_details = init_simulation.name + ':\n' + strip_tags(init_simulation.details)
        expected_galaxy_model_details = init_galaxy_model.name + ':\n' + strip_tags(init_galaxy_model.details)
        self.assert_summary_field_correctly_shown(expected_simulation_details, 'light_cone', 'simulation_description')
        self.assert_summary_field_correctly_shown(expected_galaxy_model_details, 'light_cone', 'galaxy_model_description')
        self.assert_is_displayed(self.get_summary_selector('light_cone', 'simulation_description'))
        self.assert_is_displayed(self.get_summary_selector('light_cone', 'galaxy_model_description'))

        self.click('expand_dataset')
        self.assertEqual('>>', self.selenium.find_element_by_id('expand_dataset').text)
        self.assert_not_displayed(self.get_summary_selector('light_cone', 'simulation_description'))
        self.assert_not_displayed(self.get_summary_selector('light_cone', 'galaxy_model_description'))

    def _test_summary_on_filter_list_expand(self):
        # Clicking on ">>" in output properties or bandpass filters expands the div and lists the properties in an unordered list
        self.click('tao-tabs-' + 'summary')
        self.assert_not_displayed(self.get_summary_selector('light_cone', 'output_properties_list'))

        self.click('tao-tabs-' + 'light_cone')
        self.click(self.lc_2select('op_add_all'))
        self.click('tao-tabs-' + 'summary')
        self.click('expand_output_properties')

        # check the right number of properties are displayed, and check if expanded all the right properties are listed
        simulation = Simulation.objects.all()[0]
        galaxy_model = simulation.galaxymodel_set.all()[0]
        dataset = galaxy_model.dataset_set.all()[0]
        dataset_properties = dataset.datasetproperty_set.all()
        self.click('tao-tabs-' + 'summary')
        self.assert_summary_field_correctly_shown(str(len(dataset_properties)) + ' properties selected', 'light_cone', 'output_properties')
        self.assert_summary_field_correctly_shown('\n'.join([dataset_property.label for dataset_property in dataset_properties]), 'light_cone', 'output_properties_list')

    def _test_summary_on_light_cone_dimensions_change(self):
        self.click('tao-tabs-' + 'summary')
        self.assert_summary_field_correctly_shown('', 'light_cone', 'ra_opening_angle')
        self.assert_summary_field_correctly_shown('', 'light_cone', 'dec_opening_angle')
        self.assert_summary_field_correctly_shown('', 'light_cone', 'redshift_min')
        self.assert_summary_field_correctly_shown('', 'light_cone', 'redshift_max')

        ra_opening_angle = '1'
        dec_opening_angle = '2'
        redshift_min = '3'
        redshift_max = '4'
        h = HTMLParser.HTMLParser()
        self.click('tao-tabs-' + 'light_cone')
        self.fill_in_fields({'ra_opening_angle': ra_opening_angle, 'dec_opening_angle': dec_opening_angle, 'redshift_min': redshift_min, 'redshift_max': redshift_max}, id_wrap=self.lc_id)
        self.click('tao-tabs-' + 'summary')
        self.wait(1)
        self.assert_summary_field_correctly_shown('RA: '+ra_opening_angle+h.unescape('&deg;')+',', 'light_cone', 'ra_opening_angle')
        self.assert_summary_field_correctly_shown('Dec: '+dec_opening_angle+h.unescape('&deg;'), 'light_cone', 'dec_opening_angle')
        self.assert_summary_range_correctly_shown('Redshift: ' + redshift_min + h.unescape(' &le;') + ' z ' + h.unescape('&le;') + redshift_max, 'light_cone', ['redshift_min', 'redshift_max'])

        #range displays should be intelligent, i.e. if the min or max is blank, it isn't displayed
        self.click('tao-tabs-' + 'light_cone')
        self.clear(self.lc_id('redshift_min'))
        self.click('tao-tabs-' + 'summary')
        self.assert_summary_range_correctly_shown('Redshift: z ' + h.unescape('&le;') + ' 4', 'light_cone', ['redshift_min', 'redshift_max'])
        self.click('tao-tabs-' + 'light_cone')
        self.clear(self.lc_id('redshift_max'))
        self.click('tao-tabs-' + 'summary')
        self.assert_summary_range_correctly_shown('', 'light_cone', ['redshift_min', 'redshift_max'])
        self.click('tao-tabs-' + 'light_cone')
        self.fill_in_fields({'redshift_min': 5}, id_wrap=self.lc_id)
        self.click('tao-tabs-' + 'summary')
        self.assert_summary_range_correctly_shown('Redshift: 5 ' + h.unescape('&le;') + ' z', 'light_cone', ['redshift_min', 'redshift_max'])

    def test_summary_on_light_cone_count_and_type(self):
        ra_opening_angle = '1'
        dec_opening_angle = '2'
        redshift_min = '3'
        redshift_max = '4'
        number_of_light_cones = '5'
        self.fill_in_fields({'ra_opening_angle': ra_opening_angle, 'dec_opening_angle': dec_opening_angle, 'redshift_min': redshift_min, 'redshift_max': redshift_max}, id_wrap=self.lc_id)
        self.wait(0.5)
        self.click('tao-tabs-' + 'summary_submit')
        self.assert_summary_field_correctly_shown('1 unique light-cone', 'light_cone', 'number_of_light_cones')

        self.click('tao-tabs-' + 'light_cone')
        self.click_by_css(self.lc_id('light_cone_type_1')) # select "random"
        self.clear(self.lc_id('number_of_light_cones'))
        self.fill_in_fields({'number_of_light_cones': number_of_light_cones}, id_wrap=self.lc_id)
        self.wait(0.5)
        self.click('tao-tabs-' + 'summary_submit')
        self.assert_summary_field_correctly_shown(number_of_light_cones + ' random light-cones', 'light_cone', 'number_of_light_cones')

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

    def _test_unique_random_display_on_geometry_change(self):
        self.select(self.lc_id('catalogue_geometry'), 'Box')
        self.assert_are_not_displayed('light_cone-light_cone_type')

        self.select(self.lc_id('catalogue_geometry'), 'Light-Cone')
        self.assert_are_displayed('light_cone-light_cone_type')

    def test_description_displayed_in_listing(self):
        job = JobFactory.create(user=self.user)
        self.wait(1)
        self.visit('job_index')
        self.assert_page_has_content(job.description)

    def _test_sed_elements_disabled_on_initial_load(self):
        self.click('tao-tabs-' + 'sed')
        self.assert_is_unchecked(self.sed_id('apply_sed'))
        self.assert_is_disabled(self.sed_id('single_stellar_population_model'))
        self.assert_is_disabled(self.sed_id('band_pass_filters_filter'))
        self.assert_is_disabled(self.sed_id('band_pass_filters_from'))
        self.assert_is_disabled(self.sed_id('band_pass_filters'))

    def _test_sed_module_enabled_on_check_apply(self):
        self.click('tao-tabs-' + 'sed')
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

    def _test_dust_model_disabled_on_initial_load(self):
        self.click('tao-tabs-' + 'sed')
        self.assert_is_unchecked(self.sed_id('apply_dust'))
        self.assert_is_disabled(self.sed_id('select_dust_model'))

    def _test_dust_model_enabled_on_check_apply(self):
        self.click('tao-tabs-' + 'sed')
        self.click(self.sed('apply_sed'))
        self.click(self.sed('apply_dust'))
        self.assert_is_checked(self.sed_id('apply_dust'))
        self.assert_is_enabled(self.sed_id('select_dust_model'))

        self.click(self.sed('apply_dust'))
        self.assert_is_unchecked(self.sed_id('apply_dust'))
        self.assert_is_disabled(self.sed_id('select_dust_model'))

    def _test_box_output_properties_not_shown_for_light_cone(self):
        pass

    def _test_light_cone_output_properties_not_shown_for_box(self):
        pass

    def _test_both_output_properties_shown_for_both_geometries(self):
        pass
    
    def assert_summary_range_correctly_shown(self, expected_value, form_name, field_names):
        value_displayed = ''
        for field_name in field_names:
            value_displayed += self.get_summary_field_text(form_name, field_name)
        self.assertEqual(expected_value, value_displayed)

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

    def assert_output_property_info_shown(self, output_property):
        output_property_selector_value = {
                            '.output-property-info .name': output_property.label,
                            '.output-property-info .details': strip_tags(output_property.description),
                            }
        self.assert_selector_texts_equals_expected_values(output_property_selector_value)

    def assert_stellar_model_info_shown(self, stellar_model):
        stellar_model_selector_value = {
                            '.stellar-model-info .name': stellar_model.label,
                            '.stellar-model-info .details': strip_tags(stellar_model.description),
                            }
        self.assert_selector_texts_equals_expected_values(stellar_model_selector_value)

    def assert_band_pass_filter_info_shown(self, band_pass_filter):
        band_pass_filter_selector_value = {
                            '.band-pass-info .name': band_pass_filter.label,
                            '.band-pass-info .details': strip_tags(band_pass_filter.description),
        }
        self.assert_selector_texts_equals_expected_values(band_pass_filter_selector_value)

    def assert_dust_model_info_shown(self, dust_model):
        dust_model_selector_value = {
                            '.dust-model-info .name': dust_model.name,
                            '.dust-model-info .details': strip_tags(dust_model.details),
                            }
        self.assert_selector_texts_equals_expected_values(dust_model_selector_value)

    def assert_sidebar_info_not_shown(self, field_name):
        self.assertEqual([], self.find_visible_elements('.' + field_name + '-info .name'))
        self.assertEqual([], self.find_visible_elements('.' + field_name + '-info .details'))