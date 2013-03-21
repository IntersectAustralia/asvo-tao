from django.test.testcases import TransactionTestCase

import datetime

from tao import workflow, time
from tao.forms import OutputFormatForm, RecordFilterForm, NO_FILTER
from tao.models import Snapshot, DataSetProperty
from tao.settings import OUTPUT_FORMATS
from taoui_light_cone.forms import Form as LightConeForm
from taoui_sed.forms import Form as SEDForm
from tao.tests.support import stripped_joined_lines
from tao.tests.support.factories import SimulationFactory, GalaxyModelFactory, DataSetFactory, DataSetPropertyFactory, UserFactory, StellarModelFactory, SnapshotFactory, BandPassFilterFactory
from tao.tests.support.xml import XmlDiffMixin

from tao.tests.support import UtcPlusTen
from tao.tests.helper import MockUIHolder, make_form

class MockGalaxyFactoryTests(TransactionTestCase, XmlDiffMixin):

    def setUp(self):
        super(MockGalaxyFactoryTests, self).setUp()

        self.simulation = SimulationFactory.create()
        galaxy_model = GalaxyModelFactory.create()
        self.dataset = DataSetFactory.create(simulation=self.simulation, galaxy_model=galaxy_model)
        self.filter = DataSetPropertyFactory.create(dataset=self.dataset)
        self.filter_long = DataSetPropertyFactory.create(dataset=self.dataset, data_type=DataSetProperty.TYPE_LONG_LONG)
        self.filter_float = DataSetPropertyFactory.create(dataset=self.dataset, data_type=DataSetProperty.TYPE_FLOAT)
        self.dataset.default_filter_field = self.filter
        self.dataset.save()
        SnapshotFactory.create(dataset=self.dataset)

        self.stellar_model = StellarModelFactory.create()
        self.bandpass = BandPassFilterFactory.create()

        self.user = UserFactory.create()
        #expected_timestamp = "2012-11-13 13:45:32+1000"
        time.frozen_time = datetime.datetime(2012, 11, 13, 13, 45, 32, 0, UtcPlusTen())
        self.output_format = OUTPUT_FORMATS[0]['value']
        self.default_form_values = {}
        self.default_form_values['light_cone'] = {
            'catalogue_geometry': LightConeForm.CONE,
            'dark_matter_simulation': 1,
            'galaxy_model': self.dataset.id,
            'output_properties': [str(self.filter.id)],
            'ra_opening_angle': '2',
            'dec_opening_angle': '2',
            'redshift_min': '1',
            'redshift_max': '2',
            'number_of_light_cones': '1',
            }
        self.default_form_values['sed'] = {
            'apply_sed': False,
        }
        self.default_form_values['record_filter'] = {'filter' : 'X-'+NO_FILTER}

    def tearDown(self):
        super(MockGalaxyFactoryTests, self).tearDown()
        time.frozen_time = None

    def test_output_properties_is_required(self):
        light_cone_form = make_form(self.default_form_values,LightConeForm,{
            'output_properties': [],
            },prefix='light_cone')
        self.assertEqual({
            'output_properties': [u'This field is required.'],
            }, light_cone_form.errors)

    def test_ra_dec_min_max(self):
        light_cone_form = make_form(self.default_form_values,LightConeForm,{
            'catalogue_geometry': LightConeForm.CONE,
            'ra_opening_angle': '-1',
            'dec_opening_angle': '-1',
        }, prefix='light_cone')
        self.assertEqual({
            'ra_opening_angle': ['Ensure this value is greater than or equal to 0.'],
            'dec_opening_angle': ['Ensure this value is greater than or equal to 0.'],
        }, light_cone_form.errors)

        light_cone_form = make_form(self.default_form_values,LightConeForm,{
            'catalogue_geometry': LightConeForm.CONE,
            'ra_opening_angle': '362',
            'dec_opening_angle': '362',
        }, prefix='light_cone')
        self.assertEqual({
            'ra_opening_angle': ['Ensure this value is less than or equal to 360.'],
            'dec_opening_angle': ['Ensure this value is less than or equal to 360.'],
        }, light_cone_form.errors)

    def test_ra_dec_required_for_light_cone(self):
        light_cone_form = make_form(self.default_form_values,LightConeForm,{
            'catalogue_geometry': LightConeForm.CONE,
            'ra_opening_angle': '',
            'dec_opening_angle': ''
        },prefix='light_cone')
        light_cone_form.is_valid()

        self.assertEqual({
            'ra_opening_angle': ['This field is required.'],
            'dec_opening_angle': ['This field is required.'],
        }, light_cone_form.errors)

    def test_ra_dec_not_required_for_light_box(self):
        light_cone_form = make_form(self.default_form_values,LightConeForm,{
            'catalogue_geometry': LightConeForm.BOX,
            'box_size': self.simulation.box_size,
            'snapshot': Snapshot.objects.all()[0].id,
            'ra_min': '',
            'dec_min': '',
            'ra_opening_angle': '',
            'dec_opening_angle': '',
        },prefix='light_cone')
        light_cone_form.is_valid()

        self.assertEqual({}, light_cone_form.errors)

    def test_box_size_greater_than_zero(self):
        light_cone_form = make_form(self.default_form_values,LightConeForm,{
            'catalogue_geometry': LightConeForm.BOX,
            'box_size': -10,
            'snapshot': Snapshot.objects.all()[0].id,
            },prefix='light_cone')

        self.assertFalse(light_cone_form.is_valid())
        self.assertTrue('box_size' in light_cone_form.errors)

    def test_box_size_small_or_equal_to_simulation(self):
        light_cone_form = make_form(self.default_form_values,LightConeForm,{
            'catalogue_geometry': LightConeForm.BOX,
            'box_size': self.simulation.box_size + 1,
            'snapshot': Snapshot.objects.all()[0].id,
            },prefix='light_cone')

        self.assertFalse(light_cone_form.is_valid())
        self.assertTrue('box_size' in light_cone_form.errors)

    def test_box_size_is_not_required_for_box(self):
        light_cone_form = make_form(self.default_form_values,LightConeForm,{
            'catalogue_geometry': LightConeForm.BOX,
            'snapshot': Snapshot.objects.all()[0].id,
            },prefix='light_cone')

        self.assertEqual({}, light_cone_form.errors)
        self.assertTrue(light_cone_form.is_valid())


    def test_min_and_max_not_optional_for_default_filter(self):
        light_cone_form = make_form(self.default_form_values,LightConeForm,{},prefix='light_cone')
        record_filter_form = make_form(self.default_form_values,RecordFilterForm,{'filter':'D-'+str(self.filter.id),}, prefix='record_filter',ui_holder=MockUIHolder(light_cone_form))

        self.assertFalse(record_filter_form.is_valid())

    def test_min_and_max_not_used_for_no_filter(self):
        from tao.forms import NO_FILTER
        light_cone_form = make_form(self.default_form_values, LightConeForm, {}, prefix='light_cone')
        record_filter_form = make_form(self.default_form_values, RecordFilterForm, {'filter': 'X-'+NO_FILTER}, prefix='record_filter', ui_holder=MockUIHolder(light_cone_form))

        self.assertTrue(record_filter_form.is_valid())

    def test_min_or_max_required_for_other_filter(self):
        light_cone_form = make_form(self.default_form_values,LightConeForm,{},prefix='light_cone')
        record_filter_form = make_form(self.default_form_values,RecordFilterForm,{'filter':'D-'+str(self.filter_long.id)}, prefix='record_filter',ui_holder=MockUIHolder(light_cone_form))

        self.assertFalse(record_filter_form.is_valid())

    def test_min_or_max_provided_is_valid(self):
        light_cone_form = make_form(self.default_form_values,LightConeForm,{},prefix='light_cone')
        # test on default
        record_filter_form = make_form(self.default_form_values,RecordFilterForm,{'filter':'D-'+str(self.filter.id),'min':'10'}, prefix='record_filter',ui_holder=MockUIHolder(light_cone_form))
        self.assertTrue(record_filter_form.is_valid())
        # test on other
        record_filter_form = make_form(self.default_form_values,RecordFilterForm,{'filter':'D-'+str(self.filter_long.id),'min':'10'}, prefix='record_filter',ui_holder=MockUIHolder(light_cone_form))
        self.assertTrue(record_filter_form.is_valid())

    def test_min_or_max_required_when_no_default(self):
        data_set_no_default = DataSetFactory.create(simulation=self.simulation, galaxy_model=GalaxyModelFactory.create())
        new_filter = DataSetPropertyFactory.create(dataset=data_set_no_default)
        light_cone_form = make_form(self.default_form_values,LightConeForm,{'galaxy_model': data_set_no_default.id, 'output_properties': [str(new_filter.id)],},prefix='light_cone')
        record_filter_form = make_form(self.default_form_values,RecordFilterForm,{'filter':'D-'+str(new_filter.id)}, prefix='record_filter',ui_holder=MockUIHolder(light_cone_form))

        self.assertFalse(record_filter_form.is_valid())

    def test_min_less_than_max_passes(self):
        light_cone_form = make_form(self.default_form_values,LightConeForm,{},prefix='light_cone')
        record_filter_form = make_form(self.default_form_values,RecordFilterForm,{'filter':'D-'+str(self.filter.id),'max': '30', 'min': '3'}, prefix='record_filter',ui_holder=MockUIHolder(light_cone_form))

        self.assertTrue(record_filter_form.is_valid())

    def test_min_right_type_passes(self):
        light_cone_form = make_form(self.default_form_values,LightConeForm,{},prefix='light_cone')
        for filter_obj, val in [(self.filter, '3'), (self.filter_float, '3.0'), (self.filter_long, '3')]:
            record_filter_form = make_form(self.default_form_values,RecordFilterForm,{'filter':'D-'+str(filter_obj.id),'min': val}, prefix='record_filter',ui_holder=MockUIHolder(light_cone_form))
            self.assertTrue(record_filter_form.is_valid())

    def test_min_wrong_type_fails(self):
        light_cone_form = make_form(self.default_form_values,LightConeForm,{},prefix='light_cone')
        for filter_obj, val in [(self.filter, '3.0'), (self.filter_float, 'a'), (self.filter_long, '3.0')]:
            record_filter_form = make_form(self.default_form_values,RecordFilterForm,{'filter':'D-'+str(filter_obj.id),'min': val}, prefix='record_filter',ui_holder=MockUIHolder(light_cone_form))
            self.assertFalse(record_filter_form.is_valid())

    def test_redshift_min_less_than_redshift_max_passes(self):
        light_cone_form = make_form(self.default_form_values,LightConeForm,{'redshift_max': '2', 'redshift_min': '1.5'},prefix='light_cone')
        light_cone_form.is_valid()

        self.assertEqual({}, light_cone_form.errors)
        self.assertTrue(light_cone_form.is_valid())

    def test_min_equal_max_fails(self):
        light_cone_form = make_form(self.default_form_values,LightConeForm,{},prefix='light_cone')

        record_filter_form = make_form(self.default_form_values,RecordFilterForm,{'max': '3', 'min': '3'}, prefix='record_filter',ui_holder=MockUIHolder(light_cone_form))

        self.assertFalse(record_filter_form.is_valid())
        self.assertEqual(['The "min" field must be less than the "max" field.'], record_filter_form.errors['min'])

    def test_redshift_min_equal_redshift_max_fails(self):
        light_cone_form = make_form(self.default_form_values,LightConeForm,{'redshift_max': '3', 'redshift_min': '3'},prefix='light_cone')

        self.assertFalse(light_cone_form.is_valid())
        self.assertEqual(['The minimum redshift must be less than the maximum redshift.'], light_cone_form.errors['redshift_min'])

    def test_min_greater_than_max_fails(self):
        light_cone_form = make_form(self.default_form_values,LightConeForm,{},prefix='light_cone')

        record_filter_form = make_form(self.default_form_values,RecordFilterForm,{'max': '3', 'min': '9'}, prefix='record_filter',ui_holder=MockUIHolder(light_cone_form))

        self.assertFalse(record_filter_form.is_valid())
        self.assertEqual(['The "min" field must be less than the "max" field.'], record_filter_form.errors['min'])

    def test_redshift_min_greater_than_redshift_max_fails(self):
        light_cone_form = make_form(self.default_form_values,LightConeForm,{'redshift_max': '3', 'redshift_min': '9'},prefix='light_cone')

        self.assertFalse(light_cone_form.is_valid())
        self.assertEqual(['The minimum redshift must be less than the maximum redshift.'], light_cone_form.errors['redshift_min'])

    def test_max_or_min_empty_passes(self):
        lc_form = make_form(self.default_form_values,LightConeForm,{},prefix='light_cone')

        rf_form_no_min = make_form(self.default_form_values,RecordFilterForm,{'max': '3', 'min': ''}, prefix='record_filter',ui_holder=MockUIHolder(lc_form))
        rf_form_no_max = make_form(self.default_form_values,RecordFilterForm,{'max': '', 'min': '9'}, prefix='record_filter',ui_holder=MockUIHolder(lc_form))

        self.assertTrue(rf_form_no_min.is_valid())
        self.assertTrue(rf_form_no_max.is_valid())

    # check length of any min/max input is less than or equal to 20 characters
    def test_max_min_length(self):
        lc_form = make_form(self.default_form_values,LightConeForm,{},prefix='light_cone')
        max_overflow_form = make_form(self.default_form_values,RecordFilterForm,{'filter':'D-'+str(self.filter.id), 'max': '100000000000000000000', 'min': '7'}, prefix='record_filter',ui_holder=MockUIHolder(lc_form))
        self.assertFalse(max_overflow_form.is_valid())
        self.assertEqual(['Ensure that there are no more than 20 digits in total.'], max_overflow_form.errors['max'])

        min_overflow_form = make_form(self.default_form_values,RecordFilterForm,{'filter':'D-'+str(self.filter.id), 'max': '2', 'min': '1.000000000000000000001'}, prefix='record_filter',ui_holder=MockUIHolder(lc_form))
        self.assertFalse(min_overflow_form.is_valid())
        self.assertEqual(['Ensure that there are no more than 20 digits in total.'], min_overflow_form.errors['min'])

    def test_redshift_max_redshift_min_length(self):
        redshift_max_overflow_form = make_form(self.default_form_values,LightConeForm,{'redshift_max': '123456789012345678901', 'redshift_min': '7'},prefix='light_cone')
        self.assertFalse(redshift_max_overflow_form.is_valid())
        self.assertEqual(['Ensure that there are no more than 20 digits in total.'], redshift_max_overflow_form.errors['redshift_max'])

        redshift_min_overflow_form = make_form(self.default_form_values,LightConeForm,{'redshift_max': '2', 'redshift_min': '1.0000000000000000000001'},prefix='light_cone')
        self.assertFalse(redshift_min_overflow_form.is_valid())
        self.assertEqual(['Ensure that there are no more than 20 digits in total.'], redshift_min_overflow_form.errors['redshift_min'])

    def test_sed_fields_not_required_for_no_sed(self):
        sed_form_no_sed = make_form(self.default_form_values, SEDForm, {})

        self.assertEqual({}, sed_form_no_sed.errors)
        self.assertTrue(sed_form_no_sed.is_valid())

    def test_sed_fields_required_for_sed(self):
        sed_form = make_form(self.default_form_values, SEDForm, {'apply_sed': True}, prefix='sed')

        self.assertFalse(sed_form.is_valid())
        self.assertEqual(['This field is required.'], sed_form.errors['band_pass_filters'])

    def test_dust_model_required_for_dust(self):
        sed_form_with_dust = make_form(self.default_form_values, SEDForm,
                                       {'apply_sed': True,
                                        'apply_dust': True,
                                        'single_stellar_population_model': self.stellar_model.id,
                                        'band_pass_filters': self.bandpass.id,},
                                       prefix='sed')
        self.assertFalse(sed_form_with_dust.is_valid())
        self.assertEqual(['This field is required.'], sed_form_with_dust.errors['select_dust_model'])
