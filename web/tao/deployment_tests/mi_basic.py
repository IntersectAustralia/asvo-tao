"""
Tests:

1. The image archive is present and can be extracted
"""
import logging
from os.path import join
from subprocess import Popen

from tao_validate import ValidateJob

logger = logging.getLogger('detest.'+__name__)


class Validator(ValidateJob):

    def __init__(self):
        self.doc = __doc__
        super(Validator, self).__init__()

    def validate(self, args, job_params):
        super(Validator, self).validate(args, job_params)

        fn = join(self.download_dir,
                  'images.{cid}.tar.gz'.format(cid=self.args.catalogue_id))

        sp = Popen(u'cd {wd} && tar xf {fn}'.format(
                        wd=self.download_dir, fn=fn),
                   shell=True)
        sp.wait()
        if sp.returncode != 0:
            msg = "Unable to untar: {0}".format(fn)
            logger.fatal(msg)
            raise Exception(msg)
        logger.debug(u"Extracted: {0}".format(fn))
        return


        logger.info("Finished Mock Image Basic Checks.")
        return
