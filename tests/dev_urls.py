from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_auto_endpoint.router import router as drf_router

urlpatterns = [
    path("admin/api/", include(drf_router.urls), name="admin_api"),
    path("admin/", admin.site.urls),
    path("api/", include("literature.api.urls")),
    path("", include("literature.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
