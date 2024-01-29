from django.urls import include, path
from rest_framework import routers

from .views import LiteratureViewSet

# ============= BASE ROUTERS =============
router = routers.SimpleRouter()
router.register(r"literature", LiteratureViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
