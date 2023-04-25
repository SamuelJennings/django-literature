## simple_test/api_urls.py

# from rest_framework import routers
from __future__ import annotations

from typing import Any

from drf_auto_endpoint.endpoints import Endpoint
from drf_auto_endpoint.router import router

# from .views import UserViewSet
# from .models import Literature


class DataTableMixin:
    endpoint: dict[str, Any] = {}

    class Media:
        css = {"all": ("vendor/DataTables/datatables.min.css",)}
        # js = (
        #     "vendor/DataTables/datatables.min.js",
        #     "literature/js/datatablesHyperlink.js",
        #     "literature/js/admin/change_list.js",

        # )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register_endpoint()

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["datatables_fields"] = self.get_dt_fields()
        return super().changelist_view(request, extra_context=extra_context)

    def register_endpoint(self):
        return router.register(endpoint=Endpoint(model=self.model, **self.endpoint))

    # def get_urls(self):
    #     router.register(self.get_endpoint())
    #     return [
    #         # path("api/", self.admin_site.admin_view(self.search_online), name="search"),
    #         *super().get_urls(),
    #     ]
