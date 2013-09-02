from django.test.testcases import TransactionTestCase

from tao.tests.support.factories import SimulationFactory, GalaxyModelFactory, DataSetFactory, DataSetPropertyFactory, SnapshotFactory
from tao.models import DataSetProperty

class DatasetTestCase(TransactionTestCase):

    def setUp(self):
        super(DatasetTestCase, self).setUp()

    def tearDown(self):
        super(DatasetTestCase, self).tearDown()

    def test_dark_matter_simulation_choices(self):
        from tao.datasets import dark_matter_simulation_choices
        self.assertEqual([], dark_matter_simulation_choices())

        SimulationFactory.create(id=1, name='sim', order='2')
        SimulationFactory.create(id=2, name='a sim', order='1')

        # should be ordered by name
        self.assertEqual([
                (2, u'a sim', {}),
                (1, u'sim', {}),
            ],
            dark_matter_simulation_choices()
        )

    # TODO: Currently this logic is largely done client
    # side in the UI, so this test should probably be ported
    # to a javascript testing framework
    def test_galaxy_model_choices(self):
        from tao.datasets import galaxy_model_choices
        self.assertEqual(0, len(galaxy_model_choices(1)))

        s1 = SimulationFactory.create(id=1)
        s2 = SimulationFactory.create(id=2)

        g1 = GalaxyModelFactory.create(id=1, name='boo')
        g2 = GalaxyModelFactory.create(id=2, name='aoo')
        g3 = GalaxyModelFactory.create(id=3, name='coo')

        DataSetFactory.create(simulation=s1, galaxy_model=g1)
        DataSetFactory.create(simulation=s2, galaxy_model=g2)
        DataSetFactory.create(simulation=s1, galaxy_model=g3)

        self.assertEqual([
               (2, u'aoo', {}),
               (1, u'boo', {}),
               (3, u'coo', {})
           ],
           galaxy_model_choices(s1.id))

    def test_filter_choices(self):
        from tao.datasets import filter_choices

        s1 = SimulationFactory.create()
        s2 = SimulationFactory.create()
        
        g1 = GalaxyModelFactory.create()
        g3 = GalaxyModelFactory.create()
        
        d1 = DataSetFactory.create(simulation=s1, galaxy_model=g3)
        d2 = DataSetFactory.create(simulation=s2, galaxy_model=g1)

        dp1 = DataSetPropertyFactory.create(dataset=d1, units='dp1u')
        dp2 = DataSetPropertyFactory.create(dataset=d2, units='dp2u')
        dp3 = DataSetPropertyFactory.create(dataset=d2, units='dp3u')
        DataSetPropertyFactory.create(dataset=d2, units='', data_type = DataSetProperty.TYPE_STRING)

        galaxies = [g1, g3]

        filtered1 = [filter_choices(s1.id, g.id) for g in galaxies]
        filtered1 = [val for galaxies in filtered1 for val in galaxies]

        self.assertEqual([dp1.id],[x.id for x in filtered1])

        filtered2 = [filter_choices(s2.id, g.id) for g in galaxies]
        filtered2 = [val for galaxies in filtered2 for val in galaxies]

        self.assertEqual([dp2.id,dp3.id],[x.id for x in filtered2])

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
        snapshot3 = SnapshotFactory.create(dataset=d2, redshift='0.3')
        snapshot4 = SnapshotFactory.create(dataset=d3, redshift='0.123')
        snapshot5 = SnapshotFactory.create(dataset=d3, redshift='0.012')
        snapshot6 = SnapshotFactory.create(dataset=d3, redshift='0.3')

        self.assertEqual([
                          (snapshot1.id, snapshot1.redshift, {}),
                          ],
                         snapshot_choices(d1.id))

        self.assertEqual([
                          (snapshot2.id, snapshot2.redshift, {}),
                          (snapshot3.id, snapshot3.redshift, {}),
                          ],
                         snapshot_choices(d2.id))

        self.assertEqual([
                          (snapshot5.id, snapshot5.redshift, {}),
                          (snapshot4.id, snapshot4.redshift, {}),
                          (snapshot6.id, snapshot6.redshift, {})
                          ],
                         snapshot_choices(d3.id))
