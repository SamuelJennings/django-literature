.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

.. image:: https://api.cirrus-ci.com/github/ssjenny90/django-litman.svg?branch=main
    :alt: Built Status
    :target: https://cirrus-ci.com/github/ssjenny90/django-litman
.. image:: https://readthedocs.org/projects/django-litman/badge/?version=latest
    :alt: ReadTheDocs
    :target: https://django-litman.readthedocs.io/en/stable/
.. image:: https://img.shields.io/coveralls/github/ssjenny90/django-litman/main.svg
    :alt: Coveralls
    :target: https://coveralls.io/r/ssjenny90/django-litman
.. image:: https://img.shields.io/pypi/v/django-litman.svg
    :alt: PyPI-Server
    :target: https://pypi.org/project/django-litman/
.. image:: https://img.shields.io/conda/vn/conda-forge/django-litman.svg
    :alt: Conda-Forge
    :target: https://anaconda.org/conda-forge/django-litman
.. image:: https://pepy.tech/badge/django-litman/month
    :alt: Monthly Downloads
    :target: https://pepy.tech/project/django-litman
.. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
    :alt: Twitter
    :target: https://twitter.com/django-litman

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

=============
django-litman
=============

    A research literature management application for Django


A longer description of your project goes here...


Features
========

- Flexible API
- Easily create entries from DOIs
- Custom manager for easily retrieving a DOI from a remote source



Usage
========

Fetch a DOI from the appropriate registrar if it does not already exist in the database.

obj, created = Work.objects.get_or_resolve(doi)

Update a database entry for a given doi

obj, created = Work.objects.resolve_and_update(doi)


.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.3.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
