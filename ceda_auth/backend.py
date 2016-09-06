# -*- coding: utf-8 -*-
"""
Module containing an authentication backend that authenticates users using the
CEDA userdb.
"""

__author__ = "Matt Pryor"
__copyright__ = "Copyright 2016 UK Science and Technology Facilities Council"

import md5

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

from userdb_model.models import User


class CEDAUserDBBackend(ModelBackend):
    """
    Django authentication backend that uses the CEDA userdb model for authentication.
    """
    def authenticate(self, username = None, password = None, **kwargs):
        """
        Attempt to authenticate the given username/password combination.
        """
        if not username or not password:
            return None
        try:
            ceda_user = User.objects.get(accountid = username)
        except User.DoesNotExist:
            ceda_user = None
        # Try to find a local user for the username
        LocalUser = get_user_model()
        try:
            local_user = LocalUser.objects.get(username = username)
        except LocalUser.DoesNotExist:
            local_user = None
        if ceda_user:
            if not local_user:
                # If there is a CEDA user but no local user, create the user even
                # if the password is wrong
                local_user = LocalUser.objects.create_user(username)
            # If the passwords match, return the local user
            if ceda_user.md5passwd == md5.new(password).hexdigest():
                # If the password matches return the user
                return local_user
        elif local_user:
            # If there is a local user without a CEDA user, delete them
            local_user.delete()
        return None
