import os
import logging
from os.path import abspath, join, split, exists
from subprocess import Popen

import pandas as pd

#from django.conf import settings

logger = logging.getLogger('detest.'+__name__)


class ValidateJob(object):

    def validate(self, args, job_params):
        self.args = args
        self.job_params = job_params

        self.working_dir = abspath(split(job_params.__file__)[0]) 
        self.download_dir = abspath(join(self.job_params.DOWNLOAD_DIR,
                                         self.args.catalogue_id))
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

        self.download()
        self.report()
        return

    def download(self):
        "Download and unpack the catalogue if required"
        fn = join(self.download_dir, 'catalogue.tar')

        if exists(fn):
            # No need to download twice
            return
 
        url = "{base}jobs/{id}/basic_tar".format(base=self.args.base_url,
                                       id=self.args.catalogue_id)
        sp = Popen('wget --user={un} --password={pwd} -O {fn} {url}'.format(
                        fn=fn,
                        url=url,
                        un=self.job_params.USERNAME,
                        pwd=self.job_params.PASSWORD),
                   shell=True)
        sp.wait()
        if sp.returncode != 0:
            raise Exception("FATAL: Unable to download from: {0}".format(url))
        logger.debug(u"Downloaded: {0}".format(url))

        sp = Popen(u'cd {wd} && tar xf {fn}'.format(
                        wd=self.download_dir, fn=fn),
                   shell=True)
        sp.wait()
        if sp.returncode != 0:
            msg = "uUnable to untar: {0}".format(fn)
            logger.fatal(msg)
            raise Exception(msg)
        logger.debug(u"Extracted: {0}".format(fn))
        return

    def report(self):
        """Log the summary information of the catalogues being validated and
        the test documentation"""
        
        summary_fn = join(self.download_dir, 'summary.txt')
        with open(summary_fn) as fp:
            logger.info("Catalogue Summary:\n{0}".format(fp.read()))
        # test_dic is defined by the instantioated subclass
        logger.info("Test Description:\n{0}".format(self.doc))
        return

    def load_csv(self, subcone):
        "Load the specified subcone index as a pandas DataFrame"
        fn = join(self.download_dir,
                  u"tao.{job}.{subcone}.csv".format(job=self.args.catalogue_id,
                                                   subcone=subcone))
        gz = fn+u'.gz'
        if exists(gz):
            # Need to unzip
            sp = Popen(u'gunzip {fn}'.format(fn=gz),
                       shell=True)
            sp.wait()
            if sp.returncode != 0:
                msg = u"Unable to unzip: {0}".format(gz)
                logger.fatal(msg)
                raise Exception(msg)
            logger.debug(u"unzipped: {0}".format(gz))
        df = pd.read_csv(fn)
        df.columns = [x.strip() for x in df.columns]
        logger.debug("Catalogue stats:\n{0}".format(df.describe()))
        return df
        
    def assert_true(self, condition, msg):
        if not condition:
            logger.error(msg)
