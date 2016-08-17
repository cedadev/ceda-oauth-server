# -*- coding: utf-8 -*-
"""
Registration of models with the admin interface.
"""

from django.contrib import admin
from django.contrib.admin.sites import NotRegistered

from .models import RestrictedApplication
from .forms import RestrictedApplicationForm

try:
    admin.site.unregister(RestrictedApplication)
except NotRegistered:
    pass
@admin.register(RestrictedApplication)
class RestrictedApplicationAdmin(admin.ModelAdmin):
    form = RestrictedApplicationForm
