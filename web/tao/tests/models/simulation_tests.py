from django.db import IntegrityError
from django.test.testcases import TestCase

from tao.models import Simulation

from tao.tests.support.factories import SimulationFactory


class SimulationTest(TestCase):
    def test_name_must_be_unique(self):
        name = 'some name'

        SimulationFactory.create(name=name)
        simulation_with_duplicate_name = SimulationFactory.build(name=name)

        try:
            simulation_with_duplicate_name.save()
        except IntegrityError as e:
            self.assertEqual('column name is not unique', str(e))
        else:
            self.fail("name should be validated as unique")
