from tao.tests.integration_tests.helper import LiveServerMGFTest, wait
from tao.tests.support.factories import SimulationFactory, GalaxyModelFactory, UserFactory, DataSetFactory, DataSetPropertyFactory, BandPassFilterFactory, StellarModelFactory
from tao.models import Simulation, DataSet, GalaxyModel
from tao.settings import MODULE_INDICES

class FilterTests(LiveServerMGFTest):

    def setUp(self):
        super(FilterTests, self).setUp()

        simulation1 = SimulationFactory.create()
        simulation2 = SimulationFactory.create()

        for unused in range(4):
            galaxy_model = GalaxyModelFactory.create()
            dataset = DataSetFactory.create(simulation=simulation1, galaxy_model=galaxy_model)
            DataSetPropertyFactory.create(dataset=dataset)

        for unused in range(5):
            galaxy_model = GalaxyModelFactory.create()
            dataset = DataSetFactory.create(simulation=simulation2, galaxy_model=galaxy_model)
            DataSetPropertyFactory.create(dataset=dataset)
            dsp = DataSetPropertyFactory.create(dataset=dataset, is_filter=False)
            dataset.default_filter_field = dsp
            dataset.save()

        self.bp_filters = []
        for unused in range(3):
            self.bp_filters.append(BandPassFilterFactory.create())

        StellarModelFactory.create()

        username = "user"
        password = "password"
        UserFactory.create(username=username, password=password)
        self.login(username, password)

        self.visit('mock_galaxy_factory')
        self.select_dark_matter_simulation(simulation1)
        self.select_galaxy_model(simulation1.galaxymodel_set.all().order_by('id')[0])

        initial_simulation = Simulation.objects.all().order_by('id')[0]
        initial_galaxy_model = initial_simulation.galaxymodel_set.all().order_by('id')[0]
        self.initial_dataset = DataSet.objects.get(simulation=initial_simulation, galaxy_model=initial_galaxy_model)

    def test_filter_options(self):
        # check drop-down list correspond to properties of the currently selected simulation and galaxy model
        self.click(self.lc_2select('op_add_all'))
        self.click('tao-tabs-' + MODULE_INDICES['sed'])
        self.click(self.sed_id('apply_sed'))
        self.click(self.sed_2select('op_add_all'))
        expected_filter_options = self.get_expected_filter_options(self.initial_dataset.id)
        actual_filter_options = self.get_actual_filter_options()

        self.assertEqual(expected_filter_options, actual_filter_options)

    def test_filter_options_with_band_pass_filter(self):
        # check drop-down list correspond to properties of the currently selected simulation and galaxy model
        # plus selected band-pass filter
        self.click(self.lc_2select('op_add_all'))
        self.click('tao-tabs-' + MODULE_INDICES['sed'])
        self.click(self.sed_id('apply_sed'))
        self.click(self.sed_2select('op_add_all'))
        expected_filter_options = self.get_expected_filter_options(self.initial_dataset.id)
        actual_filter_options = self.get_actual_filter_options()

        self.assertEqual(expected_filter_options, actual_filter_options)

    def test_filter_options_with_selected_band_pass_filter_after_submit_error(self):
        # check drop-down list correspond to properties of the currently selected simulation and galaxy model
        # plus selected band-pass filter
        self.click(self.lc_2select('op_add_all'))
        self.click('tao-tabs-' + MODULE_INDICES['sed'])
        self.click(self.sed_id('apply_sed'))
        self.click(self.sed_2select('op_add_all'))
        self.click('tao-tabs-' + MODULE_INDICES['record_filter'])
        self.select_record_filter(self.bp_filters[1])

        self.submit_mgf_form()

        self.assert_errors_on_field(True, self.rf_id('min'))
        self.assert_errors_on_field(True, self.rf_id('max'))

    def test_filter_options_with_selected_band_pass_filter_submit_ok(self):
        # check drop-down list correspond to properties of the currently selected simulation and galaxy model
        # plus selected band-pass filter
        self.click(self.lc_2select('op_add_all'))
        self.fill_in_fields({'ra_opening_angle':'123', 'dec_opening_angle': '123', 'redshift_min':'1', 'redshift_max':'20'}, id_wrap=self.lc_id)
        self.click('tao-tabs-' + MODULE_INDICES['sed'])
        self.click(self.sed_id('apply_sed'))
        self.click(self.sed_2select('op_add_all'))
        self.click('tao-tabs-' + MODULE_INDICES['record_filter'])
        self.select_record_filter(self.bp_filters[1])
        self.fill_in_fields({'max': '12.3', 'min': ''}, id_wrap=self.rf_id)

        self.submit_mgf_form()

        self.assert_on_page('held_jobs')

    def test_filter_options_with_selected_band_pass_filter_after_submit_other_errors(self):
        # check drop-down list correspond to properties of the currently selected simulation and galaxy model
        # plus selected band-pass filter
        self.click(self.lc_2select('op_add_all'))
        self.click('tao-tabs-' + MODULE_INDICES['sed'])
        self.click(self.sed_id('apply_sed'))
        self.click(self.sed_2select('op_add_all'))
        self.click('tao-tabs-' + MODULE_INDICES['record_filter'])
        self.select_record_filter(self.bp_filters[1])
        self.fill_in_fields({'max': '12.3', 'min': ''}, id_wrap=self.rf_id)

        self.submit_mgf_form()

        self.assert_errors_on_field(True, self.lc_id('redshift_min'))
        self.click('tao-tabs-' + MODULE_INDICES['record_filter'])
        self.assertEqual(self.bp_filters[1].label, self.get_selected_option_text(self.rf_id('filter')))
        self.assert_attribute_equals('value', {self.rf_id('min'):'',self.rf_id('max'):'12.3'})

    def test_filter_options_and_is_filter(self):
        # check drop-down list correspond to properties of the currently selected simulation and galaxy model
        simulation = Simulation.objects.all().order_by('id')[1]
        galaxy_model = simulation.galaxymodel_set.all().order_by('id')[0]
        dataset = DataSet.objects.get(simulation=simulation, galaxy_model=galaxy_model)

        self.select_dark_matter_simulation(simulation)
        self.select_galaxy_model(galaxy_model)
        self.click(self.lc_2select('op_add_all'))
        self.click('tao-tabs-' + MODULE_INDICES['sed'])
        self.click(self.sed_id('apply_sed'))
        self.click(self.sed_2select('op_add_all'))

        expected_filter_options = self.get_expected_filter_options(dataset.id)
        actual_filter_options = self.get_actual_filter_options()

        self.assertEqual(expected_filter_options, actual_filter_options)

    def test_filter_updates(self):
        # check drop-down list updates when simulation or galaxy model is changed
        simulation = Simulation.objects.all()[1]
        galaxy_model = simulation.galaxymodel_set.all()[4]
        dataset = DataSet.objects.get(simulation=simulation, galaxy_model=galaxy_model)
        expected_filter_options = self.get_expected_filter_options(dataset.id)

        self.select_dark_matter_simulation(simulation)
        self.select_galaxy_model(galaxy_model)
        self.click(self.lc_2select('op_add_all'))
        self.click('tao-tabs-' + MODULE_INDICES['sed'])
        self.click(self.sed_id('apply_sed'))
        self.click(self.sed_2select('op_add_all'))

        actual_filter_options = self.get_actual_filter_options()

        self.assertEqual(expected_filter_options, actual_filter_options)

    def test_snapshot_updates(self):
        # check drop-down list updates when simulation or galaxy model is changed
        simulation = Simulation.objects.all()[1]
        galaxy_model = simulation.galaxymodel_set.all()[4]
        dataset = DataSet.objects.get(simulation=simulation, galaxy_model=galaxy_model)
        snapshots  = dataset.snapshot_set.all()
        expected_snapshot_options = self.get_expected_snapshot_options(snapshots)

        self.select_dark_matter_simulation(simulation)
        self.select_galaxy_model(galaxy_model)

        actual_snapshot_options = self.get_actual_snapshot_options()
        self.assertEqual(expected_snapshot_options, actual_snapshot_options)

    def test_max_min_fields(self):
        simulation = Simulation.objects.all()[1]
        galaxy_model = simulation.galaxymodel_set.all()[4]
        dataset = DataSet.objects.get(simulation=simulation, galaxy_model=galaxy_model)
        self.select_dark_matter_simulation(simulation)
        self.select_galaxy_model(galaxy_model)

        self.click('tao-tabs-' + MODULE_INDICES['record_filter'])

        ## default record filter for the dataset is pre-selected
        self.assert_is_enabled(self.rf_id('max'))
        self.assert_is_enabled(self.rf_id('min'))
        self.choose_no_filter()
        self.assert_is_disabled(self.rf_id('max'))
        self.assert_is_disabled(self.rf_id('min'))

    def test_max_min_fields_after_failed_submit(self):
        simulation = Simulation.objects.all()[1]
        self.select_dark_matter_simulation(simulation)
        galaxy_model = simulation.galaxymodel_set.all()[4]
        self.select_galaxy_model(galaxy_model)
        dataset = DataSet.objects.get(simulation=simulation, galaxy_model=galaxy_model)
        dataset_parameter = dataset.datasetproperty_set.all()[0]
        self.click(self.lc_2select('op_add_all'))

        self.click('tao-tabs-' + MODULE_INDICES['record_filter'])
        self.choose_filter(dataset_parameter)
        max_input = "bad number"
        min_input = "73"
        self.fill_in_fields({'max': max_input, 'min': min_input}, id_wrap=self.rf_id)

        self.submit_mgf_form()

        # check values are the same in the form as user previously selected
        self.click('tao-tabs-' + MODULE_INDICES['light_cone'])
        self.assertEqual(simulation.name, self.get_selected_option_text(self.lc_id('dark_matter_simulation')))
        self.assertEqual(galaxy_model.name, self.get_selected_option_text(self.lc_id('galaxy_model')))

        # check after failed submit, max/min fields are both still enabled
        self.click('tao-tabs-' + MODULE_INDICES['record_filter'])
        self.assert_is_enabled(self.rf_id('max'))
        self.assert_is_enabled(self.rf_id('min'))
        self.assertEqual(dataset_parameter.option_label(), self.get_selected_option_text(self.rf_id('filter')))
        self.assertEqual(max_input, self.get_selector_value(self.rf_id('max')))
        self.assertEqual(min_input, self.get_selector_value(self.rf_id('min')))

    def test_max_min_required_for_data_sets_with_no_default(self):
        simulation = Simulation.objects.all()[0]
        self.select_dark_matter_simulation(simulation)
        galaxy_model = simulation.galaxymodel_set.all()[3]
        self.select_galaxy_model(galaxy_model)
        dataset = DataSet.objects.get(simulation=simulation, galaxy_model=galaxy_model)
        dataset_parameter = dataset.datasetproperty_set.all()[0]
        self.click(self.lc_2select('op_add_all'))

        self.click('tao-tabs-' + MODULE_INDICES['record_filter'])
        self.choose_filter(dataset_parameter)
        self.fill_in_fields({'max': '', 'min': ''}, id_wrap=self.rf_id)

        self.submit_mgf_form()

        self.assert_errors_on_field(True, self.rf_id('min'))
        self.assert_errors_on_field(True, self.rf_id('max'))

    def test_max_min_required_for_data_sets_with_a_default(self):
        simulation = Simulation.objects.all()[1]
        self.select_dark_matter_simulation(simulation)
        galaxy_model = simulation.galaxymodel_set.all()[4]
        self.select_galaxy_model(galaxy_model)
        dataset = DataSet.objects.get(simulation=simulation, galaxy_model=galaxy_model)
        dataset_parameter = dataset.default_filter_field

        self.click('tao-tabs-' + MODULE_INDICES['record_filter'])
        self.choose_filter(dataset_parameter)
        self.fill_in_fields({'max': '', 'min': ''}, id_wrap=self.rf_id)

        self.submit_mgf_form()

        self.assert_errors_on_field(True, self.rf_id('min'))
        self.assert_errors_on_field(True, self.rf_id('max'))

    def test_max_min_for_no_filter(self):
        self.click(self.lc_2select('op_add_all'))
        self.click('tao-tabs-' + MODULE_INDICES['record_filter'])
        dataset_parameter = self.initial_dataset.datasetproperty_set.all()[0]
        self.choose_filter(dataset_parameter)
        self.assert_is_enabled(self.rf_id('max'))
        self.assert_is_enabled(self.rf_id('min'))

        self.choose_no_filter()
        self.assert_is_disabled(self.rf_id('max'))
        self.assert_is_disabled(self.rf_id('min'))
        self.submit_mgf_form()
        self.assert_errors_on_field(False, self.rf_id('min'))
        self.assert_errors_on_field(False, self.rf_id('max'))

    def test_redshift_max_redshift_min_fields_after_failed_submit(self):
        redshift_max_input = "bad number"
        redshift_min_input = "73"
        self.fill_in_fields({'redshift_max': redshift_max_input, 'redshift_min': redshift_min_input}, id_wrap=self.lc_id)

        self.submit_mgf_form()

        self.assertEqual(redshift_max_input, self.get_selector_value(self.lc_id('redshift_max')))
        self.assertEqual(redshift_min_input, self.get_selector_value(self.lc_id('redshift_min')))

    def choose_filter(self, dataset_parameter):
        self.select(self.rf_id('filter'), dataset_parameter.option_label())

    def choose_no_filter(self):
        self.select(self.rf_id('filter'), 'No Filter')
