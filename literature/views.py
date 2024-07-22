import json

from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from neapolitan.views import CRUDView

from literature.choices import CSL_ALWAYS_SHOW, CSL_SUGGESTED_PROPERTIES

from .forms import ImportForm, LiteratureForm, SearchForm
from .models import LiteratureItem
from .utils.csl import process_multiple_entries


class ImportView(FormView):
    template_name = "literature/import.html"
    form_class = ImportForm
    success_url = reverse_lazy("literature-list")

    def form_valid(self, form):
        entries = json.loads(form.cleaned_data["text"])
        errors = process_multiple_entries(entries)
        if errors:
            return self.render_to_response(self.get_context_data(form=form, failed_entries=errors))
        return super().form_valid(form)


class LiteratureCreateView(CreateView):
    form_class = LiteratureForm
    template_name = "neapolitan/object_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_nav"] = self.get_form_nav()
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


class LiteratureView(CRUDView):
    model = LiteratureItem
    form_class = LiteratureForm
    fields = ["title", "item"]
    url_base = "literature"

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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # if self.instance:
        # kwargs["initial"] = csl_to_django_lit(self.instance.item)
        return kwargs

    def process_form(self, request, *args, **kwargs):
        return super().process_form(request, *args, **kwargs)
