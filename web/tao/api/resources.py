from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tao.models import WorkflowCommand


class WorkflowCommandResource(ModelResource):

    class Meta:
        queryset = WorkflowCommand.objects.all()
        fields = ['id', 'jobid', 'submittedby', 'command', 'parameters', 'execution_status', 'execution_comment']
        allowed_methods = ['get', 'put']
        authorization = Authorization()
        filtering = {
            "execution_status": 'exact',
            "jobid": 'exact',
        }