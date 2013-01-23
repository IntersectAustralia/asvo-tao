# coding=utf-8

import datetime

from decimal import Decimal

from django.test import TestCase

from tao import workflow, time
from tao.forms import OutputFormatForm, RecordFilterForm
from tao.settings import OUTPUT_FORMATS
from taoui_light_cone.forms import Form as LightConeForm
from taoui_sed.forms import Form as SEDForm
from tao.tests.support import stripped_joined_lines, UtcPlusTen
from tao.tests.support.factories import UserFactory, StellarModelFactory, SnapshotFactory, DataSetFactory, SimulationFactory, GalaxyModelFactory, DataSetPropertyFactory
from tao.tests.support.xml import XmlDiffMixin
from tao.tests.helper import MockUIHolder, make_form

class WorkflowTests(TestCase, XmlDiffMixin):
    
    def setUp(self):
        super(WorkflowTests, self).setUp()
        # "2012-12-13T13:55:36+10:00"
        time.frozen_time = datetime.datetime(2012, 12, 20, 13, 55, 36, 0, UtcPlusTen())
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
        self.filter = DataSetPropertyFactory.create(name='CentralMvir', units="Msun/h", dataset=self.dataset)
        self.snapshot = SnapshotFactory.create(dataset=self.dataset, redshift='0.1')
        stellar_model = StellarModelFactory.create(name='Stella')
        self.sed_parameters = {'single_stellar_population_model': stellar_model.id}
        self.output_format = OUTPUT_FORMATS[0]['value']
        self.output_format_parameters = {'supported_formats': self.output_format}

    def tearDown(self):
        super(WorkflowTests, self).tearDown()
        time.frozen_time = None

    def test_cone(self):
        form_parameters = {
            'catalogue_geometry': 'light-cone',
            'dark_matter_simulation': self.simulation.id,
            'galaxy_model': self.galaxy_model.id,
            'redshift_min': 0.2,
            'redshift_max': 0.3,
            'ra_opening_angle': 71.565,
            'dec_opening_angle': 41.811,
            'light_cone_type': 'unique',
            }
        xml_parameters = form_parameters.copy()
        xml_parameters.update({
            'username' : self.user.username,
            'dark_matter_simulation': self.simulation.name,
            'galaxy_model': self.galaxy_model.name,
            })
        xml_parameters.update({
            'filter': self.filter.name,
            'filter_min' : '1E+12',
            'filter_max' : 'None',
        })

        # TODO: there are commented out elements which are not implemented yet
        # comments are ignored by assertXmlEqual
        expected_parameter_xml = stripped_joined_lines("""
            <?xml version="1.0" encoding="UTF-8"?>
            <!-- Using the XML namespace provides a version for future modifiability.  The timestamp allows
                 a researcher to know when this parameter file was generated.  -->
            <tao xmlns="http://tao.asvo.org.au/schema/module-parameters-v1" timestamp="2012-12-20T13:55:36+10:00">

                <!-- Username submitting the job -->
                <username>%(username)s</username>

                <!-- Workflow name identifies which workflow is to be executed.
                     This is currently a placeholder, the name is ignored. -->
                <workflow name="alpha-light-cone-image">

                    <!-- Global Configuration Parameters -->
                    <schema-version>1.0</schema-version>

                    <!-- Light-cone module parameters -->
                    <light-cone>
                        <!-- Module Version Number -->
                        <module-version>1</module-version>

                        <!-- Is the query a light-cone or box? -->
                        <geometry>light-cone</geometry>

                        <!-- Selected Simuation -->
                        <simulation>%(dark_matter_simulation)s</simulation>

                        <!-- Selected Galaxy Model -->
                        <galaxy-model>%(galaxy_model)s</galaxy-model>

                        <!-- The number of light-cones to generate  -->
                        <box-repetition>unique</box-repetition>
                        <num-cones>1</num-cones>

                        <!-- The min and max redshifts to filter by -->
                        <redshift-min>%(redshift_min).1f</redshift-min>
                        <redshift-max>%(redshift_max).1f</redshift-max>

                        <!-- RA/Dec range for limiting the light-cone -->
                        <ra-min units="deg">0.0</ra-min>
                        <ra-max units="deg">%(ra_opening_angle).3f</ra-max>
                        <dec-min units="deg">0.0</dec-min>
                        <dec-max units="deg">%(dec_opening_angle).3f</dec-max>

                        <!-- List of fields to be included in the output file
                        <output-fields>
                            <item label="Coordinates (x,y,z)">coordinates</item>
                            <item label="Velocity (Vx,Vy,Vz)">velocity</item>
                            <item label="Disc Radius" units="Mpc">disc-radius</item>
                            <item label="Bulge mass" units="10^10 M☉/h">bulge-mass</item>
                        </output-fields> -->

                        <!-- RNG Seed -->
                        <!-- This will be added by the workflow after the job has been completed
                             to enable the job to be repeated.
                             The information stored may change, the intent is to store whatever is
                             required to re-run the job and obtain the same results.
                        <rng-seed>12345678901234567890</rng-seed> -->

                    </light-cone>

                    <!-- Record Filter -->
                    <record-filter>
                        <!-- Module Version Number -->
                        <module-version>1</module-version>

                        <!-- Note that the units are for readability,
                             no unit conversion is supported.  The consumer of the
                             parameter file should check that the expected units are provided. -->
                        <filter-type>%(filter)s</filter-type>
                        <filter-min units="Msun/h">%(filter_min)s</filter-min>
                        <filter-max units="Msun/h">%(filter_max)s</filter-max>
                    </record-filter>

                    <!-- File output module -->
                    <output-file>
                        <!-- Module Version Number -->
                        <module-version>1</module-version>

                        <!-- Output file format -->
                        <format>csv</format>
                    </output-file>

                    <!-- Image generation module parameters
                    <image-generator>
                        <!- Module Version Number ->
                        <module-version>1</module-version>

                        <!- Image size parameters ->
                        <image-width units="px">1024</image-width>
                        <image-height units="px">1024</image-height>

                        <!- Focal scale parameters ->
                        <focalx units="??">1024</focalx>
                        <focaly units="??">1024</focaly>

                        <!- Image offset parameters ->
                        <image-offsetx units="??">512</image-offsetx>
                        <image-offsety units="??">0</image-offsety>
                    </image-generator> -->

                </workflow>

                <!-- The signature is automatically generated and is intended to be used when running
                     old versions of the science modules (to remove the need for the UI to parse and check
                     every version. -->
                <signature>base64encodedsignature</signature>

            </tao>
        """) % xml_parameters

        light_cone_form = make_form({}, LightConeForm, form_parameters, prefix='light_cone')
        mock_ui_holder = MockUIHolder(light_cone_form)
        sed_form = make_form({}, SEDForm, self.sed_parameters, prefix='sed')
        record_filter_form = make_form({}, RecordFilterForm, {'filter':self.filter.id,'min':str(10E+11)}, ui_holder=mock_ui_holder, prefix='record_filter')
        output_form = make_form({}, OutputFormatForm, {'supported_formats': 'csv'}, prefix='output_format')
        self.assertEqual({}, light_cone_form.errors)
        self.assertEqual({}, sed_form.errors)
        self.assertEqual({}, record_filter_form.errors)
        self.assertEqual({}, output_form.errors)

        mock_ui_holder.set_forms([light_cone_form, sed_form, record_filter_form, output_form])
        job = workflow.save(self.user, mock_ui_holder)
        actual_parameter_xml = job.parameters

        self.assertXmlEqual(expected_parameter_xml, actual_parameter_xml)
        self.assertEqual(self.dataset.database, job.database)

    def test_box(self):
        form_parameters = {
            'catalogue_geometry': 'box',
            'dark_matter_simulation': self.simulation.id,
            'galaxy_model': self.galaxy_model.id,
            'snapshot': self.snapshot.id,
            'box_size': 20,
            }
        xml_parameters = form_parameters.copy()
        xml_parameters.update({
            'username' : self.user.username,
            'dark_matter_simulation': self.simulation.name,
            'galaxy_model': self.galaxy_model.name,
            'redshift' : float(self.snapshot.redshift),
            })
        xml_parameters.update({
            'filter': self.filter.name,
            'filter_min' : 'None',
            'filter_max' : '1E+12',
            })

        # TODO: there are commented out elements which are not implemented yet
        # comments are ignored by assertXmlEqual
        expected_parameter_xml = stripped_joined_lines("""
            <?xml version="1.0" encoding="UTF-8"?>
            <!-- Using the XML namespace provides a version for future modifiability.  The timestamp allows
                 a researcher to know when this parameter file was generated.  -->
            <tao xmlns="http://tao.asvo.org.au/schema/module-parameters-v1" timestamp="2012-12-20T13:55:36+10:00">

                <!-- Username submitting the job -->
                <username>%(username)s</username>

                <!-- Workflow name identifies which workflow is to be executed.
                     This is currently a placeholder, the name is ignored. -->
                <workflow name="alpha-light-cone-image">

                    <!-- Global Configuration Parameters -->
                    <schema-version>1.0</schema-version>

                    <!-- Light-cone module parameters -->
                    <light-cone>
                        <!-- Module Version Number -->
                        <module-version>1</module-version>

                        <!-- Is the query a light-cone or box? -->
                        <geometry>box</geometry>

                        <!-- Selected Simuation -->
                        <simulation>%(dark_matter_simulation)s</simulation>

                        <!-- Selected Galaxy Model -->
                        <galaxy-model>%(galaxy_model)s</galaxy-model>

                        <!-- The number of light-cones to generate
                        <box-repetition>unique | random</box-repetition>
                        <num-cones>1</num-cones> -->

                        <!-- The min and max redshifts to filter by -->
                        <redshift>%(redshift).1f</redshift>

                        <!-- Size of box to return -->
                        <query-box-size units="Mpc">%(box_size)d</query-box-size>

                        <!-- List of fields to be included in the output file
                        <output-fields>
                            <item label="Coordinates (x,y,z)">coordinates</item>
                            <item label="Velocity (Vx,Vy,Vz)">velocity</item>
                            <item label="Disc Radius" units="Mpc">disc-radius</item>
                            <item label="Bulge mass" units="10^10 M☉/h">bulge-mass</item>
                        </output-fields> -->

                        <!-- RNG Seed -->
                        <!-- This will be added by the workflow after the job has been completed
                             to enable the job to be repeated.
                             The information stored may change, the intent is to store whatever is
                             required to re-run the job and obtain the same results.
                        <rng-seed>12345678901234567890</rng-seed> -->

                    </light-cone>

                    <!-- Record Filter -->
                    <record-filter>
                        <!-- Module Version Number -->
                        <module-version>1</module-version>

                        <!-- Note that the units are for readability,
                             no unit conversion is supported.  The consumer of the
                             parameter file should check that the expected units are provided. -->
                        <filter-type>%(filter)s</filter-type>
                        <filter-min units="Msun/h">%(filter_min)s</filter-min>
                        <filter-max units="Msun/h">%(filter_max)s</filter-max>
                    </record-filter>

                    <!-- File output module -->
                    <output-file>
                        <!-- Module Version Number -->
                        <module-version>1</module-version>

                        <!-- Output file format -->
                        <format>csv</format>
                    </output-file>

                    <!-- Image generation module parameters
                    <image-generator>
                        <!- Module Version Number ->
                        <module-version>1</module-version>

                        <!- Image size parameters ->
                        <image-width units="px">1024</image-width>
                        <image-height units="px">1024</image-height>

                        <!- Focal scale parameters ->
                        <focalx units="??">1024</focalx>
                        <focaly units="??">1024</focaly>

                        <!- Image offset parameters ->
                        <image-offsetx units="??">512</image-offsetx>
                        <image-offsety units="??">0</image-offsety>
                    </image-generator> -->

                </workflow>

                <!-- The signature is automatically generated and is intended to be used when running
                     old versions of the science modules (to remove the need for the UI to parse and check
                     every version. -->
                <signature>base64encodedsignature</signature>

            </tao>
        """) % xml_parameters

        light_cone_form = make_form({}, LightConeForm, form_parameters, prefix='light_cone')
        mock_ui_holder = MockUIHolder(light_cone_form)
        sed_form = make_form({}, SEDForm, self.sed_parameters, prefix='sed')
        record_filter_form = make_form({}, RecordFilterForm, {'filter':self.filter.id,'max':str(10E+11)}, ui_holder=mock_ui_holder, prefix='record_filter')
        output_form = make_form({}, OutputFormatForm, {'supported_formats': 'csv'}, prefix='output_format')
        self.assertEqual({}, light_cone_form.errors)
        self.assertEqual({}, sed_form.errors)
        self.assertEqual({}, record_filter_form.errors)
        self.assertEqual({}, output_form.errors)

        mock_ui_holder.set_forms([light_cone_form, sed_form, record_filter_form, output_form])
        job = workflow.save(self.user, mock_ui_holder)
        actual_parameter_xml = job.parameters

        self.assertXmlEqual(expected_parameter_xml, actual_parameter_xml)
        self.assertEqual(self.dataset.database, job.database)
