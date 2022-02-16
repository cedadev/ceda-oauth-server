#!/usr/bin/env python3

import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()


if __name__ == "__main__":
    setup(
        name = 'ceda-oauth-server',
        setup_requires = ['setuptools_scm'],
        use_scm_version = True,
        description = 'OAuth2 provider for CEDA account information',
        long_description = README,
        classifiers = [
            "Programming Language :: Python",
            "Framework :: Django",
            "Topic :: Internet :: WWW/HTTP",
            "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
        author = 'Matt Pryor',
        author_email = 'matt.pryor@stfc.ac.uk',
        url = 'https://github.com/cedadev/ceda-oauth-server',
        keywords = 'web django ceda oauth2',
        packages = find_packages(),
        include_package_data = True,
        zip_safe = False,
        install_requires = [
            'django<4',
            # We need the old-style middleware for decorator_from_middleware
            # This will soon be replaced with a reconfiguration of the JASMIN SLCS,
            # so we don't invest a lot of time in fixing this now
            'django-oauth-toolkit<1.4.0',
            'psycopg2-binary',
            'django-bootstrap3',
            'six',
            'userdb_model',
            'dot-restrict-scopes',
            'django-onlineca',
            'fwtheme-django',
            'fwtheme-django-ceda-serv',
        ]
    )
