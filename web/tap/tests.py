import base64
from django.test import TestCase
from django.test.client import Client
from tao import models
from tao.tests.support.factories import UserFactory


class TapServerTests(TestCase):

    def setUp(self):
        super(TapServerTests, self).setUp()
        
        self.username = 'user'
        self.password = 'password'
        
        self.query = {'QUERY':'select 1'}

        self.user = UserFactory.create(username=self.username)
        self.user.set_password(self.password)
        self.user.save()
        
        self.client = Client()

    def http_auth(self, username, password):
        credentials = base64.b64encode('%s:%s' % (username, password)).strip()
        auth_string = 'Basic %s' % credentials
        return auth_string

    def test_anonymous_access(self):
        if 'HTTP_AUTHORIZATION' in self.client.defaults:
            del self.client.defaults['HTTP_AUTHORIZATION']
        response = self.client.post('/tap/sync', self.query)
        self.assertEqual(response.status_code, 401)
        
    def test_empty_query(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = self.http_auth(self.username, self.password)
        response = self.client.post('/tap/sync')
        self.assertEqual(response.status_code, 400)
        
    #def test_submit(self):
    #    self.client.defaults['HTTP_AUTHORIZATION'] = self.http_auth(self.username, self.password)
    #    response = self.client.post('/tap/sync', self.query)
    #    self.assertEqual(response.status_code, 200)
    
class SQLParsingTests(TestCase):
    
    def setUp(self):
        super(SQLParsingTests, self).setUp()
        
        
        