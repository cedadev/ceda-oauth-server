# -*- coding: utf-8 -*-
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
from django.views.decorators.csrf import csrf_exempt

from paste.deploy import loadapp
from django_wsgi.embedded_wsgi import make_wsgi_view
from oauth2_provider.decorators import protected_resource
from oauth2_provider import views as oauth_views


# Use Paste Deploy to create the online ca app
onlineca_app = loadapp(settings.ONLINECA_PASTEDEPLOY_CONF)
# Create a Django view from the WSGI app
onlineca_app = make_wsgi_view(onlineca_app)
# Make the app exempt from CSRF
onlineca_app = csrf_exempt(onlineca_app)
# Protect the resource with OAuth
onlineca_app = protected_resource(scopes = [settings.CERTIFICATE_SCOPE])(onlineca_app)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # The OnlineCA app provides oauth/trustroots/ and oauth/certificate/
    # This pattern can't be in the include below as we need to capture the
    # leading slash to pass to the underlying WSGI app
    url(r'^oauth(/trustroots/|/certificate/)$', onlineca_app, name = 'ca_server'),
    # We only provide the token-issuing OAuth URLs, and at custom endpoints
    # Applications are managed only via the admin interface
    url(r'^oauth/', include([
        url(r'^authorize$', oauth_views.AuthorizationView.as_view(), name="authorize"),
        url(r'^access_token$', oauth_views.TokenView.as_view(), name="token"),
        url(r'^revoke_token/$', oauth_views.RevokeTokenView.as_view(), name="revoke-token"),
    ])),
    url(r'^accounts/login$', auth_views.login, name = 'accounts_login'),
    url(r'^accounts/logout$', auth_views.logout,
                              { 'next_page' : settings.LOGIN_URL }, name = 'accounts_logout'),
]
