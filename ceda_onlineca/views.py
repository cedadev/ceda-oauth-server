# -*- coding: utf-8 -*-
"""
Views for the CEDA Online CA app.
"""

__author__ = "Matt Pryor"
__copyright__ = "Copyright 2018 UK Science and Technology Facilities Council"

import functools
import base64

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import decorator_from_middleware
from django.http import HttpResponse
from django.contrib.auth import authenticate

from oauth2_provider.decorators import protected_resource
from oauth2_provider.middleware import OAuth2TokenMiddleware

from onlineca import views as onlineca_views

from userdb_model.models import User


# Decorator that checks the request for a valid OAuth token
require_oauth_token = decorator_from_middleware(OAuth2TokenMiddleware)


@require_oauth_token
@protected_resource(scopes = [settings.CERTIFICATE_SCOPE])
@require_POST
@csrf_exempt
def certificate_oauth(request):
    """
    Certificate view that is protected by OAuth login.
    """
    return onlineca_views.certificate(request)


def require_http_basic_auth(view):
    """
    Decorator that looks for a HTTP Basic Auth header and authenticates the user
    for this single request.
    If a HTTP Basic Auth header is not present, the user is rejected.
    """
    @functools.wraps(view)
    def _decorated(request, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' in request.META:
            authmeth, auth_b64 = request.META['HTTP_AUTHORIZATION'].split(' ', 1)
            if authmeth.lower() == 'basic':
                # Decode the base64 encoded string
                auth = base64.b64decode(auth_b64.strip().encode()).decode()
                username, password = auth.split(':', 1)
                user = authenticate(username = username, password = password)
                if user:
                    request.user = user
                    return view(request, *args, **kwargs)
        # If auth failed, send back a 401 with a challenge
        response = HttpResponse(status = 401)
        response['WWW-Authenticate'] = 'Basic realm="%s"' % settings.BASIC_AUTH_REALM
        return response
    return _decorated


@require_http_basic_auth
@require_POST
@csrf_exempt
def certificate_basicauth(request):
    """
    Certificate view that is protected by Basic Auth login.
    """
    return onlineca_views.certificate(request)
