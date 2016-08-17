# -*- coding: utf-8 -*-
"""
Module providing a form for applications.
"""

from django import forms

from oauth2_provider.settings import oauth2_settings

from .models import RestrictedApplication


class RestrictedApplicationForm(forms.ModelForm):
    class Meta:
        model = RestrictedApplication
        fields = ('client_id', 'user', 'redirect_uris', 'client_type',
                  'authorization_grant_type', 'client_secret', 'name')

    allowed_scopes = forms.MultipleChoiceField(
        choices = oauth2_settings.SCOPES.items(),
        widget = forms.CheckboxSelectMultiple,
        initial = oauth2_settings.DEFAULT_SCOPES
    )
