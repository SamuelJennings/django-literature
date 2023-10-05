import json
import pprint

# from auto_datatables.views import AutoTableMixin
from django import forms
from django.http import HttpResponse, JsonResponse
from django.utils.encoding import force_str
from django.views.generic import TemplateView
from formset.views import FormCollectionView

from literature.models import Literature

# from literature.conf import
from .formset import LiteratureFormCollection
from .tables import LiteratureTable


class CitationMixin:
    citation_style = "bootstrap"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["citation_style"] = self.citation_style
        return context


class LiteratureList(TemplateView, CitationMixin):
    table = LiteratureTable
    template_name = "project/list.html"


class LiteratureDetail(FormCollectionView, CitationMixin):
    # model = SupplementaryMaterial
    # form_class=LiteratureForm
    collection_class = LiteratureFormCollection
    extra_context = None
    template_name = "literature/literature_form.html"

    # def get_object(self, queryset=None):
    # if self.extra_context['add'] is False:
    # return super().get_object(queryset)

    def form_valid(self, form):
        if (extra_data := self.get_extra_data()) and extra_data.get("delete") is True:
            self.object.delete()
            success_url = self.get_success_url()
            response_data = {"success_url": force_str(success_url)} if success_url else {}
            return JsonResponse(response_data)
        return super().form_valid(form)


class LiteratureForm(forms.ModelForm):
    class Meta:
        model = Literature
        exclude = ["published", "year"]

    # def __init__(self, data=None, *args, **kwargs):
    #     # modify the incoming data to ensure that keys with hyphens are replaced with
    #     data = {k.replace('-','_'):v for k,v in data.items()}
    #     super().__init__(data, *args, **kwargs)
