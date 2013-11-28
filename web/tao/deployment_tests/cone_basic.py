"""
Tests:

1. Galaxies positions are all within the light-cone geometry
2. The number of Galaxies in Catalogue 0 matches the expected number (optional)
3. The galaxy ids are unique across all light-cones (optional)
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

        self.catalogues = []
        for i in range(self.job_params.NUMBER_OF_CONES):
            self.catalogues.append(self.load_csv(i,
                usecols=['Galaxy_ID', 'Right_Ascension', 'Declination',
                         'Redshift_Cosmological']))
            self.check_geometry(self.catalogues[i])

        self.check_galaxy_count(self.catalogues[0])

        if getattr(self.job_params, 'CHECK_UNIQUE', False):
            logger.info("Checking Galaxy IDs are unique")
            for i in range(self.job_params.NUMBER_OF_CONES-1):
                for j in range(i+1, self.job_params.NUMBER_OF_CONES):
                    logger.debug("Unique Galaxies between catalogues {0} and {1}".format(
                            i, j))
                    self.unique_galaxies(self.catalogues[i], self.catalogues[j])

        logger.info("Finished Cone Basic Checks.")
        return

    def check_galaxy_count(self, cat):
        "Check the number of galaxies in the supplied catalogue"

        if getattr(self.job_params, 'GALAXY_COUNT', None) is None:
            logger.info("Skipping galaxy check count")
            return

        logger.info("Checking galaxy count")
        self.assert_true(len(cat) == self.job_params.GALAXY_COUNT,
            "Galaxy counts don't match: got {0}, expected {1}".format(
                len(cat), self.job_params.GALAXY_COUNT))
        return


    def unique_galaxies(self, cat1, cat2):
        "Check that galaxies only appear in 1 catalogue"
        gid1 = set(cat1['Galaxy_ID'].values)
        gid2 = set(cat2['Galaxy_ID'].values)
        common = gid1 & gid2
        self.assert_true(len(common) == 0,
            "Galaxy IDs are not unique: {0} in common".format(
                len(common)))
        return

    def check_geometry(self, cat):
        "Check that RA, Dec and Redshift are withing the catalogue geometry"
        stats = cat['Right_Ascension'].describe()
        self.assert_true(stats['max'] <= self.job_params.RA,
                         "Expected max RA of {0}, got {1}".format(
                                self.job_params.RA, stats['max']))
        self.assert_true(stats['min'] >= 0.0,
                         "Negative RA: {0}".format(
                                stats['min']))
        
        stats = cat['Declination'].describe()
        self.assert_true(stats['max'] <= self.job_params.DEC,
                         "Expected max Dec of {0}, got {1}".format(
                                self.job_params.DEC, stats['max']))
        self.assert_true(stats['min'] >= 0.0,
                         "Negative Dec: {0}".format(
                                stats['min']))
        
        stats = cat['Redshift_Cosmological'].describe()
        self.assert_true(stats['max'] <= self.job_params.REDSHIFT_MAX,
                         "Expected max Redshift of {0}, got {1}".format(
                                self.job_params.REDSHIFT_MAX, stats['max']))
        self.assert_true(stats['min'] >= self.job_params.REDSHIFT_MIN,
                         "Expected min Redshift of {0}, got {1}".format(
                                self.job_params.REDSHIFT_MIN, stats['min']))

        return