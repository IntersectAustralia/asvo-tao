from selenium.webdriver.firefox.webdriver import WebDriver

import django.test

import re

def wait():
    import time
    time.sleep(1)

def interact(local):
    """
        drop into an interactive shell - can be helpful for debugging
        call like interact(locals())
    """
    import code
    code.interact(local=local)


class LiveServerTest(django.test.LiveServerTestCase):
    def setUp(self):
        self.selenium = WebDriver()
        
    def tearDown(self):
        self.selenium.quit()
        
    def assert_email_body_contains(self, email, text):
        pattern = re.escape(text)
        matches = re.search(pattern, email.body)
        self.assertTrue(matches, "Email does not contain " + text)
        
    def assert_page_has_content(self, string):
        page_source = self.selenium.page_source

        pattern = re.escape(string)
        self.assertTrue(re.search(pattern, page_source), "page source did not contain %s" % pattern)

    def fill_in_fields(self, field_data):
        for field_id, text_to_input in field_data.items():
            self.selenium.find_element_by_id(field_id).send_keys(text_to_input)
            
    def login(self, username, password):
        self.visit('login')

        username_input = self.selenium.find_element_by_id('id_username')
        password_input = self.selenium.find_element_by_id('id_password')
        submit_button = self.selenium.find_element_by_tag_name('button')  # TODO make this more specific

        username_input.send_keys(username)
        password_input.send_keys(password)

        submit_button.submit()
        
    def visit(self, url_name):
        """ self.visit(name_of_url_as_defined_in_your_urlconf) """
        self.selenium.get(self.get_full_url(url_name))
        
    def get_full_url(self, url_name):
        from django.core.urlresolvers import reverse
        return "%s%s" % (self.live_server_url, reverse(url_name))