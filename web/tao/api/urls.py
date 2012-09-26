from django.conf.urls.defaults import patterns, url, include
from django.conf import settings
from django.core.urlresolvers import reverse_lazy

from piston.resource import Resource

from tao.api.handlers import JobHandler

job_handler = Resource(JobHandler)

urlpatterns = (
    url(r'jobs/(?P<id>\d+)$', job_handler),
    url(r'jobs/$', job_handler),
)
