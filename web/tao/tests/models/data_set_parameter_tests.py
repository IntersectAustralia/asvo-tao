from django.test.testcases import TestCase
from tao.tests.support.factories import DataSetParameterFactory

class DataSetParameterCase(TestCase):
    def test_label(self):
        param = DataSetParameterFactory.build(name='name', units='units')
        self.assertEqual('name (units)', param.label())
