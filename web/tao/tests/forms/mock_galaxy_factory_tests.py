from django.test.testcases import TransactionTestCase

import datetime

from tao import workflow, time
from tao.forms import OutputFormatForm, RecordFilterForm, NO_FILTER
from tao.models import Snapshot
from tao.settings import OUTPUT_FORMATS
from taoui_light_cone.forms import Form as LightConeForm
from taoui_sed.forms import Form as SEDForm
from tao.tests.support import stripped_joined_lines
from tao.tests.support.factories import SimulationFactory, GalaxyModelFactory, DataSetFactory, DataSetPropertyFactory, UserFactory, StellarModelFactory, SnapshotFactory
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
        SnapshotFactory.create(dataset=self.dataset)
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
            }
        self.default_form_values['record_filter'] = {'filter' : NO_FILTER}

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

    def test_min_less_than_max_passes(self):
        light_cone_form = make_form(self.default_form_values,LightConeForm,{'max': '127', 'min': '3'},prefix='light_cone')
        light_cone_form.is_valid()

        self.assertEqual({}, light_cone_form.errors)
        self.assertTrue(light_cone_form.is_valid())

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
        max_overflow_form = make_form(self.default_form_values,RecordFilterForm,{'filter':str(self.filter.id), 'max': '100000000000000000000', 'min': '7'}, prefix='record_filter',ui_holder=MockUIHolder(lc_form))
        self.assertFalse(max_overflow_form.is_valid())
        self.assertEqual(['Ensure that there are no more than 20 digits in total.'], max_overflow_form.errors['max'])

        min_overflow_form = make_form(self.default_form_values,RecordFilterForm,{'filter':str(self.filter.id), 'max': '2', 'min': '1.000000000000000000001'}, prefix='record_filter',ui_holder=MockUIHolder(lc_form))
        self.assertFalse(min_overflow_form.is_valid())
        self.assertEqual(['Ensure that there are no more than 20 digits in total.'], min_overflow_form.errors['min'])

    def test_redshift_max_redshift_min_length(self):
        redshift_max_overflow_form = make_form(self.default_form_values,LightConeForm,{'redshift_max': '123456789012345678901', 'redshift_min': '7'},prefix='light_cone')
        self.assertFalse(redshift_max_overflow_form.is_valid())
        self.assertEqual(['Ensure that there are no more than 20 digits in total.'], redshift_max_overflow_form.errors['redshift_max'])

        redshift_min_overflow_form = make_form(self.default_form_values,LightConeForm,{'redshift_max': '2', 'redshift_min': '1.0000000000000000000001'},prefix='light_cone')
        self.assertFalse(redshift_min_overflow_form.is_valid())
        self.assertEqual(['Ensure that there are no more than 20 digits in total.'], redshift_min_overflow_form.errors['redshift_min'])

