from django.test.testcases import TestCase

from tao.datasets import dark_matter_simulation_choices, galaxy_model_choices
from tao.models import GalaxyModel, Simulation


class DatasetTestCase(TestCase):
    def test_dark_matter_simulation_choices(self):
        self.assertEqual([], dark_matter_simulation_choices())

        Simulation(id=1, name='sim').save()
        Simulation(id=2, name='a sim').save()

        # should be ordered by name
        self.assertEqual([(2, 'a sim'), (1, 'sim')], dark_matter_simulation_choices())

    def test_galaxy_model_choices(self):
        self.assertEqual(0, len(galaxy_model_choices()))

        s = Simulation(id=1, name='sim')
        s.save()

        GalaxyModel(simulation=s, id=1, name='boo').save()
        GalaxyModel(simulation=s, id=2, name='aoo').save()
        GalaxyModel(simulation=s, id=3, name='coo').save()

        self.assertEqual([(2, 'aoo'), (1, 'boo'), (3, 'coo')], galaxy_model_choices())
