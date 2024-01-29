import json
import pprint

# from auto_datatables.views import AutoTableMixin
from django import forms
from django.http import HttpResponse, JsonResponse
from django.utils.encoding import force_str
from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin, TemplateResponseMixin, View
from formset.views import (
    EditCollectionView,
    FileUploadMixin,
    FormCollectionView,
    FormCollectionViewMixin,
    IncompleteSelectResponseMixin,
    SingleObjectMixin,
)

from literature.models import Literature

# from literature.conf import
from .formset import LiteratureFormCollection
from .tables import LiteratureTable


class LiteratureList(TemplateView):
    table = LiteratureTable
    template_name = "literature/literature_list.html"


class LiteratureDetail(FormCollectionView):
    collection_class = LiteratureFormCollection
    extra_context = None
    template_name = "literature/literature_form.html"

    # def form_valid(self, form):
    #     if (extra_data := self.get_extra_data()) and extra_data.get("delete") is True:
    #         self.object.delete()
    #         success_url = self.get_success_url()
    #         response_data = {"success_url": force_str(success_url)} if success_url else {}
    #         return JsonResponse(response_data)
    #     return super().form_valid(form)


class LiteratureViewMixin(EditCollectionView):
    model = Literature
    collection_class = LiteratureFormCollection
    template_name = "literature/literature_form.html"


# class LiteratureEditView(LiteratureViewMixin, TemplateResponseMixin, View):
class LiteratureEditView(EditCollectionView):
    model = Literature
    collection_class = LiteratureFormCollection
    template_name = "literature/literature_form.html"


class LiteratureCreateView(FormCollectionView):
    pass
