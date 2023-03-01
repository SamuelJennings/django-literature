"""Settings for Django Literature."""
from appconf import AppConf
from django.conf import settings

__all__ = ("settings", "LiteratureConf")


class LiteratureConf(AppConf):
    """Settings for Django Literature"""

    MODELS = {}
    """Point the application to the working models. Required when extending
    the default models."""

    DEFAULT_STYLE = "harvard"
    """Default citation style. Must be included in the templates/crossref/styles
     folder."""

    AUTHOR_TRUNCATE_AFTER = 2

    INACTIVE_AFTER = 5

    HYPERLINK = True

    PDF_RENAMER = "literature.utils.simple_file_renamer"

    AUTOLABEL = "literature.utils.simple_autolabeler"

    ADAPTORS = [
        "literature.adaptors.crossref.Crossref",
        "literature.adaptors.datacite.Datacite",
    ]

    class Meta:
        """Prefix for all Django Literature settings."""

        prefix = "LITERATURE"
