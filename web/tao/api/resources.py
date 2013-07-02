from django.conf.urls.defaults import url
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
        resource_name = 'workflowcommand'
        authorization = Authorization()
        authentication = IpBasedAuthentication()
        validation = ExecutionStatusValidation()
        filtering = {
            "execution_status": 'exact',
            "job_id": 'exact',
        }

    # def override_urls(self):
    #     return [
    #         url(r'^%s/(?P<id>\d+)$', self.wrap_view('dispatch_detail'), name='api_workflowcommand_by_id'),
    #         # url(r'^%s/$' % self._meta.resource_name, self.wrap_view('dispatch_list'), name="api_workflowcommand_all"),
    #         # url(r'^%s/schema$' % self._meta.resource_name, self.wrap_view('get_schema'), name="api_workflowcommand_schema"),
    #     ]

    def get_resource_uri(self, bundle_or_obj=None, url_name='api_dispatch_list'):
        return '/api/v1/%s/' % (self._meta.resource_name)