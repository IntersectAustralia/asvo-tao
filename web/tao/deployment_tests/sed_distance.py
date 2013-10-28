"""
Tests:

1. distance modulus vs. distance
"""
import logging
import math

from calc_kcor import calc_kcor
from calc_z2d import z2d

from ithelper import interact
from tao_validate import ValidateJob

logger = logging.getLogger('detest.'+__name__)

def apply_kcor(s):
    return calc_kcor('B', s['Redshift_(Cosmological)'], 'B - Rc', s['colour'])

def calc_diff(s):
    return 100.0 * s['D_M'] / s['Distance'] - 100.0

class Validator(ValidateJob):

    def __init__(self):
        self.doc = __doc__
        super(Validator, self).__init__()

    def validate(self, args, job_params):
        super(Validator, self).validate(args, job_params)
        
        self.cat0 = self.load_csv(0)
        self.h = job_params.LITTLE_H
        self.wm = job_params.WM

        logger.debug("h={0}".format(self.h))
        logger.debug("wm={0}".format(self.wm))
        self.check_distance()
        logger.info("Finished SED Distance Checks.")
        return


    def check_distance(self):
        cat = self.cat0
        cat['D_Z'] = cat['Redshift_(Cosmological)'].map(lambda x: z2d(x, h=1.0, wm=self.wm))
        cat['colour'] = cat['Johnson_B_(Apparent)'] - cat['Johnson_R_(Apparent)']
        cat['K Correction'] = cat.apply(apply_kcor, axis=1)
        cat['DM'] = cat['Johnson_B_(Apparent)'] - cat['Johnson_B_(Absolute)'] - cat['K Correction']
        cat['D Lum'] = cat['DM'].map(lambda x: math.pow(10, 0.2*x + 1)/1.0e6)
        cat['D_M'] = cat.apply(self.make_d_m(), axis=1)
        cat['Diff'] = cat.apply(calc_diff, axis=1)

        stats = cat['Diff'].describe()

        logger.info("Stats:\n{0}".format(stats))
        logger.debug("First 10:\n{0}".format(
            cat.head(10)))        
        if abs(stats['mean']) > self.job_params.MAX_MEAN_DIFFERENCE:
            logger.error("Mean difference {0} exceeds {1}".format(
                stats['mean'], self.job_params.MAX_MEAN_DIFFERENCE))

        if abs(stats['max']) > self.job_params.MAX_MAX_DIFFERENCE:
            logger.error("Max difference {0} exceeds {1}".format(
                stats['max'], self.job_params.MAX_MAX_DIFFERENCE))
        #import pdb; pdb.set_trace()

        return

    def make_d_m(self):
        def d_m(s):
            return self.h * s['D Lum'] / (1 + s['Redshift_(Cosmological)'])
        return d_m
