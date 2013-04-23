from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

from test.api import (NodeResource,
                      CheckpointResource)

node_resource = NodeResource()
checkpoint_resource = CheckpointResource()

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^test/', include(node_resource.urls)),
    url(r'^test/', include(checkpoint_resource.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
