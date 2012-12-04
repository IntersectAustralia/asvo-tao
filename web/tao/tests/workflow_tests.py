import datetime

from decimal import Decimal

from django.test import TestCase

from tao import workflow, time
from tao.tests.support.xml import XmlDiffMixin
from tao.tests.support import stripped_joined_lines, UtcPlusTen


class WorkflowTests(TestCase, XmlDiffMixin):
    
    def setUp(self):
        super(WorkflowTests, self).setUp()
        # "2012-11-14T13:45:36+10:00"
        time.frozen_time = datetime.datetime(2012, 11, 14, 13, 45, 36, 0, UtcPlusTen())

    def tearDown(self):
        super(WorkflowTests, self).tearDown()
        time.frozen_time = None

    def test_normalizes_decimals(self):
        param = workflow.param("name", Decimal('0E9'))
        self.assertEqual('0', str(param['value']))

    def test_basic(self):
        expected_parameter_xml = stripped_joined_lines("""
            <?xml version="1.0" encoding="utf-8"?>
            <tao xmlns="http://tao.asvo.org.au/schema/module-parameters-v1" timestamp="2012-11-14T13:45:36+1000">
             
                <workflow name="alpha-light-cone-image">
                    <param name="database">sqlite://sfh_bcgs200_full_z0.db</param>
                    <param name="schema-version">1.0</param>
                    <module name="light-cone">
                        <param name="query-type">light-cone</param>
                        <param name="simulation-box-size" units="Mpc">500</param>
                        <param name="redshift-min">0.2</param>
                        <param name="redshift-max">0.3</param>
                        <param name="ra-min" units="deg">18.434</param>
                        <param name="ra-max" units="deg">71.565</param>
                        <param name="dec-min" units="deg">0</param>
                        <param name="dec-max" units="deg">41.810</param>
                        <param name="filter-type">disc-radius</param>
                        <param name="filter-min" units="Mpc">0.1</param>
                        <param name="filter-max" units="Mpc">0.2</param>
                    </module>
                    <module name="sed">
                        <param name="single-stellar-population-model">Stella</param>
                    </module>
                </workflow>
            </tao>
        """)
        
        sed_parameters = [
            {
                'attrs': {
                    'name': 'single-stellar-population-model',
                },
                'value': 'Stella'
            },
        ]

        common_parameters = [
            {
                'attrs': {
                    'name': 'database',
                },
                'value': 'sqlite://sfh_bcgs200_full_z0.db',
            },
            {
                'attrs': {
                    'name': 'schema-version'
                },
                'value': '1.0',
            },
        ]

        light_cone_parameters = [
            {
                'attrs': {
                    'name': 'query-type'
                },
                'value': 'light-cone',
            },
            {
                'attrs': {
                    'name': 'simulation-box-size',
                    'units': 'Mpc',
                },
                'value': '500',
            },
            {
                'attrs': {
                    'name': 'redshift-min',
                },
                'value': '0.2',
            },
            {
                'attrs': {
                    'name': 'redshift-max',
                },
                'value': '0.3',
            },
            {
                'attrs': {
                    'name': 'ra-min',
                    'units': 'deg',
                },
                'value': '18.434',
            },
            {
                'attrs': {
                    'name': 'ra-max',
                    'units': 'deg',
                },
                'value': '71.565',
            },
            {
                'attrs': {
                    'name': 'dec-min',
                    'units': 'deg',
                },
                'value': '0',
            },
            {
                'attrs': {
                    'name': 'dec-max',
                    'units': 'deg',
                },
                'value': '41.810',
            },
            {
                'attrs': {
                    'name': 'filter-type',
                },
                'value': 'disc-radius',
            },
            {
                'attrs': {
                    'name': 'filter-min',
                    'units': 'Mpc',
                },
                'value': '0.1',
            },
            {
                'attrs': {
                    'name': 'filter-max',
                    'units': 'Mpc',
                },
                'value': '0.2',
            },
        ]

        actual_parameter_xml = workflow.to_xml(common_parameters, light_cone_parameters, sed_parameters)

        self.assertXmlEqual(expected_parameter_xml, actual_parameter_xml)
