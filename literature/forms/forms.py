from typing import Any

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, ButtonHolder, Field, Layout, Reset, Submit
from django import forms
from django.urls import reverse
from django.utils.translation import gettext as _

from literature.utils import csl_to_django_lit_flat, django_lit_to_csl

# from .choices import CSL_TYPE_CHOICES
from ..models import LiteratureItem
from . import fieldsets
from .fieldsets import HelpText

BUTTON_HOLDER = ButtonHolder(
    Submit("submit", _("Save")),
    Reset("reset", _("Reset"), css_class="btn btn-outline-secondary ms-2"),
    HTML(
        '{{% if object.pk %}}<a href="{{% url "literature-delete" pk=object.pk %}}" class="btn btn-danger ms-auto">{}</a>{{% endif %}}'.format(
            _("Delete")
        )
    ),
    css_class="sticky-bottom mb-3 d-flex w-100 border-top bg-white py-1",
)


class BaseLiteratureForm(
    fieldsets.RequiredInformation,
    fieldsets.GeneralInformation,
    fieldsets.Abstract,
    fieldsets.PublishingInformation,
    fieldsets.Provenance,
    fieldsets.ArchivalInformation,
    fieldsets.ContainerInformation,
    fieldsets.CollectionInformation,
    fieldsets.AdditionalInformation,
    fieldsets.Custom,
    forms.ModelForm,
):
    note = forms.CharField(
        label=_("Comment"),
        required=False,
        widget=forms.Textarea(),
    )

    annote = forms.CharField(
        label=_("Annotation"),
        required=False,
        widget=forms.Textarea(),
    )

    class Meta:
        model = LiteratureItem
        exclude = ["created", "modified", "key", "item", "collections", "issued"]

    class Media:
        js = (
            "bundles/js/literature.js",
            "literature/js/form.js",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "literatureForm"  # Set the form id
        self.helper.include_media = False
        self.helper.layout = Layout()

        for cls in BaseLiteratureForm.__bases__:
            if hasattr(cls, "layout"):
                self.helper.layout.append(cls.layout)

        # self.helper.layout.append(Div(template="literature/widgets/csl_date.html"))
        self.helper.layout.append(BUTTON_HOLDER)
        # for nam, field in self.fields.items():
        #     field.disabled = True

    def clean(self) -> dict[str, Any]:
        # new = csl_to_django_lit(self.cleaned_data)
        # self.cleaned_data = new
        cleaned = super().clean()

        if cleaned.get("event"):
            # event deprecated in favor of event_title
            cleaned["event_title"] = cleaned.pop("event")

        if cleaned.get("shortTitle"):
            # shortTitle deprecated in favor of title-short
            cleaned["title_short"] = cleaned.pop("shortTitle")

        return cleaned

    def save(self, commit: bool = True):
        # csl_data = csl_to_django_lit(self.cleaned_data)
        csl_data = django_lit_to_csl(self.cleaned_data)
        csl_data = {k: v for k, v in csl_data.items() if v}
        self.instance.item = csl_data
        return super().save(commit)


class LiteratureForm(BaseLiteratureForm):
    def __init__(self, *args, **kwargs):
        # if "data" in kwargs:
        # kwargs["data"] = csl_to_django_lit(kwargs["data"])
        if kwargs.get("instance"):
            kwargs["initial"] = csl_to_django_lit_flat(kwargs["instance"].item)
        super().__init__(*args, **kwargs)


class CSLForm(BaseLiteratureForm):
    """Used to validate raw CSL JSON data."""

    def __init__(self, data=None, *args, **kwargs):
        # self.data = csl_to_django_lit_flat(self.data)
        data = csl_to_django_lit_flat(data) if data else None
        super().__init__(data, *args, **kwargs)


class SearchForm(forms.Form):
    search = forms.CharField(
        label=False,
        required=True,
    )
    text = forms.CharField(
        label=False,
        required=False,
        widget=forms.HiddenInput(),
    )

    class Media:
        js = (
            "bundles/js/literature.js",
            # "literature/js/fetch.js",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "literatureSearchForm"  # Set the form id
        self.helper.form_action = reverse("literature-import")
        self.helper.include_media = False

        self.helper.layout = Layout(
            HelpText(
                _("Find a citation online using a unique identifier. Currently supported are DOI and Wikidata IDs.")
            ),
            Field("search", placeholder=_("Search")),
            "text",
            HTML("<p id='citationPreview' class='mt-3'></p>"),
        )


class ImportForm(forms.Form):
    upload = forms.FileField(
        label=False,
        required=False,
    )
    text = forms.CharField(
        label=False,
        required=False,
        widget=forms.HiddenInput(),
    )

    class Media:
        js = (
            "bundles/js/literature.js",
            # "literature/js/import.js",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            HelpText(
                _("Upload a file to import references. Supported file formats include BibTeX, RIS, and EndNote XML.")
            ),
            Field("upload"),
            "text",
            ButtonHolder(
                Submit("submit", _("Confirm import"), css_class="btn btn-primary", disabled=True),
                Reset("reset", _("Clear"), css_class="btn btn-outline-secondary ms-2"),
            ),
            HTML("<p id='citationPreview' class='mt-3'></p>"),
        )
