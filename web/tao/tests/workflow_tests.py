# coding=utf-8

import os, datetime

from decimal import Decimal

from django.test import TestCase

from tao import workflow, time
from tao.forms import FormsGraph
from tao.output_format_form import OutputFormatForm
from tao.record_filter_form import RecordFilterForm
from tao.xml_util import xml_print, xml_parse
from taoui_light_cone.forms import Form as LightConeForm
from taoui_sed.forms import Form as SEDForm
from tao.tests.support import stripped_joined_lines, UtcPlusTen
from tao.tests.support.xml import light_cone_xml
from tao.tests.support.factories import UserFactory, StellarModelFactory, SnapshotFactory, DataSetFactory, SimulationFactory, GalaxyModelFactory, DataSetPropertyFactory, BandPassFilterFactory, DustModelFactory, GlobalParameterFactory
from tao.tests.support.xml import XmlDiffMixin
from tao.tests.helper import MockUIHolder, make_form

class WorkflowTests(TestCase, XmlDiffMixin):
    
    def setUp(self):
        super(WorkflowTests, self).setUp()

        OUTPUT_FORMATS = [
            {'value':'csv', 'text':'CSV (Text2)', 'extension':'csv'},
            {'value':'hdf5', 'text':'HDF5', 'extension':'hdf5'},
            {'value': 'fits', 'text': 'FITS', 'extension': 'fits'},
            {'value': 'votable', 'text': 'VOTable', 'extension': 'xml'}
        ]
        self.output_formats = GlobalParameterFactory.create(parameter_name='output_formats', parameter_value=OUTPUT_FORMATS)
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
                'value': '2.0',
            },
        ]
        self.simulation = SimulationFactory.create(box_size=500)
        self.galaxy_model = GalaxyModelFactory.create()
        self.dataset = DataSetFactory.create(simulation=self.simulation, galaxy_model=self.galaxy_model)
        self.filter = DataSetPropertyFactory.create(name='CentralMvir rf', units="Msun/h", dataset=self.dataset)
        self.computed_filter = DataSetPropertyFactory.create(name='Computed Filter', dataset=self.dataset, is_computed = True)
        self.output_prop = DataSetPropertyFactory.create(name='Central op', dataset=self.dataset, is_filter=False)
        self.snapshot = SnapshotFactory.create(dataset=self.dataset, redshift="0.1234567891")
        self.stellar_model = StellarModelFactory.create(name='Stella')
        self.band_pass_filter = BandPassFilterFactory.create(label='bandpass')
        self.dust_model = DustModelFactory.create()
        self.sed_parameters = {'apply_sed': True, 'single_stellar_population_model': self.stellar_model.id,
                               'band_pass_filters': [str(self.band_pass_filter.id) + '_apparent'], 'apply_dust': True,
                               'select_dust_model': self.dust_model.id}
        self.sed_disabled = {'apply_sed': False}
        self.sed_parameters_no_dust = {'apply_sed': True, 'single_stellar_population_model': self.stellar_model.id,
                                       'band_pass_filters': [str(self.band_pass_filter.id) + '_absolute']}


        # from code import interact
        # interact(local=locals())

        self.output_format = OUTPUT_FORMATS[0]['value']
        self.output_format_parameters = {'supported_formats': self.output_format}

    def tearDown(self):
        super(WorkflowTests, self).tearDown()
        time.frozen_time = None
        from tao.models import Simulation
        for sim in Simulation.objects.all():
            sim.delete()

    def test_unique_cone(self):
        form_parameters = {
            'catalogue_geometry': 'light-cone',
            'dark_matter_simulation': self.simulation.id,
            'galaxy_model': self.galaxy_model.id,
            'redshift_min': 0.0,
            'redshift_max': 0.2,
            'ra_opening_angle': 12.001,
            'dec_opening_angle': 10.003,
            'output_properties' : [self.filter.id, self.output_prop.id, self.computed_filter.id],
            'light_cone_type': 'unique',
            'number_of_light_cones': 8,
            }
        xml_parameters = form_parameters.copy()
        xml_parameters.update({
            'username' : self.user.username,
            'dark_matter_simulation': self.simulation.name,
            'galaxy_model': self.galaxy_model.name,
            'output_properties_1_name' : self.filter.name,
            'output_properties_1_label' : self.filter.label,
            'output_properties_1_units' : self.filter.units,
            'output_properties_1_description' : self.filter.description,
            'output_properties_2_name' : self.output_prop.name,
            'output_properties_2_label' : self.output_prop.label,
            'output_properties_2_description' : self.output_prop.description,
            'output_properties_3_name' : self.computed_filter.name,
            'output_properties_3_label' : self.computed_filter.label,
            'output_properties_3_description' : self.computed_filter.description,
            })
        xml_parameters.update({
            'filter': self.filter.name,
            'filter_min' : '1000000',
            'filter_max' : 'None',
        })
        xml_parameters.update({
            'apply_sed': False,
        })
        xml_parameters.update({
            'ssp_encoding': self.stellar_model.encoding,
            'band_pass_filter_label': self.band_pass_filter.label,
            'band_pass_filter_id': self.band_pass_filter.filter_id,
            'band_pass_filter_name': self.band_pass_filter.filter_id,
            'dust_model_name': self.dust_model.name,
        })
        xml_parameters.update({
            'light_cone_id': FormsGraph.LIGHT_CONE_ID,
            'csv_dump_id': FormsGraph.OUTPUT_ID,
            'bandpass_filter_id': FormsGraph.BANDPASS_FILTER_ID,
            'sed_id': FormsGraph.SED_ID,
            'dust_id': FormsGraph.DUST_ID,
        })
        # TODO: there are commented out elements which are not implemented yet
        # comments are ignored by assertXmlEqual

        expected_parameter_xml = light_cone_xml(xml_parameters)

        mock_ui_holder = MockUIHolder()
        light_cone_form = make_form({}, LightConeForm, form_parameters, ui_holder=mock_ui_holder, prefix='light_cone')
        sed_form = make_form({}, SEDForm, self.sed_parameters, ui_holder=mock_ui_holder, prefix='sed')
        output_form = make_form({}, OutputFormatForm, {'supported_formats': 'csv'}, ui_holder=mock_ui_holder,
                                    prefix='output_format')
        mock_ui_holder.update(light_cone = light_cone_form, sed = sed_form, output_format = output_form)
        record_filter_form = make_form({}, RecordFilterForm, {'filter':'D-'+str(self.filter.id),'min':str(1000000)},
                                           ui_holder=mock_ui_holder, prefix='record_filter')
        self.assertEqual({}, light_cone_form.errors)
        self.assertEqual({}, sed_form.errors)
        self.assertEqual({}, record_filter_form.errors)
        self.assertEqual({}, output_form.errors)

        mock_ui_holder.update(record_filter = record_filter_form)
        mock_ui_holder.dataset = self.dataset
        job = workflow.save(self.user, mock_ui_holder)
        actual_parameter_xml = job.parameters

        self.assertEqual(self.dataset.database, job.database)
        self.assertXmlEqual(expected_parameter_xml, actual_parameter_xml)

    def test_random_cone(self):
        form_parameters = {
            'catalogue_geometry': 'light-cone',
            'dark_matter_simulation': self.simulation.id,
            'galaxy_model': self.galaxy_model.id,
            'redshift_min': 0.2,
            'redshift_max': 0.3,
            'ra_opening_angle': 71.565,
            'dec_opening_angle': 41.811,
            'output_properties' : [self.filter.id, self.output_prop.id, self.computed_filter.id],
            'light_cone_type': 'random',
            'number_of_light_cones': 10,
        }
        xml_parameters = form_parameters.copy()
        xml_parameters.update({
            'username' : self.user.username,
            'dark_matter_simulation': self.simulation.name,
            'galaxy_model': self.galaxy_model.name,
            'output_properties_1_name' : self.filter.name,
            'output_properties_1_label' : self.filter.label,
            'output_properties_1_units' : self.filter.units,
            'output_properties_1_description' : self.filter.description,
            'output_properties_2_name' : self.output_prop.name,
            'output_properties_2_label' : self.output_prop.label,
            'output_properties_2_description' : self.output_prop.description,
            'output_properties_3_name' : self.computed_filter.name,
            'output_properties_3_label' : self.computed_filter.label,
            'output_properties_3_description' : self.computed_filter.description,
        })
        xml_parameters.update({
            'filter': self.filter.name,
            'filter_min' : '1000000',
            'filter_max' : 'None',
        })
        xml_parameters.update({
            'ssp_encoding': self.stellar_model.encoding,
            'band_pass_filter_label': self.band_pass_filter.label,
            'band_pass_filter_id': self.band_pass_filter.filter_id,
            'band_pass_filter_name': self.band_pass_filter.filter_id,
            'dust_model_name': self.dust_model.name,

        })
        xml_parameters.update({
            'light_cone_id': FormsGraph.LIGHT_CONE_ID,
            'csv_dump_id': FormsGraph.OUTPUT_ID,
            'bandpass_filter_id': FormsGraph.BANDPASS_FILTER_ID,
            'sed_id': FormsGraph.SED_ID,
            'dust_id': FormsGraph.DUST_ID,
        })
        # TODO: there are commented out elements which are not implemented yet
        # comments are ignored by assertXmlEqual

        expected_parameter_xml = light_cone_xml(xml_parameters)

        mock_ui_holder = MockUIHolder()
        light_cone_form = make_form({}, LightConeForm, form_parameters, ui_holder=mock_ui_holder, prefix='light_cone')
        sed_form = make_form({}, SEDForm, self.sed_parameters, ui_holder=mock_ui_holder, prefix='sed')
        output_form = make_form({}, OutputFormatForm, {'supported_formats': 'csv'}, ui_holder=mock_ui_holder,
                                    prefix='output_format')
        mock_ui_holder.update(light_cone = light_cone_form, sed = sed_form, output_format = output_form)
        mock_ui_holder.dataset = self.dataset
        record_filter_form = make_form({}, RecordFilterForm, {'filter':'D-'+str(self.filter.id),'min':str(1000000)},
                                           ui_holder=mock_ui_holder, prefix='record_filter')
        self.assertEqual({}, light_cone_form.errors)
        self.assertEqual({}, sed_form.errors)
        self.assertEqual({}, record_filter_form.errors)
        self.assertEqual({}, output_form.errors)

        mock_ui_holder.update(record_filter = record_filter_form)
        job = workflow.save(self.user, mock_ui_holder)
        actual_parameter_xml = job.parameters

        self.assertXmlEqual(expected_parameter_xml, actual_parameter_xml)
        self.assertEqual(self.dataset.database, job.database)

    def test_box(self):
        form_parameters = {
            'catalogue_geometry': 'box',
            'dark_matter_simulation': self.simulation.id,
            'galaxy_model': self.dataset.id,
            'output_properties' : [self.filter.id],
            'snapshot': self.snapshot.id,
            'box_size': 20,
            'rng_seed': 12345678901234567890
            }
        xml_parameters = form_parameters.copy()
        xml_parameters.update({
            'username' : self.user.username,
            'dark_matter_simulation': self.simulation.name,
            'galaxy_model': self.galaxy_model.name,
            'output_properties_1_name' : self.filter.name,
            'output_properties_1_label' : self.filter.label,
            'output_properties_1_units' : self.filter.units,
            'output_properties_1_description' : self.filter.description,
            'redshift' : float(self.snapshot.redshift),
            })
        xml_parameters.update({
            'filter': self.filter.name,
            'filter_min' : 'None',
            'filter_max' : '1000000',
            })
        # TODO: there are commented out elements which are not implemented yet
        xml_parameters.update({
            'ssp_encoding': self.stellar_model.encoding,
            'band_pass_filter_label': self.band_pass_filter.label,
            'band_pass_filter_id': self.band_pass_filter.filter_id,
            'band_pass_filter_description': self.band_pass_filter.description,
            'band_pass_extension': 'apparent',
            'dust_model_name': self.dust_model.name,
            })
        xml_parameters.update({
            'light_cone_id': FormsGraph.LIGHT_CONE_ID,
            'csv_dump_id': FormsGraph.OUTPUT_ID,
            'bandpass_filter_id': FormsGraph.BANDPASS_FILTER_ID,
            'sed_id': FormsGraph.SED_ID,
            'dust_id': FormsGraph.DUST_ID,
        })
        # comments are ignored by assertXmlEqual
        expected_parameter_xml = stripped_joined_lines("""<?xml version="1.0"?>
            <!-- Using the XML namespace provides a version for future modifiability.  The timestamp allows
                 a researcher to know when this parameter file was generated.  -->
            <tao xmlns="http://tao.asvo.org.au/schema/module-parameters-v1" timestamp="2012-12-20T13:55:36+10:00">

                <!-- Username submitting the job -->
                <username>%(username)s</username>

                <!-- Workflow name identifies which workflow is to be executed.
                     This is currently a placeholder, the name is ignored. -->
                <workflow name="alpha-light-cone-image">

                    <!-- Global Configuration Parameters -->
                    <schema-version>2.0</schema-version>

                    <!-- Light-cone module parameters -->
                    <light-cone id="%(light_cone_id)s">
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
                        <redshift>%(redshift).10f</redshift>

                        <!-- Size of box to return -->
                        <query-box-size units="Mpc">%(box_size)d</query-box-size>

                        <!-- RNG Seed -->
                        <!-- This will be added by the workflow after the job has been completed
                             to enable the job to be repeated.
                             The information stored may change, the intent is to store whatever is
                             required to re-run the job and obtain the same results. -->
                        <rng-seed>12345678901234567890</rng-seed>

                        <!-- List of fields to be included in the output file -->
                        <output-fields>
                            <item description="%(output_properties_1_description)s" label="%(output_properties_1_label)s" units="%(output_properties_1_units)s">%(output_properties_1_name)s</item>
                        </output-fields>

                    </light-cone>

                    <!-- File output module -->
                    <csv id="%(csv_dump_id)s">
                        <fields>
                            <item label="%(output_properties_1_label)s" units="%(output_properties_1_units)s">%(output_properties_1_name)s</item>
                            <!-- <item label="bandpass (Absolute)">Band_pass_filter_000_absolute</item> -->
                            <item label="bandpass (Apparent)">%(band_pass_filter_id)s_%(band_pass_extension)s</item>
                        </fields>

                        <!-- Module Version Number -->
                        <module-version>1</module-version>

                        <!-- Output file format -->
                        <filename>tao.output.csv</filename>

                        <parents>
                            <item>%(bandpass_filter_id)s</item>
                        </parents>

                    </csv>

                    <!-- Optional: Spectral Energy Distribution parameters -->
                    <sed id="%(sed_id)s">
                        <!-- Module Version Number -->
                        <module-version>1</module-version>

                        <parents>
                            <item>%(light_cone_id)s</item>
                        </parents>

                        %(ssp_encoding)s
                    </sed>

                    <filter id="%(bandpass_filter_id)s">
                        <!-- Module Version Number -->
                        <module-version>1</module-version>

                        <parents>
                            <item>%(dust_id)s</item>
                        </parents>

                        <!-- Bandpass Filters) -->
                        <bandpass-filters>
                            <item description="%(band_pass_filter_description)s" label="%(band_pass_filter_label)s" selected="%(band_pass_extension)s">%(band_pass_filter_id)s</item>
                        </bandpass-filters>
                    </filter>

                    <dust id="%(dust_id)s">
                        <module-version>1</module-version>
                        <parents>
                            <item>%(sed_id)s</item>
                        </parents>
                        <model>%(dust_model_name)s</model>
                    </dust>


                    <!-- Record Filter -->
                    <record-filter>
                        <!-- Module Version Number -->
                        <module-version>1</module-version>

                        <!-- Note that the units are for readability,
                             no unit conversion is supported.  The consumer of the
                             parameter file should check that the expected units are provided. -->
                        <filter>
                            <filter-attribute>%(filter)s</filter-attribute>
                            <filter-min units="Msun/h">%(filter_min)s</filter-min>
                            <filter-max units="Msun/h">%(filter_max)s</filter-max>
                        </filter>
                    </record-filter>

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

        mock_ui_holder = MockUIHolder()
        light_cone_form = make_form({}, LightConeForm, form_parameters, ui_holder=mock_ui_holder, prefix='light_cone')
        output_form = make_form({}, OutputFormatForm, {'supported_formats': 'csv'}, prefix='output_format')
        sed_form = make_form({}, SEDForm, self.sed_parameters, ui_holder=mock_ui_holder, prefix='sed')
        mock_ui_holder.update(light_cone = light_cone_form, sed = sed_form, output_format = output_form)
        mock_ui_holder.dataset = self.dataset
        record_filter_form = make_form({}, RecordFilterForm, {'filter':'D-'+str(self.filter.id),'max':str(1000000)},
                                           ui_holder=mock_ui_holder, prefix='record_filter')
        self.assertEqual({}, light_cone_form.errors)
        self.assertEqual({}, sed_form.errors)
        self.assertEqual({}, record_filter_form.errors)
        self.assertEqual({}, output_form.errors)

        mock_ui_holder.update(record_filter = record_filter_form)
        job = workflow.save(self.user, mock_ui_holder)
        actual_parameter_xml = job.parameters

        self.assertXmlEqual(expected_parameter_xml, actual_parameter_xml)
        self.assertEqual(self.dataset.database, job.database)


    def test_no_sed(self):
        form_parameters = {
            'catalogue_geometry': 'box',
            'dark_matter_simulation': self.simulation.id,
            'galaxy_model': self.dataset.id,
            'output_properties' : [self.filter.id],
            'snapshot': self.snapshot.id,
            'box_size': 20,
            'rng_seed': 12345678901234567890
            }
        xml_parameters = form_parameters.copy()
        xml_parameters.update({
            'username' : self.user.username,
            'dark_matter_simulation': self.simulation.name,
            'galaxy_model': self.galaxy_model.name,
            'output_properties_1_name' : self.filter.name,
            'output_properties_1_label' : self.filter.label,
            'output_properties_1_units' : self.filter.units,
            'output_properties_1_description' : self.filter.description,
            'output_properties_2_name' : self.output_prop.name,
            'output_properties_2_label' : self.output_prop.label,
            'output_properties_2_description' : self.output_prop.description,
            'redshift' : float(self.snapshot.redshift),
            })
        xml_parameters.update({
            'filter': self.filter.name,
            'filter_min' : 'None',
            'filter_max' : '1000000',
            'band_pass_filter_name': self.band_pass_filter.filter_id,
            })
        xml_parameters.update({
            'ssp_encoding': self.stellar_model.encoding,
            'band_pass_filter_label': self.band_pass_filter.label,
            'band_pass_filter_id': self.band_pass_filter.filter_id,
            'band_pass_filter_name': self.band_pass_filter.filter_id,
            'dust_model_name': self.dust_model.name,
            })
        xml_parameters.update({
            'light_cone_id': FormsGraph.LIGHT_CONE_ID,
            'csv_dump_id': FormsGraph.OUTPUT_ID,
            'bandpass_filter_id': FormsGraph.BANDPASS_FILTER_ID,
            'sed_id': FormsGraph.SED_ID,
            'dust_id': FormsGraph.DUST_ID,
            })

        expected_parameter_xml = stripped_joined_lines("""<?xml version="1.0" encoding="UTF-8"?>
            <!-- Using the XML namespace provides a version for future modifiability.  The timestamp allows
                 a researcher to know when this parameter file was generated.  -->
            <tao xmlns="http://tao.asvo.org.au/schema/module-parameters-v1" timestamp="2012-12-20T13:55:36+10:00">

                <!-- Username submitting the job -->
                <username>%(username)s</username>

                <!-- Workflow name identifies which workflow is to be executed.
                     This is currently a placeholder, the name is ignored. -->
                <workflow name="alpha-light-cone-image">

                    <!-- Global Configuration Parameters -->
                    <schema-version>2.0</schema-version>

                    <!-- Light-cone module parameters -->
                    <light-cone id="%(light_cone_id)s">
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
                        <redshift>%(redshift).10f</redshift>

                        <!-- Size of box to return -->
                        <query-box-size units="Mpc">%(box_size)d</query-box-size>

                        <!-- RNG Seed -->
                        <!-- This will be added by the workflow after the job has been completed
                             to enable the job to be repeated.
                             The information stored may change, the intent is to store whatever is
                             required to re-run the job and obtain the same results. -->
                        <rng-seed>12345678901234567890</rng-seed>

                        <!-- List of fields to be included in the output file -->
                        <output-fields>
                            <item description="%(output_properties_1_description)s" label="%(output_properties_1_label)s" units="%(output_properties_1_units)s">%(output_properties_1_name)s</item>
                        </output-fields>

                    </light-cone>

                    <!-- File output module -->
                    <csv id="%(csv_dump_id)s">
                        <fields>
                            <item label="%(output_properties_1_label)s" units="%(output_properties_1_units)s">%(output_properties_1_name)s</item>
                        </fields>

                        <!-- Module Version Number -->
                        <module-version>1</module-version>

                        <!-- Output file format -->
                        <filename>tao.output.csv</filename>

                        <parents>
                            <item>%(light_cone_id)s</item>
                        </parents>

                    </csv>

                    <!-- Record Filter -->
                    <record-filter>
                        <!-- Module Version Number -->
                        <module-version>1</module-version>

                        <!-- Note that the units are for readability,
                             no unit conversion is supported.  The consumer of the
                             parameter file should check that the expected units are provided. -->
                        <filter>
                            <filter-attribute>%(filter)s</filter-attribute>
                            <filter-min units="Msun/h">%(filter_min)s</filter-min>
                            <filter-max units="Msun/h">%(filter_max)s</filter-max>
                        </filter>
                    </record-filter>

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

        mock_ui_holder = MockUIHolder()
        light_cone_form = make_form({}, LightConeForm, form_parameters, ui_holder=mock_ui_holder, prefix='light_cone')
        sed_form = make_form({}, SEDForm, self.sed_disabled, ui_holder=mock_ui_holder, prefix='sed')
        output_form = make_form({}, OutputFormatForm, {'supported_formats': 'csv'}, ui_holder=mock_ui_holder, prefix='output_format')
        mock_ui_holder.update(light_cone = light_cone_form, sed = sed_form, output_format = output_form)
        mock_ui_holder.dataset = self.dataset
        record_filter_form = make_form({}, RecordFilterForm, {'filter':'D-'+str(self.filter.id),'max':str(1000000)},
                                           ui_holder=mock_ui_holder, prefix='record_filter')
        self.assertEqual({}, light_cone_form.errors)
        self.assertEqual({}, sed_form.errors)
        self.assertEqual({}, record_filter_form.errors)
        self.assertEqual({}, output_form.errors)

        mock_ui_holder.update(record_filter = record_filter_form)
        job = workflow.save(self.user, mock_ui_holder)
        actual_parameter_xml = job.parameters

        self.assertXmlEqual(expected_parameter_xml, actual_parameter_xml)
        self.assertEqual(self.dataset.database, job.database)

    def test_no_dust(self):
        form_parameters = {
            'catalogue_geometry': 'box',
            'dark_matter_simulation': self.simulation.id,
            'galaxy_model': self.dataset.id,
            'output_properties' : [self.filter.id],
            'snapshot': self.snapshot.id,
            'box_size': 20,
            'rng_seed': 12345678901234567890
            }
        xml_parameters = form_parameters.copy()
        xml_parameters.update({
            'username' : self.user.username,
            'dark_matter_simulation': self.simulation.name,
            'galaxy_model': self.galaxy_model.name,
            'output_properties_1_name' : self.filter.name,
            'output_properties_1_label' : self.filter.label,
            'output_properties_1_units' : self.filter.units,
            'output_properties_1_description' : self.filter.description,
            'redshift' : float(self.snapshot.redshift),
            })
        xml_parameters.update({
            'filter': self.filter.name,
            'filter_min' : 'None',
            'filter_max' : '1000000',
            })
        # TODO: there are commented out elements which are not implemented yet
        xml_parameters.update({
            'ssp_encoding': self.stellar_model.encoding,
            'band_pass_filter_label': self.band_pass_filter.label,
            'band_pass_filter_id': self.band_pass_filter.filter_id,
            'band_pass_filter_name': self.band_pass_filter.filter_id,
            'band_pass_filter_description': self.band_pass_filter.description,
            'band_pass_extension': 'absolute',
            })
        xml_parameters.update({
            'light_cone_id': FormsGraph.LIGHT_CONE_ID,
            'csv_dump_id': FormsGraph.OUTPUT_ID,
            'bandpass_filter_id': FormsGraph.BANDPASS_FILTER_ID,
            'sed_id': FormsGraph.SED_ID,
            'dust_id': FormsGraph.DUST_ID,
            })
        # comments are ignored by assertXmlEqual
        expected_parameter_xml = stripped_joined_lines("""<?xml version="1.0"?>
            <!-- Using the XML namespace provides a version for future modifiability.  The timestamp allows
                 a researcher to know when this parameter file was generated.  -->
            <tao xmlns="http://tao.asvo.org.au/schema/module-parameters-v1" timestamp="2012-12-20T13:55:36+10:00">

                <!-- Username submitting the job -->
                <username>%(username)s</username>

                <!-- Workflow name identifies which workflow is to be executed.
                     This is currently a placeholder, the name is ignored. -->
                <workflow name="alpha-light-cone-image">

                    <!-- Global Configuration Parameters -->
                    <schema-version>2.0</schema-version>

                    <!-- Light-cone module parameters -->
                    <light-cone id="%(light_cone_id)s">
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
                        <redshift>%(redshift).10f</redshift>

                        <!-- Size of box to return -->
                        <query-box-size units="Mpc">%(box_size)d</query-box-size>

                        <!-- RNG Seed -->
                        <!-- This will be added by the workflow after the job has been completed
                             to enable the job to be repeated.
                             The information stored may change, the intent is to store whatever is
                             required to re-run the job and obtain the same results.-->
                        <rng-seed>12345678901234567890</rng-seed> 

                        <!-- List of fields to be included in the output file -->
                        <output-fields>
                            <item description="%(output_properties_1_description)s" label="%(output_properties_1_label)s" units="%(output_properties_1_units)s">%(output_properties_1_name)s</item>
                        </output-fields>

                    </light-cone>

                    <!-- File output module -->
                    <csv id="%(csv_dump_id)s">
                        <fields>
                            <item label="%(output_properties_1_label)s" units="%(output_properties_1_units)s">%(output_properties_1_name)s</item>
                            <item label="bandpass (Absolute)">%(band_pass_filter_name)s_absolute</item>
                            <!-- <item label="bandpass (Apparent)">%(band_pass_filter_name)s_apparent</item> -->
                        </fields>

                        <!-- Module Version Number -->
                        <module-version>1</module-version>

                        <!-- Output file format -->
                        <filename>tao.output.csv</filename>

                        <parents>
                            <item>%(bandpass_filter_id)s</item>
                        </parents>

                    </csv>

                    <!-- Optional: Spectral Energy Distribution parameters -->
                    <sed id="%(sed_id)s">
                        <!-- Module Version Number -->
                        <module-version>1</module-version>

                        <parents>
                            <item>%(light_cone_id)s</item>
                        </parents>

                        %(ssp_encoding)s
                    </sed>

                    <filter id="%(bandpass_filter_id)s">
                        <module-version>1</module-version>
                        <parents>
                            <item>%(sed_id)s</item>
                        </parents>

                        <!-- Bandpass Filters) -->
                        <bandpass-filters>
                            <item description="%(band_pass_filter_description)s" label="%(band_pass_filter_label)s" selected="%(band_pass_extension)s">%(band_pass_filter_id)s</item>
                        </bandpass-filters>
                    </filter>

                    <!-- Record Filter -->
                    <record-filter>
                        <!-- Module Version Number -->
                        <module-version>1</module-version>

                        <!-- Note that the units are for readability,
                             no unit conversion is supported.  The consumer of the
                             parameter file should check that the expected units are provided. -->
                        <filter>
                            <filter-attribute>%(filter)s</filter-attribute>
                            <filter-min units="Msun/h">%(filter_min)s</filter-min>
                            <filter-max units="Msun/h">%(filter_max)s</filter-max>
                        </filter>
                    </record-filter>

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
        
        mock_ui_holder = MockUIHolder()
        light_cone_form = make_form({}, LightConeForm, form_parameters, ui_holder=mock_ui_holder, prefix='light_cone')
        sed_form = make_form({}, SEDForm, self.sed_parameters_no_dust, ui_holder=mock_ui_holder, prefix='sed')
        output_form = make_form({}, OutputFormatForm, {'supported_formats': 'csv'}, ui_holder=mock_ui_holder, prefix='output_format')
        mock_ui_holder.update(light_cone = light_cone_form, sed = sed_form, output_format = output_form)
        mock_ui_holder.dataset = self.dataset
        record_filter_form = make_form({}, RecordFilterForm, {'filter':'D-'+str(self.filter.id),'max':str(1000000)},
                                           ui_holder=mock_ui_holder, prefix='record_filter')
        self.assertEqual({}, light_cone_form.errors)
        self.assertEqual({}, sed_form.errors)
        self.assertEqual({}, record_filter_form.errors)
        self.assertEqual({}, output_form.errors)

        mock_ui_holder.update(record_filter = record_filter_form)
        job = workflow.save(self.user, mock_ui_holder)
        actual_parameter_xml = job.parameters

        self.assertXmlEqual(expected_parameter_xml, actual_parameter_xml)
        self.assertEqual(self.dataset.database, job.database)
