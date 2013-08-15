from django.conf.urls import patterns, url

urlpatterns = patterns('tap.views',
    url(r'^$',                                               'tap'),
    url(r'^tables$',                                         'tables'),
    url(r'^capabilities$',                                   'capabilities'),
    url(r'^availability$',                                   'availability'),
    url(r'^query$',                                          'query'),
    url(r'^sync$',                                           'sync'),
    url(r'^async$',                                          'async'),
    url(r'^async/(?P<id>\d+)$',                              'job'),
    url(r'^async/(?P<id>\d+)/phase$',                        'phase'),
    url(r'^async/(?P<id>\d+)/quote$',                        'quote'),
    url(r'^async/(?P<id>\d+)/termination$',                  'termination'),
    url(r'^async/(?P<id>\d+)/destruction$',                  'destruction'),
    url(r'^async/(?P<id>\d+)/owner$',                        'owner'),
    url(r'^async/(?P<id>\d+)/error$',                        'error'),
    url(r'^async/(?P<id>\d+)/params$',                       'params'),
    url(r'^async/(?P<id>\d+)/results$',                      'results'),
    url(r'^async/(?P<id>\d+)/results/result/(?P<file>\w+)$', 'result'),
)

