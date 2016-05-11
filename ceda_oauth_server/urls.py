"""
URL configuration for the CEDA OAuth2 Server.
"""

__author__ = "Matt Pryor"
__copyright__ = "Copyright 2015 UK Science and Technology Facilities Council"

from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from paste.deploy import loadapp
from oauth2_provider.decorators import protected_resource
from django_wsgi.embedded_wsgi import make_wsgi_view

# Use Paste Deploy to create the online ca app
onlineca_app = loadapp(settings.ONLINECA_PASTEDEPLOY_CONF)
# Create a Django view from the WSGI app
onlineca_app = make_wsgi_view(onlineca_app)
# Protect the resource with OAuth
onlineca_app = protected_resource()(onlineca_app)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^oauth/', include('oauth2_provider.urls', namespace = 'oauth2_provider')),
    url(r'^accounts/login$', auth_views.login, name = 'accounts_login'),
    url(r'^accounts/logout$', auth_views.logout,
                              { 'next_page' : settings.LOGIN_URL }, name = 'accounts_logout'),
    # Mount the OnlineCA server app at /api/*
    url(r'^api(/.*)$', onlineca_app, name = 'ca_server'),
]
