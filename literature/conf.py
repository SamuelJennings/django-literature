"""Settings for Django Literature."""
from appconf import AppConf
from django.conf import settings

__all__ = ("settings", "LiteratureConf")


class LiteratureConf(AppConf):
    """Settings for Django Literature"""

    DEFAULT_CITATION_STYLE = "plain_text"
    """Default citation style. Must be included in the templates/literautre/citation/
     folder."""

    INACTIVE_AFTER = 5

    PDF_RENAMER = "literature.utils.simple_file_renamer"

    AUTOLABEL = "literature.utils.simple_autolabeler"

    CITATION_JS_SOURCE = "https://cdnjs.cloudflare.com/ajax/libs/citation-js/0.7.1/citation.min.js"

    ADMIN_NODE_SELECTOR = ".form-row"

    class Meta:
        """Prefix for all Django Literature settings."""

        prefix = "LITERATURE"
