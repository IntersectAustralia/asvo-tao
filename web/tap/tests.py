import base64
from tap.parser import *
from django.test import TestCase
from django.test.client import Client
from tao import models
from tao.tests.support.factories import UserFactory, SimulationFactory, GalaxyModelFactory, DataSetFactory, DataSetPropertyFactory


class TAPServicesTests(TestCase):
    
    def setUp(self):
        super(TAPServicesTests, self).setUp()
        
        self.username = 'user'
        self.password = 'password'
        
        self.query = {'QUERY':'select property_name from dataset_name where property_name > 0 and property_name < 10 limit 0,100',
                      'REQUEST': 'doQuery'}

        self.user = UserFactory.create(username=self.username)
        self.user.set_password(self.password)
        self.user.save()
        
        self.dataset = {'name': u'dataset_name', 'label': u'dataset_label'}
        self.property = {'name': u'property_name', 'label': u'property_label', 'units': u'property_units'}
        sim = SimulationFactory.create()
        gal = GalaxyModelFactory.create(id=1, name='gm')
        dat = DataSetFactory.create(simulation=sim, galaxy_model=gal, database=self.dataset['name'])
        DataSetPropertyFactory.create(dataset=dat, name=self.property['name'], label=self.property['label'], units=self.property['units'])
        
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
        
#     def test_sync_submit(self):
#         self.client.defaults['HTTP_AUTHORIZATION'] = self.http_auth(self.username, self.password)
#         response = self.client.post('/tap/sync', self.query)
#         self.assertEqual(response.status_code, 200)
           
    def test_async_submit(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = self.http_auth(self.username, self.password)
        response = self.client.post('/tap/async', self.query)
        self.assertEqual(response.status_code, 303)
        jobs = models.Job.objects.all()
        self.assertEqual(jobs[0].user, self.user)
        
    def test_async_delete(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = self.http_auth(self.username, self.password)
        job = models.Job(user=self.user, status=models.Job.SUBMITTED)
        job.save()
        response = self.client.delete('/tap/async/%s' % job.id)
        models.Job.objects.update()
        job = models.Job.objects.get(id=job.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(job.status, models.Job.ERROR)
        
    def test_dataset_name_parsing(self):
        query = 'select * from %s %s' % (self.dataset['name'], self.dataset['label'])
        self.assertEqual(parse_dataset_name(query), self.dataset)
        
    def test_fields_parsing(self):
        fields = [{'value': '1', 'label': '1', 'units': ''},
                  {'value': self.property['name'], 'label': self.property['label'], 'units': self.property['units']}] 
        query = 'select %s, %s from %s' % (fields[0]['value'], fields[1]['value'], self.dataset['name'])
        self.assertEqual(parse_fields(query, self.dataset), fields)
        
    def test_conditions_parsing(self):
        conditions = [self.property['name'] + ' > 0.1', self.property['name'] + ' < 10']
        query = 'select * from %s where %s' % (self.dataset['name'], ' and '.join(conditions))
        self.assertEqual(parse_conditions(query), conditions)
        
    def test_order_parsing(self):
        order = self.property['name'] + ' desc' 
        query = 'select * from %s order by %s' % (self.dataset['name'], order)
        self.assertEqual(parse_order(query), order)
        
    def test_limit_parsing(self):
        limit = '10,20' 
        query = 'select * from %s limit %s' % (self.dataset['name'], limit)
        self.assertEqual(parse_limit(query), limit)
    
    
    
    