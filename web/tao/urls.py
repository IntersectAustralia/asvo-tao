"""
==================
tao.urls
==================

Django's URL mapping definition
"""
from django.conf.urls import patterns, url, include
from django.contrib.auth.views import logout, password_reset, password_reset_done, password_change_done
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

from tastypie.api import Api
from tao.api.resources import WorkflowCommandResource, JobResource, TaoUserResource, WFJobResource
from tao.api.resources import PowerJobResource
from tao.forms import PasswordResetForm
from tao.views import password_change

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
    url(r'account_status/$', 'tao.views.account_status', name='account_status'),
    url(r'support_page/$', 'tao.views.support', name='support_page'),
    url(r'fail/$', 'tao.views.fail', name='failurl'),
)

mock_galaxy_factory_patterns = patterns('tao.views.mock_galaxy_factory',
    url(r'^$', 'index', name='mock_galaxy_factory'),
)

job_patterns = patterns('tao.views.jobs',
    url(r'^$', 'index', name='job_index'),
    url(r'^(?P<id>\d+)$', 'view_job', name='view_job'),
    url(r'^(?P<id>\d+)/file/(?P<file_path>.+)$', 'get_file', name='get_file'),
    url(r'^(?P<id>\d+)/download_zip$', 'get_zip_file', name='get_zip_file'),
    url(r'^(?P<id>\d+)/download_tar$', 'get_tar_file', name='get_tar_file'),
    url(r'^(?P<id>\d+)/basic_tar$', 'basic_tar_file', name='basic_tar_file'),
    url(r'^(?P<id>\d+)/summary_txt$', 'get_summary_txt_file', name='get_summary_txt_file'),
    url(r'^stop_job/(?P<id>\d+)$', 'stop_job', name='stop_job'),
    url(r'^rerun_job/(?P<id>\d+)$', 'rerun_job', name='rerun_job'),
    url(r'^release_job/(?P<id>\d+)$', 'release_job', name='release_job'),
    url(r'^delete_job_output/(?P<id>\d+)$', 'delete_job_output', name='delete_job_output'),
    url(r'^refresh_disk_usage/(?P<id>\d+)$', 'refresh_disk_usage', name='refresh_disk_usage'),
)

json_patterns = patterns('tao.json.views',
    ## url(r'^snapshots/(?P<sid>\d+),(?P<gid>\d+)$', 'snapshots', name='json_snapshots'),
    ## url(r'^simulation/(?P<id>\d+)$', 'simulation', name='json_simulation'),
    # url(r'^galaxy_model/(?P<id>\d+)$', 'galaxy_model', name='json_galaxy_model'),
    # url(r'^galaxy_models/(?P<id>\d+)$', 'galaxy_models', name='json_galaxy_models'),
    # url(r'^filters/(?P<id>\d+)$', 'filters', name='json_filters'),
    # url(r'^output_choices/(?P<id>\d+)$', 'output_choices', name='json_output_choices'),
    # url(r'^stellar_model/(?P<id>\d+)$', 'stellar_model', name='json_stellar_model'),
    # url(r'^dust_model/(?P<id>\d+)$', 'dust_model', name='json_dust_model'),
    ## url(r'^global_parameter/(?P<parameter_name>[-\w]+)/$', 'global_parameter', name='json_global_parameter'),
    # url(r'^bandpass_filters/', 'bandpass_filters', name='json_bandpass_filters'),
    # url(r'^dataset/(?P<id>\d+)$', 'dataset', name='json_dataset'),
    url(r'^$', 'bad_request', name='json_ctx'),
    url(r'^edit_job_description/(?P<id>\d+)$', 'edit_job_description', name='edit_job_description'),
)

v1_api = Api(api_name='v1')
v1_api.register(WorkflowCommandResource())
v1_api.register(JobResource())
v1_api.register(PowerJobResource())
v1_api.register(TaoUserResource())
v1_api.register(WFJobResource())

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
    url(r'^api/', include(v1_api.urls)),
    url(r'^assets/(?P<path>.+)$', 'tao.assets.asset_handler', name='asset'),

    url(r'^accounts/password/reset/$', password_reset,
        {'post_reset_redirect': reverse_lazy('password_reset_done'), 'password_reset_form': PasswordResetForm},
        name="password_reset"),
    url(r'^accounts/password/reset/done/$', password_reset_done, name='password_reset_done'),
    url(r'^accounts/password/change/$', password_change, {'post_change_redirect': reverse_lazy('password_change_done')},
        name='password_change'),
    url(r'^accounts/password/change/done/$', password_change_done, name='password_change_done'),

    ('^tap/', include('tap.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

urlpatterns += staticfiles_urlpatterns()
