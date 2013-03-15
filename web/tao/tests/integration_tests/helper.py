from django.core.urlresolvers import reverse

from selenium.webdriver.firefox.webdriver import WebDriver

import django.test

import re, os
import tao.datasets as datasets
from tao.models import DataSetProperty, BandPassFilter
from tao.forms import NO_FILTER
from tao.settings import MODULE_INDICES

def wait(secs=1):
    import time
    time.sleep(secs)

def interact(local):
    """
        drop into an interactive shell - can be helpful for debugging
        call like interact(local=locals())
    """
    import code
    code.interact(local=local)
    
def visit(client, view_name, *args, **kwargs):
    return client.get(reverse(view_name, args=args), follow=True)
    
class LiveServerTest(django.test.LiveServerTestCase):
    DOWNLOAD_DIRECTORY = '/tmp/work/downloads'

    ## List all ajax enabled pages that have initialization code and must wait
    AJAX_WAIT = ['mock_galaxy_factory']
    SUMMARY_INDEX = str(len(MODULE_INDICES)+1)

    def setUp(self):
        from selenium.webdriver.firefox.webdriver import FirefoxProfile
        fp = FirefoxProfile()
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.dir", self.DOWNLOAD_DIRECTORY)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/html, application/zip")
        
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

    def sed_id(self, bare_field):
        return 'id_sed-%s' % bare_field

    def sed_css(self, bare_field):
        return '#%s' % self.sed_id(bare_field)

    def sed_2select(self, bare_field):
        return 'id_sed-band_pass_filters_%s' % bare_field

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

    def get_summary_field(self, form_name, field_name):
        summary_selector = 'div.summary_%s .%s' % (form_name, field_name)
        return self.selenium.find_element_by_css_selector(summary_selector)

    def get_summary_field_text(self, form_name, field_name):
        return self.get_summary_field(form_name, field_name).text

    def get_info_field(self, section, field):
        elem = self.selenium.find_element_by_css_selector("div.%(section)s-info .%(field)s" % {'section': section, 'field': field})
        return elem.text

    def assert_email_body_contains(self, email, text):
        pattern = re.escape(text)
        matches = re.search(pattern, email.body)
        self.assertTrue(matches, "Email does not contain " + text)
        
    def assert_page_has_content(self, string):
        page_source = self.selenium.page_source

        pattern = re.escape(string)
        self.assertTrue(re.search(pattern, page_source), "page source did not contain %s" % pattern)
        
    def assert_page_does_not_contain(self, string):
        page_source = self.selenium.page_source
        
        pattern = re.escape(string)
        self.assertFalse(re.search(pattern, page_source), "page source contained %s" % pattern)
        
    def assert_element_text_equals(self, selector, expected_value):
        element = self.find_visible_element(selector)
        self.assertEqual(expected_value, element.text)

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

    def assert_are_not_displayed(self, name):
        fields = self.selenium.find_elements_by_name(name)
        self.assertFalse(all([field.is_displayed() for field in fields]))

    def assert_is_displayed(self, selector):
        field = self.selenium.find_element_by_css_selector(selector)
        self.assertTrue(field.is_displayed())
        
    def assert_not_displayed(self, selector):
        field = self.selenium.find_element_by_css_selector(selector)
        self.assertFalse(field.is_displayed())
        
    def assert_on_page(self, url_name, ignore_query_string=False):
        if not ignore_query_string:
            self.assertEqual(self.selenium.current_url, self.get_full_url(url_name))
        else:
            split_url = self.selenium.current_url.split('?')
            url = split_url[0]
            self.assertEqual(url, self.get_full_url(url_name))
            
    def fill_in_fields(self, field_data, id_wrap=None):
        for selector, text_to_input in field_data.items():
            if id_wrap:
                selector = id_wrap(selector)
            elem = self.selenium.find_element_by_css_selector(selector)
            if elem.tag_name == 'select':
                self.select(selector, str(text_to_input))
            else:
                elem.send_keys(str(text_to_input))

    def click(self, elem_id):
        elem = self.selenium.find_element_by_id(elem_id)
        elem.click()
        wait(0.5)

    def click_by_css(self, element_css):
        elem = self.selenium.find_element_by_css_selector(element_css)
        elem.click()
        wait(0.5)
            
    def login(self, username, password):
        self.visit('login')

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
            wait(1)
        
    def get_actual_filter_options(self):
        option_selector = '%s option' % self.rf_id('filter')
        return [x.get_attribute('value').encode('ascii') for x in self.selenium.find_elements_by_css_selector(option_selector)]
    
    def get_expected_filter_options(self, data_set_id):
        normal_parameters = datasets.filter_choices(data_set_id)
        bandpass_parameters = datasets.band_pass_filters_objects()
        return ['X-' + NO_FILTER] + ['D-' + str(x.id) for x in normal_parameters] + ['B-' + str(x.id) for x in bandpass_parameters]

    def get_actual_snapshot_options(self):
        option_selector = '%s option' % self.lc_id('snapshot')
        return [x.get_attribute("innerHTML") for x in self.selenium.find_elements_by_css_selector(option_selector)]

    def get_expected_snapshot_options(self, snapshots):
        return [str("%.5g" % snapshot.redshift) for snapshot in snapshots]
        
    def get_full_url(self, url_name, *args, **kwargs):
        return "%s%s" % (self.live_server_url, reverse(url_name, args=args, kwargs=kwargs))
    
    def get_selected_option_text(self, id_of_select):
        select = self.selenium.find_element_by_css_selector(id_of_select)
        options = select.find_elements_by_css_selector('option')
        selected_option = None
        for option in options:
            if option.get_attribute('selected'):
                selected_option = option
        return selected_option.text      
        
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
        wait(0.5)
        
    def select_galaxy_model(self, galaxy_model):
        self.select(self.lc_id('galaxy_model'), galaxy_model.name)
        wait(0.5)

    def select_record_filter(self, filter):
        text = ''
        if isinstance(filter, DataSetProperty):
            units_str = ''
            if filter.units is not None and len(filter.units) > 0:
                units_str = ' (' + filter.units + ')'
            text = filter.label + units_str
        elif isinstance(filter, BandPassFilter):
            text = filter.label
        else:
            raise TypeError("Unknown filter type")
        self.select(self.rf_id('filter'), text)
        
    #a function to make a list of list of text inside the table
    def table_as_text_rows(self, selector):
        table = self.selenium.find_element_by_css_selector(selector)
        rows = table.find_elements_by_css_selector('tr')
        cells = [[cell.text for cell in row.find_elements_by_css_selector('th, td')] for row in rows]
        return cells
        
class LiveServerMGFTest(LiveServerTest):
    def submit_mgf_form(self):
        submit_button = self.selenium.find_element_by_css_selector('#mgf-form input[type="submit"]')
        submit_button.submit()
        wait(1)

    def assert_errors_on_field(self, what, field_id):
        field_elem = self.selenium.find_element_by_css_selector(field_id)
        div_container = self.get_closest_by_class(field_elem, 'control-group')
        self.assertEquals(what, 'error' in self.get_element_css_classes(div_container))

