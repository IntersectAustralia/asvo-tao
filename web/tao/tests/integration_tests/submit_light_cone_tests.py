from tao.models import Job
from tao.tests.integration_tests.helper import LiveServerMGFTest
from tao.tests.support.factories import UserFactory, SimulationFactory, GalaxyModelFactory, DataSetFactory, DataSetParameterFactory, JobFactory

class SubmitLightConeTests(LiveServerMGFTest):
    def setUp(self):
        super(SubmitLightConeTests, self).setUp()
        
        simulation = SimulationFactory.create()
        galaxy_model = GalaxyModelFactory.create(simulation=simulation)
        dataset = DataSetFactory.create(simulation=simulation, galaxy_model=galaxy_model)
        DataSetParameterFactory.create(dataset=dataset)
        
        self.username = "user"
        password = "password"
        self.user = UserFactory.create(username=self.username, password=password)
        
        self.parameters = """<lightcone>
                        <database_type>sqlite</database_type>
                        <database_name>random.db</database_name>
                        <box_type>cone</box_type>
                        </lightcone>
                    """
        self.submitted_job = JobFactory.create(user=self.user, parameters=self.parameters)
        self.queued_job = JobFactory.create(user=self.user, parameters=self.parameters, status=Job.QUEUED)
        self.in_progress_job = JobFactory.create(user=self.user, parameters=self.parameters, status=Job.IN_PROGRESS)
        self.completed_job = JobFactory.create(user=self.user, parameters=self.parameters, status=Job.COMPLETED)
        
        self.login(self.username, password)
        
    def test_redirect_to_submitted_jobs_list_after_submit(self):
        self.visit('mock_galaxy_factory')
        
        ## fill in form (correctly) using default values
        self.submit_mgf_form()

        self.assert_on_page('submitted_jobs')
        
    def test_submitted_jobs_table_contains_submitted_job(self):
        self.visit('submitted_jobs')
        
        expected_jobs = [self.submitted_job]
        self.assert_job_table_equals(expected_jobs, Job.SUBMITTED)
        
    def test_queued_jobs_table_contains_queued_job(self):
        self.visit('queued_jobs')
        
        expected_jobs = [self.queued_job]
        self.assert_job_table_equals(expected_jobs, Job.QUEUED)
        
    def test_in_progress_jobs_table_contains_in_progress_jobs(self):
        self.visit('in_progress_jobs')
        
        expected_jobs = [self.in_progress_job]
        self.assert_job_table_equals(expected_jobs, Job.IN_PROGRESS)
        
    def test_completed_jobs_table_contains_completed_jobs(self):
        self.visit('completed_jobs')
        
        expected_jobs = [self.completed_job]
        self.assert_job_table_equals(expected_jobs, Job.COMPLETED)
        
    def test_all_jobs_table_contains_all_jobs(self):
        self.visit('all_jobs')
        
        expected_jobs = [self.completed_job, self.in_progress_job, self.queued_job, self.submitted_job]
        self.assert_job_table_equals(expected_jobs, 'All')
        
    def clean_parameter_lines(self, job):
        parameter_lines = job.parameters.split("\n")
        stripped_lines = [line.strip() for line in parameter_lines]
        return "\n".join(stripped_lines).strip()
        
    def assert_job_table_equals(self, expected_jobs, status):
        header_row = self.get_job_table_header(status) 
        body = [self.get_job_table_body(job, status) for job in expected_jobs]
        
        expected_table = [header_row] + body
        actual_table = self.table_as_text_rows('#jobs_table')
        self.assertEqual(expected_table, actual_table)
        
    def get_job_table_header(self, status):
        header = ['', 'Submitted at', 'Parameters']
        if status in [Job.SUBMITTED, Job.QUEUED, Job.IN_PROGRESS]:
            return header
        elif status == Job.COMPLETED:
            return header + ['Output Path']
        else:
            return ['', 'Submitted at', 'User', 'Status', 'Parameters', 'Output Path']
        
    def get_job_table_body(self, job, status):
        body = ['View', job.created_time.strftime('%a %d %b %Y %H:%m'), self.clean_parameter_lines(job)]
        if status in [Job.SUBMITTED, Job.QUEUED, Job.IN_PROGRESS]:
            return body
        elif status == Job.COMPLETED:
            return body + [job.output_path]
        else:
            return ['View', job.created_time.strftime('%a %d %b %Y %H:%m'), job.username(), job.status, self.clean_parameter_lines(job), job.output_path]