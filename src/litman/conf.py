"""Settings for Django Litman."""
from django.conf import settings
from appconf import AppConf

__all__ = ("settings", "LitmanConf")


class LitmanConf(AppConf):
    """Settings for Django Litman"""

    MODELS = {}
    """Point the application to the working models. Required when extending
    the default models."""

    DEFAULT_STYLE = 'harvard'
    """Default citation style. Must be included in the templates/crossref/styles
     folder."""

    AUTHOR_TRUNCATE_AFTER = 2

    HYPERLINK = True

    class Meta:
        """Prefix for all Django Litman settings."""
        prefix = "LITMAN"
