=============================
Django Literature
=============================

.. image:: https://badge.fury.io/py/django-literature.svg
    :target: https://badge.fury.io/py/django-literature

.. image:: https://travis-ci.org/SSJenny90/django-literature.svg?branch=master
    :target: https://travis-ci.org/SSJenny90/django-literature

.. image:: https://codecov.io/gh/SSJenny90/django-literature/branch/main/graph/badge.svg?token=0Q18CLIKZE 
 :target: https://codecov.io/gh/SSJenny90/django-literature

A scientific literature management app for Django

Documentation
-------------

The full documentation is at https://django-literature.readthedocs.io.

Quickstart
----------

Install Django Literature::

    pip install django-literature

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'literature.apps.LiteratureConfig',
        ...
    )

Add Django Literature's URL patterns:

.. code-block:: python

    from literature import urls as literature_urls


    urlpatterns = [
        ...
        url(r'^', include(literature_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

::

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
