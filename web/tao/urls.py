"""
==================
tao.urls
==================

Django's URL mapping definition
"""
from django.conf.urls import patterns, url, include
from django.contrib.auth.views import logout
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()

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
    url(r'support_page/$', 'tao.views.support', name='support_page'),
)

mock_galaxy_factory_patterns = patterns('tao.views.mock_galaxy_factory',
    url(r'^$', 'index', name='mock_galaxy_factory'),
    url(r'^fake_a_job$', 'fake_a_job', name='fake_a_job'),
)

job_patterns = patterns('tao.views.jobs',
    url(r'^$', 'index', name='job_index'),
    url(r'^(?P<id>\d+)$', 'view_job', name='view_job'),
    url(r'^(?P<id>\d+)/file/(?P<filepath>.+)$', 'get_file', name='get_file'),
    url(r'^(?P<id>\d+)/download_zip$', 'get_zip_file', name='get_zip_file'),
)

json_patterns = patterns('tao.json.views',
    url(r'^snapshots/(?P<sid>\d+),(?P<gid>\d+)$', 'snapshots', name='json_snapshots'),
    url(r'^simulation/(?P<id>\d+)$', 'simulation', name='json_simulation'),
    url(r'^galaxy_model/(?P<id>\d+)$', 'galaxy_model', name='json_galaxy_model'),
    url(r'^galaxy_models/(?P<id>\d+)$', 'galaxy_models', name='json_galaxy_models'),
    url(r'^filters/(?P<id>\d+)$', 'filters', name='json_filters'),
    url(r'^output_choices/(?P<id>\d+)$', 'output_choices', name='json_output_choices'),
    url(r'^stellar_model/(?P<id>\d+)$', 'stellar_model', name='json_stellar_model'),
    url(r'^dust_model/(?P<id>\d+)$', 'dust_model', name='json_dust_model'),
    url(r'^global_parameter/(?P<parameter_name>[-\w]+)/$', 'global_parameter', name='json_global_parameter'),
    url('^bandpass_filters/', 'bandpass_filters', name='json_bandpass_filters'),
    url(r'^$', 'bad_request', name='json_ctx'),
)

urlpatterns = patterns('',
    ('^admin/', include(admin.site.urls)),
    ('^accounts/', include(account_patterns)),
    ('^administration/', include(administration_patterns)),
    ('^mock_galaxy_factory/', include(mock_galaxy_factory_patterns)),
    ('^jobs/', include(job_patterns)),
    ('^json/', include(json_patterns)),

    ('^403.html$', 'tao.views.handle_403'),

    url(r'^mgf/$', simple_view, {'template_name': 'mgf.html'}),
    url(r'^$', 'tao.views.home', name='home'),
    url(r'^api/', include('tao.api.urls')),
    url(r'^assets/(?P<path>.+)$', 'tao.assets.asset_handler', name='asset'),


    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

urlpatterns += staticfiles_urlpatterns()