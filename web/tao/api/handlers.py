from piston.handler import BaseHandler
from tao.models import Job, WorkflowCommand

class JobHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT',)
    model = Job

    fields = ('id', 'username', 'database', 'status', 'parameters', 'error_message')

    def read(self, request, id=None, status=None):
        base = Job.objects

        if id:
            return base.get(pk=id)
        elif status:
            return base.filter(status__iexact=status)
        else:
            return base.all()

class WorkflowCommandHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT',)
    model = WorkflowCommand

    def job_stop_all(self, request, id=None, status=None):
        base = Job.objects

        if id:
            return base.get(pk=id)
        elif status:
            return base.filter(status__iexact=status)
        else:
            return base.all()
