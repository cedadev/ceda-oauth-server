"""
Registration of admin interface components. This module overrides the model admin's
from the oauth2_provider to be a bit friendlier.
"""

__author__ = "Matt Pryor"
__copyright__ = "Copyright 2015 UK Science and Technology Facilities Council"

from django.contrib import admin
from django.contrib.admin.sites import NotRegistered

from oauth2_provider.models import Grant, AccessToken, RefreshToken


try:
    admin.site.unregister(Grant)
except NotRegistered:
    pass

@admin.register(Grant)
class GrantAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'application', 'expires')
    list_filter = ('application', )
    search_fields = ('user__username', 'code')


try:
    admin.site.unregister(AccessToken)
except NotRegistered:
    pass

@admin.register(AccessToken)
class AccessTokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'user', 'application', 'expires')
    list_filter = ('application', )
    search_fields = ('user__username', 'token')


try:
    admin.site.unregister(RefreshToken)
except NotRegistered:
    pass

@admin.register(RefreshToken)
class RefreshTokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'user', 'application', 'access_token')
    list_filter = ('application', )
    search_fields = ('user__username', 'token', 'access_token__token')
