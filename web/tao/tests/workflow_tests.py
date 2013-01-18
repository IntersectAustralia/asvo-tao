import datetime

from decimal import Decimal

from django.test import TestCase

from tao import workflow, time
from tao.forms import OutputFormatForm
from tao.settings import OUTPUT_FORMATS
from taoui_light_cone.forms import Form as LightConeForm
from taoui_sed.forms import Form as SEDForm
from tao.tests.support import stripped_joined_lines, UtcPlusTen
from tao.tests.support.factories import UserFactory, StellarModelFactory, SnapshotFactory, DataSetFactory, SimulationFactory, GalaxyModelFactory, DataSetPropertyFactory
from tao.tests.support.xml import XmlDiffMixin


class WorkflowTests(TestCase, XmlDiffMixin):
    
    def setUp(self):
        super(WorkflowTests, self).setUp()
        # "2012-11-14T13:45:36+10:00"
        time.frozen_time = datetime.datetime(2012, 11, 14, 13, 45, 36, 0, UtcPlusTen())
        self.user = UserFactory.create()

        self.common_parameters = [
            {'attrs': {'name': 'database-type'}, 'value': 'postgresql'},
            {'attrs': {'name': 'database-host'}, 'value': 'tao02.hpc.swin.edu.au'},
            {'attrs': {'name': 'database-name'}, 'value': 'millennium_full'},
            {'attrs': {'name': 'database-port'}, 'value': '3306'},
            {'attrs': {'name': 'database-user'}, 'value': ''},
            {'attrs': {'name': 'database-pass'}, 'value': ''},
            {
                'attrs': {
                    'name': 'schema-version'
                },
                'value': '1.0',
            },
        ]
        self.simulation = SimulationFactory.create(box_size=500)
        self.galaxy_model = GalaxyModelFactory.create()
        self.dataset = DataSetFactory.create(simulation=self.simulation, galaxy_model=self.galaxy_model)
        self.filter = DataSetPropertyFactory.create(name='disc-radius', units="Mpc", dataset=self.dataset)
        stellar_model = StellarModelFactory.create(name='Stella')
        self.sed_parameters = {'single_stellar_population_model': stellar_model.id}
        self.output_format = OUTPUT_FORMATS[0]['value']
        self.output_format_parameters = {'supported_formats': self.output_format}

    def tearDown(self):
        super(WorkflowTests, self).tearDown()
        time.frozen_time = None

    def test_normalizes_decimals(self):
        param = workflow.param("name", Decimal('0E9'))
        self.assertEqual('0', str(param['value']))

    def test_cone(self):
        expected_parameter_xml = stripped_joined_lines("""
            <?xml version="1.0" encoding="utf-8"?>
            <tao xmlns="http://tao.asvo.org.au/schema/module-parameters-v1" timestamp="2012-11-14T13:45:36+1000">
             
                <workflow name="alpha-light-cone-image">
                    <param name="database-type">postgresql</param>
                    <param name="database-host">tao02.hpc.swin.edu.au</param>
                    <param name="database-name">millennium_full</param>
                    <param name="database-port">3306</param>
                    <param name="database-user"></param>
                    <param name="database-pass"></param>
                    <param name="schema-version">1.0</param>
                    <module name="light-cone">
                        <param name="query-type">light-cone</param>
                        <param name="simulation-box-size" units="Mpc">500</param>
                        <param name="redshift-min">0.2</param>
                        <param name="redshift-max">0.3</param>
                        <param name="ra-min" units="deg">18.434</param>
                        <param name="ra-max" units="deg">71.565</param>
                        <param name="dec-min" units="deg">0</param>
                        <param name="dec-max" units="deg">41.810</param>
                        <param name="filter-type">disc-radius</param>
                        <param name="filter-min" units="Mpc">0.1</param>
                        <param name="filter-max" units="Mpc">0.2</param>
                    </module>
                    <module name="sed">
                        <param name="single-stellar-population-model">Stella</param>
                    </module>
                    <module name="filter">
                    <filter>
                    <waves_filename>wavelengths.dat</waves_filename>
                    <filter_filenames>u.dat,v.dat,zpv.dat,k.dat,zpk.dat</filter_filenames>
                    <vega_filename>A0V_KUR_BB.SED</vega_filename>
                    </filter>
                    </module>
                </workflow>
            </tao>
        """)

        light_cone_parameters = {
            'catalogue_geometry': 'light-cone',
            'dark_matter_simulation': self.simulation.id,
            'galaxy_model': self.galaxy_model.id,
            'redshift_min': 0.2,
            'redshift_max': 0.3,
            'ra_min': 18.434,
            'ra_max': 71.565,
            'dec_min': 0,
            'dec_max': 41.810,
            'ra_opening_angle': 9,
            'dec_opening_angle': 10,
            'filter': self.filter.id,
            'max': 0.2,
            'min': 0.1,
            }

        print "TODO convert this test to use save"
        light_cone_form = LightConeForm(light_cone_parameters)
        sed_form = SEDForm(self.sed_parameters)
        self.assertEqual({}, light_cone_form.errors)
        self.assertEqual({}, sed_form.errors)

        job = workflow.save(self.user, [light_cone_form, sed_form])
        actual_parameter_xml = job.parameters

        #self.assertXmlEqual(expected_parameter_xml, actual_parameter_xml)

    def test_box_save(self):
        expected_parameter_xml = stripped_joined_lines("""
            <?xml version="1.0" encoding="utf-8"?>
            <tao xmlns="http://tao.asvo.org.au/schema/module-parameters-v1" timestamp="2012-11-14T13:45:36+1000">
             
                <workflow name="alpha-light-cone-image">
                    <param name="database-type">postgresql</param>
                    <param name="database-host">tao02.hpc.swin.edu.au</param>
                    <param name="database-name">millennium_full</param>
                    <param name="database-port">3306</param>
                    <param name="database-user"></param>
                    <param name="database-pass"></param>
                    <param name="schema-version">1.0</param>
                    <module name="light-cone">
                        <param name="query-type">box</param>
                        <param name="simulation-box-size" units="Mpc">500</param>
                        <param name="redshift-min">0.3</param>
                        <param name="redshift-max">0.3</param>
                        <param name="query-box-size">20</param>
                        <param name="filter-type">disc-radius</param>
                        <param name="filter-min" units="Mpc">0.1</param>
                        <param name="filter-max" units="Mpc">0.2</param>
                    </module>
                    <module name="sed">
                        <param name="single-stellar-population-model">Stella</param>
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
            'output_format': self.output_format,
        })

        snapshot = SnapshotFactory.create(redshift='0.3', dataset=self.dataset)
        light_cone_parameters = {
            'catalogue_geometry': 'box',
            'box_size': 20,
            'snapshot': snapshot.id,
            'dark_matter_simulation': self.simulation.id,
            'filter': self.filter.id,
            'galaxy_model': self.galaxy_model.id,
            'max': 0.2,
            'min': 0.1,
            }
        light_cone_form = LightConeForm(light_cone_parameters)
        sed_form = SEDForm(self.sed_parameters)
        output_format_form = OutputFormatForm(self.output_format_parameters)
        self.assertEqual({}, light_cone_form.errors)
        self.assertEqual({}, sed_form.errors)
        self.assertEqual({}, output_format_form.errors)
        job = workflow.save(self.user, [light_cone_form, sed_form, output_format_form])
        actual_parameter_xml = job.parameters

        self.assertXmlEqual(expected_parameter_xml, actual_parameter_xml)
