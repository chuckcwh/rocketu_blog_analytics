from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^analytics/$', 'analytics.views.main', name='main'),
    url(r'^analytics/page_map/(\d+)/$', 'analytics.views.page_map', name='page_map'),

    # ajax call
    url(r'^analytics/page_map_ajax/$', 'analytics.views.page_map_ajax', name='page_map_ajax')
)