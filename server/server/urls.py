from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'server.views.home', name='home'),
    url(r'', include('cobalt.urls')),
    url(r'^coffee/', include(admin.site.urls)),
)
