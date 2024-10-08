from typing import Any

from crispy_bootstrap5.bootstrap5 import Switch
from crispy_forms.layout import Column, Fieldset, Row
from django import forms
from django.utils.translation import gettext as _

from ..models import LiteratureItem

# from .choices import CSL_TYPE_CHOICES
from .fields import DateVariableField, NameField
from .layouts import DateVariable, HelpText
from .widgets import FlatJSONWidget


class DateFormMixin(forms.Form):
    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        cleaned_data["dates"] = []
        for f in ["accessed", "available_date", "event_date", "issued", "original_date", "submitted"]:
            if cleaned_data.get(f):
                cleaned_data["dates"].append(cleaned_data[f])

        return cleaned_data


class Abstract(forms.Form):
    abstract = forms.CharField(
        label=False,
        required=False,
        widget=forms.Textarea(),
    )

    layout = Fieldset(
        _("Abstract"),
        "abstract",
        css_id="abstract-fieldset",
    )


class Identifiers(forms.Form):
    DOI = forms.CharField(
        label=_("DOI"),
        required=False,
        help_text=_(
            "The Digital Object Identifier (DOI) of the work, a unique alphanumeric string to identify content and provide a persistent link to its location on the internet."
        ),
    )
    URL = forms.URLField(
        label=_("URL"),
        required=False,
        help_text=_("The Uniform Resource Locator (URL) of the work, a web address where the work can be accessed."),
    )
    ISBN = forms.CharField(
        label=_("ISBN"),
        required=False,
        help_text=_("The International Standard Book Number (ISBN) of the work, a unique identifier for books."),
    )
    ISSN = forms.CharField(
        label=_("ISSN"),
        required=False,
        help_text=_(
            "The International Standard Serial Number (ISSN) of the work, a unique identifier for periodicals such as journals and magazines."
        ),
    )
    PMID = forms.CharField(
        label=_("PMID"),
        required=False,
        help_text=_(
            "The PubMed Identifier (PMID) of the work, a unique number assigned to each PubMed listed publication."
        ),
    )
    PMCID = forms.CharField(
        label=_("PMCID"),
        required=False,
        help_text=_(
            "The PubMed Central Identifier (PMCID) of the work, a unique identifier for articles archived in PubMed Central."
        ),
    )

    layout = Fieldset(
        _("Identifiers"),
        "DOI",
        "URL",
        "ISBN",
        "ISSN",
        "PMID",
        "PMCID",
        css_id="identifiers-fieldset",
    )


class RequiredInformation(forms.Form):
    citation_key = forms.CharField(
        label=_("Citation Key"),
        help_text=_("A unique key used to identify the citation in your library."),
        required=False,
    )
    title = forms.CharField(
        label=_("Title"),
        help_text=_("The title of the resource being cited."),
        required=True,
    )
    type = forms.ChoiceField(
        label=_("Type"),
        required=False,
        choices=LiteratureItem.CSL_TYPE_CHOICES,
    )
    show_suggested = forms.BooleanField(
        label=_("Suggested fields only"),
        required=False,
        initial=False,
    )

    layout = Fieldset(
        _("Required Fields"),
        Row(
            Column("citation_key", css_class="col-md-6"),
            Column("type"),
        ),
        "title",
        Switch("show_suggested"),
        css_id="required-info-fieldset",
    )


class EventInformation(forms.Form):
    event_title = forms.CharField(
        label=_("Name"),
        required=False,
        help_text=_("The name or title of the event."),
    )
    event_place = forms.CharField(
        label=_("Location"), required=False, help_text=_("The location where the event took place.")
    )
    event_date = DateVariableField(
        label=_("Event Date"),
        required=False,
        help_text=_(
            "The date when the event occurred. This is typically used for conference papers, presentations, or other time-specific events."
        ),
    )

    organizer = NameField(
        label=_("Organizer(s)"), required=False, help_text=_("Name(s) of the person(s) who organized the event.")
    )
    chair = NameField(
        label=_("Chair(s)"),
        required=False,
        help_text=_("Name(s) of the person(s) who chaired the event or committee."),
    )

    layout = Fieldset(
        _("Event Information"),
        Row(
            Column("event_title", css_class="col-md-8"),
            Column("event_place"),
        ),
        DateVariable("event_date"),
        "chair",
        "organizer",
        css_id="event-info-fieldset",
    )


class ReviewedItem(forms.Form):
    reviewed_title = forms.CharField(
        label=_("Title"),
        required=False,
        help_text=_("The title of the work being reviewed."),
    )
    reviewed_genre = forms.CharField(
        label=_("Type"),
        required=False,
        help_text=_("The genre or type of the work being reviewed, such as book, article, movie, etc."),
    )
    reviewed_author = NameField(
        label=_("Reviewed Author(s)"),
        required=False,
        help_text=_("Name(s) of the author(s) of the work being reviewed."),
    )

    layout = Fieldset(
        _("Reviewed Item"),
        Row(
            Column("reviewed_title", css_class="col-md-8"),
            Column("reviewed_genre"),
        ),
        "reviewed_author",
        css_id="review-info-fieldset",
    )


class MediaProduction(forms.Form):
    performer = NameField(
        label=_("Performer(s)"),
        required=False,
        help_text=_("Name(s) of the person(s) who performed in the work, such as actors, musicians, etc."),
    )
    director = NameField(
        label=_("Director(s)"),
        required=False,
        help_text=_("Name(s) of the director(s) who oversaw the production of the film, play, or other performance."),
    )
    producer = NameField(
        label=_("Producer(s)"),
        required=False,
        help_text=_("Name(s) of the producer(s) who managed the creation and production of the work."),
    )
    script_writer = NameField(
        label=_("Script Writer(s)"),
        required=False,
        help_text=_("Name(s) of the writer(s) who created the script or screenplay."),
    )
    series_creator = NameField(
        label=_("Series Creator(s)"),
        required=False,
        help_text=_("Name(s) of the creator(s) of the series."),
    )
    interviewer = NameField(
        label=_("Interviewer(s)"), required=False, help_text=_("Name(s) of the person(s) who conducted the interview.")
    )
    narrator = NameField(
        label=_("Narrator(s)"),
        required=False,
        help_text=_("Name(s) of the person(s) who provided the narration for the work."),
    )
    executive_producer = NameField(
        label=_("Executive Producer(s)"),
        required=False,
        help_text=_("Name(s) of the executive producer(s) who oversaw the production of the work."),
    )
    guest = NameField(
        label=_("Guest(s)"), required=False, help_text=_("Name(s) of the guest(s) featured in the work or event.")
    )
    host = NameField(
        label=_("Host(s)"),
        required=False,
        help_text=_("Name(s) of the host(s) who presented or led the event or program."),
    )
    composer = NameField(
        label=_("Composer(s)"),
        required=False,
        help_text=_("Name(s) of the composer(s) who created the musical work."),
    )

    layout = Fieldset(
        _("Media Production"),
        "performer",
        "director",
        "producer",
        "script_writer",
        "series_creator",
        "interviewer",
        "narrator",
        "executive_producer",
        "guest",
        "host",
        "composer",
        css_id="media-production-fieldset",
    )


class AdditionalInformation(forms.Form):
    accessed = DateVariableField(
        label=_("Date accessed"),
        help_text=_(
            "Enter the date when the resource was last accessed or retrieved. This is often used for online resources to indicate when the information was accessed by the user."
        ),
        required=False,
    )
    source = forms.CharField(
        label=_("Source"),
        required=False,
        help_text=_("The source of the work, such as a website, journal, or other publication."),
    )
    note = forms.CharField(
        label=_("Note"),
        required=False,
        widget=forms.Textarea(),
        help_text=_("Additional notes or comments about the work or citation."),
    )
    # keyword = forms.CharField(
    #     label=_("Keyword"),
    #     required=False,
    #     help_text=_("Keywords or phrases that describe the content or subject matter of the work."),
    # )
    categories = forms.CharField(
        label=_("Categories"),
        required=False,
        help_text=_("The categories or tags associated with the work."),
    )

    layout = Fieldset(
        _("Additional Information"),
        "keyword",
        "categories",
        DateVariable("accessed"),
        "source",
        "note",
        css_id="additional-info-fieldset",
    )


class Page(forms.Form):
    page = forms.CharField(
        label=_("Page"), required=False, help_text=_("The specific page or page range within a work, such as 34-56.")
    )
    number_of_pages = forms.IntegerField(
        label=_("Number of Pages"),
        required=False,
        help_text=_("The total number of pages in the work."),
    )
    page_first = forms.CharField(
        label=_("First Page"),
        required=False,
        help_text=_("The first page number of the work, typically used for journal articles."),
    )

    layout = Fieldset(
        _("Pages"),
        "page",
        Row(
            Column("page_first", css_class="col-md-6"),
            Column("number_of_pages", css_class="col-md-6"),
        ),
        css_id="pages-fieldset",
    )

    # def clean(self):
    #     cleaned = super().clean()
    #     prange = cleaned.get("page").split("-")
    #     first = cleaned.get("page_first") or prange[0]
    #     num = cleaned.get("number_of_pages") or (int(prange[1]) - int(first) + 1)
    #     if cleaned.get("page_first"):
    #         cleaned["page"] = cleaned.pop("page_first")
    #     return cleaned


class GeneralInformation(Page, MediaProduction, EventInformation, ReviewedItem, Identifiers, forms.Form):
    title_short = forms.CharField(
        label=_("Short Title"),
        required=False,
        help_text=_("A brief version of the title, useful for references and citations."),
    )
    shortTitle = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
    )

    author = NameField(
        label=_("Author(s)"),
        required=False,
        help_text=_("Name(s) of the primary creator(s) of the work."),
    )
    authority = NameField(
        label=_("Authority"),
        required=False,
        help_text=_("The official or authoritative body associated with the work, if applicable."),
    )
    annote = forms.CharField(
        label=_("Annotation"),
        required=False,
        widget=forms.Textarea(),
        help_text=_(
            "Short markup, decoration, or annotation to the item (e.g., to indicate items included in a review); For descriptive text (e.g., in an annotated bibliography), use note instead"
        ),
    )
    chapter_number = forms.CharField(
        label=_("Chapter Number"),
        required=False,
        help_text=_("The specific chapter number within a larger work or book."),
    )
    genre = forms.CharField(
        label=_("Sub-type"),
        required=False,
        help_text=_(
            "The specific type, sub-type or category of the source material (e.g., film, brochure, artwork, government report)."
        ),
    )
    status = forms.CharField(
        label=_("Status"),
        required=False,
        help_text=_("The current status of the work, such as published, unpublished, in-progress, etc."),
    )
    version = forms.CharField(
        label=_("Version"), required=False, help_text=_("The specific version or edition of the work.")
    )

    dimensions = forms.CharField(
        label=_("Dimensions"),
        required=False,
        help_text=_("The physical dimensions of the work, typically in centimeters or inches."),
    )
    medium = forms.CharField(
        label=_("Medium"),
        required=False,
        help_text=_("The format or medium of the work, such as print, digital, audio, etc."),
    )
    volume = forms.CharField(
        label=_("Volume"), required=False, help_text=_("The volume number if the work is part of a multi-volume set.")
    )
    volume_title = forms.CharField(
        label=_("Volume Title"),
        required=False,
        help_text=_("The title of the specific volume within a larger set or series."),
    )
    volume_title_short = forms.CharField(
        label=_("Volume Short Title"),
        required=False,
        help_text=_("A brief version of the volume title, useful for references and citations."),
    )
    # locator = forms.CharField(
    #     label=_("Locator"),
    #     required=False,
    #     help_text=_("A specific location within the work, such as a paragraph, section, or figure number."),
    # )
    # locator_type = forms.CharField(
    #     label=_("Locator Type"),
    #     required=False,
    #     help_text=_("The type of locator used to identify the specific location within the work."),
    # )
    # Names
    compiler = NameField(
        label=_("Compiler(s)"),
        required=False,
        help_text=_("Name(s) of the person(s) who compiled the work from various sources."),
    )
    contributor = NameField(
        label=_("Contributor(s)"),
        required=False,
        help_text=_("Name(s) of the person(s) who contributed to the creation of the work."),
    )
    editor = NameField(
        label=_("Editor(s)"),
        required=False,
        help_text=_("Name(s) of the editor(s) who reviewed and prepared the work for publication."),
    )
    editorial_director = NameField(
        label=_("Editorial Director(s)"),
        required=False,
        help_text=_("Name(s) of the editorial director(s) overseeing the editorial process of the work."),
    )
    illustrator = NameField(
        label=_("Illustrator(s)"),
        required=False,
        help_text=_("Name(s) of the illustrator(s) who created the illustrations for the work."),
    )
    recipient = NameField(
        label=_("Recipient(s)"),
        required=False,
        help_text=_("Name(s) of the person(s) who received the correspondence or work."),
    )
    translator = NameField(
        label=_("Translator(s)"),
        required=False,
        help_text=_("Name(s) of the person(s) who translated the work from one language to another."),
    )

    jurisdiction = forms.CharField(
        label=_("Jurisdiction"),
        required=False,
        help_text=_("The legal jurisdiction or geographic scope of relevance associated with the work."),
    )

    language = forms.CharField(
        label=_("Language"),
        required=False,
        help_text=_("The language in which the work is written or presented."),
    )

    division = forms.CharField(
        label=_("Division"),
        required=False,
        help_text=_("The division or section of the work where the information can be found."),
    )

    part = forms.CharField(
        label=_("Part"),
        required=False,
        help_text=_("The specific part or section of the work where the information can be found."),
    )
    part_title = forms.CharField(
        label=_("Part Title"),
        required=False,
        help_text=_("The title of the specific part or section of the work."),
    )
    printing = forms.CharField(
        label=_("Printing"),
        required=False,
        help_text=_("The specific printing or edition of the work, such as first edition, second printing, etc."),
    )
    references = forms.CharField(
        label=_("References"),
        required=False,
        widget=forms.Textarea(),
        help_text=_("A list of references or sources cited within the work."),
    )
    scale = forms.CharField(
        label=_("Scale"),
        required=False,
        help_text=_("The scale of the work, typically used for maps or other visual representations."),
    )
    section = forms.CharField(
        label=_("Section"),
        required=False,
        help_text=_("The specific section or part of the work where the information can be found."),
    )
    supplement = forms.CharField(
        label=_("Supplement"),
        required=False,
        help_text=_("The specific supplement or additional material included with the work."),
    )

    layout = Fieldset(
        _("General Information"),
        "title_short",
        "annote",
        "chapter_number",
        "genre",
        "status",
        "version",
        "keyword",
        Fieldset(
            _("Contributors"),
            "author",
            "authority",
            "compiler",
            "contributor",
            "editor",
            "editorial_director",
            "illustrator",
            "recipient",
            "translator",
            css_id="contributors-fieldset",
        ),
        Page.layout,
        ReviewedItem.layout,
        EventInformation.layout,
        Identifiers.layout,
        MediaProduction.layout,
        Fieldset(
            _("Physical characteristics"),
            Row(
                Column("dimensions"),
                Column("scale"),
            ),
            "medium",
        ),
        Fieldset(
            _("Volume"),
            Row(
                Column("volume", css_class="col-md-3"),
                Column("volume_title"),
            ),
            "volume_title_short",
        ),
        # "locator",
        css_id="general-info-fieldset",
    )

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("shortTitle"):
            cleaned["title_short"] = cleaned.pop("shortTitle")
        return cleaned


class ContainerInformation(forms.Form):
    container_title = forms.CharField(
        label=_("Title"),
        required=False,
    )
    container_title_short = forms.CharField(
        label=_("Short title"),
        required=False,
    )
    container_author = NameField(
        label=_("Container Author(s)"),
        required=False,
        help_text=_("Name(s) of the author(s) of the larger work that contains the item being referenced."),
    )
    issue = forms.CharField(
        label=_("Issue"),
        required=False,
    )
    edition = forms.CharField(
        label=_("Edition"),
        required=False,
    )
    number = forms.CharField(
        label=_("Number"),
        required=False,
    )
    number_of_volumes = forms.IntegerField(
        label=_("Number of Volumes"),
        required=False,
    )

    journalAbbreviation = forms.CharField(  # use container_title_short instead
        required=False,
        widget=forms.HiddenInput(),
    )

    layout = Fieldset(
        _("Container Information"),
        HelpText(
            _(
                'A "container" refers to something that holds or contains the main work being cited. A container can be a journal, book, website, or any other larger work that houses smaller works. For example, an article might be contained in a journal, a chapter might be contained in a book, or a webpage might be contained within a larger website.'
            )
        ),
        Row(
            Column("container_title", css_class="col-md-8"),
            Column("container_title_short"),
        ),
        "container_author",
        Row(
            Column("issue"),
            Column("edition"),
        ),
        "number",
        "number_of_volumes",
        css_id="container-info-fieldset",
    )

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("journalAbbreviation"):
            cleaned["container_title_short"] = cleaned.pop("journalAbbreviation")
        return cleaned


class PublishingInformation(forms.Form):
    publisher = forms.CharField(
        label=_("Publisher name"),
        required=False,
        help_text=_("The name of the publisher responsible for producing and distributing the work."),
    )
    publisher_place = forms.CharField(
        label=_("Place"),
        required=False,
        help_text=_(
            "The location (city, state, country) where the publisher is based or where the work was published."
        ),
    )

    available_date = DateVariableField(
        label=_("Date available"),
        help_text=_(
            "The date when the resource became available to the public. This could refer to the date of publication or release of a digital or physical item."
        ),
        required=False,
    )
    issued = DateVariableField(
        label=_("Date published"),
        help_text=_("The date when the resource was formally published or released."),
        required=False,
    )
    submitted = DateVariableField(
        label=_("Date submitted"),
        help_text=_(
            "Enter the date when the resource was submitted for review or publication. This is often used for manuscripts, theses, or dissertations."
        ),
        required=False,
    )

    layout = Fieldset(
        _("Publishing"),
        HelpText(_("Information regarding the context in which the work was made publicly available.")),
        DateVariable("issued"),
        Row(
            Column("publisher", css_class="col-md-8"),
            Column("publisher_place"),
        ),
        DateVariable("available_date"),
        DateVariable("submitted"),
        css_id="publishing-info-fieldset",
    )


class Provenance(forms.Form):
    original_publisher = forms.CharField(
        label=_("Publisher Name"),
        required=False,
        help_text=_("The name of the original publisher if the work was republished or is a new edition."),
    )
    original_publisher_place = forms.CharField(
        label=_("Location"),
        required=False,
        help_text=_("The location (city, state, country) where the original publisher is or was based."),
    )
    original_title = forms.CharField(
        label=_("Title"),
        required=False,
        help_text=_("The title of the original work if the current work is a translation or adaptation."),
    )
    original_date = DateVariableField(
        label=_("Date"),
        help_text=_("The original publication date of the resource, if it was previously published."),
        required=False,
    )
    original_author = NameField(
        label=_("Original Author(s)"),
        required=False,
        help_text=_("Name(s) of the original creator(s) of the work, if different from the current author."),
    )

    layout = Fieldset(
        _("Provenance"),
        HelpText(
            "Use these fields when citing a work that has been republished, translated, or significantly altered from "
            "its original form. This is especially relevant for classic texts, historical documents, foundational "
            "scientific papers, and works included in anthologies."
        ),
        Row(
            Column("original_publisher", css_class="col-md-8"),
            Column("original_publisher_place"),
        ),
        "original_author",
        DateVariable("original_date"),
        css_id="publishing-info-fieldset",
    )


class ArchivalInformation(forms.Form):
    archive = forms.CharField(
        label=_("Archive name"),
        required=False,
        help_text=_("The name of the archive where the work or document is stored."),
    )

    archive_place = forms.CharField(
        label=_("Location"),
        required=False,
        help_text=_("The location (city, institution) of the archive."),
    )

    archive_collection = forms.CharField(
        label=_("Collection"),
        required=False,
        help_text=_("The name of the specific collection within the archive that contains the work."),
    )

    archive_location = forms.CharField(
        label=_("Internal Location"),
        required=False,
        help_text=_(
            "The specific location or identifier within the archive where the work can be found, such as a box or folder number."
        ),
    )

    call_number = forms.CharField(
        label=_("Call Number"),
        required=False,
        help_text=_("The call number assigned to the work within the archive, used for retrieval."),
    )

    layout = Fieldset(
        _("Archiving"),
        HelpText(
            _(
                "Information related to the archive or repository where the work is permanently stored, along with any additional information about its location and how to retrieve it."
            )
        ),
        Row(
            Column("archive", css_class="col-6"),
            Column("archive_place"),
        ),
        Row(
            Column("archive_collection", css_class="col-6"),
            Column("archive_location"),
        ),
        "call_number",
        css_id="archival-info-fieldset",
    )


class CollectionInformation(forms.Form):
    collection_title = forms.CharField(
        label=_("Collection Title"),
        required=False,
    )
    collection_number = forms.CharField(
        label=_("Collection Number"),
        required=False,
    )
    collection_editor = NameField(
        label=_("Collection Editor(s)"),
        required=False,
        help_text=_("Name(s) of the editor(s) responsible for compiling the collection of works."),
    )
    curator = NameField(
        label=_("Curator(s)"),
        required=False,
        help_text=_("Name(s) of the curator(s) responsible for organizing and managing the exhibition or collection."),
    )

    layout = Fieldset(
        _("Collection Information"),
        HelpText(
            _(
                'This section is used when citing works that are part of a larger series or anthology. For example, a book that is part of a series, such as "Studies in Modern History," would use the collection title. If it is volume 5 in that series, you would use the collection number field. If the series has editors, like Jane Smith and John Brown, you would include them in the collection editor field below. Use these fields to accurately describe the broader context of the work you are citing, ensuring it can be correctly identified within its series or anthology.'
            )
        ),
        Row(
            Column("collection_title", css_class="col-md-8"),
            Column("collection_number"),
        ),
        "collection_editor",
        "curator",
        css_id="collection-info-fieldset",
    )


class Custom(forms.Form):
    custom = forms.CharField(label=False, required=False, widget=FlatJSONWidget)

    layout = Fieldset(
        _("Custom"),
        HelpText(
            _(
                "Use this section to add any additional fields or information not covered by the standard fields above. This could include custom fields, notes, or other information that is specific to the citation you are creating."
            )
        ),
        "custom",
        css_id="custom-fieldset",
    )
