from django.test.testcases import TransactionTestCase

from tao.models import GalaxyModel, Simulation

class DatasetTestCase(TransactionTestCase):


    def test_dark_matter_simulation_choices(self):
        from tao.datasets import dark_matter_simulation_choices, galaxy_model_choices
        self.assertEqual([], dark_matter_simulation_choices())

        Simulation(id=1, name='sim').save()
        Simulation(id=2, name='a sim').save()

        # should be ordered by name
        self.assertEqual([
                (2, u'a sim', {}),
                (1, u'sim', {}),
            ],
            dark_matter_simulation_choices()
        )

    def test_galaxy_model_choices(self):
        from tao.datasets import dark_matter_simulation_choices, galaxy_model_choices
        self.assertEqual(0, len(galaxy_model_choices()))

        s1 = Simulation(id=1, name='sim')
        s1.save()

        s2 = Simulation(id=2, name='sim2')
        s2.save()

        GalaxyModel(simulation=s1, id=1, name='boo').save()
        GalaxyModel(simulation=s2, id=2, name='aoo').save()
        GalaxyModel(simulation=s1, id=3, name='coo').save()

        self.assertEqual([
               (2, u'aoo', {'data-simulation_id': u'2'}),
               (1, u'boo', {'data-simulation_id': u'1'}),
               (3, u'coo', {'data-simulation_id': u'1'})
           ],
           galaxy_model_choices())
