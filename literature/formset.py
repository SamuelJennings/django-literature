from typing import Any, Dict

from django import forms
from django.forms.models import ModelForm, construct_instance, model_to_dict
from django.utils.translation import gettext as _
from formset.collection import FormCollection
from formset.fieldset import Fieldset, FieldsetMixin
from formset.renderers import bootstrap
from formset.richtext.widgets import RichTextarea
from formset.widgets import (
    DateInput,
    DualSortableSelector,
    Selectize,
    UploadedFileInput,
)

from .choices import TypeChoices
from .csl_map import CSL_FIELDS, CSL_TYPES
from .models import Literature, SupplementaryMaterial
from .widgets import PDFFileInput


class CSLMixin:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_fields()
        self.update_field_visibility()

    def update_fields(self):
        for field in self.Meta.fields:
            attrs = CSL_FIELDS[field]
            if attrs["type"] == "standard":
                self.fields[field] = forms.CharField(
                    label=attrs["name"],
                    help_text=_(attrs["description"]),
                    required=False,
                    widget=self.Meta.widgets.get(field, None),
                )
                self.fields[field].widget.attrs.update({"show-if": ""})

    def update_field_visibility(self):
        for csl_type, fields in CSL_TYPES.items():
            for field_name in fields:
                if field_name in self.fields:
                    if not self.fields[field_name].widget.attrs["show-if"]:
                        self.fields[field_name].widget.attrs["show-if"] += f"literature.type == '{csl_type}'"
                    else:
                        self.fields[field_name].widget.attrs["show-if"] += f" || literature.type == '{csl_type}'"


class LiteratureRequired(FieldsetMixin, ModelForm):
    legend = "Required Content"

    class Meta:
        model = Literature
        fields = ["title", "published", "container_title"]
        widgets = {
            "abstract": RichTextarea(),
            "published": DateInput,
            "authors": DualSortableSelector,  # or DualSelector
        }


class LiteratureExtra(FieldsetMixin, ModelForm):
    legend = "Extra Content"
    help_text = "These fields are not required but are highly recommended."

    class Meta:
        model = Literature
        fields = ["pdf"]
        widgets = {
            "pdf": PDFFileInput(),
            "abstract": RichTextarea(),
            "published": DateInput,
            "authors": DualSortableSelector,  # or DualSelector
        }


class SuppMatForm(ModelForm):
    class Meta:
        model = SupplementaryMaterial
        fields = ["file"]
        widgets = {
            "file": UploadedFileInput(),
        }


class SuppMatCollection(FormCollection):
    legend = _("Supplementary Material")
    help_text = _("Upload supplementary material related to this publication.")
    min_siblings = 0
    extra_siblings = 1
    default_renderer = bootstrap.FormRenderer()

    supplementary_material = SuppMatForm()

    def model_to_dict(self, literature):
        opts = self.declared_holders["supps"]._meta
        return [{"supp": model_to_dict(supp, fields=opts.fields)} for supp in literature.supplementary.all()]

    def construct_instance(self, literature, data):
        for d in data:
            try:
                supp_object = literature.supplementary.get(id=d["supplementary"]["id"])
            except (KeyError, SupplementaryMaterial.DoesNotExist):
                supp_object = SupplementaryMaterial(literature=literature)
            form_class = self.declared_holders["supps"].__class__
            form = form_class(data=d["supplementary"], instance=supp_object)
            if form.is_valid():
                if form.marked_for_removal:
                    supp_object.delete()
                else:
                    construct_instance(form, supp_object)
                    form.save()


class LiteratureForm(FormCollection):
    default_renderer = bootstrap.FormRenderer()
    required = LiteratureRequired()
    extra = LiteratureExtra()


class LiteratureFormWithSupps(FormCollection):
    legend = "I'm the literature form"
    help_text = "I'm a form designed to edit a literature object"

    default_renderer = bootstrap.FormRenderer()
    required = LiteratureRequired()
    extra = LiteratureExtra()
    supps = SuppMatCollection()


class PublisherForm(CSLMixin, Fieldset):
    legend = _("Publishing")
    # help_text = "I'm a form designed to edit a literature object"

    class Meta:
        fields = ["publisher", "publisher-place", "original-publisher", "original-publisher-place"]
        widgets: Dict[str, Any] = {}


class CSLForm(CSLMixin, Fieldset):
    type = forms.ChoiceField(  # noqa: A003
        label=_("type"), choices=TypeChoices.choices, required=True, widget=Selectize
    )

    class Meta:
        fields = ["title", "abstract"]
        widgets = {
            # "pdf": PDFFileInput(),
            "abstract": RichTextarea(),
            # "published": DateInput,
            # "authors": DualSortableSelector,  # or DualSelector
        }


class LiteratureFormCollection(FormCollection):
    # legend = "I'm the literature form"
    # help_text = "I'm a form designed to edit a literature object"

    default_renderer = bootstrap.FormRenderer(field_css_classes="mb-3")

    literature = CSLForm()
    publishing = PublisherForm()
