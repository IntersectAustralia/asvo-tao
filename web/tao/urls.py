import tao.views

from django.conf.urls.defaults import patterns, url, include
from django.conf import settings
from django.core.urlresolvers import reverse, reverse_lazy

from django.contrib import admin
admin.autodiscover()

from django.contrib.auth.views import login, logout

tao_patterns = patterns('',
    # Example:
    # (r'^{{ project_name }}/', include('{{ project_name }}.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'tao.views.home', name='home'),
)

account_patterns = patterns('',
    url(r'login/$', login, name='login'),
    url(r'logout/$', logout, {'next_page': reverse_lazy('home')}, name='logout'),
    url(r'register/$', tao.views.register, name='register'),
)

tao_patterns += patterns('',
    ('^accounts/', include(account_patterns)),
)

urlpatterns = patterns('',
    ('', include(tao_patterns)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
