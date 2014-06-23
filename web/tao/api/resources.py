from tastypie import fields
from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from tastypie.validation import Validation
from tao.models import WorkflowCommand, Job, TaoUser, STATUS_CHOICES

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

class TaoUserResource(ModelResource):
    class Meta:
        queryset = TaoUser.objects.all()
        fields = ['username']
        resource_name = 'jobusername'
        allowed_methods = ['get']
        authorization = Authorization()
        authentication = IpBasedAuthentication()
        validation = ExecutionStatusValidation()

class JobResource(ModelResource):
    user_id = fields.ToOneField(TaoUserResource, 'user', full=True)

    class Meta:
        queryset = Job.objects.all()
        resource_name = 'job'
        fields = ['id', 'username', 'database', 'status', 'parameters', 'error_message', 'output_path']
        allowed_methods = ['get', 'put']
        authorization = Authorization()
        authentication = IpBasedAuthentication()
        validation = ExecutionStatusValidation()
        limit = 0
        filtering = {
            "status": 'exact',
        }

class PowerJobResource(ModelResource):
    user_id = fields.ToOneField(TaoUserResource, 'user', full=True)

    class Meta:
        queryset = Job.objects.all()
        resource_name = 'pjob'
        fields = ['id', 'username', 'description', 'database', 'status',
                  'parameters', 'error_message', 'output_path']
        authorization = Authorization()
        authentication = BasicAuthentication()
        validation = ExecutionStatusValidation()
        limit = 0
        filtering = {
            "status": 'exact',
            "id": 'exact'
        }

class WFJobResource(ModelResource):
    class Meta:
        queryset = Job.objects.all()
        fields = ['id']
        resource_name = 'wfjobid'
        allowed_methods = ['get', 'put']
        authorization = Authorization()
        authentication = IpBasedAuthentication()
        validation = ExecutionStatusValidation()

class WorkflowCommandResource(ModelResource):
    job_id = fields.ToOneField(WFJobResource, 'job_id', full=True, null=True)

    class Meta:
        queryset = WorkflowCommand.objects.all()
        fields = ['id', 'job_id', 'submitted_by', 'command', 'parameters', 'execution_status', 'execution_comment']
        allowed_methods = ['get', 'put']
        resource_name = 'workflowcommand'
        authorization = Authorization()
        authentication = IpBasedAuthentication()
        validation = ExecutionStatusValidation()
        filtering = {
            "execution_status": 'exact',
            "job_id": 'exact',
        }
