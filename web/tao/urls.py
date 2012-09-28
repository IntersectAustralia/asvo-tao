from django.conf.urls.defaults import patterns, url, include
from django.conf import settings
from django.contrib.auth.views import logout
from django.core.urlresolvers import reverse_lazy

from django.contrib import admin
admin.autodiscover()

from django.shortcuts import render

from tao.models import Job

simple_view = lambda request, template_name: render(request, template_name)

administration_patterns = patterns('',
    url(r'^$', 'tao.views.admin_index', name='admin_index'),
    url(r'^access_requests$', 'tao.views.access_requests', name='access_requests'),
    url(r'^approve_user/(?P<user_id>\d+)$', 'tao.views.approve_user', name='approve_user'),
    url(r'^reject_user/(?P<user_id>\d+)$', 'tao.views.reject_user', name='reject_user'),
)

account_patterns = patterns('',
    url(r'login/$', 'tao.views.login', name='login'),
    url(r'logout/$', logout, {'next_page': reverse_lazy('home')}, name='logout'),
    url(r'register/$', 'tao.views.register', name='register'),
)

mock_galaxy_factory_patterns = patterns('tao.views.mock_galaxy_factory',
    url(r'^$', 'index', name='mock_galaxy_factory'),
    url(r'^my_jobs_with_status/(?P<status>.*)$', 'my_jobs_with_status'),
    url(r'^my_jobs_with_status/$', 'my_jobs_with_status', name='all_jobs'),
    url(r'^my_jobs_with_status/SUBMITTED$', 'my_jobs_with_status', {'status': Job.SUBMITTED}, name='submitted_jobs'),
    url(r'^my_jobs_with_status/IN_PROGRESS$', 'my_jobs_with_status', {'status': Job.IN_PROGRESS}, name='in_progress_jobs'),
    url(r'^my_jobs_with_status/QUEUED', 'my_jobs_with_status', {'status': Job.QUEUED}, name='queued_jobs'),
    url(r'^my_jobs_with_status/COMPLETED', 'my_jobs_with_status', {'status': Job.QUEUED}, name='completed_jobs'),

    url(r'^fake_a_job$', 'fake_a_job', name='fake_a_job'),
)

job_patterns = patterns('tao.views.jobs',
    url(r'^$', 'index', name='job_index'),
    url(r'^(?P<id>\d+)$', 'view_job', name='view_job'),
    url(r'^(?P<id>\d+)/file/(?P<filepath>.+)$', 'get_file', name='get_file'),
)

urlpatterns = patterns('',
    ('^admin/', include(admin.site.urls)),
    ('^accounts/', include(account_patterns)),
    ('^administration/', include(administration_patterns)),
    ('^mock_galaxy_factory/', include(mock_galaxy_factory_patterns)),
    ('^jobs/', include(job_patterns)),

    url(r'^mgf/$', simple_view, {'template_name': 'mgf.html'}),
    url(r'^$', 'tao.views.home', name='home'),
    url(r'^api/', include('tao.api.urls')),


    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
