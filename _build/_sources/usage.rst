=====
Usage
=====

To use Django Literature in a project, add it to your `INSTALLED_APPS`:

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
