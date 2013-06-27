from django.conf.urls.defaults import patterns, url, include
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect

from piston.resource import Resource

from tao.api.handlers import JobHandler


class IpBasedAuthenticator(object):
    def is_authenticated(self, request):
        ip_addr = request.META.get('REMOTE_ADDR')
        return ip_addr in settings.API_ALLOWED_IPS
    
    def challenge(self):
        return redirect(reverse_lazy('tao.views.handle_403'))
    
ip_auth = IpBasedAuthenticator()
job_handler = Resource(JobHandler, authentication=ip_auth)

urlpatterns = (
    url(r'jobs/status/(?P<status>.+)$', job_handler, name='api_jobs_by_status'),
    url(r'jobs/(?P<id>\d+)$', job_handler, name='api_jobs_by_id'),
    url(r'jobs/$', job_handler, name='api_jobs'),
)
