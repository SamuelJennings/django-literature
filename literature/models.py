import json
import warnings

import citeproc
from citeproc.source.json import CiteProcJSON
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from django_jsonform.models.fields import JSONField
from partial_date import PartialDateField
from sortedm2m.fields import SortedManyToManyField
from taggit.managers import TaggableManager

from .choices import CSL_TYPE_CHOICES
from .utils import file_upload_path, suppfile_upload_path

with open("tests/data/authors.json") as f:
    author_schema = json.load(f)


class Name(models.Model):
    """Model for storing names of authors, editors, etc."""

    created = models.DateTimeField(_("created"), auto_now_add=True)
    modified = models.DateTimeField(_("modified"), auto_now=True)

    family = models.CharField(_("family name"), max_length=255, blank=True, null=True)
    given = models.CharField(_("given name"), max_length=255, blank=True, null=True)
    suffix = models.CharField(_("suffix"), max_length=255, blank=True, null=True)
    dropping_particle = models.CharField(_("dropping particle"), max_length=255, blank=True, null=True)
    non_dropping_particle = models.CharField(_("non-dropping particle"), max_length=255, blank=True, null=True)

    literal = models.CharField(_("literal"), max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _("name")
        verbose_name_plural = _("names")
        # ensure either family or literal is set
        constraints = [
            models.CheckConstraint(
                check=models.Q(family__isnull=False) | models.Q(literal__isnull=False),
                name="family_or_literal",
            )
        ]
        # ordering = ["family", "given"]

    def __str__(self):
        return f"{self.family}, {self.given}"


class NameThrough(models.Model):
    """Model for storing the order of names"""

    NAME_TYPES = models.TextChoices("NameTypes", citeproc.NAMES)

    type = models.CharField(
        _("type"),
        choices=NAME_TYPES.choices,
        max_length=len(max(NAME_TYPES, key=len)),
    )

    name = models.ForeignKey(
        to="literature.Name",
        verbose_name=_("name"),
        related_name="name_through",
        on_delete=models.CASCADE,
    )
    literature = models.ForeignKey(
        to="literature.Literature",
        verbose_name=_("literature"),
        related_name="name_through",
        on_delete=models.CASCADE,
    )
    order = models.PositiveIntegerField(_("order"))

    class Meta:
        verbose_name = _("name through")
        verbose_name_plural = _("names through")
        ordering = ["order"]
        unique_together = ("name", "literature")

    def __str__(self):
        return f"{self.name} - {self.literature}"


class Date(models.Model):
    """Model for storing date data"""

    DATE_TYPES = models.TextChoices("DateTypes", citeproc.DATES)

    item = models.ForeignKey(
        to="literature.Literature",
        verbose_name=_("item"),
        related_name="dates",
        on_delete=models.CASCADE,
    )

    type = models.CharField(
        _("type"),
        choices=DATE_TYPES.choices,
        max_length=len(max(DATE_TYPES, key=len)),
    )

    begin = PartialDateField(_("date"), blank=True, null=True)
    end = PartialDateField(_("date to"), blank=True, null=True)
    season = models.CharField(_("season"), max_length=255, blank=True, null=True)
    circa = models.BooleanField(_("circa"), default=False)

    class Meta:
        verbose_name = _("date")
        verbose_name_plural = _("dates")
        unique_together = ("item", "type")

    def __str__(self):
        if self.begin and self.end:
            return f"{self.begin}/{self.end}"
        elif self.begin:
            return force_str(self.begin)
        elif self.season:
            return force_str(self.season)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.type} {self}>"

    def serialize(self):
        result = {}
        if self.begin:
            result["raw"] = str(self.begin)
        if self.end:
            result["raw"] += f"/{self.end}"
        if self.season:
            result["season"] = self.season
        if self.circa:
            result["circa"] = self.circa

        return result


tmp_map = {
    "archive_place": "archive-place",
}


class Literature(models.Model):
    """Model for storing bibliographic data"""

    # TypeChoices = TypeChoices
    TypeChoices = CSL_TYPE_CHOICES
    type = models.CharField(_("type"), choices=TypeChoices, max_length=22)

    custom_author = JSONField(schema=author_schema, blank=True, default=list)

    abstract = models.TextField(
        _("abstract"),
        blank=True,
        null=True,
    )
    annote = models.TextField(
        _("annotation"),
        help_text=_(
            "Short markup, decoration, or annotation to the item (e.g., to indicate items included in a review); For descriptive text (e.g., in an annotated bibliography), use note instead"
        ),
        blank=True,
        null=True,
    )
    archive = models.CharField(
        _("archive name"),
        help_text=_("Archive where the item is stored"),
        max_length=255,
        blank=True,
        null=True,
    )
    archive_collection = models.CharField(
        _("archive collection"),
        help_text=_("Collection within the archive where the item is stored"),
        max_length=255,
        blank=True,
        null=True,
    )
    archive_location = models.CharField(
        _("archive location"),
        help_text=_("Storage location within an archive (e.g. a box and folder number)"),
        max_length=255,
        blank=True,
        null=True,
    )
    archive_place = models.CharField(
        _("archive place"),
        help_text=_("Geographic location of the archive"),
        max_length=255,
        blank=True,
        null=True,
    )
    authority = models.CharField(
        _("authority"),
        help_text=_(
            "Issuing or judicial authority (e.g. “USPTO” for a patent, “Fairfax Circuit Court” for a legal case)"
        ),
        max_length=255,
        blank=True,
        null=True,
    )
    call_number = models.CharField(
        _("call number"),
        help_text=_("Used to locate the item within a library"),
        max_length=255,
        blank=True,
        null=True,
    )
    chapter_number = models.CharField(
        _("chapter number"),
        max_length=255,
        help_text=_("Chapter number (e.g. chapter number in a book; track number on an album)"),
        blank=True,
        null=True,
    )
    citation_key = models.CharField(
        _("citation key"),
        help_text=_("Unique key used to reference the citation in text."),
        max_length=255,
        unique=True,
        blank=True,
        null=True,
    )
    collection_number = models.CharField(
        _("collection number"),
        max_length=255,
        help_text=_("Identifiying number within the collection"),
        blank=True,
        null=True,
    )
    collection_title = models.CharField(
        _("collection title"),
        help_text=_("Title of the collection holding the item"),
        max_length=255,
        blank=True,
        null=True,
    )
    container_title = models.CharField(
        _("title"),
        help_text=_(
            "The title of the larger work that contains the work being cited. E.g. the title of a book, journal, website, etc."
        ),
        max_length=512,
        null=True,
        blank=True,
    )
    container_title_short = models.CharField(
        _("short title"),
        help_text=_("Short/abbreviated form of the container title"),
        max_length=255,
        blank=True,
        null=True,
    )
    custom = models.JSONField(
        _("custom"),
        help_text=_("Custom fields"),
        blank=True,
        default=dict,
    )
    DOI = models.CharField(
        _("DOI"),
        help_text=_("Digital Object Identifier"),
        max_length=255,
        blank=True,
        null=True,
    )
    dimensions = models.CharField(
        _("dimensions"),
        help_text=_("Physical (e.g. size) or temporal (e.g. running time) dimensions of the item"),
        max_length=255,
        blank=True,
        null=True,
    )
    division = models.CharField(
        _("division"),
        help_text=_("Minor subdivision of a court with a jurisdiction for a legal item"),
        max_length=255,
        blank=True,
        null=True,
    )
    edition = models.CharField(
        _("edition"),
        max_length=255,
        help_text=_("Edition of the container holding the item"),
        blank=True,
        null=True,
    )
    # event = models.CharField(
    #     _("event"),
    #     help_text=_("Deprecated legacy variant of event-title"),
    #     max_length=255,
    #     blank=True,
    #     null=True,
    # )
    event_title = models.CharField(
        _("event title"),
        help_text=_(
            "Name of the event related to the item (e.g. the conference name when citing a conference paper; the meeting where presentation was made)"
        ),
        max_length=255,
        blank=True,
        null=True,
    )
    event_place = models.CharField(
        _("event place"),
        help_text=_("Geographic location of the event related to the item (e.g. “Amsterdam, The Netherlands”)"),
        max_length=255,
        blank=True,
        null=True,
    )
    genre = models.CharField(
        _("sub-type"),
        help_text=_(
            "Class or sub-type of the item (e.g. “Doctoral dissertation” for a PhD thesis; “NIH Publication” for an NIH technical report)"
        ),
        max_length=255,
        blank=True,
        null=True,
    )
    ISBN = models.CharField(
        _("ISBN"),
        help_text=_("International Standard Book Number"),
        max_length=255,
        blank=True,
        null=True,
    )
    ISSN = models.CharField(
        _("ISSN"),
        help_text=_("International Standard Serial Number"),
        max_length=255,
        blank=True,
        null=True,
    )
    issue = models.CharField(
        _("issue"),
        max_length=255,
        help_text=_("Issue number of the item or container holding the item"),
        blank=True,
        null=True,
    )
    jurisdiction = models.CharField(
        _("jurisdiction"),
        help_text=_("Geographic scope of relevance (e.g. “US” for a US patent; the court hearing a legal case)"),
        max_length=255,
        blank=True,
        null=True,
    )
    language = models.CharField(
        _("language"),
        help_text=_(
            "The language of the item; Should be entered as an ISO 639-1 two-letter language code (e.g. “en”, “zh”), optionally with a two-letter locale code (e.g. “de-DE”, “de-AT”)"
        ),
        max_length=255,
        blank=True,
        null=True,
    )
    license = models.CharField(
        _("license"),
        help_text=_(
            "The license information applicable to an item (e.g. the license an article or software is released under; the copyright information for an item; the classification status of a document)"
        ),
        max_length=255,
        blank=True,
        null=True,
    )
    locator = models.CharField(
        _("locator"),
        help_text=_(
            "A cite-specific pinpointer within the item (e.g. a page number within a book, or a volume in a multi-volume work)"
        ),
        max_length=255,
        blank=True,
        null=True,
    )
    medium = models.CharField(
        _("medium"),
        help_text=_("Description of the item’s format or medium (e.g. “CD”, “DVD”, “Album”, etc.)"),
        max_length=255,
        blank=True,
        null=True,
    )
    note = models.TextField(
        _("note"),
        help_text=_("Descriptive text or notes about an item (e.g. in an annotated bibliography)"),
        blank=True,
        null=True,
    )
    number = models.CharField(
        _("number"),
        max_length=255,
        help_text=_("Number identifying the item (e.g. a report number)"),
        blank=True,
        null=True,
    )
    number_of_pages = models.CharField(
        _("number of pages"),
        max_length=255,
        help_text=_("Total number of pages of the cited item"),
        blank=True,
        null=True,
    )
    number_of_volumes = models.CharField(
        _("total volumes"),
        max_length=255,
        help_text=_("Total number of volumes in the container holding the item"),
        blank=True,
        null=True,
    )
    original_publisher = models.CharField(
        _("publisher name"),
        help_text=_("Original publisher, for items that have been republished by a different publisher"),
        max_length=255,
        blank=True,
        null=True,
    )
    original_publisher_place = models.CharField(
        _("original publisher place"),
        help_text=_("Geographic location of the original publisher (e.g. “London, UK”)"),
        max_length=255,
        blank=True,
        null=True,
    )
    original_title = models.CharField(
        _("original title"),
        help_text=_("Title of the original version of the item (e.g. for a translated work)"),
        max_length=255,
        blank=True,
        null=True,
    )
    page = models.CharField(
        _("page range"),
        help_text=_("Range of pages the item (e.g. a journal article) covers in a container (e.g. a journal issue)"),
        max_length=255,
        blank=True,
        null=True,
    )
    page_first = models.CharField(
        _("page"),
        help_text=_(
            "First page of the range of pages the item (e.g. a journal article) covers in a container (e.g. a journal issue)"
        ),
        max_length=255,
        blank=True,
        null=True,
    )
    part_number = models.CharField(
        _("part number"),
        max_length=255,
        help_text=_(
            "Number of the specific part of the item being cited (e.g. part 2 of a journal article); Use part-title for the title of the part, if any"
        ),
        blank=True,
        null=True,
    )
    part_title = models.CharField(
        _("part title"),
        help_text=_("Title of the part of the item being cited (e.g. “Introduction” for a book chapter)"),
        max_length=255,
        blank=True,
        null=True,
    )
    PMCID = models.CharField(
        _("PMCID"),
        help_text=_("PubMed Central ID"),
        max_length=255,
        blank=True,
        null=True,
    )
    PMID = models.CharField(
        _("PMID"),
        help_text=_("PubMed ID"),
        max_length=255,
        blank=True,
        null=True,
    )
    printing_number = models.CharField(
        _("printing number"),
        max_length=255,
        help_text=_("Printing number of the item or container holding the item"),
        blank=True,
        null=True,
    )
    publisher = models.CharField(
        _("publisher name"),
        max_length=255,
        blank=True,
        null=True,
    )
    publisher_place = models.CharField(
        _("publisher place"),
        help_text=_("Geographic location of the publisher"),
        max_length=255,
        blank=True,
        null=True,
    )
    references = models.TextField(
        _("references"),
        help_text=_(
            "Resources related to the procedural history of a legal case or legislation; Can also be used to refer to the procedural history of other items (e.g. “Conference canceled” for a presentation accepted as a conference that was subsequently canceled; details of a retraction or correction notice)"
        ),
        blank=True,
        null=True,
    )
    reviewed_genre = models.CharField(
        _("reviewed genre"),
        help_text=_("Type of the item being reviewed by the current item (e.g. book, film)"),
        max_length=255,
        blank=True,
        null=True,
    )
    reviewed_title = models.CharField(
        _("reviewed title"),
        help_text=_("Title of the item being reviewed by the current item"),
        max_length=255,
        blank=True,
        null=True,
    )
    scale = models.CharField(
        _("scale"),
        help_text=_("Scale of the item (e.g. “1:100,000” for a map)"),
        max_length=255,
        blank=True,
        null=True,
    )
    section = models.CharField(
        _("section"),
        help_text=_(
            "Section of the item or container holding the item (e.g. “§2.0.1” for a law; “politics” for a newspaper article)"
        ),
        max_length=255,
        blank=True,
        null=True,
    )
    source = models.CharField(
        _("source"),
        help_text=_("Source from whence the item originates (e.g. a library catalog or database)"),
        max_length=255,
        blank=True,
        null=True,
    )
    status = models.CharField(
        _("status"),
        help_text=_(
            "Publication status of the item (e.g. “forthcoming”; “in press”; “advance online publication”; “retracted”)"
        ),
        max_length=255,
        blank=True,
        null=True,
    )
    supplement_number = models.CharField(
        _("supplement number"),
        max_length=255,
        help_text=_(
            "Supplement number of the item or container holding the item (e.g. for secondary legal items that are regularly updated between editions)"
        ),
        blank=True,
        null=True,
    )
    title = models.CharField(
        _("title"),
        max_length=1000,
        blank=True,
        null=True,
    )
    title_short = models.CharField(
        _("title short"),
        help_text=_("Short/abbreviated form of title"),
        max_length=255,
        blank=True,
        null=True,
    )
    URL = models.CharField(
        _("URL"),
        help_text=_("Uniform Resource Locator"),
        max_length=255,
        blank=True,
        null=True,
    )
    version = models.CharField(
        _("version"),
        help_text=_("Version of the item (e.g. “2.0.9” for a software program)"),
        max_length=255,
        blank=True,
        null=True,
    )
    volume = models.CharField(
        _("number"),
        max_length=255,
        help_text=_("Volume number"),
        blank=True,
        null=True,
    )
    volume_title = models.CharField(
        _("title"),
        help_text=_("Title of the volume of the item or container holding the item"),
        max_length=255,
        blank=True,
        null=True,
    )

    volume_title_short = models.CharField(
        _("Short title"),
        help_text=_("Short/abbreviated form of volume-title"),
        max_length=255,
        blank=True,
        null=True,
    )
    author = SortedManyToManyField(
        to="literature.Name",
        related_name="authors",
        verbose_name=_("author"),
        help_text=_("Author(s) of the item."),
        blank=True,
    )

    names = models.ManyToManyField(
        to="literature.Name",
        through="literature.NameThrough",
        verbose_name=_("names"),
        help_text=_("Authors, editors, etc."),
        blank=True,
    )

    # DJANGO LITERATURE SPECIFIC FIELDS
    keyword = TaggableManager(
        verbose_name=_("key words"),
        help_text=_("Keyword(s) or tag(s) attached to the item."),
        blank=True,
    )
    created = models.DateTimeField(_("created"), auto_now_add=True)
    modified = models.DateTimeField(_("modified"), auto_now=True)
    collections = models.ManyToManyField(
        to="literature.collection",
        verbose_name=_("collection"),
        help_text=_("Add the entry to a collection."),
        blank=True,
    )
    file = models.FileField(
        _("file"),
        upload_to=file_upload_path,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("literature item")
        verbose_name_plural = _("literature items")
        ordering = ["created"]
        default_related_name = "literature"

    def __str__(self):
        return force_str(self.title)
        # return render_bibliography(self)

    def get_absolute_url(self):
        return reverse("literature-detail", kwargs={"pk": self.pk})

    def file_download_link(self):
        if url := getattr(self.file, "url", None):
            icon = render_to_string("icons/file.svg")
            return mark_safe(f'<a href="{url}" target="_blank">{icon}</a>')  # noqa: S308

    file_download_link.short_description = _("file")

    @property
    def reference(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            citeproc_json = CiteProcJSON(self)

        return next(iter(citeproc_json.items()))[0]

    @staticmethod
    def autocomplete_search_fields():
        return ("title__icontains",)


class Collection(models.Model):
    """
    Model representing a collection of publications.
    """

    created = models.DateTimeField(_("created"), auto_now_add=True)
    modified = models.DateTimeField(_("modified"), auto_now=True)

    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"))

    class Meta:
        ordering = ("name",)
        verbose_name = _("collection")
        verbose_name_plural = _("collections")

    def __str__(self):
        return force_str(self.name)


class SupplementaryMaterial(models.Model):
    created = models.DateTimeField(_("created"), auto_now_add=True)
    modified = models.DateTimeField(_("modified"), auto_now=True)

    literature = models.ForeignKey(
        to="literature.Literature",
        verbose_name=_("literature"),
        related_name="supplementary",
        on_delete=models.CASCADE,
    )
    file = models.FileField(_("file"), upload_to=suppfile_upload_path)

    class Meta:
        verbose_name = _("supplementary material")
        verbose_name_plural = _("supplementary material")
