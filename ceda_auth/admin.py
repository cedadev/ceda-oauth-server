"""
Registration of admin interface components. This module overrides the model admin's
from the oauth2_provider to be a bit friendlier.
"""

__author__ = "Matt Pryor"
__copyright__ = "Copyright 2018 UK Science and Technology Facilities Council"

from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.db import models

from oauth2_provider.models import Grant, AccessToken, RefreshToken

from userdb_model.models import User


class _HasJASMINAccount(admin.SimpleListFilter):
    title = 'has JASMIN account'
    parameter_name = 'has_jasmin_account'

    OPTION_YES = '1'
    OPTION_NO = '0'

    def lookups(self, request, model_admin):
        return (
            (self.OPTION_YES, 'Yes'),
            (self.OPTION_NO, 'No'),
        )

    def queryset(self, request, queryset):
        has_jasmin_account = models.Q(jasminaccountid__isnull = False)  \
                           & ~models.Q(jasminaccountid__iexact = '')
        if self.value() == self.OPTION_YES:
            return queryset.filter(has_jasmin_account)
        elif self.value() == self.OPTION_NO:
            return queryset.filter(~has_jasmin_account)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('accountid', 'jasminaccountid')
    list_filter = (_HasJASMINAccount, )
    fields = ('accountid', 'jasminaccountid')
    readonly_fields = ('accountid', )
    ordering = ('accountid', )
    search_fields = ('accountid', 'jasminaccountid')


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
