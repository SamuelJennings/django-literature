from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "literature"
urlpatterns = [
    path("", views.LiteratureList.as_view(), name="list"),
    path("create/", views.LiteratureEditView.as_view(), name="create"),
    path("<int:pk>/", RedirectView.as_view(pattern_name="literature:edit", permanent=False)),
    path("<int:pk>/edit/", views.LiteratureEditView.as_view(extra_context="edit"), name="edit"),
]
