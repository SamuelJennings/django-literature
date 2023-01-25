# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # path("", include("filer.urls")),
    path("admin/", admin.site.urls),
    # path("", include("literature.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
