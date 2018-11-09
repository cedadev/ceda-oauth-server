# -*- coding: utf-8 -*-
"""
Database router that redirects operations on the CEDA userdb models to a database
named ``userdb``. This database must be configured in ``DATABASES``, and the
router specified in ``DATABASE_ROUTERS``:

::

    DATABASES = {
        'default': ...,
        'userdb' : ...,
    }
    DATABASE_ROUTERS = ['ceda_oauth_server.router.Router']
"""

__author__ = "Matt Pryor"
__copyright__ = "Copyright 2018 UK Science and Technology Facilities Council"


class Router:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'userdb_model':
            return 'userdb'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'userdb_model':
            return 'userdb'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'userdb_model':
            return obj2._meta.app_label == 'userdb_model'
        if obj2._meta.app_label == 'userdb_model':
            return obj1._meta.app_label == 'userdb_model'
        return None

    def allow_migrate(self, db, app_label, model_name = None, **hints):
        if app_label == 'userdb_model':
            return False
        return None
