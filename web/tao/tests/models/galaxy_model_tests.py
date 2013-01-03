from django.db import IntegrityError
from django.test.testcases import TestCase

from tao.models import GalaxyModel

from tao.tests.support.factories import GalaxyModelFactory


class GalaxyModelTest(TestCase):
    def test_name_must_be_unique(self):
        name = 'some name'

        model = GalaxyModelFactory.create(name=name)

        model_with_duplicate_name = GalaxyModelFactory.build(name=name)

        try:
            model_with_duplicate_name.save()
        except IntegrityError as e:
            self.assertEqual('column name is not unique', str(e))
        else:
            self.fail("name should be validated as unique")

    def test_name_must_be_unique_ignoring_leading_or_trailing_whitespace(self):
        name = 'some name'
        spaced_name = ' %s ' % name

        model = GalaxyModelFactory.create(name=name)

        model_with_duplicate_spaced_name = GalaxyModelFactory.build(name=spaced_name)

        try:
            model_with_duplicate_spaced_name.save()
        except IntegrityError as e:
            self.assertEqual('column name is not unique', str(e))
        else:
            self.fail("name should be validated as unique")
