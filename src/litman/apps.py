from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LitmanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'litman'
    verbose_name = _('Literature Manager')

    def ready(self) -> None:
        # from litman.adaptors import crossref, datacite
        return super().ready()
