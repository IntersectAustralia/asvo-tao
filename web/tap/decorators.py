import base64
from django.http import HttpResponse
from django.contrib.sites.models import Site
from django.contrib.auth import authenticate, login
from django.http import HttpResponseBadRequest, Http404
from django.core.exceptions import PermissionDenied
from tao.models import Job

def tap_job_submission_request(function):
    """ Decorator for the TAP job submission that requires 
        doQuery and QUERY in the POST data
    """
    def actual_decorator(request, *args, **kwargs):
        if ('REQUEST' not in request.POST) or (request.POST['REQUEST'] != 'doQuery'):
            return HttpResponseBadRequest('Request is missing')
    
        if 'QUERY' not in request.POST:
            return HttpResponseBadRequest('Query is missing')
        
        return function(request, *args, **kwargs)
        
    return actual_decorator

def http_auth(function):
    """ Decorator that requires Basic HTTP authentication
    """
    def actual_decorator(request, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2:
                if auth[0].lower() == "basic":
                    uname, passwd = base64.b64decode(auth[1]).split(':')
                    user = authenticate(username=uname, password=passwd)
                    if user is not None:
                        if user.is_active:
                            login(request, user)
                            return function(request, *args, **kwargs)
                    
        return HttpResponseNotAuthorized(HttpResponse)
        
    return actual_decorator
    
class HttpResponseNotAuthorized(HttpResponse):
    """ Basic HTTP authentication response 
    """
    status_code = 401
    def __init__(self, redirect_to):
        HttpResponse.__init__(self)
        self['WWW-Authenticate'] = 'Basic realm="%s"' % Site.objects.get_current().name
        
def access_job(function):
    """ Decorator to check if job exists and if the user has access to it, then 
        add the job to the function arguments
    """
    def actual_decorator(request, *args, **kwargs):
        try:
            job = Job.objects.get(id=kwargs['id'])
        except Job.DoesNotExist:
            raise Http404
        
        if not job.can_read_job(request.user):
            raise PermissionDenied
        
        kwargs['job'] = job
        
        return function(request, *args, **kwargs)
        
    return actual_decorator        

