#!/usr/bin/env python2.7

import os, re

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

try:
    import ceda_oauth_server.__version__ as version
except ImportError:
    # If we get an import error, find the version string manually
    version = "unknown"
    with open(os.path.join(here, 'ceda_oauth_server', '__init__.py')) as f:
        for line in f:
            match = re.search('__version__ *= *[\'"](?P<version>.+)[\'"]', line)
            if match:
                version = match.group('version')
                break

with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

requires = [
    'django',
    'django-oauth-toolkit',
    'psycopg2',
    'django-bootstrap3',
    'django-wsgi',
    'ContrailOnlineCAService',
    'PasteDeploy',
]

if __name__ == "__main__":

    setup(
        name = 'ceda-oauth-server',
        version = version,
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
        url = 'http://www.ceda.ac.uk',
        keywords = 'web django ceda oauth2',
        packages = find_packages(),
        include_package_data = True,
        zip_safe = False,
        install_requires = requires,
        tests_require = requires,
        test_suite = "ceda_oauth_server.test",
    )
