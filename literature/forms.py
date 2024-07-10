import ast
from typing import Any

import citeproc
from crispy_bootstrap5.bootstrap5 import Switch
from crispy_forms.bootstrap import PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, ButtonHolder, Column, Div, Field, Fieldset, Layout, Reset, Row, Submit
from django import forms
from django.urls import reverse
from django.utils.translation import gettext as _
from django_select2.forms import Select2TagWidget

from .fields import NameField, PartialDateFormField

# from .choices import CSL_TYPE_CHOICES
from .models import Date, Literature, Name
from .utils import icon, parse_author
from .widgets import CSLDateField

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


# class DateField( ):
#     def __init__(self, *args, **kwargs):
#         fields = (
#             forms.DateField(
#                 required=False,
#                 widget=forms.DateInput(attrs={"type": "date"}),
#             ),
#             forms.DateField(
#                 required=False,
#                 widget=forms.DateInput(attrs={"type": "date"}),
#             ),
#         )
#         super().__init__(fields, *args, **kwargs)

#     def compress(self, data_list):
#         return data_list


class CustomAuthorWidget(Select2TagWidget):
    def optgroups(self, name, values, attrs=None):
        selected = set(values)
        subgroup = [self.create_option(name, v, v, selected, i) for i, v in enumerate(values)]
        return [(None, subgroup, 0)]

    def create_option(self, name, value, label, selected, index):
        author = ast.literal_eval(value)
        value = "{given} {particle} {family} {suffix}".format(
            given=author.get("given", ""),
            particle=author.get("non-dropping-particle", ""),
            family=author.get("family", ""),
            suffix=author.get("suffix", ""),
        ).strip()
        option = super().create_option(name, value, value, selected, index)
        return option


class CustomAuthorField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = CustomAuthorWidget(attrs={"data-token-separators": ","})

    def to_python(self, value):
        value = [str(v).strip() for v in value]
        processed = []
        for val in value:
            processed.append({k: v for k, v in parse_author(val).items() if v})
        return processed

    def prepare_value(self, value):
        return value


class FormText(HTML):
    def __init__(self, html, *args, **kwargs):
        super().__init__(f'<p class="form-text">{html}</p>', *args, **kwargs)


class DateFormMixin(forms.Form):
    dates = forms.ModelMultipleChoiceField(
        queryset=Date.objects.all(),
        required=False,
        widget=forms.HiddenInput(),
    )
    accessed = PartialDateFormField(
        label=_("Date accessed"),
        help_text=_(
            "Enter the date when the resource was last accessed or retrieved. This is often used for online resources to indicate when the information was accessed by the user."
        ),
        required=False,
    )
    available_date = PartialDateFormField(
        label=_("Date available"),
        help_text=_(
            "The date when the resource became available to the public. This could refer to the date of publication or release of a digital or physical item."
        ),
        required=False,
    )
    event_date = PartialDateFormField(
        label=_("Event date"),
        help_text=_(
            "The date of the event related to the resource. This is typically used for conference papers, presentations, or other time-specific events."
        ),
        required=False,
    )
    issued = CSLDateField(
        label=_("Date issued"),
        help_text=_("The date when the resource was formally published or released."),
        required=False,
    )
    original_date = PartialDateFormField(
        label=_("Original date"),
        help_text=_("Enter the original publication date of the resource, if it was previously published."),
        required=False,
    )
    submitted = PartialDateFormField(
        label=_("Date submitted"),
        help_text=_(
            "Enter the date when the resource was submitted for review or publication. This is often used for manuscripts, theses, or dissertations."
        ),
        required=False,
    )

    dates_layout = Fieldset(
        _("Dates"),
        PrependedText("accessed", icon("calendar"), wrapper_class="col-9"),
        PrependedText("available_date", icon("calendar"), wrapper_class="col-9"),
        PrependedText("event_date", icon("calendar"), wrapper_class="col-9"),
        PrependedText("issued", icon("calendar"), wrapper_class="col-9"),
        PrependedText("submitted", icon("calendar"), wrapper_class="col-9"),
        css_id="dates-fieldset",
    )

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        cleaned_data["dates"] = []
        for f in ["accessed", "available_date", "event_date", "issued", "original_date", "submitted"]:
            if cleaned_data.get(f):
                cleaned_data["dates"].append(cleaned_data[f])

        return cleaned_data


class NameForm(forms.ModelForm):
    class Meta:
        model = Name
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML(
                "<p>{}</p>".format(
                    _(
                        "Contributor names can be specified either as constituent parts (preferred) or as a literal string. Where both parts and a literal representation are given, the literal form will take precedence in citations. Learn more about CSL name variables <a href='https://docs.citationstyles.org/en/stable/specification.html#name-variables' target='_blank'>here</a>."
                    )
                )
            ),
            Fieldset(
                _("Name parts"),
                Row(
                    Column("given"),
                    Column("family"),
                    Column("suffix"),
                ),
                Row(
                    Column("dropping_particle"),
                    Column("non_dropping_particle"),
                ),
            ),
            Div(
                HTML(f'<b>{_("Or...")}</b>'),
                css_class="w-100 text-center",
            ),
            "literal",
            BUTTON_HOLDER,
        )


class DateForm(forms.ModelForm):
    raw = forms.CharField(
        label=_("Raw date"),
        required=False,
    )
    season = forms.CharField(
        label=_("Season"),
        required=False,
    )
    circa = forms.BooleanField(
        label=_("Circa"),
        required=False,
    )

    begin = PartialDateFormField(
        label=_("Begin"),
        required=False,
    )
    end = PartialDateFormField(
        label=_("End"),
        required=False,
    )

    class Meta:
        model = Date
        # fields = "__all__"
        exclude = ["item", "type"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            PrependedText("begin", icon("calendar"), wrapper_class="col-6"),
            PrependedText("end", icon("calendar"), wrapper_class="col-6"),
            BUTTON_HOLDER,
        )


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
        self.helper.form_action = reverse("import")
        self.helper.layout = Layout(
            FormText(
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
            FormText(
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


class BaseLiteratureForm(DateFormMixin, forms.ModelForm):
    title = forms.CharField(label=_("Title"), required=True)
    # author = AuthorFormField(label=_("Author(s)"))

    # author = CustomAuthorField(
    #     label=_("Author(s)"),
    #     required=False,
    #     # widget=Select2TagWidget(),
    #     # widget=Select2TagWidget(attrs={"data-token-separators": ","}),
    #     # widget=CustomAuthorWidget(attrs={"data-token-separators": ","}),
    # )

    custom_author = CustomAuthorField(
        label=_("Custom Author(s)"),
        required=False,
        # widget=Select2TagWidget(),
        # widget=Select2TagWidget(attrs={"data-token-separators": ","}),
        # widget=CustomAuthorWidget(attrs={"data-token-separators": ","}),
    )

    # custom_author = forms.MultipleChoiceField(
    #     choices=[("a", "a"), ("b", "b")],
    # )

    show_suggested = forms.BooleanField(
        label=_("Suggested fields only"),
        required=False,
        initial=True,
    )

    # page = PageRangeField(label=_("Page Range"), required=False)

    publisher_place = forms.CharField(
        label=_("Location"),
        required=False,
    )

    original_publisher_place = forms.CharField(
        label=_("Location"),
        required=False,
    )

    reviewed_title = forms.CharField(
        label=_("Title"),
        required=False,
    )
    reviewed_genre = forms.CharField(
        label=_("Type"),
        help_text=_("E.g. journal article, book, film, etc."),
        required=False,
    )

    event_title = forms.CharField(
        label=_("Name"),
        required=False,
    )
    event_place = forms.CharField(
        label=_("Location"),
        required=False,
    )

    collection_title = forms.CharField(
        label=_("Title"),
        help_text=_("The title of the collection"),
        required=False,
    )
    collection_number = forms.CharField(
        label=_("Number"),
        help_text=_("An identifiying number within the collection"),
        required=False,
    )

    note = forms.CharField(
        label=_("Comment"),
        required=False,
        widget=forms.Textarea(),
    )

    class Meta:
        model = Literature
        exclude = ["created", "modified"]

    class Media:
        js = (
            "bundles/js/literature.js",
            "literature/js/form.js",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # if self.instance.author:
        # self.fields["author"].queryset = Name.objects.all()
        # self.data = csl_to_django_lit(self.data)
        self.helper = FormHelper()
        self.helper.form_id = "literatureForm"  # Set the form id
        self.helper.layout = Layout(
            Row(
                Column("citation_key", css_class="col-md-5"),
                Column("type"),
            ),
            Switch("show_suggested"),
            Fieldset(
                _("General Information"),
                "title",
                "title_short",
                # "author",
                "authority",
                "chapter_number",
                "genre",
                "status",
                "version",
                "number_of_pages",
                "keyword",
                PrependedText("page", _("Pages"), wrapper_class="col-9"),
                Fieldset(
                    _("Physical"),
                    Row(
                        Column("dimensions"),
                        Column("medium"),
                    ),
                ),
                Fieldset(
                    _("Volume"),
                    FormText(
                        _(
                            'Use volume number to indicate the volume of a multi-volume book or journal. For example, if you are citing volume 3 of a book series, you would use the volume number field to indicate this. If the volume has a title, like "The History of the World," you would include that in the volume title field below. A short title may also be provided where applicable.'
                        )
                    ),
                    Row(
                        Column("volume", css_class="col-md-3"),
                        Column("volume_title"),
                    ),
                    "volume_title_short",
                ),
                # "page_first",
                # "number_of_pages",
                "locator",
                css_id="general-info-fieldset",
            ),
            # Authors
            Fieldset(
                _("Authors"),
                # "author",
                "custom_author",
                # HTML(
                #     "{% for author in object.author.all %}{{author}}{% endfor %}<button type='button' class='btn btn-primary'>Edit</button>"
                # ),
                css_id="abstract-fieldset",
            ),
            self.dates_layout,
            Fieldset(
                _("Abstract"),
                "abstract",
                css_id="abstract-fieldset",
            ),
            Fieldset(
                _("Container"),
                # HTML("<i class='position-absolute top-0 right-0'>?</i>"),
                FormText(
                    _(
                        'A "container" refers to something that holds or contains the main work being cited. A container can be a journal, book, website, or any other larger work that houses smaller works. For example, an article might be contained in a journal, a chapter might be contained in a book, or a webpage might be contained within a larger website.'
                    )
                ),
                Row(
                    Column("container_title", css_class="col-md-8"),
                    Column("container_title_short"),
                ),
                Row(
                    Column("issue"),
                    Column("edition"),
                ),
                "number",
                "number_of_volumes",
                css_id="container-info-fieldset",
                css_class="position-relative",
            ),
            # PUBLISHER
            Fieldset(
                _("Publisher"),
                Row(
                    Column("publisher", css_class="col-md-8"),
                    Column("publisher_place"),
                ),
                css_id="publication-details-fieldset",
            ),
            # ORIG PUBLISHER
            Fieldset(
                _("Original Publisher"),
                FormText(
                    _(
                        "If the item being cited was originally published by a different publisher, provide information related to the original publication below."
                    )
                ),
                PrependedText("original_date", icon("calendar"), wrapper_class="col-9"),
                "original_title",
                Row(
                    Column("original_publisher", css_class="col-md-8"),
                    Column("original_publisher_place"),
                ),
            ),
            Fieldset(
                _("Archiving"),
                Row(
                    Column("archive"),
                    Column("archive_place"),
                ),
                Row(
                    Column("archive_collection"),
                    Column("archive_location"),
                ),
                "call_number",
                css_id="archival-info-fieldset",
            ),
            Fieldset(
                _("Collection Information"),
                FormText(
                    _(
                        'This section is used when citing works that are part of a larger series or anthology. For example, a book that is part of a series, such as "Studies in Modern History," would use the collection title. If it is volume 5 in that series, you would use the collection number field. If the series has editors, like Jane Smith and John Brown, you would include them in the collection editor field below. Use these fields to accurately describe the broader context of the work you are citing, ensuring it can be correctly identified within its series or anthology.'
                    )
                ),
                Row(
                    Column("collection_number", css_class="col-md-3"),
                    Column("collection_title"),
                ),
                css_id="collection-info-fieldset",
            ),
            Fieldset(
                _("Event"),
                Row(
                    Column("event_title"),
                    Column("event_place"),
                ),
            ),
            Fieldset(
                _("Reviewed Item"),
                Row(
                    Column("reviewed_title"),
                    Column("reviewed_genre"),
                ),
            ),
            Fieldset(
                _("Additional Information"),
                "source",
                "references",
                # "custom",
                css_id="notes-fieldset",
            ),
            Fieldset(
                _("Comment"),
                FormText("Use this section to add any additional comments or notes about the citation."),
                "note",
                "annote",
                css_id="comment-fieldset",
            ),
            Fieldset(
                _("Identifiers"),
                "DOI",
                "URL",
                "ISBN",
                "ISSN",
                "PMID",
                "PMCID",
                css_id="identifiers-fieldset",
            ),
            # Fieldset(
            #     _("Deprecated Fields"),
            #     "event",
            #     "title_short",
            #     "collections",
            # ),
            BUTTON_HOLDER,
        )

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


class LiteratureForm(BaseLiteratureForm):
    pass


class CSLForm(BaseLiteratureForm):
    """Used to validate raw CSL JSON data."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in citeproc.NAMES:
            self.fields[field] = NameField(label=field.capitalize())

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self, commit: bool = ...) -> Any:
        obj = super().save(commit)
        obj.dates.set(self.cleaned_data["dates"], bulk=False)
        return obj

    def save_m2m(self):
        return super().save_m2m()
