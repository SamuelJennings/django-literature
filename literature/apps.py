from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LiteratureConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "literature"
    verbose_name = _("Literature Manager")

    def ready(self) -> None:
        # from literature.models import Literature

        # data, errors = Literature.objects.resolve_doi("10.1093/gji/ggz376")
        return super().ready()
