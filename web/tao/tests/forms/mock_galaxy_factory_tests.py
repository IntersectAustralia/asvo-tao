from django.test.testcases import TransactionTestCase
from tao.tests.support.factories import SimulationFactory, GalaxyModelFactory, DataSetFactory, DataSetParameterFactory, UserFactory

from tao.forms import MockGalaxyFactoryForm
from tao.models import DataSet

from tao.tests.support import stripped_joined_lines
from tao.tests.support.xml import XmlDiffMixin

class MockGalaxyFactoryTests(TransactionTestCase, XmlDiffMixin):
    
    def setUp(self):
        super(MockGalaxyFactoryTests, self).setUp()
        
        simulation = SimulationFactory.create()
        galaxy_model = GalaxyModelFactory.create(simulation=simulation)
        dataset = DataSetFactory.create(simulation=simulation, galaxy_model=galaxy_model)
        DataSetParameterFactory.create(dataset=dataset)
        self.user = UserFactory.create()
        
    def make_form(self, values):
        default_values = {
                          'box_type': MockGalaxyFactoryForm.CONE,
                          'dark_matter_simulation': 1,
                          'galaxy_model': '1',
                          'filter': '1',
                          'ra_min': '1',
                          'ra_max': '2',
                          'dec_min': '1',
                          'dec_max': '2',
                          }
        default_values.update(values)
        return MockGalaxyFactoryForm(default_values)

    def test_ra_dec_min_max(self):
        mock_galaxy_factory_form = self.make_form({
            'box_type': MockGalaxyFactoryForm.CONE,
            'ra_min': '-182',
            'dec_min': '-92',
            'ra_max': '-181',
            'dec_max': '-91',
        })
        self.assertEqual({
            'ra_min': ['Ensure this value is greater than or equal to -180.'],
            'dec_min': ['Ensure this value is greater than or equal to -90.'],
            'ra_max': ['Ensure this value is greater than or equal to -180.'],
            'dec_max': ['Ensure this value is greater than or equal to -90.'],
        }, mock_galaxy_factory_form.errors)

        mock_galaxy_factory_form = self.make_form({
            'box_type': MockGalaxyFactoryForm.CONE,
            'ra_min': '181',
            'dec_min': '91',
            'ra_max': '182',
            'dec_max': '92',
        })
        self.assertEqual({
            'ra_min': ['Ensure this value is less than or equal to 180.'],
            'dec_min': ['Ensure this value is less than or equal to 90.'],
            'ra_max': ['Ensure this value is less than or equal to 180.'],
            'dec_max': ['Ensure this value is less than or equal to 90.'],
        }, mock_galaxy_factory_form.errors)

    def test_ra_and_dec_min_max(self):
        mock_galaxy_factory_form = self.make_form({
            'box_type': MockGalaxyFactoryForm.CONE,
            'ra_min': '2',
            'dec_min': '1',
            'ra_max': '2',
            'dec_max': '1'
        })
        mock_galaxy_factory_form.is_valid()
        self.assertEqual({
            'ra_min': ['The "RA min" field must be less than the "RA max" field.'],
            'dec_min': ['The "dec min" field must be less than the "dec max" field.'],
        }, mock_galaxy_factory_form.errors)

    def test_ra_dec_required_for_light_cone(self):
        mock_galaxy_factory_form = self.make_form({
            'box_type': MockGalaxyFactoryForm.CONE,
            'ra_min': '',
            'dec_min': '',
            'ra_max': '',
            'dec_max': ''
        })
        mock_galaxy_factory_form.is_valid()

        self.assertEqual({
            'ra_min': ['This field is required.'],
            'ra_max': ['This field is required.'],
            'dec_min': ['This field is required.'],
            'dec_max': ['This field is required.'],
        }, mock_galaxy_factory_form.errors)

    def test_ra_dec_not_required_for_light_box(self):
        mock_galaxy_factory_form = self.make_form({
            'box_type': MockGalaxyFactoryForm.BOX,
            'box_size': 1,
            'ra_min': '',
            'dec_min': '',
            'ra_max': '',
            'dec_max': '',
        })
        mock_galaxy_factory_form.is_valid()

        self.assertEqual({}, mock_galaxy_factory_form.errors)

    def test_box_size_required_for_box(self):
        mock_galaxy_factory_form = self.make_form({'box_type': MockGalaxyFactoryForm.BOX})
        
        self.assertFalse(mock_galaxy_factory_form.is_valid())
        self.assertEqual(['The "Box Size" field is required when "Box" is selected'], mock_galaxy_factory_form.errors['box_size'])
        
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
        
    def test_xml_parameters(self):
        from tao.datasets import NO_FILTER
        database_name = 'sqlite://sfh_bcgs200_full_z0.db'
        database_box_size = 500

        simulation = SimulationFactory.create(box_size=database_box_size, box_size_units='Mpc')
        galaxy_model = GalaxyModelFactory.create()
        dataset = DataSetFactory.create(database=database_name, simulation=simulation, galaxy_model=galaxy_model, box_size=database_box_size)

        filter_parameter = DataSetParameterFactory.create(dataset=dataset)
        filter_min = '0.93'
        filter_max = '3.345'

        ra_min = '1.23'
        ra_max = '2.34'

        dec_min = '12.34'
        dec_max = '32.56'
        rmin = '0.1'

        mgf_form = self.make_form({
                                   'box_type': MockGalaxyFactoryForm.CONE,
                                   'dark_matter_simulation': simulation.id,
                                   'galaxy_model': galaxy_model.id,
                                   'filter': filter_parameter.id,
                                   'min': filter_min,
                                   'max': filter_max,
                                   'ra_min': ra_min,
                                   'ra_max': ra_max,
                                   'dec_min': dec_min,
                                   'dec_max': dec_max,
                                   'rmax': 2.5,
                                   'rmin': 1.5,
                                })

        mgf_form.is_valid()  # trigger validation

        job = mgf_form.save(self.user)

        expected_parameter_xml = stripped_joined_lines("""
            <?xml version="1.0" encoding="utf-8"?>
            <tao timestamp="2012-11-13 13:45:32+1000" version="1.0">

                <workflow name="alpha-light-cone-image">
                    <module name="light-cone">
                        <param name="database">%(database_name)s</param>
                        <param name="schema-version">1.0</param>
                        <param name="query-type">%(light_cone)s</param>
                        <param name="simulation-box-size" units="Mpc">500</param>
                        <param name="ra-min" units="deg">%(ra_min)s</param>
                        <param name="ra-max" units="deg">%(ra_max)s</param>
                        <param name="dec-min" units="deg">%(dec_min)s</param>
                        <param name="dec-max" units="deg">%(dec_max)s</param>
                        <param name="filter-type">%(filter_type)s</param>
                        <param name="filter-min" units="Mpc">%(filter_min)s</param>
                        <param name="filter-max" units="Mpc">%(filter_max)s</param>
                    </module>
                </workflow>
            </tao>
        """ % {
            'database_name': database_name,
            'light_cone': MockGalaxyFactoryForm.CONE,
            'ra_min': ra_min,
            'ra_max': ra_max,
            'dec_min': dec_min,
            'dec_max': dec_max,
            'rmin': rmin,
            'filter_type': filter_parameter.name,
            'filter_min': filter_min,
            'filter_max': filter_max,
        })

        self.assertXmlEqual(expected_parameter_xml, job.parameters)

    def test_xml_parameters_without_filter(self):
        from tao.datasets import NO_FILTER
        database_name = 'sqlite://sfh_bcgs200_full_z0.db'
        database_box_size = 500

        simulation = SimulationFactory.create(box_size=database_box_size, box_size_units='Mpc')
        galaxy_model = GalaxyModelFactory.create()
        dataset = DataSetFactory.create(database=database_name, simulation=simulation, galaxy_model=galaxy_model, box_size=database_box_size)

        ra_min = '1.23'
        ra_max = '2.34'

        dec_min = '12.34'
        dec_max = '32.56'
        rmin = '0.1'

        mgf_form = self.make_form({
                                   'box_type': MockGalaxyFactoryForm.CONE,
                                   'dark_matter_simulation': simulation.id,
                                   'galaxy_model': galaxy_model.id,
                                   'filter': NO_FILTER,
                                   'ra_min': ra_min,
                                   'ra_max': ra_max,
                                   'dec_min': dec_min,
                                   'dec_max': dec_max,
                                   'rmax': 2.5,
                                   'rmin': 1.5
                                })

        mgf_form.is_valid()  # trigger validation

        job = mgf_form.save(self.user)

        expected_parameter_xml = stripped_joined_lines("""
            <?xml version="1.0" encoding="utf-8"?>
            <tao timestamp="2012-11-13 13:45:32+1000" version="1.0">
             
                <workflow name="alpha-light-cone-image">
                    <module name="light-cone">
                        <param name="database">%(database_name)s</param>
                        <param name="schema-version">1.0</param>
                        <param name="query-type">%(light_cone)s</param>
                        <param name="simulation-box-size" units="Mpc">500</param>
                        <param name="ra-min" units="deg">%(ra_min)s</param>
                        <param name="ra-max" units="deg">%(ra_max)s</param>
                        <param name="dec-min" units="deg">%(dec_min)s</param>
                        <param name="dec-max" units="deg">%(dec_max)s</param>
                    </module>
                </workflow>
            </tao>
        """ % {
            'database_name': database_name,
            'light_cone': MockGalaxyFactoryForm.CONE,
            'ra_min': ra_min,
            'ra_max': ra_max,
            'dec_min': dec_min,
            'dec_max': dec_max,
            'rmin': rmin,
        })

        self.assertXmlEqual(expected_parameter_xml, job.parameters)
