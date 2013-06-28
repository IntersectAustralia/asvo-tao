from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tao.models import WorkflowCommand, Job

class JobResource(ModelResource):
    class Meta:
        queryset = Job.objects.all()
        resource_name = 'job'

class WorkflowCommandResource(ModelResource):
    job_id = fields.ToOneField(JobResource, 'job_id', full=True)

    class Meta:
        queryset = WorkflowCommand.objects.all()
        fields = ['id', 'job_id', 'submitted_by', 'command', 'parameters', 'execution_status', 'execution_comment']
        allowed_methods = ['get', 'put']
        authorization = Authorization()
        filtering = {
            "execution_status": 'exact',
            "job_id": 'exact',
        }