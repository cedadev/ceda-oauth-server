# -*- coding: utf-8 -*-
"""
URL configuration for the Online CA Django app.
"""

__author__ = "Matt Pryor"
__copyright__ = "Copyright 2015 UK Science and Technology Facilities Council"

from django.conf import settings
from django.conf.urls import url, include

from . import views


app_name = 'onlineca'
urlpatterns = [
    # Provide the /trustroots/ and /certificate/ endpoints under /onlineca
    url(r'^onlineca/', include([
        url(r'^trustroots/$', views.trustroots, name="trustroots"),
        url(r'^certificate/$', views.certificate_basicauth, name="certificate_basicauth"),
    ])),
    # Also provide the /certificate/ endpoint under /oauth
    url(r'^oauth/', include([
        url(r'^certificate/$', views.certificate_oauth, name="certificate_oauth"),
    ])),
]
