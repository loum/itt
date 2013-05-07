from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings

from test.api import (NodeResource,
                      CheckpointResource)

node_resource = NodeResource()
checkpoint_resource = CheckpointResource()

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^config/$', 'config.views.index'),
    url(r'^server/$', 'server.views.index'),
    url(r'^server/insert', 'server.views.insert'),
    url(r'^testconfig/$', 'test_config.views.index'),
    url(r'^testconfig/update/$', 'test_config.views.update'),
    url(r'^testconfig/delete/$', 'test_config.views.delete'),
    url(r'^test/', include(node_resource.urls)),
    url(r'^test/', include(checkpoint_resource.urls)),

    # The following patterns are a temporary hack to enable
    # access to the ITT docs via the Django test server.
    url(r'^docs/$',
        'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT,
         'path': 'index.html'}),
    url(r'^docs/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
