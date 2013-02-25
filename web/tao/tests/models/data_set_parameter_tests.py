from django.test.testcases import TestCase
from tao.tests.support.factories import DataSetPropertyFactory

class DataSetParameterCase(TestCase):
    def test_option_label(self):
        param = DataSetPropertyFactory.build(name='name', units='units', label='label')
        self.assertEqual('name (units)', param.option_label())
