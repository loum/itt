from django.conf.urls.defaults import patterns, include, url
from test.api import CheckpointResource

checkpoint_resource = CheckpointResource()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'control.views.home', name='home'),
    # url(r'^control/', include('control.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^test/', include(checkpoint_resource.urls)),
)
