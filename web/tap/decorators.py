import base64
from django.http import HttpResponse
from django.contrib.sites.models import Site
from django.contrib.auth import authenticate, login
from django.http import HttpResponseBadRequest

def tap_job_submission_request(function):
    """ Decorator for the TAP job submission that requires 
        doQuery and QUERY in the POST data
    """
    def wrapper(request, *args, **kwargs):
        if ('REQUEST' not in request.POST) or (request.POST['REQUEST'] != 'doQuery'):
            return HttpResponseBadRequest('Request is missing')
    
        if 'QUERY' not in request.POST:
            return HttpResponseBadRequest('Query is missing')
        
        return function(request, *args, **kwargs)
        
    wrapper.__doc__ = function.__doc__
    wrapper.__name__ = function.__name__
    return wrapper

def http_auth_required(function):
    """ Decorator that requires HTTP Basic authentication
    """
    def wrapper(request, *args, **kwargs):
        return http_auth(request, function, *args, **kwargs)
        
    wrapper.__doc__ = function.__doc__
    wrapper.__name__ = function.__name__
    return wrapper
       
def http_auth(request, function, *args, **kwargs):
    """ Requires Apache directive WSGIPassAuthorization to be set 'On', or in .htaccess:
        RewriteRule ^(.*)$ django.fcgi/$1 [QSA,L,E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
    """ 
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

class HttpResponseNotAuthorized(HttpResponse):
    status_code = 401
    def __init__(self, redirect_to):
        HttpResponse.__init__(self)
        self['WWW-Authenticate'] = 'Basic realm="%s"' % Site.objects.get_current().name
        
        