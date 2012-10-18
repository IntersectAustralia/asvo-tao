from selenium.webdriver.firefox.webdriver import WebDriver

import django.test

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
    def assert_page_has_content(self, string):
        import re

        page_source = self.selenium.page_source

        pattern = re.escape(string)
        self.assertTrue(re.search(pattern, page_source), "page source did not contain %s" % pattern)

    def login(self, username, password):
        self.visit('login')

        username_input = self.selenium.find_element_by_id('id_username')
        password_input = self.selenium.find_element_by_id('id_password')
        submit_button = self.selenium.find_element_by_tag_name('button')  # TODO make this more specific

        username_input.send_keys(username)
        password_input.send_keys(password)

        submit_button.submit()
    
    def setUp(self):
        self.selenium = WebDriver()
        
    def tearDown(self):
        self.selenium.quit()
        
    def visit(self, url_name):
        """ self.visit(name_of_url_as_defined_in_your_urlconf) """
        from django.core.urlresolvers import reverse
        self.selenium.get("%s%s" % (self.live_server_url, reverse(url_name)))