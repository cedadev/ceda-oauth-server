# -*- coding: utf-8 -*-
"""
Utility functions for the CEDA Online CA app.
"""

__author__ = "Matt Pryor"
__copyright__ = "Copyright 2018 UK Science and Technology Facilities Council"


from userdb_model.models import User as CedaUser


def django_user_to_ceda_openid(user):
    """
    Returns the CEDA openid for the given Django user.
    """
    return CedaUser.objects.get(accountid = user.username).openid
