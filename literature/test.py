from django import forms
from django.forms import fields
from formset.collection import FormCollection
from formset.renderers import bootstrap
from formset.views import FormCollectionView
from formset.widgets import (
    Selectize,
)


class CustomWidget(Selectize):
    pass


class TestForm(forms.Form):
    default_renderer = bootstrap.FormRenderer()
    # custom_widget = fields.ImageField(widget=CustomWidget)
    # default_widget = fields.ImageField()
    city = fields.ChoiceField(
        choices=[(1, "London"), (2, "New York"), (3, "Tokyo"), (4, "Sidney"), (5, "Vienna")],
        widget=Selectize,
    )

    sister_city = fields.ChoiceField(
        choices=[(1, "London"), (2, "New York"), (3, "Tokyo"), (4, "Sidney"), (5, "Vienna")],
        widget=CustomWidget,
    )

    # class Meta:
    #     widgets = {
    #         # "custom_widget": CustomWidget(),
    #         "default_widget": UploadedFileInput(),
    #     }


class TestFormCollection(FormCollection):
    default_renderer = bootstrap.FormRenderer()

    test_form = TestForm()


# class MyUpdateView(FormView):
#     form_class = TestForm
#     template_name = 'test.html'


class MyUpdateView(FormCollectionView):
    collection_class = TestFormCollection
    extra_context = None
    template_name = "test.html"
