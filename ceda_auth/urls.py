# -*- coding: utf-8 -*-
"""
URL configuration for the CEDA profile OAuth endpoints.
"""

__author__ = "Matt Pryor"
__copyright__ = "Copyright 2018 UK Science and Technology Facilities Council"

from django.conf import settings
from django.conf.urls import url, include

from . import views


urlpatterns = [
    url(r'^profile/$', views.profile, name = "profile"),
    url(r'^jasmin_link/$', views.jasmin_link, name = "jasmin_link"),
]
