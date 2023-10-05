from auto_datatables.table import DataTable
from django.conf import settings
from django.urls import reverse_lazy

from .api.serialize import LiteratureSerializer
from .models import Literature


class LiteratureTableConfig:
    dom = "fBpit"
    serverSide = True
    scroller = True
    scrollY = "100vh"
    scrollX = True
    colReorder = True
    stateSave = True


class LiteratureTable(DataTable):
    config_class = getattr(settings, "LITERATURE_TABLE_CONFIG", LiteratureTableConfig)
    url = reverse_lazy("literature-list")
    serializer_class = LiteratureSerializer
    model = Literature
    fields = [
        "title",
    ]
