from django.test.testcases import TransactionTestCase

from tao.tests.support.factories import SimulationFactory, GalaxyModelFactory, DataSetFactory, DataSetParameterFactory

class DatasetTestCase(TransactionTestCase):


    def test_dark_matter_simulation_choices(self):
        from tao.datasets import dark_matter_simulation_choices
        self.assertEqual([], dark_matter_simulation_choices())

        SimulationFactory.create(id=1, name='sim')
        SimulationFactory.create(id=2, name='a sim')

        # should be ordered by name
        self.assertEqual([
                (2, u'a sim', {}),
                (1, u'sim', {}),
            ],
            dark_matter_simulation_choices()
        )

    def test_galaxy_model_choices(self):
        from tao.datasets import galaxy_model_choices
        self.assertEqual(0, len(galaxy_model_choices()))

        s1 = SimulationFactory.create()
        s2 = SimulationFactory.create()

        GalaxyModelFactory.create(simulation=s1, id=1, name='boo')
        GalaxyModelFactory.create(simulation=s2, id=2, name='aoo')
        GalaxyModelFactory.create(simulation=s1, id=3, name='coo')

        self.assertEqual([
               (2, u'aoo', {'data-simulation_id': u'2'}),
               (1, u'boo', {'data-simulation_id': u'1'}),
               (3, u'coo', {'data-simulation_id': u'1'})
           ],
           galaxy_model_choices())

    def test_filter_choices(self):
        from tao.datasets import filter_choices
        self.assertEqual(1, len(filter_choices()))
        
        s1 = SimulationFactory.create()
        s2 = SimulationFactory.create()
        
        g1 = GalaxyModelFactory.create(simulation=s1)
        g2 = GalaxyModelFactory.create(simulation=s2)
        g3 = GalaxyModelFactory.create(simulation=s1)
        
        d1 = DataSetFactory.create(simulation=s1, galaxy_model=g3)
        d2 = DataSetFactory.create(simulation=s2, galaxy_model=g1)
        d3 = DataSetFactory.create(simulation=s2, galaxy_model=g2)
        
        dp1 = DataSetParameterFactory.create(dataset=d1)
        dp2 = DataSetParameterFactory.create(dataset=d2)
        dp3 = DataSetParameterFactory.create(dataset=d3)
        
        self.assertEqual([
                          ('no_filter', 'No Filter', {}),
                          (dp1.id, dp1.name, {'data-simulation_id': unicode(s1.id), 'data-galaxy_model_id': unicode(g3.id)}),
                          (dp2.id, dp2.name, {'data-simulation_id': unicode(s2.id), 'data-galaxy_model_id': unicode(g1.id)}),
                          (dp3.id, dp3.name, {'data-simulation_id': unicode(s2.id), 'data-galaxy_model_id': unicode(g2.id)})
                          ], 
                         filter_choices())