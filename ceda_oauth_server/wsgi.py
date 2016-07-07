# -*- coding: utf-8 -*-
"""
WSGI config for the CEDA OAuth2 Server.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

import django
import django_wsgi.handler

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ceda_oauth_server.settings")

django.setup()
application = django_wsgi.handler.APPLICATION
