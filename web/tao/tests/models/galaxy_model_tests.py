from django.db import IntegrityError
from django.test.testcases import TestCase

from tao.models import GalaxyModel

from tao.tests.support.factories import GalaxyModelFactory


class GalaxyModelTest(TestCase):
    def test_name_must_be_unique(self):
        name = 'some name'

        model = GalaxyModelFactory.create(name=name)

        model_with_duplicate_name = GalaxyModelFactory.build(name=name, simulation=model.simulation)

        try:
            model_with_duplicate_name.save()
        except IntegrityError as e:
            self.assertEqual('column name is not unique', str(e))
        else:
            self.fail("name should be validated as unique")
