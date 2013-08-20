from django.conf import settings
from django.template import Context, loader
from django.test.utils import override_settings

from tao.forms import FormsGraph
from tao.models import Job, BandPassFilter, WorkflowCommand
from tao.tests import helper
from tao.tests.integration_tests.helper import LiveServerTest
from tao.tests.support.factories import GlobalParameterFactory, JobFactory, UserFactory, SimulationFactory, GalaxyModelFactory, DataSetFactory, DataSetPropertyFactory, StellarModelFactory, DustModelFactory, BandPassFilterFactory, SnapshotFactory
from tao.tests.support.xml import light_cone_xml

import os, zipfile, html2text, codecs


class JobTest(LiveServerTest):
    
    fixtures = ['rules.json']

    def setUp(self):
        super(JobTest, self).setUp()
        
        self.username = 'user'
        self.password = 'password'

        self.user = UserFactory.create(username=self.username, is_superuser=True)
        self.user.set_password(self.password)
        self.user.save()

        # self.job_description = 'This is a job description'
        self.job = JobFactory.create(user=self.user)
        GlobalParameterFactory.create(parameter_name='maximum-random-light-cones', parameter_value='10000')

        self.simulation = SimulationFactory.create()
        self.galaxy = GalaxyModelFactory.create()
        self.dataset = DataSetFactory.create(simulation=self.simulation, galaxy_model=self.galaxy)
        self.output_prop = DataSetPropertyFactory.create(dataset=self.dataset, name='Central op', is_filter=False)
        self.filter = DataSetPropertyFactory.create(name='CentralMvir rf', units="Msun/h", dataset=self.dataset)
        self.computed_filter = DataSetPropertyFactory.create(name='Computed Property', dataset=self.dataset, is_computed=True)
        self.sed = StellarModelFactory.create()
        self.dust = DustModelFactory.create()
        self.snapshot = SnapshotFactory.create(dataset=self.dataset, redshift='0.33')
        self.band_pass_filters = [BandPassFilterFactory.create(), BandPassFilterFactory.create()]

        self.output_paths = ['job1', 'large_job']
        self.dir_paths = [os.path.join(settings.FILES_BASE, output_path) for output_path in self.output_paths]
        txt_template = loader.get_template('jobs/summary.txt')
        summary_context = Context(self.make_parameters())
        self.summary_text = txt_template.render(summary_context)
        self.file_names_to_contents = {
                                       'file1': 'abc\n',
                                       'filez2.txt': 'pqr\n',
                                       'file3': 'xyz\n',
                                       'job2/fileA.html': 'aaaahhhh & aaaaa',
                                       'job2/fileB': 'baaaaaa',
                                       'summary.txt': self.summary_text,
                                       }
        self.file_names_to_contents2 = {
                                       'waybigfile1': 'xnfaihnehrawlrwerajelrjxmjaeimrjwmrejlxaljrxm;kjmrlakjemrajlejrljrljaereirje;rjmriarie;rirjijeaim;jea;ljmxirjwra;ojer',
                                       'waybigfile2': 'xnfaihnehrawlrwerajelrjxmjaeimrjwmrejlxaljrxm;kjmrlakjemrajlejrljrljaereirje;rjmriarie;rirjijeaim;jea;ljmxirjwra;ojer',
                                       'waybigfile3': 'xnfaihnehrawlrwerajelrjxmjaeimrjwmrejlxaljrxm;kjmrlakjemrajlejrljrljaereirje;rjmriarie;rirjijeaim;jea;ljmxirjwra;ojer',
                                       'waybigfile4': 'xnfaihnehrawlrwerajelrjxmjaeimrjwmrejlxaljrxm;kjmrlakjemrajlejrljrljaereirje;rjmriarie;rirjijeaim;jea;ljmxirjwra;ojer',
                                       'waybigfile5': 'xnfaihnehrawlrwerajelrjxmjaeimrjwmrejlxaljrxm;kjmrlakjemrajlejrljrljaereirje;rjmriarie;rirjijeaim;jea;ljmxirjwra;ojer',
                                       }
        for file_name in self.file_names_to_contents.keys():
            helper.create_file(self.dir_paths[0], file_name, self.file_names_to_contents)
        for file_name in self.file_names_to_contents2.keys():
            helper.create_file(self.dir_paths[1], file_name, self.file_names_to_contents2)
        parameters = self.make_xml_parameters()
        self.job.parameters = parameters
        self.job.save()
        self.completed_job = JobFactory.create(user=self.user, status=Job.COMPLETED, output_path=self.output_paths[0], parameters=parameters)
        self.held_job = JobFactory.create(user=self.user, parameters=parameters, status=Job.HELD)
        self.error_job = JobFactory.create(user=self.user, parameters=parameters, status=Job.ERROR, error_message="error")
        self.in_progress_job = JobFactory.create(user=self.user, parameters=parameters, status=Job.IN_PROGRESS)
        self.submitted_job = JobFactory.create(user=self.user, parameters=parameters, status=Job.SUBMITTED)
        self.queued_job = JobFactory.create(user=self.user, parameters=parameters, status=Job.QUEUED)

    def tearDown(self):
        super(JobTest, self).tearDown()
        for root, dirs, files in os.walk(settings.FILES_BASE, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    def make_parameters(self):
        parameters = {
            'catalogue_geometry': 'light-cone',
            'dark_matter_simulation': self.simulation.id,
            'galaxy_model': self.galaxy.id,
            'redshift_min': 0.2,
            'redshift_max': 0.3,
            'ra_opening_angle': 71.565,
            'dec_opening_angle': 41.811,
            'output_properties': [self.filter.id, self.output_prop.id],
            'light_cone_type': 'random', #'unique',
            'number_of_light_cones': 1,
            }
        parameters.update({
            'username' : self.username,
            'dark_matter_simulation': self.simulation.name,
            'galaxy_model': self.galaxy.name,
            'output_properties': [(self.filter, self.filter.units), (self.output_prop, self.output_prop.units)],
            'output_properties_1_name' : self.filter.name,
            'output_properties_1_label' : self.filter.label,
            'output_properties_1_units' : self.filter.units,
            'output_properties_1_description' : self.filter.description,
            'output_properties_2_name' : self.output_prop.name,
            'output_properties_2_label' : self.output_prop.label,
            'output_properties_2_description' : self.output_prop.description,
            'output_properties_3_name' : self.computed_filter.name,
            'output_properties_3_label' : self.computed_filter.label,
            'output_properties_3_description' : self.computed_filter.description,
            })
        parameters.update({
            'filter': self.filter.name,
            'filter_min': '1000000',
            'filter_max': 'None',
            })
        parameters.update({
            'ssp_name': self.sed.name,
            'band_pass_filters': [self.band_pass_filters[0].label + ' (Apparent)'],
            'band_pass_filter_label': self.band_pass_filters[0].label + ' (Apparent)',
            'band_pass_filter_id': self.band_pass_filters[0].filter_id,
            'band_pass_filter_name': self.band_pass_filters[0].filter_id,
            'dust_model_name': self.dust.name,
            })
        parameters.update({
            'light_cone_id': FormsGraph.LIGHT_CONE_ID,
            'csv_dump_id': FormsGraph.OUTPUT_ID,
            'bandpass_filter_id': FormsGraph.BANDPASS_FILTER_ID,
            'sed_id': FormsGraph.SED_ID,
            'dust_id': FormsGraph.DUST_ID,
            })
        parameters.update({
            'geometry': 'Light-Cone',
            'simulation_details': html2text.html2text(self.simulation.details),
            'galaxy_model_details': html2text.html2text(self.galaxy.details),
            'apply_sed': True,
            'ssp_description': html2text.html2text(self.sed.description),
            'apply_dust': True,
            'dust_label': self.dust.label,
            'dust_model_details': html2text.html2text(self.dust.details),
            'filter_label': self.filter.label,
            'filter_units': self.filter.units,
            'record_filter': '1000000 ' + u'\u2264' + ' ' + self.filter.label + ' (' + self.filter.units + ')',
            'output_format': 'CSV (Text)',
        })
        return parameters

    def make_xml_parameters(self):
        return light_cone_xml(self.make_parameters())

    def test_view_job_summary(self):
        self.login(self.username, self.password)
        self.visit('view_job', self.completed_job.id)
        self.wait(2)
        self.assert_element_text_equals('#id-job_description', self.completed_job.description)
        self.assert_page_has_content('Download')
        self.assert_page_has_content('Status')
        self.assert_page_has_content('Summary')
        self.assert_summary_field_correctly_shown(self.simulation.name, 'light_cone', 'simulation')
        self.assert_summary_field_correctly_shown(self.galaxy.name, 'light_cone', 'galaxy_model')
        self.assert_summary_field_correctly_shown('1 random light cones', 'light_cone', 'number_of_light_cones')
        self.assert_summary_field_correctly_shown(self.sed.label, 'sed', 'single_stellar_population_model')
        self.assert_summary_field_correctly_shown(self.dust.name, 'sed', 'dust_model')
        self.assert_summary_field_correctly_shown(u"1000000 \u2264 %s (%s)" % (self.filter.label, self.filter.units), 'record_filter', 'record_filter')

        band_pass_filters = BandPassFilter.objects.all()
        self.wait(2)
        self.assert_summary_field_correctly_shown('1 filter selected', 'sed', 'band_pass_filters')
        self.click('expand_band_pass_filters')  # this click doesn't work, it just grabs the focus
        self.click('expand_band_pass_filters')  # need a second call to actually do the click
        self.assert_summary_field_correctly_shown(band_pass_filters[0].label + ' (Apparent)', 'sed', 'band_pass_filters_list')

    def test_job_with_files_downloads(self):
        self.login(self.username, self.password)
        self.visit('view_job', self.completed_job.id)

        li_elements = self.selenium.find_elements_by_css_selector('#id_completed_jobs li')
        filenames_with_sizes = ['summary.txt']
        for file_name in self.file_names_to_contents:
            file_size = helper.get_file_size(self.dir_paths[0],file_name)
            filenames_with_sizes.append(file_name + " (" + file_size + ")")
        self.assertEqual(sorted(filenames_with_sizes), sorted([li.text for li in li_elements]))

        self.wait(1)
        # test files download
        for li in li_elements:
            li.find_element_by_css_selector('a').click()
        self.wait(1)

        for job_file in self.completed_job.files():
            download_path = os.path.join(self.DOWNLOAD_DIRECTORY, job_file.file_name.replace('/','_'))
            self.assertTrue(os.path.exists(download_path))
            with codecs.open(download_path, encoding='utf-8') as f:
                self.assertEqual(self.file_names_to_contents[job_file.file_name], f.read())

    def test_summary_txt_displayed(self):
        self.login(self.username, self.password)
        self.visit('view_job', self.completed_job.id)
        self.assert_page_has_content('summary.txt')

        self.visit('view_job', self.job.id)
        self.assert_page_has_content('summary.txt')

    def test_summary_txt_downloads_correctly(self):
        self.login(self.username, self.password)
        self.visit('view_job', self.completed_job.id)

        self.wait(1)
        self.click('id_download_summary_txt')
        summary_txt_path = os.path.join(self.DOWNLOAD_DIRECTORY, 'summary.txt')
        with codecs.open(summary_txt_path, encoding='utf-8') as f:
            self.assertEqual(self.summary_text, f.read())

    # test that anonymous user cannot view job or download files
    def test_anonymous_user_cannot_view_or_download(self):
        completed_job = JobFactory.create(user=self.user, status=Job.COMPLETED, output_path=self.output_paths[0])
        self.visit('view_job', completed_job.id)
        
        self.assert_on_page('login', ignore_query_string=True)
        
        first_filename = self.file_names_to_contents.keys()[0]

        self.visit('get_file', completed_job.id, first_filename) 
        
        self.assert_on_page('login', ignore_query_string=True)
        
        download_path = os.path.join(self.DOWNLOAD_DIRECTORY, first_filename)
        self.assertFalse(os.path.exists(download_path))
        
    # test that another logged-in user cannot view job or download files created by the original user
    def test_other_user_cannot_view_or_download(self):
        username = 'user2'
        password = 'password2'

        user2 = UserFactory.create(username=username)
        user2.set_password(password)
        user2.save()
                
        completed_job = JobFactory.create(user=self.user, status=Job.COMPLETED, output_path=self.output_paths[0])
        
        helper.create_file(self.dir_paths[0], 'file1', self.file_names_to_contents)
        
        self.login(username, password)
        self.visit('view_job', completed_job.id)
        self.assert_page_has_content('Forbidden')
        
        self.visit('get_file', completed_job.id, 'file1')
        self.assert_page_has_content('Forbidden')
        
        download_path = os.path.join(self.DOWNLOAD_DIRECTORY, 'file1')
        self.assertFalse(os.path.exists(download_path))
        
    def test_cannot_view_not_completed_job(self):
        self.login(self.username, self.password)
        
        self.visit('job_index')
        self.assert_page_does_not_contain('(View)')

    def test_zip_file_download(self):
        self.login(self.username, self.password)
        self.visit('view_job', self.completed_job.id)
            
        download_link = self.selenium.find_element_by_id('id_download_as_zip')
        download_link.click()

        download_path = os.path.join(self.DOWNLOAD_DIRECTORY, 'tao_output.zip')

        self.wait()
        self.assertTrue(os.path.exists(download_path))
        
        # extract the files
        extract_path = os.path.join(self.DOWNLOAD_DIRECTORY, 'tao_output')
        self._extract_zipfile_to_dir(download_path, extract_path)
        
        self._assert_directories_match(self.dir_paths[0], extract_path)
                
    def test_zip_file_displayed(self):
        self.login(self.username, self.password)
        self.visit('view_job', self.completed_job.id)

        self.assert_page_has_content('Download zip file')

    def test_save_job_description_edit(self):
        self.login(self.username, self.password)
        self.visit('view_job', self.job.id)
        self.assert_element_text_equals('#id-job_description', self.job.description)
        new_description = 'This is an updated job description; '
        old_description = self.job.description
        self.fill_in_fields({'#id-job_description': new_description})# fill_in_fields sends text to the start of input field, without overriding the original input
        self.click('id-save_edit')
        self.assert_element_text_equals('#id-job_description', new_description + old_description)

        self.selenium.refresh()
        self.assert_element_text_equals('#id-job_description', new_description + old_description)

    def test_cancel_job_description_edit(self):
        self.login(self.username, self.password)
        self.visit('view_job', self.job.id)
        temp_description = "Here's some text that will be removed faweirhiclzklhrehure "
        original_description = self.job.description
        self.fill_in_fields({'#id-job_description': temp_description})
        self.assert_element_text_equals('#id-job_description', temp_description + original_description)
        self.click('id-cancel_edit')
        self.assert_element_text_equals('#id-job_description', original_description)

        self.selenium.refresh()
        self.assert_element_text_equals('#id-job_description', original_description)

    def test_stop_rerun_release_buttons_enabled_with_status(self):
        self.login(self.username, self.password)

        self.visit('view_job', self.submitted_job.id)
        self._check_job_buttons_enabled_or_disabled({'enabled': ['stop'], 'disabled': ['rerun', 'release']})

        self.visit('view_job', self.queued_job.id)
        self._check_job_buttons_enabled_or_disabled({'enabled': ['stop'], 'disabled': ['rerun', 'release']})

        self.visit('view_job', self.in_progress_job.id)
        self._check_job_buttons_enabled_or_disabled({'enabled': ['stop'], 'disabled': ['rerun', 'release']})

        self.visit('view_job', self.completed_job.id)
        self._check_job_buttons_enabled_or_disabled({'enabled': ['rerun'], 'disabled': ['stop', 'release']})

        self.visit('view_job', self.error_job.id)
        self._check_job_buttons_enabled_or_disabled({'enabled': ['rerun'], 'disabled': ['stop', 'release']})

        self.visit('view_job', self.held_job.id)
        self._check_job_buttons_enabled_or_disabled({'enabled': ['release'], 'disabled': ['stop', 'rerun']})

    def test_stop_job_button(self):
        self.login(self.username, self.password)
        self.visit('view_job', self.in_progress_job.id)
        self.assertEqual(0, len(WorkflowCommand.objects.all()))

        self.click(self.job_select('stop'))
        self.click('id_confirm_stop')
        self.assertEqual(1, len(WorkflowCommand.objects.all()))
        stop_job_command = WorkflowCommand.objects.get(pk=1)
        self.assertEqual(self.in_progress_job, stop_job_command.job_id)
        self.assertEqual(self.user, stop_job_command.submitted_by)
        self.assertEqual('Job_Stop', stop_job_command.command)
        self.assertEqual('SUBMITTED', stop_job_command.execution_status)

    def test_rerun_job_button(self):
        self.login(self.username, self.password)
        self.visit('view_job', self.completed_job.id)
        self.click(self.job_select('rerun'))
        self.click('id_confirm_rerun')
        self._check_job_buttons_enabled_or_disabled({'enabled': ['stop'], 'disabled': ['rerun', 'release']})

        updated_job = Job.objects.get(id=self.completed_job.id)
        self.assertEqual('SUBMITTED', updated_job.status)

    def test_delete_job_output_button(self):
        self.login(self.username, self.password)
        self.visit('view_job', self.completed_job.id)
        self.assertEqual(0, len(WorkflowCommand.objects.all()))

        self.click(self.job_select('output_delete'))
        self.click('id_confirm_delete_output')
        self.assertEqual(1, len(WorkflowCommand.objects.all()))
        delete_job_output_command = WorkflowCommand.objects.get(pk=1)
        self.assertEqual(self.completed_job, delete_job_output_command.job_id)
        self.assertEqual(self.user, delete_job_output_command.submitted_by)
        self.assertEqual('Job_Output_Delete', delete_job_output_command.command)
        self.assertEqual('SUBMITTED', delete_job_output_command.execution_status)

    def test_release_job_button(self):
        self.login(self.username, self.password)
        self.visit('view_job', self.held_job.id)
        self.click(self.job_select('release'))
        self.click('id_confirm_release')
        self._check_job_buttons_enabled_or_disabled({'enabled': ['stop'], 'disabled': ['rerun', 'release']})

        updated_job = Job.objects.get(id=self.held_job.id)
        self.assertEqual('SUBMITTED', updated_job.status)

    def _extract_zipfile_to_dir(self, download_path, dirname):
        fullpathhandle = open(download_path, 'r')
        zipfile_obj = zipfile.ZipFile(fullpathhandle)
        for filename in zipfile_obj.namelist(): 
            fullpath = os.path.join(dirname, filename)
            helper.mkdir_p(os.path.dirname(fullpath))
            helper.write_file_from_zip(zipfile_obj, filename, fullpath)
            
    def _assert_directories_match(self, expected_dir_path, actual_dir_path):
        expected_dir_list = self._list_all_files(expected_dir_path)
        actual_dir_list = self._list_all_files(actual_dir_path)
        self.assertEqual(len(expected_dir_list), len(actual_dir_list))
        
        expected_dir_list.sort()
        actual_dir_list.sort()
        self.assertEqual(expected_dir_list, actual_dir_list)
        
        for first, second in zip(expected_dir_list, actual_dir_list):
            first_path = os.path.join(expected_dir_path, first)
            second_path = os.path.join(actual_dir_path, second)
            with open(first_path, 'r') as f1:
                with open(second_path, 'r') as f2:
                    self.assertEqual(f1.read(), f2.read())
            
    def _click_view_job(self, job):
        job_id = job.id
        job_link = self.selenium.find_element_by_id("view_job_%s" % job_id)
        job_link.click()

    def _list_all_files(self, dir):
        list_of_files = []
        for root, dirnames, filenames in os.walk(dir):
            for name in filenames:
                list_of_files.append(os.path.join(root[len(dir)+1:], name))
        return list_of_files

    def _check_job_buttons_enabled_or_disabled(self, enabler):
        self.wait(1.5)
        for button in enabler['enabled']:
            self.assert_is_enabled(self.job_id(button))

        for button in enabler['disabled']:
            self.assert_is_disabled(self.job_id(button))