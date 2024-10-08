from django.urls import path

from .views import (
    ImportView,
    LiteratureCreateView,
    LiteratureDeleteView,
    LiteratureDetailView,
    LiteratureTableView,
    LiteratureUpdateView,
)

urlpatterns = [
    path("import/", ImportView.as_view(), name="literature-import"),
    path("new/", LiteratureCreateView.as_view(), name="literature-create"),
    path("", LiteratureTableView.as_view(), name="literature-list"),
    path("<pk>/", LiteratureDetailView.as_view(), name="literature-detail"),
    path("<pk>/edit/", LiteratureUpdateView.as_view(), name="literature-edit"),
    path("<pk>/delete/", LiteratureDeleteView.as_view(), name="literature-delete"),
]
