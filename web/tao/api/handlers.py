from piston.handler import BaseHandler
from tao.models import Job

class JobHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT',)
    model = Job
    def read(self, request, id=None):
        base = Job.objects

        if id:
            return base.get(pk=id)
        else:
            return base.all()
