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
from django_wsgi.embedded_wsgi import call_wsgi_app
from oauth2_provider.decorators import protected_resource
from oauth2_provider import views as oauth_views

from userdb_model.models import User


# Use Paste Deploy to create the online ca app
onlineca_app = loadapp(settings.ONLINECA_PASTEDEPLOY_CONF)

@protected_resource(scopes = [settings.CERTIFICATE_SCOPE])
@csrf_exempt
def onlineca_view(request, path_info):
    # Try to retrieve the openid for the user
    if request.user.is_authenticated():
        try:
            ceda_user = User.objects.get(accountid = request.user.username)
        except User.DoesNotExist:
            pass
        else:
            request.environ['OPENID'] = ceda_user.openid
    return call_wsgi_app(onlineca_app, request, path_info)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # The OnlineCA app provides oauth/trustroots/ and oauth/certificate/
    # This pattern can't be in the include below as we need to capture the
    # leading slash to pass to the underlying WSGI app
    url(r'^oauth(/trustroots/|/certificate/)$', onlineca_view, name = 'ca_server'),
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
