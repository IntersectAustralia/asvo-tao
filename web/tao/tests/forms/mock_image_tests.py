from lxml.html import document_fromstring as fromstring
from lxml.cssselect import CSSSelector as css
from django.test import TestCase
from tao.ui_modules import UIModulesHolder
from taoui_mock_image.forms import Form, SingleForm
from tao.xml_util import create_root, child_element
from tao.tests.support.factories import SimulationFactory, GalaxyModelFactory, DataSetFactory, BandPassFilterFactory
from tao.xml_util import xml_print, xml_parse

##
## Test server responses.
##
class ResponseTestCase(TestCase):
    fixtures = ['sample.json']

    def test_form_in_response(self):
        code, html = self.get_html()
        self.assertTrue(code, 200)
        self.assertTrue(css('.id_mock_image-apply_mock_image')(html))
        self.assertTrue(css('#mock_image_params')(html))

    def test_one_sub_form_in_response(self):
        code, html = self.get_html()
        self.assertTrue(code, 200)
        self.assertTrue(css('#single_form_template')(html))

    def setUp(self):
        self.uih = UIModulesHolder(UIModulesHolder.POST)
        self.mi = Form(self.uih)
        self.client.login(username='test', password='test')

    def tearDown(self):
        pass

    def get_html(self):
        resp = self.client.get('/mock_galaxy_factory/')
        return (resp.status_code, fromstring(resp.content))

    def post_html(self, data={}):
        resp = self.client.post('/mock_galaxy_factory/', data)
        return (resp.status_code, fromstring(resp.content))

##
## Test form specifics.
##    
class FormTestCase(TestCase):

    def setUp(self):
        simulation = SimulationFactory.create()
        galaxy_model = GalaxyModelFactory.create()
        dataset = DataSetFactory.create(simulation=simulation, galaxy_model=galaxy_model, max_job_box_count=11)
        BandPassFilterFactory.create()
        self.uih = UIModulesHolder(UIModulesHolder.POST)
        self.prefix = 'mock_image'
        self.mgmt_data = {
            'mock_image-apply_mock_image': True,
            'mock_image-TOTAL_FORMS': 1,
            'mock_image-INITIAL_FORMS': 1,
            'mock_image-MAX_NUM_FORMS': 1000,
            ## 'mock_image-0-sub_cone': 'blah',
        }
        form = SingleForm()
        self.fields = [f.name for f in form]

    def test_no_forms(self):
        form = Form(self.uih, {
            'mock_image-apply_mock_image': True,
            'mock_image-TOTAL_FORMS': 1,
            'mock_image-INITIAL_FORMS': 0,
            'mock_image-MAX_NUM_FORMS': 1000
        }, prefix=self.prefix)
        self.assertFalse(form.is_valid(), msg='Must not accept zero forms.')
        form = Form(self.uih, {
            'mock_image-apply_mock_image': True,
            'mock_image-TOTAL_FORMS': 0,
            'mock_image-INITIAL_FORMS': 0,
            'mock_image-MAX_NUM_FORMS': 1000
        }, prefix=self.prefix)
        self.assertFalse(form.is_valid(), msg='Must not accept zero forms.')

    def test_missing_sub_forms(self):
        form = Form(self.uih, self.mgmt_data, prefix=self.prefix)
        self.assertEqual(1, form.total_form_count())
        self.assertFalse(form.is_valid(), msg='Empty form is not accepted')

    def test_missing_field(self):
        sf = SingleForm()
        for field in self.fields:
            if not sf.fields[field].required: continue
            data = dict(self.mgmt_data.items() + self.make_sub_form_data(0).items())
            del data['mock_image-0-' + field]
            form = Form(self.uih, data, prefix=self.prefix)
            self.assertFalse(form.is_valid(), field + ' is required')
            self.assertTrue(field in form.errors[0], field + ' not in error')

    def test_missing_apply_check(self):
        data = dict(self.mgmt_data.items() + self.make_sub_form_data(0).items())
        del data['mock_image-apply_mock_image']
        Form(self.uih, data, prefix=self.prefix)
        self.assertRaises(lambda: Form(self.uih, data, prefix=self.prefix))

    def test_to_xml_single_form(self):
        data = dict(self.mgmt_data.items() + self.make_sub_form_data(0).items())
        form = Form(self.uih, data, prefix=self.prefix)
        self.assertTrue(form.is_valid())
        root = create_root('root')
        form.to_xml(root)
        self.assertTrue(css('skymaker[id="6"]')(root))
        self.assertTrue(css('skymaker module-version')(root))
        self.assertTrue(css('skymaker module-version')(root))
        self.assertTrue(css('skymaker parents item')(root))
        self.assertEqual(len(css('skymaker images item')(root)), 1)

    def test_to_xml_multi_form(self):
        data = dict(self.make_mgmt_data(2).items() + self.make_sub_form_data(0).items() + self.make_sub_form_data(1).items())
        form = Form(self.uih, data, prefix=self.prefix)
        self.assertTrue(form.is_valid())
        root = create_root('root')
        form.to_xml(root)
        self.assertTrue(css('skymaker[id="6"]')(root))
        self.assertTrue(css('skymaker module-version')(root))
        self.assertTrue(css('skymaker module-version')(root))
        self.assertTrue(css('skymaker parents item')(root))
        self.assertEqual(len(css('skymaker images item')(root)), 2)

    def test_from_xml_multi_form(self):
        data = dict(self.make_mgmt_data(2).items() + self.make_sub_form_data(0).items() + self.make_sub_form_data(1).items())
        form = Form(self.uih, data, prefix=self.prefix)
        self.assertTrue(form.is_valid())
        root = create_root('tao', xmlns='http://tao.asvo.org.au/schema/module-parameters-v1')
        work = child_element(root, 'workflow')
        child_element(work, 'schema-version', '2.0')
        form.to_xml(work)
        root = xml_parse(xml_print(root)) ## do this to recover namespace info not explicit above
        form = Form.from_xml(self.uih, root, self.prefix)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.total_form_count(), 2, msg='Must create extra form.')

    def make_mgmt_data(self, total):
        data = dict(self.mgmt_data)
        data['mock_image-TOTAL_FORMS'] = total
        data['mock_image-INITIAL_FORMS'] = total
        return data

    def make_sub_form_data(self, idx):
        data = {}
        for field in self.fields:
            if field == 'sub_cone':
                val = 'ALL'
            elif field == 'mag_field':
                val = '1_apparent'
            elif field == 'format':
                val = 'FITS'
            else:
                val = 0
            data[self.prefix + '-' + str(idx) + '-' + field] = val
        return data
