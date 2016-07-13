"""
Views for the Online CA app. These are wrappers around the Online CA WSGI app.
"""

__author__ = "Matt Pryor"
__copyright__ = "Copyright 2015 UK Science and Technology Facilities Council"

import functools

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_safe, require_POST
from django.utils.decorators import decorator_from_middleware
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate

from paste.deploy import loadapp
from django_wsgi.embedded_wsgi import call_wsgi_app
from oauth2_provider.decorators import protected_resource
from oauth2_provider.middleware import OAuth2TokenMiddleware

from userdb_model.models import User


# Use Paste Deploy to create the online ca app
onlineca_app = loadapp(settings.ONLINECA_PASTEDEPLOY_CONF)


@require_safe
def trustroots(request):
    """
    Django view that calls the OnlineCA WSGI app with ``/trustroots/`` as the
    path info.
    """
    return call_wsgi_app(onlineca_app, request, '/trustroots/')


def certificate(request):
    """
    Django view that calls the OnlineCA WSGI app with ``/certificate/`` as the
    path info and the logged in user's openid in the environ.

    There must be a logged in user by some mechanism.
    """
    # The user must be authenticated
    if not request.user.is_authenticated():
        return HttpResponseForbidden()
    # Try to retrieve the openid for the user
    try:
        ceda_user = User.objects.get(accountid = request.user.username)
    except User.DoesNotExist:
        pass
    else:
        request.environ['OPENID'] = ceda_user.openid
    return call_wsgi_app(onlineca_app, request, '/certificate/')


#: Decorator that checks the request for a valid OAuth token
require_oauth_token = decorator_from_middleware(OAuth2TokenMiddleware)

@protected_resource(scopes = [settings.CERTIFICATE_SCOPE])
@require_oauth_token
@require_POST
@csrf_exempt
def certificate_oauth(request):
    """
    Certificate view that is protected by OAuth login.
    """
    return certificate(request)


def require_http_basic_auth(view):
    """
    Decorator that looks for a HTTP Basic Auth header and authenticates the user
    for this single request.

    If a HTTP Basic Auth header is not present, the user is rejected.
    """
    @functools.wraps(view)
    def _decorator(request, *args, **kwargs):
        if request.META.has_key('HTTP_AUTHORIZATION'):
            authmeth, auth = request.META['HTTP_AUTHORIZATION'].split(' ', 1)
            if authmeth.lower() == 'basic':
                username, password = auth.strip().decode('base64').split(':', 1)
                user = authenticate(username = username, password = password)
                if user:
                    request.user = user
                    return view(request, *args, **kwargs)
        return HttpResponseForbidden()
    return _decorator

@require_http_basic_auth
@require_POST
@csrf_exempt
def certificate_basicauth(request):
    """
    Certificate view that is protected by Basic Auth login.
    """
    return certificate(request)
