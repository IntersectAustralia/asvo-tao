"""
Tests:

1. The number of Galaxies in Catalogue 0 matches the expected number (optional)
2. The galaxy coordinates are within the simulation space
"""
import logging

from tao_validate import ValidateJob

logger = logging.getLogger('detest.'+__name__)

class Validator(ValidateJob):

    def __init__(self):
        self.doc = __doc__
        super(Validator, self).__init__()

    def validate(self, args, job_params):
        super(Validator, self).validate(args, job_params)
        
        self.cat0 = self.load_csv(0)

        self.check_galaxy_count()
        self.check_basic_stats()
        logger.info("Finished Box Basic Checks.")
        return


    def check_galaxy_count(self):
        "Check the number of galaxies in the catalogue"

        if self.job_params.GALAXY_COUNT is None:
            logger.info("Skipping galaxy count check")
            return

        logger.info("Checking galaxy count")
        self.assert_true(len(self.cat0) == self.job_params.GALAXY_COUNT,
            "Galaxy counts don't match: got {0}, expected {1}".format(
                len(self.cat0), self.job_params.GALAXY_COUNT))


    def check_basic_stats(self):
        "Check that the galaxy coordinates are within expectations"
        min_range = self.job_params.COORDINATE_MIN_RANGE
        max_range = self.job_params.COORDINATE_MAX_RANGE
        for coordinate in ['x', 'y', 'z']:
            stats = self.cat0[coordinate].describe()
            self._check_range(coordinate, stats['min'], min_range)
            self._check_range(coordinate, stats['max'], max_range)
        return


    def _check_range(self, coordinate, val, range):
            self.assert_true(val >= range[0],
                "min {c}: {v} < {e}".format(
                        c=coordinate,
                        v=val,
                        e=range[0]))
            self.assert_true(val <= range[1],
                "min {c}: {v} > {e}".format(
                        c=coordinate,
                        v=val,
                        e=range[1]))
            return
