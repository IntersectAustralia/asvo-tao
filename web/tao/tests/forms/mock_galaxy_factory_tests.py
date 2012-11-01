from django.test.testcases import TransactionTestCase
from tao.tests.support.factories import SimulationFactory, GalaxyModelFactory, DataSetFactory, DataSetParameterFactory

from tao.forms import MockGalaxyFactoryForm

class MockGalaxyFactoryTests(TransactionTestCase):
    
    def setUp(self):
        super(MockGalaxyFactoryTests, self).setUp()
        
        simulation = SimulationFactory.create()
        galaxy_model = GalaxyModelFactory.create(simulation=simulation)
        dataset = DataSetFactory.create(simulation=simulation, galaxy_model=galaxy_model)
        DataSetParameterFactory.create(dataset=dataset)
        
    def make_form(self, values):
        default_values = {
                          'dark_matter_simulation': 1,
                          'galaxy_model': '1',
                          'filter': '1',
                          }
        default_values.update(values)
        return MockGalaxyFactoryForm(default_values)
                
    def test_min_less_than_max_passes(self):
        mock_galaxy_factory_form = self.make_form({'max': '127', 'min': '3'})
        mock_galaxy_factory_form.is_valid()
        
        self.assertEqual({}, mock_galaxy_factory_form.errors)
        self.assertTrue(mock_galaxy_factory_form.is_valid())
        
    def test_rmin_less_than_rmax_passes(self):
        mock_galaxy_factory_form = self.make_form({'rmax': '2', 'rmin': '1.5'})
        mock_galaxy_factory_form.is_valid()
        
        self.assertEqual({}, mock_galaxy_factory_form.errors)
        self.assertTrue(mock_galaxy_factory_form.is_valid())
        
    def test_min_equal_max_fails(self):
        mock_galaxy_factory_form = self.make_form({'max': '3', 'min': '3'})
        
        self.assertFalse(mock_galaxy_factory_form.is_valid())
        self.assertEqual(['The "min" field must be less than the "max" field.'], mock_galaxy_factory_form.errors['min'])
        
    def test_rmin_equal_rmax_fails(self):
        mock_galaxy_factory_form = self.make_form({'rmax': '3', 'rmin': '3'})
        
        self.assertFalse(mock_galaxy_factory_form.is_valid())
        self.assertEqual(['The "Rmin" field must be less than the "Rmax" field.'], mock_galaxy_factory_form.errors['rmin'])
        
    def test_min_greater_than_max_fails(self):
        mock_galaxy_factory_form = self.make_form({'max': '3', 'min': '9'})
        
        self.assertFalse(mock_galaxy_factory_form.is_valid())
        self.assertEqual(['The "min" field must be less than the "max" field.'], mock_galaxy_factory_form.errors['min'])
        
    def test_rmin_greater_than_rmax_fails(self):
        mock_galaxy_factory_form = self.make_form({'rmax': '3', 'rmin': '9'})
        
        self.assertFalse(mock_galaxy_factory_form.is_valid())
        self.assertEqual(['The "Rmin" field must be less than the "Rmax" field.'], mock_galaxy_factory_form.errors['rmin'])
        
    def test_max_or_min_empty_passes(self):
        form_no_min = self.make_form({'max': '3', 'min': ''})
        form_no_max = self.make_form({'max': '', 'min': '9'})
        
        self.assertTrue(form_no_min.is_valid())
        self.assertTrue(form_no_max.is_valid())
        
    def test_rmax_or_rmin_empty_passes(self):
        form_no_min = self.make_form({'rmax': '3', 'rmin': ''})
        form_no_max = self.make_form({'rmax': '', 'rmin': '9'})
        
        self.assertTrue(form_no_min.is_valid())
        self.assertTrue(form_no_max.is_valid())
        
    # check length of any min/max input is less than or equal to 20 characters
    def test_max_min_length(self):
        max_overflow_form = self.make_form({'max': '100000000000000000000', 'min': '7'})
        self.assertFalse(max_overflow_form.is_valid())
        self.assertEqual(['Ensure that there are no more than 20 digits in total.'], max_overflow_form.errors['max'])
        
        min_overflow_form = self.make_form({'max': '2', 'min': '1.000000000000000000001'})
        self.assertFalse(min_overflow_form.is_valid())
        self.assertEqual(['Ensure that there are no more than 20 digits in total.'], min_overflow_form.errors['min'])
        
    def test_rmax_rmin_length(self):
        rmax_overflow_form = self.make_form({'rmax': '123456789012345678901', 'rmin': '7'})
        self.assertFalse(rmax_overflow_form.is_valid())
        self.assertEqual(['Ensure that there are no more than 20 digits in total.'], rmax_overflow_form.errors['rmax'])
        
        rmin_overflow_form = self.make_form({'rmax': '2', 'rmin': '1.0000000000000000000001'})
        self.assertFalse(rmin_overflow_form.is_valid())
        self.assertEqual(['Ensure that there are no more than 20 digits in total.'], rmin_overflow_form.errors['rmin'])