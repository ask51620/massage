"""massage_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
##from connect.views import connect
from connect.views import fb_webhook, send_ssl_file, certificate
urlpatterns = [
##    url(r'^admin/', admin.site.urls),
##    url(r'^webhook/', connect),
##    url(r'^\w+', connect),
    url(r'^.well-known/acme-challenge/xxxxxxxx$', send_ssl_file),
    url(r'^fb_webhook$', fb_webhook.as_view()),
    url(r'^certificate$', certificate)
    
]
