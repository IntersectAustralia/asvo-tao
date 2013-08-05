from django.test.testcases import TransactionTestCase

import os, datetime

# from tao import workflow, time
# from tao.forms import OutputFormatForm, RecordFilterForm, NO_FILTER
# from tao.models import Snapshot, DataSetProperty
# from tao.settings import OUTPUT_FORMATS
# from taoui_light_cone.forms import Form as LightConeForm
# from taoui_sed.forms import Form as SEDForm
# from tao.tests.support import stripped_joined_lines
# from tao.tests.support.factories import SimulationFactory, GalaxyModelFactory, DataSetFactory, DataSetPropertyFactory, UserFactory, StellarModelFactory, SnapshotFactory, BandPassFilterFactory
from tao.forms import FormsGraph
from tao.tests.support.xml import light_cone_xml, fits_output_format_xml
from tao.tests.helper import MockUIHolder, make_form_xml, make_form
from tao.output_format_form import OutputFormatForm
from tao.record_filter_form import RecordFilterForm
from taoui_light_cone.forms import Form as LightConeForm
from taoui_sed.forms import Form as SedForm
from tao.tests.support.factories import UserFactory, StellarModelFactory, SnapshotFactory, DataSetFactory, SimulationFactory, GalaxyModelFactory, DataSetPropertyFactory, BandPassFilterFactory, DustModelFactory
from unittest import TestCase
#
# from tao.tests.support import UtcPlusTen
# from tao.tests.helper import MockUIHolder, make_form

class XmlFormsTests(TestCase):

    def setUp(self):
        self.simulation = SimulationFactory.create(box_size=500)
        self.galaxy_model = GalaxyModelFactory.create()
        self.dataset = DataSetFactory.create(simulation=self.simulation, galaxy_model=self.galaxy_model)
        self.filter = DataSetPropertyFactory.create(name='CentralMvir rf', units="Msun/h", dataset=self.dataset)
        self.computed_filter = DataSetPropertyFactory.create(name='Central Value', units="useless", dataset=self.dataset, is_computed=True)
        self.output_prop = DataSetPropertyFactory.create(name='Central op', dataset=self.dataset, is_filter=False)
        self.snapshot = SnapshotFactory.create(dataset=self.dataset, redshift='0.33')
        self.stellar_model = StellarModelFactory.create()
        self.band_pass_filter = BandPassFilterFactory.create()
        self.dust_model = DustModelFactory.create()

    def tearDown(self):
        super(XmlFormsTests, self).tearDown()
        from tao.models import Simulation
        for sim in Simulation.objects.all():
            sim.delete()

    def test_output_format_form(self):
        xml_parameters = {
            'catalogue_geometry': 'light-cone',
            'dark_matter_simulation': self.simulation.id,
            'galaxy_model': self.galaxy_model.id,
            'redshift_min': 0.2,
            'redshift_max': 0.3,
            'ra_opening_angle': 71.565,
            'dec_opening_angle': 41.811,
            'output_properties' : [1L, 2L], #[self.filter.id, self.output_prop.id],
            'light_cone_type': 'unique',
            'number_of_light_cones': 1,
            }
        xml_parameters.update({
            'username' : 'test', # self.user.username,
            'dark_matter_simulation': self.simulation.name,
            'galaxy_model': self.galaxy_model.name,
            'output_properties_1_name' : 'FN', # self.filter.name,
            'output_properties_1_label' : 'FL', # self.filter.label,
            'output_properties_1_units' : 'FU', # self.filter.units,
            'output_properties_1_description' : 'FD', # self.filter.units,
            'output_properties_2_name' : 'OPN', # self.output_prop.name,
            'output_properties_2_label' : 'OPL', # self.output_prop.label,
            'output_properties_2_description' : 'OD', # self.filter.units,
            'output_properties_3_name' : self.computed_filter.name,
            'output_properties_3_label' : self.computed_filter.label,
            'output_properties_3_description' : self.computed_filter.description,
            })
        xml_parameters.update({
            'filter': 'FN', # self.filter.name,
            'filter_min' : '1000000',
            'filter_max' : 'None',
            })
        xml_parameters.update({
            'ssp_name': 'SM', # self.stellar_model.name,
            'band_pass_filter_label': 'BPFN', # self.band_pass_filter.label,
            'band_pass_filter_id': 1L, # self.band_pass_filter.filter_id,
            'band_pass_filter_name': 'BPFN',
            'dust_model_name': 'DM', # self.dust_model.name,
            })
        xml_parameters.update({
            'light_cone_id': FormsGraph.LIGHT_CONE_ID,
            'csv_dump_id': FormsGraph.OUTPUT_ID,
            'bandpass_filter_id': FormsGraph.BANDPASS_FILTER_ID,
            'sed_id': FormsGraph.SED_ID,
            'dust_id': FormsGraph.DUST_ID,
            })
        xml_str = light_cone_xml(xml_parameters)
        form = make_form_xml(OutputFormatForm, xml_str, prefix='output_format')
        self.assertEquals('csv', form.data['output_format-supported_formats'])

    def test_output_format_selection(self):
        xml_parameters = {
            'catalogue_geometry': 'light-cone',
            'dark_matter_simulation': self.simulation.id,
            'galaxy_model': self.galaxy_model.id,
            'redshift_min': 0.2,
            'redshift_max': 0.3,
            'ra_opening_angle': 71.565,
            'dec_opening_angle': 41.811,
            'output_properties' : [1L, 2L], #[self.filter.id, self.output_prop.id],
            'light_cone_type': 'unique',
            'number_of_light_cones': 1,
            }
        xml_parameters.update({
            'username' : 'test', # self.user.username,
            'dark_matter_simulation': self.simulation.name,
            'galaxy_model': self.galaxy_model.name,
            'output_properties_1_name' : 'FN', # self.filter.name,
            'output_properties_1_label' : 'FL', # self.filter.label,
            'output_properties_1_units' : 'FU', # self.filter.units,
            'output_properties_1_description' : 'FD', # self.filter.units,
            'output_properties_2_name' : 'OPN', # self.output_prop.name,
            'output_properties_2_label' : 'OPL', # self.output_prop.label,
            'output_properties_2_description' : 'OD', # self.filter.units,
            })
        xml_parameters.update({
            'filter': 'FN', # self.filter.name,
            'filter_min' : '1000000',
            'filter_max' : 'None',
            })
        xml_parameters.update({
            'ssp_name': 'SM', # self.stellar_model.name,
            'band_pass_filter_label': 'BPFN', # self.band_pass_filter.label,
            'band_pass_filter_id': 1L, # self.band_pass_filter.filter_id,
            'band_pass_filter_name': 'BPFN',
            'dust_model_name': 'DM', # self.dust_model.name,
            })
        xml_parameters.update({
            'light_cone_id': FormsGraph.LIGHT_CONE_ID,
            'csv_dump_id': FormsGraph.OUTPUT_ID,
            'bandpass_filter_id': FormsGraph.BANDPASS_FILTER_ID,
            'sed_id': FormsGraph.SED_ID,
            'dust_id': FormsGraph.DUST_ID,
            })
        xml_str = fits_output_format_xml(xml_parameters)
        form = make_form_xml(OutputFormatForm, xml_str, prefix='output_format')
        self.assertEquals('fits', form.data['output_format-supported_formats'])

    def test_record_filter_form(self):
        xml_parameters = {
            'catalogue_geometry': 'light-cone',
            'dark_matter_simulation': 1l, # self.simulation.id,
            'galaxy_model': 1l, #self.galaxy_model.id,
            'redshift_min': 0.2,
            'redshift_max': 0.3,
            'ra_opening_angle': 71.565,
            'dec_opening_angle': 41.811,
            'output_properties' : [1L, 2L], #[self.filter.id, self.output_prop.id],
            'light_cone_type': 'unique',
            'number_of_light_cones': 1,
            }
        xml_parameters.update({
            'username' : 'test', # self.user.username,
            'dark_matter_simulation': self.simulation.name,
            'galaxy_model': self.galaxy_model.name,
            'output_properties_1_name' : 'FN', # self.filter.name,
            'output_properties_1_label' : 'FL', # self.filter.label,
            'output_properties_1_units' : 'FU', # self.filter.units,
            'output_properties_1_description' : 'FD', # self.filter.units,
            'output_properties_2_name' : 'OPN', # self.output_prop.name,
            'output_properties_2_label' : 'OPL', # self.output_prop.label,
            'output_properties_2_description' : 'OD', # self.filter.units,
            'output_properties_3_name' : self.computed_filter.name,
            'output_properties_3_label' : self.computed_filter.label,
            'output_properties_3_description' : self.computed_filter.description,
        })
        xml_parameters.update({
            'filter': self.filter.name, #'D-'+str(self.filter.id),
            'filter_min' : '1000000',
            'filter_max' : 'None',
            })
        xml_parameters.update({
            'ssp_name': 'SM', # self.stellar_model.name,
            'band_pass_filter_label': 'BPFN', # self.band_pass_filter.label,
            'band_pass_filter_id': 1L, # self.band_pass_filter.filter_id,
            'band_pass_filter_name': 'BPFN',
            'dust_model_name': 'DM', # self.dust_model.name,
        })
        xml_parameters.update({
            'light_cone_id': FormsGraph.LIGHT_CONE_ID,
            'csv_dump_id': FormsGraph.OUTPUT_ID,
            'bandpass_filter_id': FormsGraph.BANDPASS_FILTER_ID,
            'sed_id': FormsGraph.SED_ID,
            'dust_id': FormsGraph.DUST_ID,
        })
        mock_ui_holder = MockUIHolder()
        xml_str = light_cone_xml(xml_parameters)
        light_cone_form = make_form({}, LightConeForm, {'simulation':self.simulation.id, 'galaxy_model':self.dataset.id}, prefix='light_cone')
        mock_ui_holder.update(light_cone = light_cone_form)
        rf_form = make_form_xml(RecordFilterForm, xml_str, prefix='record_filter', ui_holder=mock_ui_holder)

        self.assertEquals('D-' + str(self.filter.id), rf_form.data['record_filter-filter'])
        self.assertEquals('1000000', rf_form.data['record_filter-min'])
        self.assertEquals(None, rf_form.data['record_filter-max'])

    def test_sed_form(self):
        xml_parameters = {
            'catalogue_geometry': 'light-cone',
            'dark_matter_simulation': self.simulation.id, # self.simulation.id,
            'galaxy_model': self.galaxy_model.id, #self.galaxy_model.id,
            'redshift_min': 0.2,
            'redshift_max': 0.3,
            'ra_opening_angle': 71.565,
            'dec_opening_angle': 41.811,
            'output_properties' : [1L, 2L], #[self.filter.id, self.output_prop.id],
            'light_cone_type': 'unique',
            'number_of_light_cones': 1,
            }
        xml_parameters.update({
            'username' : 'test', # self.user.username,
            'dark_matter_simulation': self.simulation.name,
            'galaxy_model': self.galaxy_model.name,
            'output_properties_1_name' : 'FN', # self.filter.name,
            'output_properties_1_label' : 'FL', # self.filter.label,
            'output_properties_1_units' : 'FU', # self.filter.units,
            'output_properties_1_description' : 'FD', # self.filter.units,
            'output_properties_2_name' : 'OPN', # self.output_prop.name,
            'output_properties_2_label' : 'OPL', # self.output_prop.label,
            'output_properties_2_description' : 'OD', # self.filter.units,
            'output_properties_3_name' : self.computed_filter.name,
            'output_properties_3_label' : self.computed_filter.label,
            'output_properties_3_description' : self.computed_filter.description,
        })
        xml_parameters.update({
            'filter': 'FN', # self.filter.name,
            'filter_min' : '1000000',
            'filter_max' : 'None',
            })
        xml_parameters.update({
            'ssp_name': self.stellar_model.name,
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
        xml_str = light_cone_xml(xml_parameters)
        form = make_form_xml(SedForm, xml_str, prefix='sed')
        self.assertEquals(True, form.data['sed-apply_sed'])
        self.assertEquals(self.stellar_model.id, form.data['sed-single_stellar_population_model'])

    def test_light_cone_geometry(self):
        xml_parameters = {
            'catalogue_geometry': 'light-cone',
            'dark_matter_simulation': self.simulation.id, # self.simulation.id,
            'galaxy_model': self.galaxy_model.id, #self.galaxy_model.id,
            'redshift_min': 0.2,
            'redshift_max': 0.3,
            'ra_opening_angle': 71.565,
            'dec_opening_angle': 41.811,
            'output_properties' : [self.filter.id, self.output_prop.id],
            'light_cone_type': 'unique',
            'number_of_light_cones': 1,
            }
        xml_parameters.update({
            'username' : 'test', # self.user.username,
            'dark_matter_simulation': self.simulation.name,
            'galaxy_model': self.galaxy_model.name,
            'output_properties_1_name' : self.filter.name,
            'output_properties_1_label' : self.filter.label,
            'output_properties_1_units' : self.filter.units,
            'output_properties_1_description' : 'FD', # self.filter.units,
            'output_properties_2_name' : self.output_prop.name,
            'output_properties_2_label' : self.output_prop.label,
            'output_properties_2_description' : 'OD', # self.filter.units,
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
            'ssp_name': self.stellar_model.name,
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
        xml_str = light_cone_xml(xml_parameters)
        form = make_form_xml(LightConeForm, xml_str, prefix='light_cone')
        self.assertEquals(LightConeForm.CONE, form.data['light_cone-catalogue_geometry'])
        self.assertEquals(self.dataset.id, form.data['light_cone-galaxy_model'])
        self.assertEquals(self.simulation.id, form.data['light_cone-dark_matter_simulation'])
        self.assertEquals('unique', form.data['light_cone-light_cone_type'])
        self.assertEquals('1', form.data['light_cone-number_of_light_cones'])
        self.assertEquals('0.2', form.data['light_cone-redshift_min'])
        self.assertEquals('0.3', form.data['light_cone-redshift_max'])
        self.assertEquals('71.565', form.data['light_cone-ra_opening_angle'])
        self.assertEquals('71.565', form.data['light_cone-ra_opening_angle'])
        self.assertEquals('41.811', form.data['light_cone-dec_opening_angle'])
        op_list = form.data['light_cone-output_properties']
        self.assertEquals(2, len(op_list))
        self.assertTrue(self.filter.id in op_list)
        self.assertTrue(self.output_prop.id in op_list)

    def test_box_geometry(self):
        xml_parameters = {
            'catalogue_geometry': 'box',
            'dark_matter_simulation': self.simulation.id, # self.simulation.id,
            'galaxy_model': self.galaxy_model.id, #self.galaxy_model.id,
            'redshift': self.snapshot.redshift,
            'box_size': 11.3,
            'output_properties' : [self.filter.id, self.output_prop.id],
            }
        xml_parameters.update({
            'username' : 'test', # self.user.username,
            'dark_matter_simulation': self.simulation.name,
            'galaxy_model': self.galaxy_model.name,
            'output_properties_1_name' : self.filter.name,
            'output_properties_1_label' : self.filter.label,
            'output_properties_1_units' : self.filter.units,
            'output_properties_1_description' : 'FD', # self.filter.units,
            'output_properties_2_name' : self.output_prop.name,
            'output_properties_2_label' : self.output_prop.label,
            'output_properties_2_description' : 'OD', # self.filter.units,
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
            'ssp_name': self.stellar_model.name,
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
        xml_str = light_cone_xml(xml_parameters)
        form = make_form_xml(LightConeForm, xml_str, prefix='light_cone')
        self.assertEquals(LightConeForm.BOX, form.data['light_cone-catalogue_geometry'])
        self.assertEquals(self.dataset.id, form.data['light_cone-galaxy_model'])
        self.assertEquals(self.simulation.id, form.data['light_cone-dark_matter_simulation'])
        self.assertEquals(self.snapshot.id, form.data['light_cone-snapshot'])
        self.assertEquals(11.3, float(form.data['light_cone-box_size']))
        op_list = form.data['light_cone-output_properties']
        self.assertEquals(2, len(op_list))
        self.assertTrue(self.filter.id in op_list)
        self.assertTrue(self.output_prop.id in op_list)


