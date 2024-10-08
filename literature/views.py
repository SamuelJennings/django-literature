import json

from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import CreateView, DeleteView, FormView, UpdateView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin, tables
from easy_icons.templatetags.easy_icons import icon

from literature.choices import CSL_ALWAYS_SHOW, CSL_SUGGESTED_PROPERTIES

from .filters import LiteratureSimpleFilter
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
    template_name = "literature/literatureitem_form.html"

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


class LiteratureTable(tables.Table):
    title = tables.columns.Column(linkify=True)
    # edit = tables.columns.Column(empty_values=(), orderable=False)

    class Meta:
        model = LiteratureItem
        fields = ["citation_key", "title"]

    def render_edit(self, record):
        return mark_safe(  # noqa: S308
            "<a class='text-success' href="
            + reverse_lazy("literature-detail", args=[record.pk])
            + f'>{icon("pencil.svg")}</a>'
        )


class LiteratureTableView(SingleTableMixin, FilterView):
    table_class = LiteratureTable
    model = LiteratureItem
    filterset_class = LiteratureSimpleFilter
    template_name = "literature/literatureitem_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["quick_search_form"] = SearchForm()
        return context


class LiteratureMixin:
    model = LiteratureItem
    form_class = LiteratureForm

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


class LiteratureDetailView(LiteratureMixin, UpdateView):
    pass


class LiteratureUpdateView(LiteratureMixin, UpdateView):
    pass


class LiteratureDeleteView(DeleteView):
    model = LiteratureItem
    success_url = reverse_lazy("literatue-list")
