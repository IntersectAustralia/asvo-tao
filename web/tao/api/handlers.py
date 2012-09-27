from piston.handler import BaseHandler
from tao.models import Job

class JobHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT',)
    model = Job

    exclude = ()  # We want to show id - the BaseHandler excludes it by default

    def read(self, request, id=None, status=None):
        base = Job.objects

        if id:
            return base.get(pk=id)
        elif status:
            return base.filter(status=status)
        else:
            return base.all()
