from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from tastypie.validation import Validation
from tao.models import WorkflowCommand, Job, STATUS_CHOICES

from django.conf import settings

class IpBasedAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        ip_addr = request.META.get('REMOTE_ADDR')
        return ip_addr in settings.API_ALLOWED_IPS

    def get_identifier(self, request):
        return request.META.get('REMOTE_ADDR')

class ExecutionStatusValidation(Validation):
    def is_valid(self, bundle, request=None):
        errors = {}

        if not bundle.data:
            return errors

        for key, value in bundle.data.items():
            if key == 'execution_status':
                if not (value, value.title()) in STATUS_CHOICES:
                    errors[key] = ['Please input a valid execution status']
        return errors

class JobResource(ModelResource):
    class Meta:
        queryset = Job.objects.all()
        allowed_methods = ['get', 'put']
        authorization = Authorization()
        authentication = IpBasedAuthentication()
        validation = ExecutionStatusValidation()

class WorkflowCommandResource(ModelResource):
    job_id = fields.ToOneField(JobResource, 'job_id', full=True)

    class Meta:
        queryset = WorkflowCommand.objects.all()
        fields = ['id', 'job_id', 'submitted_by', 'command', 'parameters', 'execution_status', 'execution_comment']
        allowed_methods = ['get', 'put']
        authorization = Authorization()
        authentication = IpBasedAuthentication()
        validation = ExecutionStatusValidation()
        filtering = {
            "execution_status": 'exact',
            "job_id": 'exact',
        }