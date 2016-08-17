# -*- coding: utf-8 -*-
"""
Module providing the custom ``django-oauth-toolkit`` application model.
"""

from django.db import models
from django.contrib.postgres.fields import ArrayField

from oauth2_provider.settings import oauth2_settings
from oauth2_provider.models import AbstractApplication


class RestrictedApplication(AbstractApplication):
    """
    Application implementation where the allowed scopes are specified on a
    per-application basis.
    """
    allowed_scopes = ArrayField(models.CharField(max_length = 250))
