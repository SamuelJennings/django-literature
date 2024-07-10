import json

from django.urls import reverse_lazy
from django.views.generic import FormView
from neapolitan.views import CRUDView

from literature.choices import CSL_ALWAYS_SHOW, CSL_SUGGESTED_PROPERTIES

from .forms import CSLForm, DateForm, ImportForm, LiteratureForm, NameForm, SearchForm
from .models import Date, Literature, Name


class ImportView(FormView):
    template_name = "literature/import.html"
    form_class = ImportForm
    success_url = reverse_lazy("literature-list")

    def form_valid(self, form):
        entries = json.loads(form.cleaned_data["text"])

        errors = []

        for entry in entries:
            entry_form = CSLForm(entry)
            if entry_form.is_valid():
                entry_form.save()
            else:
                errors.append((entry["id"], entry_form.errors))

        if errors:
            return self.render_to_response(self.get_context_data(form=form, failed_entries=errors))
            # return self.form_invalid(errors)

        return super().form_valid(form)


class SearchOnlineView(FormView):
    form_class = SearchForm


class LiteratureView(CRUDView):
    model = Literature
    form_class = LiteratureForm
    fields = ["title", "author"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_nav"] = self.get_form_nav()
        context["quick_search_form"] = SearchForm()
        context["js_config"] = {
            "CSL_SUGGESTED_PROPERTIES": CSL_SUGGESTED_PROPERTIES,
            "CSL_ALWAYS_SHOW": CSL_ALWAYS_SHOW,
        }
        return context

    def get_form_nav(self):
        form = self.get_form_class()()
        layout = form.helper.layout
        form_nav = []
        for item in layout:
            item_id = getattr(item, "css_id", None)
            legend = getattr(item, "legend", None)
            if item_id and legend:
                form_nav.append({"id": item_id, "name": legend})
        return form_nav

    def process_form(self, request, *args, **kwargs):
        return super().process_form(request, *args, **kwargs)


class NameView(CRUDView):
    model = Name
    form_class = NameForm
    fields = ["family", "given"]

    def get_success_url(self):
        # Try to get the referring URL from the HTTP headers
        return self.request.META.get("HTTP_REFERER")


class DateView(CRUDView):
    model = Date
    form_class = DateForm
    fields = ["date"]

    def get_success_url(self):
        # Try to get the referring URL from the HTTP headers
        return self.request.META.get("HTTP_REFERER")
