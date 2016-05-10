# ceda-oauth-server

OAuth server for CEDA.


## Requirements

The reference platform is a fully patched CentOS 6.x installation with Python 2.7
and PostgreSQL.

To install Python 2.7 in CentOS 6.x, the following can be used:

```sh
sudo yum install https://centos6.iuscommunity.org/ius-release.rpm
sudo yum install python27 python27-devel python27-pip python27-virtualenv
```

To install and configure PostgreSQL, use the following:

```sh
sudo yum install postgresql postgresql-devel postgresql-server
sudo service postgresql initdb
sudo chkconfig postgresql on
sudo service postgresql start
```


## Creating a venv

To ensure that you are using the correct Python version and libraries, it is recommended to
use a Python virtual environment (venv):

```sh
virtualenv-2.7 $PYENV
```

where `$PYENV` is the directory where the created venv will live (e.g. `~/venv`).

`ceda-oauth-server` uses [pip](https://pypi.python.org/pypi/pip) to manage dependencies
and installation.


## Developing

Installing the code in development mode, via pip, ensures that dependencies
are installed and entry points are set up properly but changes we make to the source
code are instantly picked up.

```sh
# Clone the repository
git clone https://github.com/cedadev/ceda-oauth-server.git

# Install in editable (i.e. development) mode
#   NOTE: This will install the LATEST versions of any packages
#         This is what you want for development, as we should be keeping up to date!
$PYENV/bin/pip install -e ceda-oauth-server
```

Next, create a PostgreSQL database that is accessible by the user that you are
doing your development with:

```sh
sudo -Hi -u postgres createuser -DRS -w $USER
sudo -Hi -u postgres createdb -E UTF8 -O $USER -w ceda_oauth_server
```

Then copy `ceda_oauth_server/settings.py.example` to `ceda_oauth_server/settings.py` and
adjust the settings for your platform (see https://docs.djangoproject.com/en/1.9/topics/settings/).

You can then launch the development server:

```sh
$PYENV/bin/python manage.py runserver
```

The CEDA OAuth Server will then be available in a web browser at `localhost:8000`.

**NOTE:** The development server is not suitable for running in production!
