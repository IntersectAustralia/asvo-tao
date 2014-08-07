"""
Tests:

1. The image archive is present and can be extracted
2. The image error file isn't present
"""
import logging
from os.path import join, exists
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

        iefn = 'image_errors.txt'
        img_err_fn = join(self.download_dir, iefn)
        if exists(img_err_fn):
            logger.error("Image error log exists ({0})".format(iefn))

        logger.info("Finished Mock Image Basic Checks.")
        return
