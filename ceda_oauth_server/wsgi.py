# -*- coding: utf-8 -*-
"""
WSGI config for the CEDA OAuth2 Server.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os


from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ceda_oauth_server.settings")
application = get_wsgi_application()
