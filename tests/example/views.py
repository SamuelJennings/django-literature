from django.db import transaction
from django.http import JsonResponse
from formset.views import EditCollectionView

from .formsets import ObjectFormCollection
from .models import Product


class ProductEditView(EditCollectionView):
    model = Product
    template_name = "literature/literature_formset.html"
    collection_class = ObjectFormCollection

    def form_collection_valid(self, form_collection):
        with transaction.atomic():
            form_collection.construct_instance(self.object)
        # integrity errors may occur during construction, hence revalidate collection
        if form_collection.is_valid():
            self.object.properties = form_collection.cleaned_data
            self.object.save()
            # return super().form_collection_valid(form_collection)
            return JsonResponse({"success_url": self.get_success_url()})
        else:
            return self.form_collection_invalid(form_collection)
