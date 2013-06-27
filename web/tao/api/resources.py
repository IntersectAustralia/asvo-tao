from tastypie.resources import ModelResource
from tao.models import WorkflowCommand

class WorkflowCommandResource(ModelResource):
    class Meta:
        queryset = WorkflowCommand.objects.all()
        fields = ['id', 'jobid', 'submittedby', 'command', 'parameters', 'execution_status', 'execution_comment']
        allowed_methods = ['get', 'put']
        filtering = {
            "execution_status": 'exact',
        }