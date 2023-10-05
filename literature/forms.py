from django import forms
from django.forms.models import ModelForm, construct_instance, model_to_dict
from django.utils.translation import gettext as _
from entangled.forms import EntangledModelForm

from literature.conf import settings

from .csl_map import CSL_FIELDS, LITERATURE_FIELD_MAP
from .models import Literature, SupplementaryMaterial
from .widgets import OnlineSearchWidget, PDFFileInput, PreviewWidget

csl_fields = [f.replace("-", "_") for f in CSL_FIELDS.keys()]


class CitationJSFormMixin(forms.Form):
    """A mixin that adds a hidden text field for the CSL JSON data and a preview field
    that renders the formatted content.
    """

    CSL = forms.JSONField(widget=forms.HiddenInput())
    preview = forms.CharField(label=_("Preview"), required=False, widget=PreviewWidget)

    class Media:
        js = (
            settings.LITERATURE_CITATION_JS_SOURCE,
            "literature/js/main.js",
        )

    def clean_CSL(self):
        """Clean the CSL JSON data so that a single dict is returned"""
        data = self.cleaned_data["CSL"]
        return data[0]


class OnlineSearchForm(CitationJSFormMixin, forms.ModelForm):
    """A form that renders a search bar for DOI, PMCID, PMID, Wikidata and previews the
    formatted content below. Data is appended to a hidden text field when submitting.
    """

    identifier = forms.CharField(
        label=_("Identifier"),
        help_text=_(
            "Enter a valid DOI, ISBN, PMCID, PMID, Wikidata QID or GitHub repository URL to gather citation data"
        ),
        widget=forms.TextInput(attrs={"onchange": "fetchCitation();"}),
        # widget=OnlineSearchWidget,
        required=False,
    )

    class Meta:
        model = Literature
        fields = ["identifier", "CSL", "preview"]


class BibFileUploadForm(CitationJSFormMixin, forms.ModelForm):
    """A form that accepts a bibliography file, parses and previews it using citation.js,
    then submits CSL-JSON data to the server for validation and saving via a hidden text
    field.
    """

    file = forms.FileField(
        label=_("Bibliography File"),
        help_text=_("Upload a bibliography file."),
        widget=forms.FileInput(attrs={"onchange": "readFileContents();"}),
        required=False,
    )

    class Meta:
        model = Literature
        fields = ["file", "CSL", "preview"]


class CSLForm(forms.Form):
    DOI = forms.CharField(
        label="DOI", help_text=_("Digital Object Identifier (e.g. “10.1128/AEM.02591-07”)"), required=False
    )
    ISBN = forms.CharField(
        label="ISBN", help_text=_("International Standard Book Number (e.g. “978-3-8474-1017-1”)"), required=False
    )
    ISSN = forms.CharField(label="ISSN", help_text=_("International Standard Serial Number"), required=False)
    PMCID = forms.CharField(label="PMCID", help_text=_("PubMed Central reference number"), required=False)
    PMID = forms.CharField(label="PMID", help_text=_("PubMed reference number"), required=False)
    URL = forms.URLField(
        label="URL",
        help_text=_("Uniform Resource Locator (e.g. “https://aem.asm.org/cgi/content/full/74/9/2766”)"),
        required=False,
    )
    abstract = forms.CharField(
        label=_("abstract"),
        help_text=_("Abstract of the item (e.g. the abstract of a journal article)"),
        required=False,
        widget=forms.Textarea,
    )
    accessed = forms.DateField(label=_("accessed"), help_text=_("Date the item has been accessed"), required=False)
    annote = forms.CharField(
        label=_("annote"),
        help_text=_(
            "Short markup, decoration, or annotation to the item (e.g., to indicate items included in a review); For"
            " descriptive text (e.g., in an annotated bibliography), use note instead"
        ),
        required=False,
    )
    archive = forms.CharField(label=_("archive"), help_text=_("Archive storing the item"), required=False)
    archive_place = forms.CharField(
        label=_("archive place"), help_text=_("Geographic location of the archive"), required=False
    )
    archive_collection = forms.CharField(
        label=_("archive collection"), help_text=_("Collection the item is part of within an archive"), required=False
    )
    archive_location = forms.CharField(
        label=_("archive location"),
        help_text=_("Storage location within an archive (e.g. a box and folder number)"),
        required=False,
    )
    author = forms.CharField(label=_("author"), help_text=_("Author"), required=False)
    authority = forms.CharField(
        label=_("authority"),
        help_text=_(
            "Issuing or judicial authority (e.g. “USPTO” for a patent, “Fairfax Circuit Court” for a legal case)"
        ),
        required=False,
    )
    available_date = forms.DateField(
        label=_("available date"),
        help_text=_(
            "Date the item was initially available (e.g. the online publication date of a journal article before its "
            "formal publication date; the date a treaty was made available for signing)"
        ),
        required=False,
    )
    call_number = forms.CharField(
        label=_("call number"), help_text=_("Call number (to locate the item in a library)"), required=False
    )
    chair = forms.CharField(
        label=_("chair"),
        help_text=_(
            "The person leading the session containing a presentation (e.g. the organizer of the container title of a "
            "speech)"
        ),
        required=False,
    )
    chapter_number = forms.IntegerField(
        label=_("chapter number"),
        help_text=_("Chapter number (e.g. chapter number in a book; track number on an album)"),
        required=False,
    )
    citation_key = forms.CharField(
        label=_("citation key"),
        help_text=_(
            "Identifier of the item in the input data file (analogous to BibTeX entrykey); Use this variable to "
            "facilitate conversion between word-processor and plain-text writing systems; For an identifer intended as"
            " formatted output label for a citation (e.g. “Ferr78”), use citation-label instead"
        ),
        required=False,
    )
    citation_label = forms.CharField(
        label=_("citation label"),
        help_text=_(
            "Label identifying the item in in-text citations of label styles (e.g. “Ferr78”); May be assigned by the "
            "CSL processor based on item metadata; For the identifier of the item in the input data file, use citation "
            "key instead"
        ),
        required=False,
    )
    citation_number = forms.IntegerField(
        label=_("citation number"),
        help_text=_(
            "Index (starting at 1) of the cited reference in the bibliography (generated by the CSL processor)"
        ),
        required=False,
    )
    collection_editor = forms.CharField(
        label=_("collection editor"),
        help_text=_("Editor of the collection holding the item (e.g. the series editor for a book)"),
        required=False,
    )
    collection_number = forms.IntegerField(
        label=_("collection number"),
        help_text=_("Number identifying the collection holding the item (e.g. the series number for a book)"),
        required=False,
    )
    collection_title = forms.CharField(
        label=_("collection title"),
        help_text=_(
            "Title of the collection holding the item (e.g. the series title for a book; the lecture series title for a"
            " presentation)"
        ),
        required=False,
    )
    compiler = forms.CharField(
        label=_("compiler"),
        help_text=_(
            "Person compiling or selecting material for an item from the works of various persons or bodies (e.g. for "
            "an anthology)"
        ),
        required=False,
    )
    composer = forms.CharField(label=_("composer"), help_text=_("Composer (e.g. of a musical score)"), required=False)
    container_author = forms.CharField(
        label=_("container author"),
        help_text=_("Author of the container holding the item (e.g. the book author for a book chapter)"),
        required=False,
    )
    container_title = forms.CharField(
        label=_("container title"),
        help_text=_(
            "Title of the container holding the item (e.g. the book title for a book chapter, the journal title for a "
            "journal article; the album title for a recording; the session title for multi-part presentation at a "
            "conference)"
        ),
        required=False,
    )
    container_title_short = forms.CharField(
        label=_("container title (short)"),
        help_text=_(
            'Short/abbreviated form of container-title; Deprecated; use variable="container title" form="short" instead'
        ),
        required=False,
    )
    contributor = forms.CharField(
        label=_("contributor"),
        help_text=_(
            "A minor contributor to the item; typically cited using “with” before the name when listed in a "
            "bibliography"
        ),
        required=False,
    )
    curator = forms.CharField(
        label=_("curator"), help_text=_("Curator of an exhibit or collection (e.g. in a museum)"), required=False
    )
    dimensions = forms.CharField(
        label=_("dimensions"),
        help_text=_("Physical (e.g. size) or temporal (e.g. running time) dimensions of the item"),
        required=False,
    )
    director = forms.CharField(label=_("director"), help_text=_("Director (e.g. of a film)"), required=False)
    division = forms.CharField(
        label=_("division"),
        help_text=_("Minor subdivision of a court with a jurisdiction for a legal item"),
        required=False,
    )
    edition = forms.IntegerField(
        label=_("edition"),
        help_text=_("Edition holding the item (e.g. “3” when citing a chapter in the third edition of a book)"),
        required=False,
    )
    editor = forms.CharField(label=_("editor"), help_text=_("Editor"), required=False)
    editor_translator = forms.CharField(
        label=_("editor translator"),
        help_text=_(
            "Combined editor and translator of a work; The citation processory must be automatically generate if editor"
            " and translator variables are identical; May also be provided directly in item data"
        ),
        required=False,
    )
    editorial_director = forms.CharField(
        label=_("editorial director"),
        help_text=_("Managing editor (“Directeur de la Publication” in French)"),
        required=False,
    )
    event = forms.CharField(
        label=_("event"),
        help_text=_("Deprecated legacy variant of event-title"),
        required=False,
    )
    # event_date = forms.DateField(
    event_date = forms.JSONField(
        label=_("event date"),
        help_text=_("Date the event related to an item took place"),
        required=False,
    )
    event_place = forms.CharField(
        label=_("event place"),
        help_text=_("Geographic location of the event related to the item (e.g. “Amsterdam, The Netherlands”)"),
        required=False,
    )
    event_title = forms.CharField(
        label=_("event title"),
        help_text=_(
            "Name of the event related to the item (e.g. the conference name when citing a conference paper; the "
            "meeting where presentation was made)"
        ),
        required=False,
    )
    executive_producer = forms.CharField(
        label=_("executive producer"), help_text=_("Executive producer (e.g. of a television series)"), required=False
    )
    first_reference_note_number = forms.IntegerField(
        label=_("first reference note number"),
        help_text=_(
            "Number of a preceding note containing the first reference to the item; Assigned by the CSL processor; "
            "Empty in non-note-based styles or when the item hasn`t been cited in any preceding notes in a document"
        ),
        required=False,
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
    guest = forms.CharField(label=_("guest"), help_text=_("Guest (e.g. on a TV show or podcast)"), required=False)
    host = forms.CharField(label=_("host"), help_text=_("Host (e.g. of a TV show or podcast)"), required=False)
    illustrator = forms.CharField(
        label=_("illustrator"),
        help_text=_("Illustrator (e.g. of a children`s book or graphic novel)"),
        required=False,
    )
    interviewer = forms.CharField(
        label=_("interviewer"), help_text=_("Interviewer (e.g. of an interview)"), required=False
    )
    issue = forms.IntegerField(
        label=_("issue"),
        help_text=_(
            "Issue number of the item or container holding the item (e.g. “5” when citing a journal article from "
            "journal volume 2, issue 5); Use volume title for the title of the issue, if any"
        ),
        required=False,
    )
    # issued = forms.DateField(
    issued = forms.JSONField(label=_("issued"), help_text=_("Date the item was issued/published"), required=False)
    jurisdiction = forms.CharField(
        label=_("jurisdiction"),
        help_text=_("Geographic scope of relevance (e.g. “US” for a US patent; the court hearing a legal case)"),
        required=False,
    )
    keyword = forms.CharField(
        label=_("keyword"), help_text=_("Keyword(s) or tag(s) attached to the item"), required=False
    )
    language = forms.CharField(
        label=_("language"),
        help_text=_(
            "The language of the item; Should be entered as an ISO 639-1 two-letter language code (e.g. “en”, “zh”), "
            "optionally with a two-letter locale code (e.g. “de-DE”, “de-AT”)"
        ),
        required=False,
    )
    license = forms.CharField(  # noqa: A003
        label=_("license"),
        help_text=_(
            "The license information applicable to an item (e.g. the license an article or software is released under; "
            "the copyright "
            "information for an item; the classification status of a document)"
        ),
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
    medium = forms.CharField(
        label=_("medium"),
        help_text=_("Description of the item`s format or medium (e.g. “CD”, “DVD”, “Album”, etc.)"),
        required=False,
    )
    narrator = forms.CharField(label=_("narrator"), help_text=_("Narrator (e.g. of an audio book)"), required=False)
    note = forms.CharField(
        label=_("note"),
        help_text=_("Descriptive text or notes about an item (e.g. in an annotated bibliography)"),
        required=False,
    )
    number = forms.IntegerField(
        label=_("number"), help_text=_("Number identifying the item (e.g. a report number)"), required=False
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
    organizer = forms.CharField(
        label=_("organizer"),
        help_text=_("Organizer of an event (e.g. organizer of a workshop or conference)"),
        required=False,
    )
    original_author = forms.CharField(
        label=_("original author"),
        help_text=_(
            "The original creator of a work (e.g. the form of the author name listed on the original version of a book;"
            " the historical author of a work; the original songwriter or performer for a musical piece; the original"
            " developer or programmer for a piece of software; the original author of an adapted work such as a book"
            " adapted into a screenplay)"
        ),
        required=False,
    )
    original_date = forms.DateField(
        label=_("original date"), help_text=_("Issue date of the original version"), required=False
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
    page = forms.IntegerField(
        label=_("page"),
        help_text=_("Range of pages the item (e.g. a journal article) covers in a container (e.g. a journal issue)"),
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
    performer = forms.CharField(
        label=_("performer"),
        help_text=_("Performer of an item (e.g. an actor appearing in a film; a muscian performing a piece of music)"),
        required=False,
    )
    printing_number = forms.IntegerField(
        label=_("printing number"),
        help_text=_("Printing number of the item or container holding the item"),
        required=False,
    )
    producer = forms.CharField(
        label=_("producer"), help_text=_("Producer (e.g. of a television or radio broadcast)"), required=False
    )
    publisher = forms.CharField(label=_("publisher"), help_text=_("Publisher"), required=False)
    publisher_place = forms.CharField(
        label=_("publisher place"),
        help_text=_("Geographic location of the publisher"),
        required=False,
    )
    recipient = forms.CharField(label=_("recipient"), help_text=_("Recipient (e.g. of a letter)"), required=False)
    references = forms.CharField(
        label=_("references"),
        help_text=_(
            "Resources related to the procedural history of a legal case or legislation; Can also be used to refer to "
            "the procedural history of other items (e.g. “Conference canceled” for a presentation accepted as a "
            "conference that was subsequently canceled; details of a retraction or correction notice)"
        ),
        required=False,
    )
    reviewed_author = forms.CharField(
        label=_("reviewed author"), help_text=_("Author of the item reviewed by the current item"), required=False
    )
    reviewed_genre = forms.CharField(
        label=_("reviewed genre"),
        help_text=_("Type of the item being reviewed by the current item (e.g. book, film)"),
        required=False,
    )
    reviewed_title = forms.CharField(
        label=_("reviewed title"), help_text=_("Title of the item reviewed by the current item"), required=False
    )
    scale = forms.CharField(label=_("scale"), help_text=_("Scale of e.g. a map or model"), required=False)
    script_writer = forms.CharField(
        label=_("script writer"),
        help_text=_("Writer of a script or screenplay (e.g. of a film)"),
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
    series_creator = forms.CharField(
        label=_("series creator"),
        help_text=_("Creator of a series (e.g. of a television series)"),
        required=False,
    )
    source = forms.CharField(
        label=_("source"),
        help_text=_("Source from whence the item originates (e.g. a library catalog or database)"),
        required=False,
    )
    status = forms.CharField(
        label=_("status"),
        help_text=_(
            "Publication status of the item (e.g. “forthcoming”; “in press”; “advance online publication”; “retracted”)"
        ),
        required=False,
    )
    submitted = forms.DateField(
        label=_("submitted"),
        help_text=_("Date the item (e.g. a manuscript) was submitted for publication"),
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
    title = forms.CharField(label=_("title"), help_text=_("Primary title of the item"), required=False)
    title_short = forms.CharField(
        label=_("title short"),
        help_text=_('Short/abbreviated form of title; Deprecated; use variable="title" form="short" instead'),
        required=False,
    )
    translator = forms.CharField(label=_("translator"), help_text=_("Translator"), required=False)
    version = forms.IntegerField(
        label=_("version"),
        help_text=_("Version of the item (e.g. “2.0.9” for a software program)"),
        required=False,
    )
    volume = forms.IntegerField(
        label=_("volume"),
        help_text=_(
            "Volume number of the item (e.g. “2” when citing volume 2 of a book) or the container holding the item"
            " (e.g. “2” when citing a chapter from volume 2 of a book); Use volume title for the title of the volume,"
            " if any"
        ),
        required=False,
    )
    volume_title = forms.CharField(
        label=_("volume title"),
        help_text=_(
            "Title of the volume of the item or container holding the item; Also use for titles of periodical special "
            "issues, special sections, and the like"
        ),
        required=False,
    )
    year_suffix = forms.CharField(
        label=_("year suffix"),
        help_text=_("Disambiguating year suffix in author date styles (e.g. “a” in “Doe, 1999a”)"),
        required=False,
    )

    class Media:
        js = ("literature/js/form.js",)


class LiteratureForm(CSLForm, EntangledModelForm):
    class Meta:
        model = Literature
        entangled_fields = {"CSL": csl_fields}
        untangled_fields = [
            "type",
            "pdf",
        ]
        parent_selector = settings.LITERATURE_ADMIN_NODE_SELECTOR
        parent_selector_override = {}

        widgets = {
            "type": forms.Select(choices=Literature.TypeChoices.choices, attrs={"onchange": "updateForm(event);"}),
            "pdf": forms.ClearableFileInput(),
        }

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.fields["type"].widget.attrs["data-CSL-parent"] = self.Meta.parent_selector_override.get(
            "type", self.Meta.parent_selector
        )

        # add a data-lit-show="true" attribute to the form fields listed in Meta.always_show. Default to Meta.untangled_fields.
        for field in self.Meta.entangled_fields["CSL"]:
            # this attribute is used by javascript to hide/show fields depending on the "type" field
            self.fields[field].widget.attrs["data-CSL"] = "true"
            self.fields[field].widget.attrs["data-CSL-parent"] = self.Meta.parent_selector_override.get(
                field, self.Meta.parent_selector
            )

    def full_clean(self, *args, **kwargs):
        """Override full_clean to remove the CSL field from the cleaned_data dict"""
        super().full_clean(*args, **kwargs)

        # map for fields back to the correct hyphen-separated format
        CSL_DATA = self.cleaned_data["CSL"]
        for field in LITERATURE_FIELD_MAP:
            if field in CSL_DATA:
                print(f"changing {field} to {LITERATURE_FIELD_MAP[field]} ")
                CSL_DATA[LITERATURE_FIELD_MAP[field]] = CSL_DATA.pop(field)

        import pprint

        pprint.pprint(self.cleaned_data)

        # self.cleaned_data.pop("CSL", None)
