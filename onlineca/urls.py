# -*- coding: utf-8 -*-
"""
URL configuration for the Online CA Django app.
"""

__author__ = "Matt Pryor"
__copyright__ = "Copyright 2015 UK Science and Technology Facilities Council"

from django.conf import settings
from django.conf.urls import url, include

from . import views


urlpatterns = [
    # The OnlineCA app provides /oauth/trustroots/ and /oauth/certificate/ with
    # /oauth/certificate/ protected by a scope
    url(r'^oauth/', include([
        url(r'^trustroots/$', views.trustroots, name="trustroots_oauth"),
        url(r'^certificate/$', views.certificate_oauth, name="certificate_oauth"),
    ])),
    # We also provide the same endpoints under /onlineca with /onlineca/certificate/
    # protected by HTTP Basic Auth
    url(r'^onlineca/', include([
        url(r'^trustroots/$', views.trustroots, name="trustroots_basicauth"),
        url(r'^certificate/$', views.certificate_basicauth, name="certificate_basicauth"),
    ])),
]
