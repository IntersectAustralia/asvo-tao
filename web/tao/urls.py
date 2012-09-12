from django.conf.urls.defaults import patterns, url, include
from django.conf import settings
from django.core.urlresolvers import reverse_lazy

from django.shortcuts import render

from django.contrib import admin
admin.autodiscover()

from django.contrib.auth.views import logout

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
    url(r'^submitted_jobs$', 'submitted_jobs', name='submitted_jobs'),
)

tao_patterns = patterns('',
    ('^admin/', include(admin.site.urls)),
    ('^accounts/', include(account_patterns)),
    ('^administration/', include(administration_patterns)),
    ('^mock_galaxy_factory/', include(mock_galaxy_factory_patterns)),

    url(r'^mgf/$', simple_view, {'template_name': 'mgf.html'}),
    url(r'^$', 'tao.views.home', name='home'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

urlpatterns = patterns('',
    ('', include(tao_patterns)),
)
