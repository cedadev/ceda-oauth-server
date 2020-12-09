# -*- coding: utf-8 -*-
"""
URL configuration for the CEDA OAuth2 Server.
"""

__author__ = "Matt Pryor"
__copyright__ = "Copyright 2018 UK Science and Technology Facilities Council"

import functools

from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.utils.decorators import decorator_from_middleware
from django.contrib.auth import get_user_model

from oauth2_provider import views as oauth_views

from dj_security_middleware.middleware import DJSecurityMiddleware


# The *only* view that requires interactive login is the OAuth authorize view
# Even though code exists in this project to authenticate a CEDA user for Basic
# auth, we want to use dj-security-middleware for this so that the user:
#   (1) Doesn't have to log in again if already signed in
#   (2) Gets the proper login page
dj_security = decorator_from_middleware(DJSecurityMiddleware)

def ceda_user_to_django_user(view):
    """
    Decorator that converts the authenticated_user from the dj-security-middleware
    into a Django user that the application can use.
    """
    @functools.wraps(view)
    def wrapper(request, *args, **kwargs):
        # If the user gets to here, we know that they are an authenticated CEDA user
        # So just create the corresponding local user with the same username
        username = request.authenticated_user['userid']
        UserModel = get_user_model()
        try:
            request.user = UserModel.objects.get(username = username)
        except UserModel.DoesNotExist:
            request.user = UserModel.objects.create_user(username)
        return view(request, *args, **kwargs)
    return wrapper

# Wrap the authorization view in the decorators
oauth_authorize = dj_security(ceda_user_to_django_user(oauth_views.AuthorizationView.as_view()))


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # We only provide the token-issuing OAuth URLs from oauth2_provider at custom endpoints
    # Applications are managed only via the admin interface
    url(r'^oauth/', include([
        url(r'^authorize$', oauth_authorize, name="authorize"),
        url(r'^access_token$',
            oauth_views.TokenView.as_view(),
            name="token"),
    ])),
    # Include profile oauth endpoints
    url(r'^oauth/', include('ceda_auth.urls')),
    # Include urls for the Online CA
    url(r'^', include('ceda_onlineca.urls')),
]
