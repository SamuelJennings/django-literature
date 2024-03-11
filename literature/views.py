from django.db import transaction
from django.http import JsonResponse
from django.views.generic import TemplateView
from formset.views import EditCollectionView

from literature.models import Literature

from .forms import LiteratureForm
from .tables import LiteratureTable


class LiteratureList(TemplateView):
    table = LiteratureTable
    template_name = "literature/literature_list.html"


class LiteratureEditView(EditCollectionView):
    model = Literature
    collection_class = LiteratureForm
    template_name = "literature/literature_form.html"
    success_url = "."

    def get_object(self):
        if not self.kwargs.get("pk"):
            return None
        return self.model.objects.get(pk=self.kwargs.get("pk"))

    def form_collection_valid(self, form_collection):
        with transaction.atomic():
            form_collection.construct_instance(self.object)
        # integrity errors may occur during construction, hence revalidate collection
        if form_collection.is_valid():
            return super().form_collection_valid(form_collection)
        else:
            return self.form_collection_invalid(form_collection)

    def form_collection_invalid(self, form_collection):
        return super().form_collection_invalid(form_collection)

    def form_valid(self, form):
        if extra_data := self.get_extra_data():
            if extra_data.get("add") is True:
                form.instance.save()
            if extra_data.get("delete") is True:
                form.instance.delete()
                return JsonResponse({"success_url": self.get_success_url()})
        return super().form_valid(form)
