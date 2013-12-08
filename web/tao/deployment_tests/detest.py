#!/usr/bin/env python

import os
import sys
import argparse
import logging
import logging.config
from getpass import getpass
from os.path import abspath, join, split
from time import sleep

import common_settings
from django.conf import settings
from ithelper import DeploymentTester, interact

#from taoui_light_cone.forms import Form as LightConeForm


class SubmitJob(DeploymentTester):

    def setUp(self):
        self.username = self.job_params.USERNAME
        password = self.job_params.PASSWORD

        super(SubmitJob, self).setUp()

        self.login(self.username, password)
        self.visit('mock_galaxy_factory')

    def tearDown(self):
        super(SubmitJob, self).tearDown()

    def submit(self, args, job_params):
        self.job_params = job_params
        
        if self.job_params.PARAMS_FILE is not None:
            self.submit_params(args, job_params)
        else:
            self.submit_browser(args, job_params)
        return

    def submit_params(self, args, job_params):
        self.setUp()
        fpath = join(abspath(split(__file__)[0]), self.job_params.PARAMS_FILE)
        self.upload_params_file(fpath)
        self.submit_mgf_form(job_params.DESCRIPTION)
        self.assert_on_page('jobs/')
        return


    def submit_browser(self, args, job_params):
        self.setUp()
        self.click('tao-tabs-' + 'light_cone')
        self.fill_in_fields({
            'dark_matter_simulation' : self.job_params.SIMULATION,
            'galaxy_model' : self.job_params.GALAXY_MODEL},
                            id_wrap=self.lc_id)
        if job_params.GEOMETRY == 'Box':
            self.configure_box_geometry()
        else:
            self.configure_lc_geometry()

        properties = getattr(self.job_params, 'OUTPUT_PROPERTIES', None)
        if properties == 'All':
            self.click(self.lc_2select('op_add_all'))
        elif properties is not None:
            for prop_filter in properties:
                self.fill_in_fields({
                    'output_properties-filter': prop_filter},
                    id_wrap=self.lc_id, clear=True)
                self.click(self.lc_2select('op_add_all'))

        if getattr(job_params, 'APPLY_SED', None):
            self.configure_sed()
        if getattr(job_params, 'APPLY_MOCK_IMAGE', None):
            self.configure_mock_image()
        self.configure_record_filter()
        self.submit_mgf_form(job_params.DESCRIPTION)
        self.assert_on_page('jobs/')
        return

    def configure_lc_geometry(self):
        self.select(self.lc_id('catalogue_geometry'), 'Light-Cone')
        self.fill_in_fields({
            'ra_opening_angle': str(self.job_params.RA),
            'dec_opening_angle': str(self.job_params.DEC),
            'redshift_min': str(self.job_params.REDSHIFT_MIN),
            'redshift_max': str(self.job_params.REDSHIFT_MAX),
            }, id_wrap=self.lc_id)
        if self.job_params.REPETITION == 'Random':
            self.click_by_css(self.lc_id('light_cone_type_1')) # select "random"
        else:
            self.click_by_css(self.lc_id('light_cone_type_0')) # select "unique"
        self.fill_in_fields({
            'number_of_light_cones': str(self.job_params.NUMBER_OF_CONES)
            }, id_wrap=self.lc_id, clear=True)
        return

    def configure_box_geometry(self):
        self.select(self.lc_id('catalogue_geometry'), 'Box')
        field_vals = {}
        if self.job_params.BOX_SIZE:
            self.clear(self.lc_id('box_size'))
            field_vals['box_size'] = self.job_params.BOX_SIZE
        if self.job_params.REDSHIFT:
            field_vals['snapshot'] = self.job_params.REDSHIFT
        self.fill_in_fields(field_vals, id_wrap=self.lc_id)
        return

    def configure_sed(self):
        self.click('tao-tabs-sed')
        self.click(self.sed('apply_sed'))
        ssp = getattr(self.job_params, 'SED_SSP', None)
        if ssp is not None:
            self.select(self.sed_id('single_stellar_population_model'), ssp)
        filters = getattr(self.job_params, 'BP_FILTERS', None)
        if filters == 'All':
            self.click(self.sed_2select('op_add_all'))
        elif filters is not None:
            for mag_filter in filters:
                self.fill_in_fields({
                    'band_pass_filters-filter': mag_filter},
                    id_wrap=self.sed_id, clear=True)
                self.click(self.sed_2select('op_add_all'))
        return

    def configure_mock_image(self):
        self.click('tao-tabs-mock_image')
        self.click(self.mi_id('apply_mock_image'))
        return

    def configure_record_filter(self):
        self.click('tao-tabs-record_filter')
        self.fill_in_fields({
            'min': self.job_params.FILTER_MIN,
            'max': self.job_params.FILTER_MAX,
        }, id_wrap=self.rf_id, clear=True)



if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='TAO Deployment Test Framework')
    parser.add_argument('cmd',
            help='Command: SUBMIT or VALIDATE')
    parser.add_argument('name',
            help='Test Name')
    parser.add_argument('base_url',
            help='Server base url for submitting, e.g. https://tao.asvo.org.au/taostaging/')
    parser.add_argument('--id',
            dest='catalogue_id',
            help='Catalogue ID for validation'),
    parser.add_argument('-u', default=None,
            dest='username',
            help='TAO Username'),
    parser.add_argument('-p', default=None,
            dest='password',
            help='TAO Password')
    parser.add_argument('-d', dest='debug', action='store_true',
            default=False,
            help='Load pdb and halt')

    args = parser.parse_args()
    if args.debug:
        import pdb
        pdb.set_trace()

    logging.config.dictConfig(common_settings.LOGGING)
    logger = logging.getLogger('detest')
    logger.info("Starting...")

    if args.username:
        common_settings.USERNAME = args.username
    if args.password:
        common_settings.PASSWORD = args.password
    if common_settings.USERNAME is None:
        common_settings.USERNAME = raw_input("Username: ")
    if common_settings.PASSWORD is None:
        common_settings.PASSWORD = getpass("Password: ")

    if args.name == "all":
        all_jobs = []
        for root, dirs, files in os.walk('jobs'):
            for file in files:
                fname, ftype = os.path.splitext(file)
                if ftype == ".py" and fname != "__init__":
                    all_jobs.append("jobs."+fname)
    else:
        all_jobs = [args.name]

    i = 1
    for job in all_jobs:
        job_params = __import__(job)
        name_parts = job.split('.')
        for name_part in name_parts[1:]:
            job_params = getattr(job_params, name_part)
        job_params.BASE_URL = args.base_url

        if args.cmd.lower() == 'submit':
            logger.info("Submitting {0} of {1}".format(
                i, len(all_jobs)))
            ctrl = SubmitJob()
            ctrl.submit(args, job_params)
            sleep(5.0)
            ctrl.tearDown()
        elif args.cmd.lower() == 'validate':
            for validator in job_params.VALIDATORS:
                ctrl = validator()
                ctrl = ctrl.validate(args, job_params)
        sleep(1.0)
        i += 1

    logger.info("Finished.")
    exit(0)
