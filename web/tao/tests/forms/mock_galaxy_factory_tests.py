from django.test.testcases import TransactionTestCase

import datetime

from tao import workflow, time
from tao.forms import OutputFormatForm
from tao.models import Snapshot
from tao.settings import OUTPUT_FORMATS
from taoui_light_cone.forms import Form as LightConeForm
from taoui_sed.forms import Form as SEDForm
from tao.tests.support import stripped_joined_lines
from tao.tests.support.factories import SimulationFactory, GalaxyModelFactory, DataSetFactory, DataSetPropertyFactory, UserFactory, StellarModelFactory, SnapshotFactory
from tao.tests.support.xml import XmlDiffMixin

from tao.tests.support import UtcPlusTen


class MockGalaxyFactoryTests(TransactionTestCase, XmlDiffMixin):

    def setUp(self):
        super(MockGalaxyFactoryTests, self).setUp()

        simulation = SimulationFactory.create()
        galaxy_model = GalaxyModelFactory.create()
        dataset = DataSetFactory.create(simulation=simulation, galaxy_model=galaxy_model)
        DataSetPropertyFactory.create(dataset=dataset)
        SnapshotFactory.create(dataset=dataset)
        self.user = UserFactory.create()
        #expected_timestamp = "2012-11-13 13:45:32+1000"
        time.frozen_time = datetime.datetime(2012, 11, 13, 13, 45, 32, 0, UtcPlusTen())
        self.output_format = OUTPUT_FORMATS[0]['value']

    def tearDown(self):
        super(MockGalaxyFactoryTests, self).tearDown()
        time.frozen_time = None

    def make_light_cone_form(self, values):
        default_values = {
                          'catalogue_geometry': LightConeForm.CONE,
                          'dark_matter_simulation': 1,
                          'galaxy_model': '1',
                          'filter': '1',
                          'ra_opening_angle': '2',
                          'dec_opening_angle': '2',
                          'redshift_min': '1',
                          'redshift_max': '2',
                          }
        default_values.update(values)
        return LightConeForm(default_values)

    def test_ra_dec_min_max(self):
        light_cone_form = self.make_light_cone_form({
            'catalogue_geometry': LightConeForm.CONE,
            'ra_opening_angle': '-1',
            'dec_opening_angle': '-1',
        })
        self.assertEqual({
            'ra_opening_angle': ['Ensure this value is greater than or equal to 0.'],
            'dec_opening_angle': ['Ensure this value is greater than or equal to 0.'],
        }, light_cone_form.errors)

        light_cone_form = self.make_light_cone_form({
            'catalogue_geometry': LightConeForm.CONE,
            'ra_opening_angle': '362',
            'dec_opening_angle': '362',
        })
        self.assertEqual({
            'ra_opening_angle': ['Ensure this value is less than or equal to 360.'],
            'dec_opening_angle': ['Ensure this value is less than or equal to 360.'],
        }, light_cone_form.errors)

    def test_ra_dec_required_for_light_cone(self):
        light_cone_form = self.make_light_cone_form({
            'catalogue_geometry': LightConeForm.CONE,
            'ra_opening_angle': '',
            'dec_opening_angle': ''
        })
        light_cone_form.is_valid()

        self.assertEqual({
            'ra_opening_angle': ['This field is required.'],
            'dec_opening_angle': ['This field is required.'],
        }, light_cone_form.errors)

    def test_ra_dec_not_required_for_light_box(self):
        light_cone_form = self.make_light_cone_form({
            'catalogue_geometry': LightConeForm.BOX,
            'box_size': 1,
            'snapshot': Snapshot.objects.all()[0].id,
            'ra_min': '',
            'dec_min': '',
            'ra_opening_angle': '',
            'dec_opening_angle': '',
        })
        light_cone_form.is_valid()

        self.assertEqual({}, light_cone_form.errors)

    def test_box_size_is_not_required_for_box(self):
        light_cone_form = self.make_light_cone_form({
            'catalogue_geometry': LightConeForm.BOX,
            'snapshot': Snapshot.objects.all()[0].id,
            })

        self.assertTrue(light_cone_form.is_valid())

    def test_min_less_than_max_passes(self):
        light_cone_form = self.make_light_cone_form({'max': '127', 'min': '3'})
        light_cone_form.is_valid()

        self.assertEqual({}, light_cone_form.errors)
        self.assertTrue(light_cone_form.is_valid())

    def test_redshift_min_less_than_redshift_max_passes(self):
        light_cone_form = self.make_light_cone_form({'redshift_max': '2', 'redshift_min': '1.5'})
        light_cone_form.is_valid()

        self.assertEqual({}, light_cone_form.errors)
        self.assertTrue(light_cone_form.is_valid())

    def test_min_equal_max_fails(self):
        light_cone_form = self.make_light_cone_form({'max': '3', 'min': '3'})

        self.assertFalse(light_cone_form.is_valid())
        self.assertEqual(['The "min" field must be less than the "max" field.'], light_cone_form.errors['min'])

    def test_redshift_min_equal_redshift_max_fails(self):
        light_cone_form = self.make_light_cone_form({'redshift_max': '3', 'redshift_min': '3'})

        self.assertFalse(light_cone_form.is_valid())
        self.assertEqual(['The minimum redshift must be less than the maximum redshift.'], light_cone_form.errors['redshift_min'])

    def test_min_greater_than_max_fails(self):
        light_cone_form = self.make_light_cone_form({'max': '3', 'min': '9'})

        self.assertFalse(light_cone_form.is_valid())
        self.assertEqual(['The "min" field must be less than the "max" field.'], light_cone_form.errors['min'])

    def test_redshift_min_greater_than_redshift_max_fails(self):
        light_cone_form = self.make_light_cone_form({'redshift_max': '3', 'redshift_min': '9'})

        self.assertFalse(light_cone_form.is_valid())
        self.assertEqual(['The minimum redshift must be less than the maximum redshift.'], light_cone_form.errors['redshift_min'])

    def test_max_or_min_empty_passes(self):
        form_no_min = self.make_light_cone_form({'max': '3', 'min': ''})
        form_no_max = self.make_light_cone_form({'max': '', 'min': '9'})

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

    def test_redshift_max_redshift_min_length(self):
        redshift_max_overflow_form = self.make_light_cone_form({'redshift_max': '123456789012345678901', 'redshift_min': '7'})
        self.assertFalse(redshift_max_overflow_form.is_valid())
        self.assertEqual(['Ensure that there are no more than 20 digits in total.'], redshift_max_overflow_form.errors['redshift_max'])

        redshift_min_overflow_form = self.make_light_cone_form({'redshift_max': '2', 'redshift_min': '1.0000000000000000000001'})
        self.assertFalse(redshift_min_overflow_form.is_valid())
        self.assertEqual(['Ensure that there are no more than 20 digits in total.'], redshift_min_overflow_form.errors['redshift_min'])

    def test_xml_parameters(self):
        database_name = 'sqlite://sfh_bcgs200_full_z0.db'
        database_box_size = 500

        simulation = SimulationFactory.create(box_size=database_box_size, box_size_units='Mpc')
        galaxy_model = GalaxyModelFactory.create()
        dataset = DataSetFactory.create(database=database_name, simulation=simulation, galaxy_model=galaxy_model)

        stellar_model = StellarModelFactory.create(name='some_name')

        filter_parameter = DataSetPropertyFactory.create(dataset=dataset, units='blah')
        filter_min = '0.93'
        filter_max = '3.345'

        ra_opening_angle = '2.34'

        dec_opening_angle = '32.56'

        redshift_min = '0.1'
        redshift_max = '0.2'

        lc_form = self.make_light_cone_form({
                                   'catalogue_geometry': LightConeForm.CONE,
                                   'dark_matter_simulation': simulation.id,
                                   'galaxy_model': galaxy_model.id,
                                   'filter': filter_parameter.id,
                                   'min': filter_min,
                                   'max': filter_max,
                                   'ra_opening_angle': ra_opening_angle,
                                   'dec_opening_angle': dec_opening_angle,
                                   'redshift_max': redshift_max,
                                   'redshift_min': redshift_min,
                                })

        lc_form.is_valid()
        self.assertEqual({}, lc_form.errors)

        sed_form = SEDForm({'single_stellar_population_model': stellar_model.id})
        sed_form.is_valid()

        output_format_form = OutputFormatForm({'supported_formats': self.output_format})
        output_format_form.is_valid()

        job = workflow.save(self.user, [lc_form, sed_form, output_format_form])

        expected_parameter_xml = stripped_joined_lines("""
            <?xml version="1.0" encoding="utf-8"?>
            <tao xmlns="http://tao.asvo.org.au/schema/module-parameters-v1" timestamp="2012-11-13T13:45:32+1000">

                <workflow name="alpha-light-cone-image">
                    <param name="database-type">postgresql</param>
                    <param name="database-host">tao02.hpc.swin.edu.au</param>
                    <param name="database-name">millennium_full</param>
                    <param name="database-port">3306</param>
                    <param name="database-user"></param>
                    <param name="database-pass"></param>
                    <param name="schema-version">1.0</param>
                    <module name="light-cone">
                        <param name="query-type">%(light_cone)s</param>
                        <param name="simulation-box-size" units="Mpc">500</param>
                        <param name="redshift-min">0.1</param>
                        <param name="redshift-max">0.2</param>
                        <param name="ra-min" units="deg">0</param>
                        <param name="ra-max" units="deg">%(ra_opening_angle)s</param>
                        <param name="dec-min" units="deg">0</param>
                        <param name="dec-max" units="deg">%(dec_opening_angle)s</param>
                        <param name="filter-type">%(filter_type)s</param>
                        <param name="filter-min" units="%(filter_units)s">%(filter_min)s</param>
                        <param name="filter-max" units="%(filter_units)s">%(filter_max)s</param>
                    </module>
                    <module name="sed">
                        <param name="single-stellar-population-model">%(model_id)s</param>
                    </module>
                    <module name="filter">
                    <filter>
                    <waves_filename>wavelengths.dat</waves_filename>
                    <filter_filenames>u.dat,v.dat,zpv.dat,k.dat,zpk.dat</filter_filenames>
                    <vega_filename>A0V_KUR_BB.SED</vega_filename>
                    </filter>
                    </module>
                    <module name="output-file">
                        <param name="format">%(output_format)s</param>
                    </module>
                </workflow>
            </tao>
        """ % {
            'database_name': database_name,
            'light_cone': LightConeForm.CONE,
            'ra_opening_angle': ra_opening_angle,
            'dec_opening_angle': dec_opening_angle,
            'redshift_min': redshift_min,
            'filter_type': filter_parameter.name,
            'filter_min': filter_min,
            'filter_max': filter_max,
            'model_id': stellar_model.name,
            'filter_units': filter_parameter.units,
            'output_format': self.output_format,
        })

        self.assertXmlEqual(expected_parameter_xml, job.parameters)

    def test_xml_parameters_without_filter(self):
        from tao.datasets import NO_FILTER
        database_name = 'some database'
        database_box_size = 500

        simulation = SimulationFactory.create(box_size=database_box_size, box_size_units='Mpc')
        galaxy_model = GalaxyModelFactory.create()
        dataset = DataSetFactory.create(database=database_name, simulation=simulation, galaxy_model=galaxy_model)

        ra_opening_angle = '2.34'

        dec_opening_angle = '32.56'
        redshift_min = '0.1'
        redshift_max = '0.2'

        lc_form = self.make_light_cone_form({
                                   'catalogue_geometry': LightConeForm.CONE,
                                   'dark_matter_simulation': simulation.id,
                                   'galaxy_model': galaxy_model.id,
                                   'filter': NO_FILTER,
                                   'redshift_min': redshift_min,
                                   'redshift_max': redshift_max,
                                   'ra_opening_angle': ra_opening_angle,
                                   'dec_opening_angle': dec_opening_angle,
                                   'redshift_max': redshift_max,
                                   'redshift_min': redshift_min,
                                })

        lc_form.is_valid()  # trigger validation

        stellar_model = StellarModelFactory.create()
        sed_form = SEDForm({'single_stellar_population_model': stellar_model.id})
        sed_form.is_valid()

        output_format_form = OutputFormatForm({'supported_formats': self.output_format})
        output_format_form.is_valid()

        job = workflow.save(self.user, [lc_form, sed_form, output_format_form])

        expected_parameter_xml = stripped_joined_lines("""
            <?xml version="1.0" encoding="utf-8"?>
            <tao xmlns="http://tao.asvo.org.au/schema/module-parameters-v1" timestamp="2012-11-13T13:45:32+1000">

                <workflow name="alpha-light-cone-image">
                    <param name="database-type">postgresql</param>
                    <param name="database-host">tao02.hpc.swin.edu.au</param>
                    <param name="database-name">millennium_full</param>
                    <param name="database-port">3306</param>
                    <param name="database-user"></param>
                    <param name="database-pass"></param>
                    <param name="schema-version">1.0</param>
                    <module name="light-cone">
                        <param name="query-type">%(light_cone)s</param>
                        <param name="simulation-box-size" units="Mpc">500</param>
                        <param name="redshift-min">%(redshift_min)s</param>
                        <param name="redshift-max">%(redshift_max)s</param>
                        <param name="ra-min" units="deg">0</param>
                        <param name="ra-max" units="deg">%(ra_opening_angle)s</param>
                        <param name="dec-min" units="deg">0</param>
                        <param name="dec-max" units="deg">%(dec_opening_angle)s</param>
                    </module>
                    <module name="sed">
                        <param name="single-stellar-population-model">%(model_id)s</param>
                    </module>
                    <module name="filter">
                    <filter>
                    <waves_filename>wavelengths.dat</waves_filename>
                    <filter_filenames>u.dat,v.dat,zpv.dat,k.dat,zpk.dat</filter_filenames>
                    <vega_filename>A0V_KUR_BB.SED</vega_filename>
                    </filter>
                    </module>
                    <module name="output-file">
                        <param name="format">%(output_format)s</param>
                    </module>
                </workflow>
            </tao>
        """ % {
            'database_name': database_name,
            'light_cone': LightConeForm.CONE,
            'ra_opening_angle': ra_opening_angle,
            'dec_opening_angle': dec_opening_angle,
            'redshift_min': redshift_min,
            'redshift_max': redshift_max,
            'model_id': stellar_model.name,
            'output_format': self.output_format,
        })

        self.assertXmlEqual(expected_parameter_xml, job.parameters)
