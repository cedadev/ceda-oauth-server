# -*- coding: utf-8 -*-
"""
Views for the Online CA app. These are wrappers around the Online CA WSGI app.
"""

__author__ = "Matt Pryor"
__copyright__ = "Copyright 2018 UK Science and Technology Facilities Council"

import functools, re

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_safe, require_POST
from django.utils.decorators import decorator_from_middleware
from django.http import (
    HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
)
from django.core.exceptions import ValidationError

from oauth2_provider.decorators import protected_resource
from oauth2_provider.middleware import OAuth2TokenMiddleware

from userdb_model.models import User


# Convert the OAuth token middleware into a view decorator
require_oauth_token = decorator_from_middleware(OAuth2TokenMiddleware)


def with_ceda_user(view):
    """
    View decorator that sets a keyword argument ``ceda_user`` to the associated
    ``userdb_model.models.User``.
    """
    @functools.wraps(view)
    def wrapper(request, *args, **kwargs):
        # The user must be authenticated
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        # If the user is successfully logged in, this should not fail
        kwargs['ceda_user'] = User.objects.get(accountid = request.user.username)
        return view(request, *args, **kwargs)
    return wrapper


@protected_resource(scopes = [settings.PROFILE_SCOPE])
@require_oauth_token
@csrf_exempt
@require_safe
@with_ceda_user
def profile(request, ceda_user):
    """
    Handler for ``/profile``. Responds to GET only.

    Returns a JSON response containing CEDA profile information for the logged in user.
    """
    return JsonResponse({
        'status' : 'success',
        'profile' : {
            'accountid' : ceda_user.accountid,
            'jasminaccountid' : ceda_user.jasminaccountid,
        },
    })


_JASMIN_ACCOUNT_ID_REGEX = '^[a-zA-Z][a-zA-Z0-9_-]+[a-zA-Z0-9]$'

@protected_resource(scopes = [settings.JASMIN_LINK_SCOPE])
@require_oauth_token
@csrf_exempt
@require_POST
@with_ceda_user
def jasmin_link(request, ceda_user):
    """
    Handler for ``/jasmin_link/``. Responds to POST only.

    Attempts to link the specified JASMIN account with the currently logged in CEDA account.
    """
    # The POST data must be present
    if 'jasminaccountid' not in request.POST:
        return JsonResponse(
            status = 400,
            data = {
                'status' : 'error',
                'error_message' : 'jasminaccountid must be present in POST data',
            }
        )
    jasminaccountid = request.POST['jasminaccountid'].strip()
    # Validate the jasmin account id
    if not re.match(_JASMIN_ACCOUNT_ID_REGEX, jasminaccountid):
        return JsonResponse(
            status = 400,
            data = {
                'status' : 'error',
                'error_message' : 'jasminaccountid did not match required format',
            }
        )
    # If the jasminaccountid is already linked to a different CEDA account, return
    # a 409 Conflict response
    if User.objects.filter(jasminaccountid__iexact = jasminaccountid)  \
                   .exclude(accountid = ceda_user.accountid)  \
                   .exists():
        return JsonResponse(
            status = 409,
            data = {
                'status' : 'error',
                'error_message' : 'JASMIN account is already linked with another CEDA account',
            }
        )
    # If the CEDA account is already linked to a different JASMIN account, return
    # a 409 Conflict response
    if ceda_user.jasminaccountid and ceda_user.jasminaccountid != jasminaccountid:
        return JsonResponse(
            status = 409,
            data = {
                'status' : 'error',
                'error_message' : 'CEDA account is already linked with another JASMIN account',
            }
        )
    # Update the jasminaccountid directly, to avoid changing any other fields accidentally
    User.objects.filter(accountid = ceda_user.accountid).update(jasminaccountid = jasminaccountid)
    return JsonResponse({
        'status' : 'success',
        'message' : 'JASMIN account linked successfully',
    })
