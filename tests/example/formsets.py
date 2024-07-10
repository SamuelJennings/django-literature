from django import forms
from formset.collection import FormCollection
from formset.fieldset import Fieldset
from formset.renderers import bootstrap

from literature.utils import parse_author


class RequiredForm(Fieldset):
    type = forms.ChoiceField(
        choices=(
            ("book", "Book"),
            ("article", "Article"),
            ("inproceedings", "Inproceedings"),
        ),
    )
    title = forms.CharField(
        max_length=255,
    )
    default_renderer = bootstrap.FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "type": "col-4",
            "title": "col-12",
        },
    )


class DateForm(forms.Form):
    begin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    end = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )


class NameForm(forms.Form):
    name = forms.CharField(
        max_length=255,
    )

    default_renderer = bootstrap.FormRenderer(
        field_css_classes="row mb-3",
        label_css_classes="col-auto",
        control_css_classes="col",
    )

    def clean(self):
        return parse_author(self.cleaned_data["name"])

    def model_to_dict(self, instance):
        return {
            "name": instance["given"] + " " + instance["family"],
        }


class NameCollection(FormCollection):
    # extra_siblings = 0
    min_siblings = 0
    # related_field = "item"
    is_sortable = True
    name = NameForm()

    @property
    def cleaned_data(self):
        if self._errors is None or not self.is_valid():
            raise AttributeError(f"'{self.__class__}' object has no attribute 'cleaned_data'")
        return [holder.cleaned_data for valid_holders in self.valid_holders for holder in valid_holders.values()]

    def models_to_list(self, names):
        return [self.model_to_dict(instance) for instance in names]

    def model_to_dict(self, name):
        object_data = {}
        for holder_name, holder in self.declared_holders.items():
            object_data[holder_name] = holder.model_to_dict(name)
        return object_data

    def full_clean(self):
        return super().full_clean()


class ObjectFormCollection(FormCollection):
    required = RequiredForm()
    author = NameCollection(legend="Authors")
    chair = NameCollection(legend="Chair")

    default_renderer = bootstrap.DefaultFormRenderer(
        form_css_classes="row",
    )

    def model_to_dict(self, instance):
        object_data = {}
        for name, holder in self.declared_holders.items():
            value = instance.properties.get(name)
            if getattr(holder, "has_many", False):
                object_data[name] = holder.models_to_list(value or [])
            else:
                if callable(getattr(holder, "model_to_dict", None)):
                    object_data[name] = holder.model_to_dict(value)
                else:
                    object_data[name] = holder.model_to_dict(value)
        return object_data
