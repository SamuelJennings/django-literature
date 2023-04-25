# Django Literature 

[![Github Build](https://github.com/SSJenny90/django-literature/actions/workflows/build.yml/badge.svg)](https://github.com/SSJenny90/django-literature/actions/workflows/build.yml)
[![Github Docs](https://github.com/SSJenny90/django-literature/actions/workflows/docs.yml/badge.svg)](https://github.com/SSJenny90/django-literature/actions/workflows/docs.yml)
[![CodeCov](https://codecov.io/gh/SSJenny90/django-literature/branch/main/graph/badge.svg?token=0Q18CLIKZE)](https://codecov.io/gh/SSJenny90/django-literature)
![GitHub](https://img.shields.io/github/license/SSJenny90/django-literature)
![GitHub last commit](https://img.shields.io/github/last-commit/SSJenny90/django-literature)
![PyPI](https://img.shields.io/pypi/v/django-literature)
<!-- [![RTD](https://readthedocs.org/projects/django-literature/badge/?version=latest)](https://django-literature.readthedocs.io/en/latest/readme.html) -->
<!-- [![Documentation](https://github.com/SSJenny90/django-literature/actions/workflows/build-docs.yml/badge.svg)](https://github.com/SSJenny90/django-literature/actions/workflows/build-docs.yml) -->
<!-- [![PR](https://img.shields.io/github/issues-pr/SSJenny90/django-literature)](https://github.com/SSJenny90/django-literature/pulls)
[![Issues](https://img.shields.io/github/issues-raw/SSJenny90/django-literature)](https://github.com/SSJenny90/django-literature/pulls) -->
<!-- ![PyPI - Downloads](https://img.shields.io/pypi/dm/django-literature) -->
<!-- ![PyPI - Status](https://img.shields.io/pypi/status/django-literature) -->

A scientific literature management app for Django

Documentation
-------------

The full documentation is at https://ssjenny90.github.io/django-literature/

Quickstart
----------

Install Django Literature::

    pip install django-literature

Add it to your `INSTALLED_APPS`:


    INSTALLED_APPS = (
        ...
        'literature',
        ...
    )

Add Django Literature's URL patterns:

    urlpatterns = [
        ...
        path('', include("literature.urls")),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

