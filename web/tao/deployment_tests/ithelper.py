from django.core.urlresolvers import reverse
from django.utils.html import strip_tags

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

import django.test

import re, os, time
import tao.datasets as datasets
#from tao.models import DataSetProperty, BandPassFilter, Simulation
from tao.settings import MODULE_INDICES
from tao.tests.helper import TaoModelsCleanUpMixin

def interact(local=locals()):
    """
        drop into an interactive shell - can be helpful for debugging
        call like interact(local=locals())
    """
    import code
    code.interact(local=local)
    
def visit(client, view_name, *args, **kwargs):
    return client.get(reverse(view_name, args=args), follow=True)

class LiveServerTest(object):
    fixtures = ['rules.json']

    DOWNLOAD_DIRECTORY = '/tmp/work/downloads'


    ## List all ajax enabled pages that have initialization code and must wait
    AJAX_WAIT = ['mock_galaxy_factory', 'view_job']
    SUMMARY_INDEX = str(len(MODULE_INDICES)+1)
    OUTPUT_FORMATS = [
        {'value':'csv', 'text':'CSV (Text)', 'extension':'csv'},
        {'value':'hdf5', 'text':'HDF5', 'extension':'hdf5'},
        {'value': 'fits', 'text': 'FITS', 'extension': 'fits'},
        {'value': 'votable', 'text': 'VOTable', 'extension': 'xml'}
    ]

    def wait(self, secs=1):
        time.sleep(secs * 1.0)

    def setUp(self):

        from selenium.webdriver.firefox.webdriver import FirefoxProfile
        fp = FirefoxProfile()
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.dir", self.DOWNLOAD_DIRECTORY)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/html, application/zip, text/plain, application/force-download, application/x-tar")
        
        self.selenium = WebDriver(firefox_profile=fp)
        self.selenium.implicitly_wait(1) # wait one second before failing to find

        # create the download dir
        if not os.path.exists(self.DOWNLOAD_DIRECTORY):
            os.makedirs(self.DOWNLOAD_DIRECTORY)

    def tearDown(self):
        self.selenium.quit()
        # remove the download dir
        for root, dirs, files in os.walk(self.DOWNLOAD_DIRECTORY, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    def lc_id(self, bare_field):
        return '#id_light_cone-%s' % bare_field

    def lc_2select(self, bare_field):
        return 'id_light_cone-output_properties_%s' % bare_field

    def rf_id(self, bare_field):
        return '#id_record_filter-%s' % bare_field

    def sed(self, bare_field):
        return 'id_sed-%s' % bare_field

    def mi_id(self, bare_field):
        return 'id_mock_image-%s' % bare_field

    def sed_id(self, bare_field):
        return '#%s' % self.sed(bare_field)

    def sed_2select(self, bare_field):
        return 'id_sed-band_pass_filters_%s' % bare_field

    def job_select(self, bare_field):
        return 'id-job_%s' % bare_field

    def job_id(self, bare_field):
        return '#%s' % self.job_select(bare_field)

    def get_parent_element(self, element):
        return self.selenium.execute_script('return arguments[0].parentNode;', element)

    def get_element_css_classes(self, element):
        list = []
        found = element.get_attribute('class')
        if found is not None: list = found.split()
        return list

    def get_closest_by_class(self, element, css_class):
        while css_class not in self.get_element_css_classes(element):
            element = self.get_parent_element(element)
        return element

    def get_summary_selector(self, form_name, field_name):
        return 'div.summary_%s .%s' % (form_name, field_name)

    def get_summary_field(self, form_name, field_name):
        summary_selector = self.get_summary_selector(form_name, field_name)
        return self.selenium.find_element_by_css_selector(summary_selector)

    def get_summary_field_text(self, form_name, field_name):
        return self.get_summary_field(form_name, field_name).text

    def get_info_field(self, section, field):
        elem = self.selenium.find_element_by_css_selector("div.%(section)s-info .%(field)s" % {'section': section, 'field': field})
        return elem.text

    def find_element_by_css_selector(self, selector):
        retries = 3
        while retries > 0:
            try:
                elem = self.selenium.find_element_by_css_selector(selector)
                return elem
            except NoSuchElementException:
                retries -= 1
                self.wait(1)
        # If it hasn't been found by now, try one more time and let the exception through
        return self.selenium.find_element_by_css_selector(selector)

    def find_element_by_id(self, elem_id):
        retries = 3
        while retries > 0:
            try:
                elem = self.selenium.find_element_by_id(elem_id)
                return elem
            except NoSuchElementException:
                retries -= 1
                self.wait(1)
        # If it hasn't been found by now, try one more time and let the exception through
        return self.selenium.find_element_by_id(elem_id)

    def assert_email_body_contains(self, email, text):
        pattern = re.escape(text)
        matches = re.search(pattern, email.body)
        self.assertTrue(matches, "Email does not contain " + text)

    def get_page_source(self):
        try:
            return self.selenium.page_source
        except:
            while True:
                self.wait(0.2)
                try:
                    self.selenium.switch_to_alert().accept()
                except:
                    return self.selenium.page_source

    def assertTrue(self, value, msg):
        if not value:
            raise AssertionError(msg)
        return

    def assertEqual(self, vala, valb):
        if vala != valb:
            msg = 'FAIL: "{0}" != "{1}"'.format(vala, valb)
            raise AssertionError(msg)
        return


    def assert_page_has_content(self, string):
        page_source = self.get_page_source()
        pattern = re.escape(string)
        self.assertTrue((string in page_source) or re.search(pattern, page_source), "page source did not contain %s" % pattern)
        
    def assert_page_does_not_contain(self, string):
        page_source = self.get_page_source()
        
        pattern = re.escape(string)
        self.assertFalse(re.search(pattern, page_source), "page source contained %s" % pattern)
        
    def assert_element_text_equals(self, selector, expected_value):
        text = self.find_visible_element(selector).text.strip()
        self.assertEqual(expected_value.strip(), text.strip())

    def assert_element_value_equals(self, selector, expected_value):
        text = self.find_visible_element(selector).get_attribute('value')
        self.assertEqual(expected_value.strip(), text.strip())

    def assert_selector_texts_equals_expected_values(self, selector_value):
        # selector_value is a dict of selectors to expected text values
        for selector, expected_value in selector_value.items():
            self.assert_element_text_equals(selector, unicode(expected_value))
    
    def assert_attribute_equals(self, attribute, selector_values):
        # selector_values is a dict of selectors to attribute values
        for selector, expected_value in selector_values.items():
            element = self.find_visible_element(selector)
            actual_value = element.get_attribute(attribute)
            self.assertEqual(expected_value, actual_value)

    def assert_is_checked(self, selector):
        field = self.selenium.find_element_by_css_selector(selector)
        self.assertEqual('true', field.get_attribute('checked'))

    def assert_is_unchecked(self, selector):
        field = self.selenium.find_element_by_css_selector(selector)
        self.assertIsNone(field.get_attribute('checked'))

    def assert_is_enabled(self, selector):
        field = self.selenium.find_element_by_css_selector(selector)
        self.assertIsNone(field.get_attribute('disabled'))
        
    def assert_is_disabled(self, selector):
        field = self.selenium.find_element_by_css_selector(selector)
        self.assertEqual('true', field.get_attribute('disabled'))

    def assert_are_displayed(self, name):
        fields = self.selenium.find_elements_by_name(name)
        self.assertTrue([field.is_displayed() for field in fields])

    def assert_are_displayed_by_class_name(self, name):
        fields = self.selenium.find_elements_by_class_name(name)
        self.assertTrue([field.is_displayed() for field in fields])

    def assert_are_not_displayed(self, name):
        fields = self.selenium.find_elements_by_name(name)
        self.assertFalse(all([field.is_displayed() for field in fields]))

    def assert_is_displayed(self, selector):
        field = self.selenium.find_element_by_css_selector(selector)
        self.assertTrue(field.is_displayed())
        
    def assert_not_displayed(self, selector):
        field = self.selenium.find_element_by_css_selector(selector)
        self.assertFalse(field.is_displayed())

    def assert_not_in_page(self, selector):
        "Assert that the supplied selector is not part of the page content"
        elements = self.selenium.find_elements_by_css_selector(selector)
        self.assertTrue(len(elements) == 0)

    def assert_on_page(self, url_name, ignore_query_string=False):
        retries = 30
        while retries > 0:
            try:
                self._assert_on_page(url_name, ignore_query_string)
                return
            except AssertionError:
                retries -= 1
                print "assert_on_page: retry"
                self.wait(1)
        self._assert_on_page(url_name, ignore_query_string)

    def _assert_on_page(self, url_name, ignore_query_string=False):
        if not ignore_query_string:
            self.assertEqual(self.selenium.current_url, self.get_full_url(url_name))
        else:
            split_url = self.selenium.current_url.split('?')
            url = split_url[0]
            self.assertEqual(url, self.get_full_url(url_name))

    def assert_multi_selected_text_equals(self, id_of_select, expected):
        actual = self.get_multi_selected_option_text(id_of_select)
        remaining = []
        for value in expected:
            if value not in actual:
                remaining.append(value)
            else:
                actual.remove(value)
        self.assertTrue(not actual and not remaining)

    def assert_summary_field_correctly_shown(self, expected_value, form_name, field_name):
        value_displayed = self.get_summary_field_text(form_name, field_name)
        self.assertEqual(expected_value, strip_tags(value_displayed))

    def fill_in_fields(self, field_data, id_wrap=None, clear=False):
        for selector, text_to_input in field_data.items():
            if id_wrap:
                selector = id_wrap(selector)
            elem = self.selenium.find_element_by_css_selector(selector)
            if elem.tag_name == 'select':
                self.select(selector, str(text_to_input))
            else:
                if clear:
                    elem.clear()
                elem.send_keys(str(text_to_input))
        self.wait(0.5)

    def clear(self, selector):
        elem = self.selenium.find_element_by_css_selector(selector)
        elem.clear()

    def click(self, elem_id):
        elem = self.find_element_by_id(elem_id)
        elem.click()
        self.wait(0.5)

    def click_by_css(self, element_css):
        elem = self.selenium.find_element_by_css_selector(element_css)
        elem.click()
        self.wait(0.5)

    def click_by_class_name(self, class_name):
        elem = self.selenium.find_element_by_class_name(class_name)
        elem.click()
        self.wait(0.5)

    def login(self, username, password):
        self.visit('accounts/login')

        username_input = self.selenium.find_element_by_id('id_username')
        password_input = self.selenium.find_element_by_id('id_password')
        submit_button = self.selenium.find_element_by_tag_name('button')  # TODO make this more specific

        username_input.send_keys(username)
        password_input.send_keys(password)

        submit_button.submit()
        
    def visit(self, url_name, *args, **kwargs):
        """ self.visit(name_of_url_as_defined_in_your_urlconf) """
        self.selenium.get(self.get_full_url(url_name, *args, **kwargs))
        if url_name in LiveServerTest.AJAX_WAIT:
            self.wait(2)
            self.assertTrue(self.selenium.execute_script('return (window.catalogue !== undefined ? catalogue._loaded : true)'),
                            'catalogue.js loading error')

    def get_actual_filter_options(self):
        option_selector = '%s option' % self.rf_id('filter')
        return [x.get_attribute('value').encode('ascii') for x in self.selenium.find_elements_by_css_selector(option_selector)]
    
    def get_expected_filter_options(self, data_set):
        def gen_bp_pairs(objs):
            for obj in objs:
                yield ('B-' + str(obj.id) + '_apparent')
                yield ('B-' + str(obj.id) + '_absolute')
        normal_parameters = datasets.filter_choices(data_set.simulation.id, data_set.galaxy_model.id)
        bandpass_parameters = datasets.band_pass_filters_objects()
        return ['D-' + str(x.id) for x in normal_parameters] + [pair for pair in gen_bp_pairs(bandpass_parameters)]

    def get_actual_snapshot_options(self):
        option_selector = '%s option' % self.lc_id('snapshot')
        return [x.get_attribute("innerHTML") for x in self.selenium.find_elements_by_css_selector(option_selector)]

    def get_expected_snapshot_options(self, snapshots):
        return [str("%.5g" % snapshot.redshift) for snapshot in snapshots]
        
    def get_full_url(self, url_name, *args, **kwargs):
        return "%s%s" % (self.job_params.BASE_URL, url_name)
    
    def get_selected_option_text(self, id_of_select):
        select = self.selenium.find_element_by_css_selector(id_of_select)
        options = select.find_elements_by_css_selector('option')
        selected_option = None
        for option in options:
            if option.get_attribute('selected'):
                selected_option = option
        return selected_option.text

    def get_multi_selected_option_text(self, id_of_select):
        select = self.selenium.find_element_by_css_selector(id_of_select)
        options = select.find_elements_by_css_selector('option')
        return [option.text for option in options]

        
    def get_selector_value(self, selector): 
        return self.selenium.find_element_by_css_selector(selector).get_attribute('value')
    
    def select(self, selector, value):
        from selenium.webdriver.support.ui import Select

        elem = self.selenium.find_element_by_css_selector(selector)
        select = Select(elem)

        select.select_by_visible_text(value)
        
    def find_visible_elements(self, css_selector):
        elements = self.selenium.find_elements_by_css_selector(css_selector)
        return [elem for elem in elements if elem.is_displayed()]
    
    def find_visible_element(self, css_selector):
        elements = self.find_visible_elements(css_selector)
        num_elements = len(elements)
        if num_elements != 1:
            raise Exception("Found %s elements for selector %s" % (num_elements, css_selector))
        return elements[0]
    
    def select_dark_matter_simulation(self, simulation):
        self.select(self.lc_id('dark_matter_simulation'), simulation.name)
        self.wait(0.5)
        
    def select_galaxy_model(self, galaxy_model):
        self.select(self.lc_id('galaxy_model'), galaxy_model.name)
        self.wait(0.5)

    def select_stellar_model(self, stellar_model):
        self.select(self.sed_id('single_stellar_population_model'), stellar_model.label)
        self.wait(0.5)

    def select_record_filter(self, filter, extension=None):
        text = ''
        if isinstance(filter, DataSetProperty):
            units_str = ''
            if filter.units is not None and len(filter.units) > 0:
                units_str = ' (' + filter.units + ')'
            text = filter.label + units_str
        elif isinstance(filter, BandPassFilter):
            text = filter.label
            if extension is not None:
                text += ' (' + extension.capitalize() + ')'
        else:
            raise TypeError("Unknown filter type")
        self.select(self.rf_id('filter'), text)
        
    #a function to make a list of list of text inside the table
    def table_as_text_rows(self, selector):
        table = self.selenium.find_element_by_css_selector(selector)
        rows = table.find_elements_by_css_selector('tr')
        cells = [[cell.text for cell in row.find_elements_by_css_selector('th, td')] for row in rows]
        return cells

    def submit_support_form(self):
        submit_button = self.selenium.find_element_by_css_selector('button[type="submit"]')
        submit_button.submit()

class DeploymentTester(LiveServerTest):
    def submit_mgf_form(self, description=''):
        self.click('tao-tabs-summary_submit')
        #self.click('id-job_description')
        self.fill_in_fields({'#job_description': description},
                            clear=True)
 
        submit_button = self.selenium.find_element_by_css_selector('#mgf-form #form_submit')
        submit_button.click()

    def assert_cant_submit_mgf_form(self):
        self.click('tao-tabs-summary_submit')
        try:
            submit_button = self.selenium.find_element_by_css_selector('#mgf-form #form_submit')
            self.fail('Submit button present')
        except NoSuchElementException:
            pass
        self.selenium.find_element_by_css_selector('#mgf-form #form_errors')

    def assert_errors_on_field(self, what, field_id):
        field_elem = self.selenium.find_element_by_css_selector(field_id)
        div_container = self.get_closest_by_class(field_elem, 'control-group')
        self.assertEquals(what, 'error' in self.get_element_css_classes(div_container))

    def assert_required_on_field(self, what, field_id):
        field_elem = self.selenium.find_element_by_css_selector(field_id)
        div_container = self.get_closest_by_class(field_elem, 'control-group')
        label = div_container.find_element_by_css_selector('label')
        self.assertTrue(label.get_attribute('class').find('error') != -1, '%s label is not in error' % (field_id,))

    def upload_params_file(self, fname):
        self.find_element_by_id('id_job_type-params_file').send_keys(fname)
