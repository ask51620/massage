from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from welcome.views import index, health
from connect.views import fb_webhook, send_ssl_file, certificate

urlpatterns = [
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', index),
    url(r'^health$', health),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
        url(r'^.well-known/acme-challenge/xxxxxxxx$', send_ssl_file),
        url(r'^fb_webhook$', fb_webhook.as_view()),
        url(r'^certificate$', certificate),
    ] + urlpatterns
