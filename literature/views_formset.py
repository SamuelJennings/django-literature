from django.db import transaction
from formset.views import EditCollectionView

from literature.models import Literature
from tests.example.formsets import ObjectFormCollection


class LiteratureEditView(EditCollectionView):
    model = Literature
    collection_class = ObjectFormCollection
    template_name = "literature/literature_formset.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        if isinstance(initial, dict) and self.object:
            collection_class = self.get_collection_class()
            initial.update(collection_class().model_to_dict(self.object))
        return initial

    def form_collection_valid(self, form_collection):
        with transaction.atomic():
            form_collection.construct_instance(self.object)
        # integrity errors may occur during construction, hence revalidate collection
        if form_collection.is_valid():
            return super().form_collection_valid(form_collection)
        else:
            return self.form_collection_invalid(form_collection)
