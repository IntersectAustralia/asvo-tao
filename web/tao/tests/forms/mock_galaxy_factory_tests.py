from django.test.testcases import TransactionTestCase

import datetime

from tao import workflow, time
from tao.forms import LightConeForm, SEDForm
from tao.tests.support import stripped_joined_lines
from tao.tests.support.factories import SimulationFactory, GalaxyModelFactory, DataSetFactory, DataSetParameterFactory, UserFactory, StellarModelFactory
from tao.tests.support.xml import XmlDiffMixin

from tao.tests.support import UtcPlusTen


class MockGalaxyFactoryTests(TransactionTestCase, XmlDiffMixin):

    def setUp(self):
        super(MockGalaxyFactoryTests, self).setUp()

        simulation = SimulationFactory.create()
        galaxy_model = GalaxyModelFactory.create(simulation=simulation)
        dataset = DataSetFactory.create(simulation=simulation, galaxy_model=galaxy_model)
        DataSetParameterFactory.create(dataset=dataset)
        self.user = UserFactory.create()
        #expected_timestamp = "2012-11-13 13:45:32+1000"
        time.frozen_time = datetime.datetime(2012, 11, 13, 13, 45, 32, 0, UtcPlusTen())

    def tearDown(self):
        super(MockGalaxyFactoryTests, self).tearDown()
        time.frozen_time = None

    def make_light_cone_form(self, values):
        default_values = {
                          'box_type': LightConeForm.CONE,
                          'dark_matter_simulation': 1,
                          'galaxy_model': '1',
                          'filter': '1',
                          'ra_min': '1',
                          'ra_max': '2',
                          'dec_min': '1',
                          'dec_max': '2',
                          }
        default_values.update(values)
        return LightConeForm(default_values)

    def test_ra_dec_min_max(self):
        light_cone_form = self.make_light_cone_form({
            'box_type': LightConeForm.CONE,
            'ra_min': '-2',
            'dec_min': '-2',
            'ra_max': '-1',
            'dec_max': '-1',
        })
        self.assertEqual({
            'ra_min': ['Ensure this value is greater than or equal to 0.'],
            'dec_min': ['Ensure this value is greater than or equal to 0.'],
            'ra_max': ['Ensure this value is greater than or equal to 0.'],
            'dec_max': ['Ensure this value is greater than or equal to 0.'],
        }, light_cone_form.errors)

        light_cone_form = self.make_light_cone_form({
            'box_type': LightConeForm.CONE,
            'ra_min': '361',
            'dec_min': '361',
            'ra_max': '362',
            'dec_max': '362',
        })
        self.assertEqual({
            'ra_min': ['Ensure this value is less than or equal to 360.'],
            'dec_min': ['Ensure this value is less than or equal to 360.'],
            'ra_max': ['Ensure this value is less than or equal to 360.'],
            'dec_max': ['Ensure this value is less than or equal to 360.'],
        }, light_cone_form.errors)

    def test_ra_and_dec_min_max(self):
        light_cone_form = self.make_light_cone_form({
            'box_type': LightConeForm.CONE,
            'ra_min': '2',
            'dec_min': '1',
            'ra_max': '2',
            'dec_max': '1'
        })
        light_cone_form.is_valid()
        self.assertEqual({
            'ra_min': ['The "RA min" field must be less than the "RA max" field.'],
            'dec_min': ['The "dec min" field must be less than the "dec max" field.'],
        }, light_cone_form.errors)

    def test_ra_dec_required_for_light_cone(self):
        light_cone_form = self.make_light_cone_form({
            'box_type': LightConeForm.CONE,
            'ra_min': '',
            'dec_min': '',
            'ra_max': '',
            'dec_max': ''
        })
        light_cone_form.is_valid()

        self.assertEqual({
            'ra_min': ['This field is required.'],
            'ra_max': ['This field is required.'],
            'dec_min': ['This field is required.'],
            'dec_max': ['This field is required.'],
        }, light_cone_form.errors)

    def test_ra_dec_not_required_for_light_box(self):
        light_cone_form = self.make_light_cone_form({
            'box_type': LightConeForm.BOX,
            'box_size': 1,
            'ra_min': '',
            'dec_min': '',
            'ra_max': '',
            'dec_max': '',
        })
        light_cone_form.is_valid()

        self.assertEqual({}, light_cone_form.errors)

    def test_box_size_required_for_box(self):
        light_cone_form = self.make_light_cone_form({'box_type': LightConeForm.BOX})

        self.assertFalse(light_cone_form.is_valid())
        self.assertEqual(['The "Box Size" field is required when "Box" is selected'], light_cone_form.errors['box_size'])

    def test_min_less_than_max_passes(self):
        light_cone_form = self.make_light_cone_form({'max': '127', 'min': '3'})
        light_cone_form.is_valid()

        self.assertEqual({}, light_cone_form.errors)
        self.assertTrue(light_cone_form.is_valid())

    def test_rmin_less_than_rmax_passes(self):
        light_cone_form = self.make_light_cone_form({'rmax': '2', 'rmin': '1.5'})
        light_cone_form.is_valid()

        self.assertEqual({}, light_cone_form.errors)
        self.assertTrue(light_cone_form.is_valid())

    def test_min_equal_max_fails(self):
        light_cone_form = self.make_light_cone_form({'max': '3', 'min': '3'})

        self.assertFalse(light_cone_form.is_valid())
        self.assertEqual(['The "min" field must be less than the "max" field.'], light_cone_form.errors['min'])

    def test_rmin_equal_rmax_fails(self):
        light_cone_form = self.make_light_cone_form({'rmax': '3', 'rmin': '3'})

        self.assertFalse(light_cone_form.is_valid())
        self.assertEqual(['The "Rmin" field must be less than the "Rmax" field.'], light_cone_form.errors['rmin'])

    def test_min_greater_than_max_fails(self):
        light_cone_form = self.make_light_cone_form({'max': '3', 'min': '9'})

        self.assertFalse(light_cone_form.is_valid())
        self.assertEqual(['The "min" field must be less than the "max" field.'], light_cone_form.errors['min'])

    def test_rmin_greater_than_rmax_fails(self):
        light_cone_form = self.make_light_cone_form({'rmax': '3', 'rmin': '9'})

        self.assertFalse(light_cone_form.is_valid())
        self.assertEqual(['The "Rmin" field must be less than the "Rmax" field.'], light_cone_form.errors['rmin'])

    def test_max_or_min_empty_passes(self):
        form_no_min = self.make_light_cone_form({'max': '3', 'min': ''})
        form_no_max = self.make_light_cone_form({'max': '', 'min': '9'})

        self.assertTrue(form_no_min.is_valid())
        self.assertTrue(form_no_max.is_valid())

    def test_rmax_or_rmin_empty_passes(self):
        form_no_min = self.make_light_cone_form({'rmax': '3', 'rmin': ''})
        form_no_max = self.make_light_cone_form({'rmax': '', 'rmin': '9'})

        self.assertTrue(form_no_min.is_valid())
        self.assertTrue(form_no_max.is_valid())

    # check length of any min/max input is less than or equal to 20 characters
    def test_max_min_length(self):
        max_overflow_form = self.make_light_cone_form({'max': '100000000000000000000', 'min': '7'})
        self.assertFalse(max_overflow_form.is_valid())
        self.assertEqual(['Ensure that there are no more than 20 digits in total.'], max_overflow_form.errors['max'])

        min_overflow_form = self.make_light_cone_form({'max': '2', 'min': '1.000000000000000000001'})
        self.assertFalse(min_overflow_form.is_valid())
        self.assertEqual(['Ensure that there are no more than 20 digits in total.'], min_overflow_form.errors['min'])

    def test_rmax_rmin_length(self):
        rmax_overflow_form = self.make_light_cone_form({'rmax': '123456789012345678901', 'rmin': '7'})
        self.assertFalse(rmax_overflow_form.is_valid())
        self.assertEqual(['Ensure that there are no more than 20 digits in total.'], rmax_overflow_form.errors['rmax'])

        rmin_overflow_form = self.make_light_cone_form({'rmax': '2', 'rmin': '1.0000000000000000000001'})
        self.assertFalse(rmin_overflow_form.is_valid())
        self.assertEqual(['Ensure that there are no more than 20 digits in total.'], rmin_overflow_form.errors['rmin'])

    def test_xml_parameters(self):
        database_name = 'sqlite://sfh_bcgs200_full_z0.db'
        database_box_size = 500

        simulation = SimulationFactory.create(box_size=database_box_size, box_size_units='Mpc')
        galaxy_model = GalaxyModelFactory.create()
        dataset = DataSetFactory.create(database=database_name, simulation=simulation, galaxy_model=galaxy_model)

        filter_parameter = DataSetParameterFactory.create(dataset=dataset, units='blah')
        filter_min = '0.93'
        filter_max = '3.345'

        ra_min = '1.23'
        ra_max = '2.34'

        dec_min = '12.34'
        dec_max = '32.56'
        rmin = '0.1'
        rmax = '0.2'

        lc_form = self.make_light_cone_form({
                                   'box_type': LightConeForm.CONE,
                                   'dark_matter_simulation': simulation.id,
                                   'galaxy_model': galaxy_model.id,
                                   'filter': filter_parameter.id,
                                   'min': filter_min,
                                   'max': filter_max,
                                   'ra_min': ra_min,
                                   'ra_max': ra_max,
                                   'dec_min': dec_min,
                                   'dec_max': dec_max,
                                   'rmax': rmax,
                                   'rmin': rmin,
                                })

        lc_form.is_valid()  # trigger validation

        stellar_model = StellarModelFactory.create(name='some_name')
        sed_form = SEDForm({'single_stellar_population_model': stellar_model.id})
        sed_form.is_valid()

        job = workflow.save(self.user, lc_form, sed_form)

        expected_parameter_xml = stripped_joined_lines("""
            <?xml version="1.0" encoding="utf-8"?>
            <tao xmlns="http://tao.asvo.org.au/schema/module-parameters-v1" timestamp="2012-11-13T13:45:32+1000">

                <workflow name="alpha-light-cone-image">
                    <param name="database">%(database_name)s</param>
                    <param name="schema-version">1.0</param>
                    <module name="light-cone">
                        <param name="query-type">%(light_cone)s</param>
                        <param name="simulation-box-size" units="Mpc">500</param>
                        <param name="redshift-min">0.1</param>
                        <param name="redshift-max">0.2</param>
                        <param name="ra-min" units="deg">%(ra_min)s</param>
                        <param name="ra-max" units="deg">%(ra_max)s</param>
                        <param name="dec-min" units="deg">%(dec_min)s</param>
                        <param name="dec-max" units="deg">%(dec_max)s</param>
                        <param name="filter-type">%(filter_type)s</param>
                        <param name="filter-min" units="%(filter_units)s">%(filter_min)s</param>
                        <param name="filter-max" units="%(filter_units)s">%(filter_max)s</param>
                    </module>
                    <module name="sed">
                        <param name="single-stellar-population-model">%(model_id)s</param>
                    </module>
                </workflow>
            </tao>
        """ % {
            'database_name': database_name,
            'light_cone': LightConeForm.CONE,
            'ra_min': ra_min,
            'ra_max': ra_max,
            'dec_min': dec_min,
            'dec_max': dec_max,
            'rmin': rmin,
            'filter_type': filter_parameter.name,
            'filter_min': filter_min,
            'filter_max': filter_max,
            'model_id': stellar_model.name,
            'filter_units': filter_parameter.units,
        })

        self.assertXmlEqual(expected_parameter_xml, job.parameters)

    def test_xml_parameters_without_filter(self):
        from tao.datasets import NO_FILTER
        database_name = 'some database'
        database_box_size = 500

        simulation = SimulationFactory.create(box_size=database_box_size, box_size_units='Mpc')
        galaxy_model = GalaxyModelFactory.create()
        dataset = DataSetFactory.create(database=database_name, simulation=simulation, galaxy_model=galaxy_model)

        ra_min = '1.23'
        ra_max = '2.34'

        dec_min = '12.34'
        dec_max = '32.56'
        rmin = '0.1'
        rmax = '0.2'

        lc_form = self.make_light_cone_form({
                                   'box_type': LightConeForm.CONE,
                                   'dark_matter_simulation': simulation.id,
                                   'galaxy_model': galaxy_model.id,
                                   'filter': NO_FILTER,
                                   'rmin': rmin,
                                   'rmax': rmax,
                                   'ra_min': ra_min,
                                   'ra_max': ra_max,
                                   'dec_min': dec_min,
                                   'dec_max': dec_max,
                                   'rmax': rmax,
                                   'rmin': rmin,
                                })

        lc_form.is_valid()  # trigger validation

        stellar_model = StellarModelFactory.create()
        sed_form = SEDForm({'single_stellar_population_model': stellar_model.id})
        sed_form.is_valid()

        job = workflow.save(self.user, lc_form, sed_form)

        expected_parameter_xml = stripped_joined_lines("""
            <?xml version="1.0" encoding="utf-8"?>
            <tao xmlns="http://tao.asvo.org.au/schema/module-parameters-v1" timestamp="2012-11-13T13:45:32+1000">

                <workflow name="alpha-light-cone-image">
                    <param name="database">%(database_name)s</param>
                    <param name="schema-version">1.0</param>
                    <module name="light-cone">
                        <param name="query-type">%(light_cone)s</param>
                        <param name="simulation-box-size" units="Mpc">500</param>
                        <param name="redshift-min">%(rmin)s</param>
                        <param name="redshift-max">%(rmax)s</param>
                        <param name="ra-min" units="deg">%(ra_min)s</param>
                        <param name="ra-max" units="deg">%(ra_max)s</param>
                        <param name="dec-min" units="deg">%(dec_min)s</param>
                        <param name="dec-max" units="deg">%(dec_max)s</param>
                    </module>
                    <module name="sed">
                        <param name="single-stellar-population-model">%(model_id)s</param>
                    </module>
                </workflow>
            </tao>
        """ % {
            'database_name': database_name,
            'light_cone': LightConeForm.CONE,
            'ra_min': ra_min,
            'ra_max': ra_max,
            'dec_min': dec_min,
            'dec_max': dec_max,
            'rmin': rmin,
            'rmax': rmax,
            'model_id': stellar_model.name,
        })

        self.assertXmlEqual(expected_parameter_xml, job.parameters)

    def test_redshift_defaults_to_dataset_limits(self):
        from tao.datasets import NO_FILTER
        database_name = 'sqlite://sfh_bcgs200_full_z0.db'
        database_box_size = 500

        simulation = SimulationFactory.create(box_size=database_box_size, box_size_units='Mpc')
        galaxy_model = GalaxyModelFactory.create()
        dataset = DataSetFactory.create(
            database=database_name,
            simulation=simulation,
            galaxy_model=galaxy_model,
            min_snapshot=0,
            max_snapshot=1,
        )

        expected_timestamp = "2012-11-13T13:45:32+1000"

        ra_min = '1.23'
        ra_max = '2.34'

        dec_min = '12.34'
        dec_max = '32.56'

        lc_form = self.make_light_cone_form({
                                   'box_type': LightConeForm.CONE,
                                   'dark_matter_simulation': simulation.id,
                                   'galaxy_model': galaxy_model.id,
                                   'filter': NO_FILTER,
                                   'ra_min': ra_min,
                                   'ra_max': ra_max,
                                   'dec_min': dec_min,
                                   'dec_max': dec_max,
                                   'rmax': '',
                                   'rmin': '',
                                })

        lc_form.is_valid()  # trigger validation

        stellar_model = StellarModelFactory.create()
        sed_form = SEDForm({'single_stellar_population_model': stellar_model.id})
        sed_form.is_valid()

        job = workflow.save(self.user, lc_form, sed_form)

        expected_parameter_xml = stripped_joined_lines("""
            <?xml version="1.0" encoding="utf-8"?>
            <tao xmlns="http://tao.asvo.org.au/schema/module-parameters-v1" timestamp="%(expected_timestamp)s">

                <workflow name="alpha-light-cone-image">

                    <param name="database">%(database_name)s</param>
                    <param name="schema-version">1.0</param>

                    <module name="light-cone">
                        <param name="query-type">%(light_cone)s</param>
                        <param name="simulation-box-size" units="Mpc">500</param>
                        <param name="redshift-min">%(rmin)s</param>
                        <param name="redshift-max">%(rmax)s</param>
                        <param name="ra-min" units="deg">%(ra_min)s</param>
                        <param name="ra-max" units="deg">%(ra_max)s</param>
                        <param name="dec-min" units="deg">%(dec_min)s</param>
                        <param name="dec-max" units="deg">%(dec_max)s</param>
                    </module>
                    <module name="sed">
                        <param name="single-stellar-population-model">%(model_id)s</param>
                    </module>
                </workflow>
            </tao>
        """ % {
            'database_name': database_name,
            'light_cone': LightConeForm.CONE,
            'ra_min': ra_min,
            'ra_max': ra_max,
            'dec_min': dec_min,
            'dec_max': dec_max,
            'rmin': 0,
            'rmax': 1,
            'model_id': stellar_model.name,
            'expected_timestamp': expected_timestamp
        })

        self.assertXmlEqual(expected_parameter_xml, job.parameters)
