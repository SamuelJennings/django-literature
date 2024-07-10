from django.urls import path
from django.views.generic import CreateView

from .forms import DateForm, LiteratureForm, NameForm
from .views import DateView, ImportView, LiteratureView, NameView
from .views_formset import LiteratureEditView

# app_name = "literature"
urlpatterns = [
    path("import/", ImportView.as_view(), name="import"),
    *LiteratureView.get_urls(),
    path(
        "literature/create/",
        CreateView.as_view(form_class=LiteratureForm, template_name="neapolitan/object_form.html"),
        name="literature-create",
    ),
    *NameView.get_urls(),
    path(
        "name/create/",
        CreateView.as_view(form_class=NameForm, template_name="neapolitan/object_form.html"),
        name="name-create",
    ),
    *DateView.get_urls(),
    path(
        "date/create/",
        CreateView.as_view(form_class=DateForm, template_name="neapolitan/object_form.html"),
        name="date-create",
    ),
    path("literature/<pk>/formset/", LiteratureEditView.as_view(), name="literature-edit"),
]
