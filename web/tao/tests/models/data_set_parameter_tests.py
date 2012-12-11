from django.test.testcases import TestCase
from tao.tests.support.factories import DataSetParameterFactory

class DataSetParameterCase(TestCase):
    def test_option_label(self):
        param = DataSetParameterFactory.build(name='name', units='units', label='label')
        self.assertEqual('label (units)', param.option_label())
