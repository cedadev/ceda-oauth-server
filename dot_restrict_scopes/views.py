# -*- coding: utf-8 -*-
"""
Module providing a customised authorization view that limits the scopes an
application can ask for.
"""

import logging

from oauth2_provider.views import AuthorizationView as BaseAuthorizationView

from .models import RestrictedApplication


_log = logging.getLogger(__name__)


class AuthorizationView(BaseAuthorizationView):
    def _restrict_scopes(self, credentials, scopes):
        """
        Returns the subset of the given ``scopes`` that the application specified in
        ``credentials`` is allowed to access.

        Also logs any requested scopes that are not allowed for an application.
        """
        app = RestrictedApplication.objects.get(client_id = credentials['client_id'])
        scopes_set = set(scopes)
        # Log any scopes that were requested that aren't allowed for the application
        not_allowed = scopes_set.difference(app.allowed_scopes)
        if not_allowed:
            _log.warning("Application %s requested disallowed scopes (%s)",
                         app.client_id, ' '.join(not_allowed))
        # Restrict the scopes to the allowed scopes
        return list(scopes_set.intersection(app.allowed_scopes))

    def validate_authorization_request(self, request):
        # Override this method to limit the scopes presented for authorization
        # to those allowed for the application
        scopes, credentials = super(AuthorizationView, self).validate_authorization_request(request)
        return self._restrict_scopes(credentials, scopes), credentials

    def create_authorization_response(self, request, scopes, credentials, allow):
        # Override this method to limit the scopes in the authorization response
        # to those allowed for the application
        scopes = ' '.join(self._restrict_scopes(credentials, scopes.split()))
        return super(AuthorizationView, self).create_authorization_response(request, scopes, credentials, allow)
