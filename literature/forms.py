from django import forms
from django.utils.translation import gettext as _
from formset.collection import FormCollection
from formset.fieldset import Fieldset, FieldsetMixin
from formset.renderers.bootstrap import FormRenderer
from formset.widgets import Selectize

from .choices import CSL_TYPE_CHOICES
from .utils import get_types_for_property
from .widgets import PreviewWidget

# BASE CLASSES ====================

SHOW_ALL_CSS = "position-absolute top-0 end-0 mt-2 w-auto"


class CitationJSFormMixin(forms.Form):
    """A mixin that adds a hidden text field for the CSL JSON data and a preview field
    that renders the formatted content.
    """

    CSL = forms.JSONField(widget=forms.HiddenInput())
    preview = forms.CharField(label=_("Preview"), required=False, widget=PreviewWidget)

    class Media:
        js = (
            "https://cdnjs.cloudflare.com/ajax/libs/citation-js/0.7.1/citation.min.js",
            "literature/js/main.js",
        )

    def clean_CSL(self):
        """Clean the CSL JSON data so that a single dict is returned"""
        data = self.cleaned_data["CSL"]
        return data[0]


class CSLFieldset(Fieldset):
    show_all = forms.BooleanField(
        label=_("show non-recommended fields"),
        required=False,
    )

    default_field_css = {
        "*": "mb-2",
        "show_all": "position-absolute top-0 end-0 w-auto",
    }

    def __init__(self, **kwargs):
        self.default_renderer.fieldset_css_classes = "row"
        self.default_renderer.form_css_classes = "row"

        if self.default_renderer.field_css_classes is not None:
            self.default_renderer.field_css_classes.update(self.default_field_css)
        else:
            self.default_renderer.field_css_classes = self.default_field_css

        super().__init__(**kwargs)
        for _fname, f in self.fields.items():
            f.required = False
        # if self.show_all is not True:
        self.update_field_visibility()

    def update_field_visibility(self):
        for fname, field in self.fields.items():
            types = get_types_for_property(fname)
            if not types:
                continue

            show_if = " || ".join([f"basic.type == '{t}'" for t in types])

            field.widget.attrs.update({"df-show": f".show_all || {show_if}"})


class CSLCollection(FormCollection):
    add_label = _("Add")
    default_renderer = FormRenderer(
        collection_css_classes="border-0",
    )


# FORMS ==========================


class DateVariableForm(forms.Form):
    """After the 'date-variable' term list in the CSL specification. Used for fields such as issued, accessed, etc."""

    default_renderer = FormRenderer(
        fieldset_css_classes="row",
        form_css_classes="row",
        field_css_classes={
            "date_type": "col-3",
            "date_format": "col-4",
            "date": "col-6 input-group",
            "season": "col-6",
            "literal": "col-6",
            "circa": "col-1",
        },
    )

    date_type = forms.ChoiceField(
        label=_("type"),
        choices=[
            ("accessed", _("Date Accessed")),
            ("available_date", _("Date Available")),
            ("event_date", _("Event Date")),
            ("issued", _("Date of Issue")),
            ("original_date", _("Original Date")),
            ("submitted", _("Date Submitted")),
        ],
    )
    date_format = forms.ChoiceField(
        label=_("format"),
        choices=[
            ("date-parts", _("Date")),
            ("season", _("Season")),
            ("circa", _("Circa")),
            ("literal", _("Literal")),
            ("raw", _("Raw")),
        ],
    )
    date = forms.CharField(
        label="",
        # help_text=_("Date associated with the item"),
        required=False,
    )
    season = forms.CharField(
        label=_("value"),
        help_text=_("Season associated with the item (e.g. “Spring”)"),
        required=False,
        widget=forms.TextInput(attrs={"df-show": ".date_format=='season'"}),
    )
    circa = forms.BooleanField(
        label=_("circa"),
        # help_text=_("Date is approximate"),
        required=False,
        # widget=forms.TextInput(attrs={"df-show": ".date_format=='circa'"}),
    )

    literal = forms.CharField(
        label=_("value"),
        help_text=_("Literal (e.g. “circa 1900”)"),
        widget=forms.TextInput(attrs={"df-show": ".date_format=='literal'"}),
        required=False,
    )

    def full_clean(self):
        super().full_clean()
        if hasattr(self, "cleaned_data"):
            new_data = {}

            # raise error if all of date, season or literal are Falsey
            if not any(
                [self.cleaned_data.get("date"), self.cleaned_data.get("season"), self.cleaned_data.get("literal")]
            ):
                raise forms.ValidationError(_("Please specify either a date, season or literal value"))

            # # raise error if more than one of date, season or literal are Truey
            # if (
            #     sum(
            #         [
            #             bool(self.cleaned_data.get("date")),
            #             bool(self.cleaned_data.get("season")),
            #             bool(self.cleaned_data.get("literal")),
            #         ]
            #     )
            #     > 1
            # ):
            #     raise forms.ValidationError(_("Please specify only one of date, season or literal"))

            if self.cleaned_data.get("date"):
                new_data["date-parts"] = self.cleaned_data.get("date")

            # add non-empty field
            for field in ["season", "literal", "circa"]:
                if self.cleaned_data.get(field):
                    new_data[field] = self.cleaned_data.get(field)

            self.cleaned_data = {self.cleaned_data.get("date_type"): new_data}

            # if not any()


class NameVariableForm(forms.Form):
    """After the 'name-variable' term list in the CSL specification. Used for fields such as author, editor, etc."""

    default_renderer = FormRenderer(
        fieldset_css_classes="row",
        field_css_classes={
            "*": "mb-2",
            "name_type": "mb-2 col-2",
            "family": "mb-2 col-3",
            "given": "mb-2 col-3",
            "suffix": "mb-2 col-2",
            "name_more": "mb-2 col-2",
            "date_type": "mb-2 col-3",
            "literal": "mb-2 col-10",
        },
    )

    name_type = forms.ChoiceField(
        label=_("format"),
        choices=[
            ("parts", _("Parts")),
            ("literal", _("Literal")),
        ],
        required=False,
    )

    family = forms.CharField(
        label=_("family name"),
        widget=forms.TextInput(attrs={"df-show": ".name_type=='parts'"}),
    )
    given = forms.CharField(
        label=_("given name"),
        widget=forms.TextInput(attrs={"df-show": ".name_type=='parts'"}),
    )
    suffix = forms.CharField(
        label=_("suffix"),
        widget=forms.TextInput(attrs={"df-show": ".name_type=='parts'"}),
    )

    name_more = forms.BooleanField(
        label="",
        help_text=_("more options"),
        widget=forms.CheckboxInput(attrs={"df-show": ".name_type=='parts'"}),
        # widget=forms.CheckboxInput(attrs={"onchange": "updateName(event);"}),
    )

    comma_suffix = forms.CharField(
        label=_("comma suffix"),
        help_text=_("Suffix (e.g. “Jr.”) preceded by a comma"),
        widget=forms.TextInput(attrs={"df-show": ".name_more", "df-hide": ".name_type=='literal'"}),
    )
    non_dropping_particle = forms.CharField(
        label=_("non-dropping particle"),
        help_text=_("Non-dropping particle (e.g. “van” or “de” in Dutch names)"),
        widget=forms.TextInput(attrs={"df-show": ".name_more"}),
    )
    dropping_particle = forms.CharField(
        label=_("dropping particle"),
        help_text=_("Dropping particle (e.g. “van” or “de” in Dutch names)"),
        required=False,
        widget=forms.TextInput(attrs={"df-show": ".name_more"}),
    )
    comma_suffix = forms.CharField(
        label=_("comma suffix"),
        help_text=_("Suffix (e.g. “Jr.”) preceded by a comma"),
        widget=forms.TextInput(attrs={"df-show": ".name_more"}),
    )

    literal = forms.CharField(
        label=_("literal"),
        help_text=_("Literal (e.g. “Anonymous” or “The Association of Medical Professionals”)"),
        widget=forms.TextInput(attrs={"df-show": ".name_type=='literal'"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # set all fields required = False
        for field in self.fields:
            self.fields[field].required = False


class IdentifierForm(forms.Form):
    """After the 'identifier' term list in the CSL specification. Used for fields such as DOI, ISBN, etc."""

    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "identifier_type": "col-3",
            "DOI": "col-9",
            "ISBN": "col-9",
            "ISSN": "col-9",
            "PMCID": "col-9",
            "PMID": "col-9",
            "URL": "col-9",
        },
    )

    identifier_type = forms.ChoiceField(
        label="",
        choices=[
            ("DOI", _("DOI")),
            ("ISBN", _("ISBN")),
            ("ISSN", _("ISSN")),
            ("PMCID", _("PMCID")),
            ("PMID", _("PMID")),
            ("URL", _("URL")),
        ],
    )

    DOI = forms.CharField(
        label="",
        help_text=_("Digital Object Identifier (e.g. “10.1128/AEM.02591-07”)"),
        widget=forms.TextInput(attrs={"df-show": ".identifier_type=='DOI'"}),
        required=False,
    )
    ISBN = forms.CharField(
        label="",
        help_text=_("International Standard Book Number (e.g. “978-3-8474-1017-1”)"),
        widget=forms.TextInput(attrs={"df-show": ".identifier_type=='ISBN'"}),
        required=False,
    )
    ISSN = forms.CharField(
        label="",
        help_text=_("International Standard Serial Number"),
        widget=forms.TextInput(attrs={"df-show": ".identifier_type=='ISSN'"}),
        required=False,
    )
    PMCID = forms.CharField(
        label="",
        help_text=_("PubMed Central reference number"),
        widget=forms.TextInput(attrs={"df-show": ".identifier_type=='PMCID'"}),
        required=False,
    )
    PMID = forms.CharField(
        label="",
        help_text=_("PubMed reference number"),
        widget=forms.TextInput(attrs={"df-show": ".identifier_type=='PMID'"}),
        required=False,
    )
    URL = forms.URLField(
        label="",
        help_text=_("Uniform Resource Locator (e.g. “https://aem.asm.org/cgi/content/full/74/9/2766”)"),
        widget=forms.TextInput(attrs={"df-show": ".identifier_type=='URL'"}),
        required=False,
    )


class Custom(forms.Form):
    default_renderer = FormRenderer(
        fieldset_css_classes="row",
        form_css_classes="row",
        field_css_classes={
            "key": "col-3",
            "value": "col-9",
        },
    )

    key = forms.CharField(
        label=_("key"),
    )
    value = forms.CharField(
        label=_("value"),
        widget=forms.Textarea,
    )


# FIELDSETS ======================


class Basic(CSLFieldset):
    legend = _("basic")
    default_renderer = FormRenderer(
        field_css_classes={
            "type": "mb-2 col-6",
            "citation_key": "mb-2 col-6",
        },
    )

    type = forms.ChoiceField(choices=CSL_TYPE_CHOICES, initial="article", widget=Selectize())
    citation_key = forms.RegexField(
        label=_("citation key"),
        help_text=_("Item identifier (analogous to BibTeX entrykey)"),
        regex=r"^\S+$",
    )
    title = forms.CharField(
        label=_("title"),
        help_text=_("Primary title of the item"),
    )
    number = forms.IntegerField(
        label=_("number"),
        help_text=_("Number identifying the item (e.g. a report number)"),
    )
    event_title = forms.CharField(
        label=_("title"),
        help_text=_(
            "Name of the event related to the item (e.g. the conference name when citing a conference paper; the "
            "meeting where presentation was made)"
        ),
        required=False,
    )

    reviewed_genre = forms.CharField(
        label=_("reviewed genre"),
        help_text=_("Type of the item being reviewed by the current item (e.g. book, film)"),
        required=False,
    )
    reviewed_title = forms.CharField(
        label=_("reviewed title"),
        help_text=_("Title of the item reviewed by the current item"),
    )

    dimensions = forms.CharField(
        label=_("dimensions"),
        help_text=_("Physical (e.g. size) or temporal (e.g. running time) dimensions of the item"),
        required=False,
    )
    medium = forms.CharField(
        label=_("medium"),
        help_text=_("Description of the item`s format or medium (e.g. “CD”, “DVD”, “Album”, etc.)"),
        required=False,
    )
    # map related
    scale = forms.CharField(
        label=_("scale"),
        help_text=_("Scale of e.g. a map or model"),
    )

    genre = forms.CharField(
        label=_("genre"),
        help_text=_(
            "Type, class, or subtype of the item (e.g. “Doctoral dissertation” for a PhD thesis; “NIH Publication” for "
            "an NIH technical report); Do not use for topical descriptions or categories (e.g. “adventure” for an "
            "adventure movie)"
        ),
        required=False,
    )

    event = forms.CharField(
        label=_("event"),
        help_text=_("Deprecated legacy variant of event-title"),
        required=False,
    )
    event_place = forms.CharField(
        label=_("place"),
        help_text=_("Geographic location of the event related to the item (e.g. “Amsterdam, The Netherlands”)"),
        required=False,
    )

    def full_clean(self):
        super().full_clean()
        if hasattr(self, "cleaned_data"):
            del self.cleaned_data["show_all"]


class Container(CSLFieldset):
    legend = _("container")
    help_text = _(
        """Container refers to the larger work that contains the specific referenced item. It is used to represent the context in which the cited work appears. Containers are particularly relevant for types such as "chapter," "article," and "paper-conference.

        For example, in a book citation (type: "book"), the "container" would refer to the book itself. In a chapter citation (type: "chapter"), the "container" would refer to the book or collection containing the specific chapter."""
    )
    default_renderer = FormRenderer(
        field_css_classes={
            "part_number": "col-3",
            "part_title": "col-9",
            "volume": "col-3",
            "volume_title": "col-9",
            "issue": "col-3",
        },
    )
    container_title = forms.CharField(
        label=_("title"),
        help_text=_("Title of the container holding the item"),
        required=False,
    )
    container_title_short = forms.CharField(
        label=_("short title"),
        help_text=_("Short/abbreviated form of the title"),
        required=False,
    )

    part_number = forms.IntegerField(
        label=_("part number"),
        help_text=_(
            "Number of the specific part of the item being cited (e.g. part 2 of a journal article); Use part-title for"
            " the title of the part, if any"
        ),
        required=False,
    )
    part_title = forms.CharField(
        label=_("part title"),
        help_text=_("Title of the specific part of an item being cited"),
        required=False,
    )

    section = forms.IntegerField(
        label=_("section"),
        help_text=_(
            "Section of the item or container holding the item (e.g. “§2.0.1” for a law; “politics” for a newspaper "
            "article)"
        ),
        required=False,
    )

    supplement_number = forms.IntegerField(
        label=_("supplement number"),
        help_text=_(
            "Supplement number of the item or container holding the item (e.g. for secondary legal items that are "
            "regularly updated between editions)"
        ),
        required=False,
    )

    issue = forms.IntegerField(
        label=_("issue"),
        help_text=_("Issue number of the item or container holding the item"),
        required=False,
    )
    volume = forms.IntegerField(
        label=_("volume"),
        help_text=_("Volume number of the item or the container holding the item"),
        required=False,
    )
    volume_title = forms.CharField(
        label=_("volume title"),
        help_text=_(
            "Title of the issue/volume of the item or container holding the item; Also use for titles of periodical"
            " special issues, special sections, and the like"
        ),
        required=False,
    )

    number_of_pages = forms.IntegerField(
        label=_("number of pages"),
        help_text=_("Total number of pages of the cited item"),
        required=False,
    )
    number_of_volumes = forms.IntegerField(
        label=_("number of volumes"),
        help_text=_("Total number of volumes, used when citing multi-volume books and such"),
        required=False,
    )
    printing_number = forms.IntegerField(
        label=_("printing number"),
        help_text=_("Printing number of the item or container holding the item"),
        required=False,
    )

    chapter_number = forms.IntegerField(
        label=_("chapter number"),
        help_text=_("Chapter number (e.g. chapter number in a book; track number on an album)"),
        required=False,
    )

    page = forms.IntegerField(
        label=_("page"),
        help_text=_("Range of pages the item (e.g. a journal article) covers in a container (e.g. a journal issue)"),
        required=False,
    )


class Collection(CSLFieldset):
    legend = _("collection")
    help_text = _("Collection holding the item")
    default_renderer = FormRenderer(
        field_css_classes={
            "collection_number": "col-6",
            "collection_title": "col-6",
        },
    )
    collection_title = forms.CharField(
        label=_("title"),
        help_text=_(
            "Title of the collection holding the item (e.g. the series title for a book; the lecture series title for a"
            " presentation)"
        ),
        required=False,
    )
    collection_title_short = forms.CharField(
        label=_("short title"),
        help_text=_("Short/abbreviated form of collection-title"),
        required=False,
    )


class Detailed(CSLFieldset):
    legend = _("detailed")
    help_text = _("Information related to the item")
    default_renderer = FormRenderer(
        control_css_classes="form-control-sm",
        field_css_classes={
            "collection_number": "col-6",
            "collection_title": "col-6",
            "volume": "col-3",
            "volume_title": "col-9",
        },
    )

    title_short = forms.CharField(
        label=_("short title"),
        help_text=_("Short/abbreviated form of title"),
        required=False,
    )

    abstract = forms.CharField(
        label=_("abstract"),
        help_text=_("Abstract of the item (e.g. the abstract of a journal article)"),
        required=False,
        widget=forms.Textarea,
    )

    status = forms.CharField(
        label=_("status"),
        help_text=_(
            "Publication status of the item (e.g. “forthcoming”; “in press”; “advance online publication”; “retracted”)"
        ),
        required=False,
    )

    publisher = forms.CharField(
        label=_("publisher"),
        help_text=_("Publisher"),
    )
    publisher_place = forms.CharField(
        label=_("publisher place"),
        help_text=_("Geographic location of the publisher"),
        required=False,
    )

    edition = forms.IntegerField(
        label=_("edition"),
        help_text=_("Edition holding the item (e.g. “3” when citing a chapter in the third edition of a book)"),
        required=False,
    )

    locator = forms.IntegerField(
        label=_("locator"),
        help_text=_(
            "A cite-specific pinpointer within the item (e.g. a page number within a book, or a volume in a"
            " multi-volume work); Must be accompanied in the input data by a label indicating the locator type (see the"
            " Locators term list), which determines which term is rendered by cs:label when the locator variable is"
            " selected."
        ),
        required=False,
    )

    page_first = forms.IntegerField(
        label=_("page first"),
        help_text=_(
            "First page of the range of pages the item (e.g. a journal article) covers in a container (e.g. a journal "
            "issue)"
        ),
        required=False,
    )

    authority = forms.CharField(
        label=_("authority"),
        help_text=_(
            "Issuing or judicial authority (e.g. “USPTO” for a patent, “Fairfax Circuit Court” for a legal case)"
        ),
        required=False,
    )
    division = forms.CharField(
        label=_("division"),
        help_text=_("Minor subdivision of a court with a jurisdiction for a legal item"),
        required=False,
    )
    jurisdiction = forms.CharField(
        label=_("jurisdiction"),
        help_text=_("Geographic scope of relevance (e.g. “US” for a US patent; the court hearing a legal case)"),
        required=False,
    )
    references = forms.CharField(
        label=_("references"),
        help_text=_(
            "Resources related to the procedural history of a legal case or legislation; Can also be used to refer to "
            "the procedural history of other items (e.g. “Conference canceled” for a presentation accepted as a "
            "conference that was subsequently canceled; details of a retraction or correction notice)"
        ),
        required=False,
    )


class Archive(CSLFieldset):
    legend = _("archive")
    help_text = _("Archive holding the item")

    default_renderer = FormRenderer(
        form_css_classes="row",
        fieldset_css_classes="row",
        field_css_classes={
            "*": "mb-3",
            "archive": "mb-3 col-6",
            "archive_place": "mb-3 col-6",
            "archive_collection": "mb-3 col-4",
            "archive_location": "mb-3 col-4",
            "call_number": "mb-3 col-4",
        },
    )

    archive = forms.CharField(
        label=_("name"),
        help_text=_("Archive storing the item"),
    )
    archive_place = forms.CharField(
        label=_("place"),
        help_text=_("Geographic location of the archive"),
    )
    archive_collection = forms.CharField(
        label=_("collection"),
        help_text=_("Collection the item is part of within an archive"),
    )
    archive_location = forms.CharField(
        label=_("location"),
        help_text=_("Storage location within an archive (e.g. a box and folder number)"),
        required=False,
    )

    call_number = forms.CharField(
        label=_("call number"),
        help_text=_("Call number (to locate the item in a library)"),
    )


class Origin(CSLFieldset):
    default_renderer = FormRenderer(
        fieldset_css_classes="row",
        field_css_classes={
            "*": "mb-3",
            "original_publisher": "mb-3 col-6",
            "original_publisher_place": "mb-3 col-6",
            "original_title": "mb-3 col-6",
        },
    )

    original_publisher = forms.CharField(
        label=_("original publisher"),
        help_text=_("Original publisher, for items that have been republished by a different publisher"),
        required=False,
    )
    original_publisher_place = forms.CharField(
        label=_("original publisher place"),
        help_text=_("Geographic location of the original publisher (e.g. “London, UK”)"),
        required=False,
    )
    original_title = forms.CharField(
        label=_("original title"),
        help_text=_(
            "Title of the original version (e.g. “Boйнa и миp”, the untranslated Russian title of “War and Peace”)"
        ),
        required=False,
    )


class Metadata(CSLFieldset):
    legend = _("metadata")
    help_text = _("Metadata associated with the item")
    default_renderer = FormRenderer()

    keyword = forms.CharField(
        label=_("keyword"),
        help_text=_("Keyword(s) or tag(s) attached to the item"),
    )
    language = forms.CharField(
        label=_("language"),
        help_text=_(
            "The language of the item; Should be entered as an ISO 639-1 two-letter language code (e.g. “en”, “zh”), "
            "optionally with a two-letter locale code (e.g. “de-DE”, “de-AT”)"
        ),
        required=False,
    )
    license = forms.CharField(
        label=_("license"),
        help_text=_(
            "The license information applicable to an item (e.g. the license an article or software is released under; "
            "the copyright "
            "information for an item; the classification status of a document)"
        ),
        required=False,
    )
    source = forms.CharField(
        label=_("source"),
        help_text=_("Source from whence the item originates (e.g. a library catalog or database)"),
        required=False,
    )

    version = forms.IntegerField(
        label=_("version"),
        help_text=_("Version of the item (e.g. “2.0.9” for a software program)"),
        required=False,
    )

    note = forms.CharField(
        label=_("note"),
        help_text=_("Descriptive text or notes about an item (e.g. in an annotated bibliography)"),
        required=False,
    )
    annote = forms.CharField(
        label=_("annote"),
        help_text=_(
            "Short markup, decoration, or annotation to the item (e.g., to indicate items included in a review); For"
            " descriptive text (e.g., in an annotated bibliography), use note instead"
        ),
        required=False,
    )


# COLLECTIONS ======================


class DateCollection(CSLCollection):
    legend = _("dates")
    extra_siblings = 0
    min_siblings = 0
    date = DateVariableForm()

    @property
    def cleaned_data(self):
        """
        Return the cleaned data for this collection and nested forms/collections.
        """
        cleaned_data = super().cleaned_data
        new_data = {}

        for data_dict in cleaned_data:
            for _k, v in data_dict.items():
                new_data.update(v)

        return new_data


class NameCollection(CSLCollection):
    extra_siblings = 1
    is_sortable = True
    name = NameVariableForm()


class IdentifierCollection(CSLCollection):
    legend = _("identifiers")
    help_text = _(
        "Identifiers associated with the item. Only one identifier of each type is allowed. To associate additional"
        " identifiers with the item, use the custom key-value pairs at the bottom of the form."
    )
    max_siblings = 6
    identifier = IdentifierForm()


class History(CSLCollection):
    legend = _("history")
    help_text = _("History of the item")
    origin = Origin()
    original_author = NameCollection(
        legend=_("Original authors"),
        help_text=_(
            "The original creator of a work (e.g. the form of the author name listed on the original version of a book;"
            " the historical author of a work; the original songwriter or performer for a musical piece; the original"
            " developer or programmer for a piece of software; the original author of an adapted work such as a book"
            " adapted into a screenplay)"
        ),
    )


class Provenance(CSLCollection):
    legend = _("provenance")
    help_text = _("Provenance information for the item")

    archive = Archive()
    history = History()


class Persons(CSLCollection):
    legend = _("contributors")
    help_text = _("Persons or organizations associated with the item")

    author = NameCollection(legend=_("Authors"))
    chair = NameCollection(
        legend=_("Chairs"),
        help_text=_(
            "The person leading the session containing a presentation (e.g. the organizer of the container title of a "
            "speech)"
        ),
    )
    collection_editor = NameCollection(
        legend=_("Collection editors"),
        help_text=_("Editor of the collection holding the item (e.g. the series editor for a book)"),
    )
    compiler = NameCollection(
        legend=_("Compilers"),
        help_text=_(
            "Person compiling or selecting material for an item from the works of various persons or bodies (e.g. for "
            "an anthology)"
        ),
    )
    composer = NameCollection(
        legend=_("Composers"),
        help_text=_("Composer (e.g. of a musical score)"),
    )
    container_author = NameCollection(
        legend=_("Container authors"),
        help_text=_("Author of the container holding the item (e.g. the book author for a book chapter)"),
    )
    contributor = NameCollection(
        legend=_("Minor contributors"),
        help_text=_(
            "A minor contributor to the item; typically cited using “with” before the name when listed in a "
            "bibliography"
        ),
    )
    curator = NameCollection(
        legend=_("Curators"),
        help_text=_("Curator of an exhibit or collection (e.g. in a museum)"),
    )
    director = NameCollection(
        legend=_("Directors"),
        help_text=_("Director (e.g. of a film)"),
    )
    editor = NameCollection(legend=_("Editors"), help_text=_("Editor/s of the item"))
    editorial_director = NameCollection(
        legend=_("Editorial directors"),
        help_text=_("Managing editor (“Directeur de la Publication” in French)"),
    )
    executive_producer = NameCollection(
        legend=_("Executive producers"),
        help_text=_("Executive producer (e.g. of a television series)"),
    )
    guest = NameCollection(
        legend=_("Guests"),
        help_text=_("Guest (e.g. on a TV show or podcast)"),
    )
    host = NameCollection(
        legend=_("Hosts"),
        help_text=_("Host (e.g. of a TV show or podcast)"),
    )
    interviewer = NameCollection(
        legend=_("Interviewers"),
        help_text=_("Interviewer (e.g. of an interview)"),
    )
    illustrator = NameCollection(
        legend=_("Illustrators"),
        help_text=_("Illustrator (e.g. of a children`s book or graphic novel)"),
    )
    narrator = NameCollection(
        legend=_("Narrators"),
        help_text=_("Narrator (e.g. of an audio book)"),
    )
    organizer = NameCollection(
        legend=_("Organizers"),
        help_text=_("Organizer of an event (e.g. organizer of a workshop or conference)"),
    )

    performer = NameCollection(
        legend=_("Performers"),
        help_text=_("Performer of an item (e.g. an actor appearing in a film; a muscian performing a piece of music)"),
    )
    producer = NameCollection(
        legend=_("Producers"),
        help_text=_("Producer (e.g. of a television or radio broadcast)"),
    )
    recipient = NameCollection(
        legend=_("Recipients"),
        help_text=_("Recipient (e.g. of a letter)"),
    )
    reviewed_author = NameCollection(
        legend=_("Reviewed authors"),
        help_text=_("Author of the item reviewed by the current item"),
    )
    script_writer = NameCollection(
        legend=_("Script writers"),
        help_text=_("Writer of a script or screenplay (e.g. of a film)"),
    )
    series_creator = NameCollection(
        legend=_("Series creators"),
        help_text=_("Creator of a series (e.g. of a television series)"),
    )
    translator = NameCollection(legend=_("Translators"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fname, holder in self.declared_holders.items():
            types = get_types_for_property(fname)
            if not types:
                continue

            show_if = " || ".join([f"required.type == '{t}'" for t in types])
            self.recursive_holder_update(holder, show_if)

    def recursive_holder_update(self, holder, show_if):
        for field in holder.declared_holders.values():
            if issubclass(type(field), FormCollection):
                self.recursive_holder_update(field, show_if)
            elif issubclass(type(field), FieldsetMixin):
                holder.show_condition = show_if


class CustomData(CSLCollection):
    legend = _("custom")
    help_text = _(
        "Used to store additional information that does not have a designated CSL JSON field. The custom field is"
        " preferred over the note field for storing custom data, particularly for storing key-value pairs, as the note"
        " field is used for user annotations in annotated bibliography styles."
    )
    extra_siblings = 1

    custom = Custom()


# USEABLE FORMS ===================
class LiteratureForm(FormCollection):
    default_renderer = FormRenderer(
        form_css_classes="row",
        control_css_classes="form-control-sm",
        fieldset_css_classes="row",
        collection_css_classes="pb-4 mt-4 border-bottom",
        field_css_classes={
            "*": "mb-3",
        },
    )

    basic = Basic()
    dates = DateCollection()

    @property
    def cleaned_data(self):
        """
        Return the cleaned data for this collection and nested forms/collections.
        """
        cleaned_data = super().cleaned_data
        return cleaned_data

    def construct_instance(self, instance=None):
        return super().construct_instance(instance)

    # def full_clean(self):
    #     super().full_clean()
    #     new_data = {}
    #     for value in self.cleaned_data.values():
    #         new_data.update(value)

    #     self.cleaned_data = new_data

    #     x = 8

    # container = Container()
    # collection = Collection()
    # detailed = Detailed()
    # identifiers = IdentifierCollection()
    # # persons = Persons()

    # dates = DateCollection()
    # provenance = Provenance()
    # metadata = Metadata()
    # custom = CustomData()
