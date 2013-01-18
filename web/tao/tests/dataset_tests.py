from django.test.testcases import TransactionTestCase

from tao.tests.support.factories import SimulationFactory, GalaxyModelFactory, DataSetFactory, DataSetPropertyFactory, SnapshotFactory

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

        g1 = GalaxyModelFactory.create(id=1, name='boo')
        g2 = GalaxyModelFactory.create(id=2, name='aoo')
        g3 = GalaxyModelFactory.create(id=3, name='coo')

        DataSetFactory.create(simulation=s1, galaxy_model=g1)
        DataSetFactory.create(simulation=s2, galaxy_model=g2)
        DataSetFactory.create(simulation=s1, galaxy_model=g3)

        self.assertEqual([
               (2, u'aoo', {'data-galaxy_model_id': u'2'}),
               (1, u'boo', {'data-galaxy_model_id': u'1'}),
               (3, u'coo', {'data-galaxy_model_id': u'3'})
           ],
           galaxy_model_choices())

    def test_filter_choices(self):
        from tao.datasets import filter_choices
        self.assertEqual(1, len(filter_choices()))
        
        s1 = SimulationFactory.create()
        s2 = SimulationFactory.create()
        
        g1 = GalaxyModelFactory.create()
        g2 = GalaxyModelFactory.create()
        g3 = GalaxyModelFactory.create()
        
        d1 = DataSetFactory.create(simulation=s1, galaxy_model=g3)
        d2 = DataSetFactory.create(simulation=s2, galaxy_model=g1)
        d3 = DataSetFactory.create(simulation=s2, galaxy_model=g2)
        
        dp1 = DataSetPropertyFactory.create(dataset=d1, units='dp1u')
        dp2 = DataSetPropertyFactory.create(dataset=d2, units='dp2u')
        dp3 = DataSetPropertyFactory.create(dataset=d3, units='dp3u')
        
        self.assertEqual([
                          ('no_filter', 'No Filter', {}),
                          (dp1.id, '%s (%s)' % (dp1.label, dp1.units), {'data-simulation_id': str(s1.id), 'data-galaxy_model_id': str(g3.id)}),
                          (dp2.id, '%s (%s)' % (dp2.label, dp2.units), {'data-simulation_id': str(s2.id), 'data-galaxy_model_id': str(g1.id)}),
                          (dp3.id, '%s (%s)' % (dp3.label, dp3.units), {'data-simulation_id': str(s2.id), 'data-galaxy_model_id': str(g2.id)})
                          ], 
                         filter_choices())

    def test_snapshot_choices(self):
        from tao.datasets import snapshot_choices

        s1 = SimulationFactory.create()
        s2 = SimulationFactory.create()

        g1 = GalaxyModelFactory.create()
        g2 = GalaxyModelFactory.create()
        g3 = GalaxyModelFactory.create()

        d1 = DataSetFactory.create(simulation=s1, galaxy_model=g3)
        d2 = DataSetFactory.create(simulation=s2, galaxy_model=g1)
        d3 = DataSetFactory.create(simulation=s2, galaxy_model=g2)

        snapshot1 = SnapshotFactory.create(dataset=d1, redshift='0.123')
        snapshot2 = SnapshotFactory.create(dataset=d2, redshift='0.012')
        snapshot3 = SnapshotFactory.create(dataset=d3, redshift='0.3')

        self.assertEqual([
                          (snapshot2.id, snapshot2.redshift, {'data-simulation_id': str(s2.id), 'data-galaxy_model_id': str(g1.id)}),
                          (snapshot1.id, snapshot1.redshift, {'data-simulation_id': str(s1.id), 'data-galaxy_model_id': str(g3.id)}),
                          (snapshot3.id, snapshot3.redshift, {'data-simulation_id': str(s2.id), 'data-galaxy_model_id': str(g2.id)})
                          ],
                         snapshot_choices())
