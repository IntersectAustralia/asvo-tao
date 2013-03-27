from django.test.testcases import TransactionTestCase

import datetime

# from tao import workflow, time
# from tao.forms import OutputFormatForm, RecordFilterForm, NO_FILTER
# from tao.models import Snapshot, DataSetProperty
# from tao.settings import OUTPUT_FORMATS
# from taoui_light_cone.forms import Form as LightConeForm
# from taoui_sed.forms import Form as SEDForm
# from tao.tests.support import stripped_joined_lines
# from tao.tests.support.factories import SimulationFactory, GalaxyModelFactory, DataSetFactory, DataSetPropertyFactory, UserFactory, StellarModelFactory, SnapshotFactory, BandPassFilterFactory
from tao.tests.support.xml import light_cone_xml
from tao.tests.helper import make_form_xml
from tao.forms import OutputFormatForm
from unittest import TestCase
#
# from tao.tests.support import UtcPlusTen
# from tao.tests.helper import MockUIHolder, make_form

class XmlFormsTests(TestCase):

    def setUp(self):
        # super(TestCase, self).setUp()
        pass


    def tearDown(self):
        # super(TestCase, self).tearDown()
        pass

    def test_output_format_form(self):
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
            'dark_matter_simulation': 'DMS', # self.simulation.name,
            'galaxy_model': 'GM', # self.galaxy_model.name,
            'output_properties_1_name' : 'FN', # self.filter.name,
            'output_properties_1_label' : 'FL', # self.filter.label,
            'output_properties_1_units' : 'FU', # self.filter.units,
            'output_properties_2_name' : 'OPN', # self.output_prop.name,
            'output_properties_2_label' : 'OPL', # self.output_prop.label,
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
            'dust_model_name': 'DM', # self.dust_model.name,
            })
        xml_str = light_cone_xml(xml_parameters)
        form = make_form_xml(OutputFormatForm, xml_str, prefix='output_format')
        self.assertEquals('csv', form.data['output_format-supported_formats'])
