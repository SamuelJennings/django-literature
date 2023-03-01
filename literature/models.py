from datetime import date

from django.core.validators import (
    FileExtensionValidator,
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.translation import gettext as _
from model_utils import FieldTracker
from model_utils.models import TimeStampedModel
from sortedm2m.fields import SortedManyToManyField
from taggit.managers import TaggableManager

from .choices import MonthChoices
from .managers import AuthorManager, LiteratureManager
from .utils import get_current_year, pdf_file_renamer


class LiteratureAuthor(models.Model):
    """An intermediate table for the Work-Author m2m relationship.
    `SortedManyToManyField` automatically creates this table, however, there is no access via querysets. Defining here instead allows us to have access to the intermediate table in order to query author position.
    """

    literature = models.ForeignKey("literature.Literature", on_delete=models.CASCADE)
    author = models.ForeignKey(
        "literature.Author", related_name="position", on_delete=models.CASCADE
    )
    position = models.IntegerField()

    _sort_field_name = "position"

    def __str__(self):
        return str(self.position)


class Author(TimeStampedModel):
    objects = AuthorManager()

    given = models.CharField(_("given name"), max_length=255, blank=True, null=True)
    family = models.CharField(_("family name"), max_length=255, blank=True)
    ORCID = models.CharField(
        "ORCID",
        max_length=64,
        validators=[RegexValidator("^(?:\d{4}-){3}\d{3}[\d,x]")],
        blank=True,
        null=True,
    )

    # literature = SortedManyToManyField(
    #     to="literature.Literature",
    #     verbose_name=_("literature"),
    #     related_name="authors",
    #     through=LiteratureAuthor,
    #     sort_value_field_name="position",
    #     blank=True,
    # )

    class Meta:
        verbose_name = _("author")
        verbose_name_plural = _("authors")
        ordering = ["family"]

    def __str__(self):
        return self.given_family()

    def get_absolute_url(self):
        return reverse("literature:author_detail", kwargs={"pk": self.pk})

    @staticmethod
    def autocomplete_search_fields():
        return (
            "family__icontains",
            "given__icontains",
        )

    def given_family(self):
        """Returns "John Smith" """
        return f"{self.given} {self.family}"

    def family_given(self):
        """Returns "Smith, John" """
        return f"{self.family}, {self.given}"

    def g_family(self):
        """Returns "J. Smith" """
        return f"{self.given[0]}. {self.family}"

    def family_g(self):
        """Returns "Smith, J." """
        return f"{self.family}, {self.given[0]}."


class Literature(TimeStampedModel):
    """Model for storing literature data"""

    objects = LiteratureManager()

    abstract = models.TextField(_("abstract"), blank=True, null=True)
    authors = SortedManyToManyField(
        to="literature.Author",
        verbose_name=_("authors"),
        related_name="literature",
        through=LiteratureAuthor,
        sort_value_field_name="number",
        blank=True,
    )
    author_str = models.TextField(
        _("authors"),
        null=True,
        blank=True,
        help_text=_(
            'List of authors in the format "LastName, GivenName" separated by semi-colons. E.g Smith, John; Klose, Sarah;'
        ),
    )
    comment = models.TextField(
        _("comment"),
        help_text=_("General comments regarding the entry."),
        blank=True,
        null=True,
    )
    container_title = models.CharField(
        _("container title"),
        help_text=_("The journal, book or other container title of the entry."),
        max_length=512,
        null=True,
        blank=True,
    )
    collections = models.ManyToManyField(
        to="literature.collection",
        verbose_name=_("collection"),
        help_text=_("Add the entry to a collection."),
        blank=True,
    )
    doi = models.CharField(
        max_length=255, verbose_name="DOI", blank=True, null=True, unique=True
    )
    institution = models.CharField(
        _("institution"),
        max_length=255,
        help_text=_("Name of the institution."),
        blank=True,
        null=True,
    )
    issn = models.CharField(
        "ISSN",
        max_length=255,
        null=True,
        blank=True,
    )
    isbn = models.CharField(
        "ISBN",
        max_length=255,
        null=True,
        blank=True,
    )
    issue = models.IntegerField(_("issue number"), blank=True, null=True)
    keywords = TaggableManager(
        verbose_name=_("key words"),
        help_text=_("A list of comma-separated keywords."),
        blank=True,
    )
    label = models.CharField(
        _("label"),
        help_text=_(
            "A human readable identifier. Whitespace and hyphens will be converted to underscores."
        ),
        max_length=255,
        blank=True,
        # null=True,
        unique=True,
    )
    language = models.CharField(_("language"), max_length=2, blank=True, null=True)
    month = models.PositiveSmallIntegerField(
        _("month"),
        help_text=_("The month of publication."),
        choices=MonthChoices.choices,
        blank=True,
        null=True,
    )
    pages = models.CharField(
        _("pages"),
        help_text=_(
            "Either a single digit indicating the page number or two hyphen-separated digits representing a range."
        ),
        max_length=32,
        validators=[RegexValidator("^(\d+-{1,2}?\d+)$")],
        null=True,
        blank=True,
    )
    pdf = models.FileField(
        "PDF",
        upload_to=pdf_file_renamer,
        validators=[FileExtensionValidator(["pdf"])],
        null=True,
        blank=True,
    )
    published = models.DateField(
        _("date published"),
        max_length=255,
        validators=[MaxValueValidator(date.today)],
    )
    publisher = models.CharField(
        _("publisher"),
        help_text=_("Name of the publisher."),
        blank=True,
        null=True,
        max_length=255,
    )
    source = models.CharField(
        _("source"),
        help_text=_("The source of metadata for the entry."),
        max_length=255,
        default="Admin Upload",
        blank=True,
    )
    title = models.CharField(
        _("title"),
        max_length=512,
    )
    type = models.CharField(_("entry type"), max_length=255)
    url = models.URLField(
        "URL", help_text=_("A link to the URL resource."), blank=True, null=True
    )
    volume = models.IntegerField(_("volume"), blank=True, null=True)
    year = models.PositiveSmallIntegerField(
        _("year"),
        help_text=_("The year of publication."),
        validators=[MinValueValidator(1900), MaxValueValidator(get_current_year)],
    )

    last_synced = models.DateTimeField(
        _("last synced"),
        help_text=_("Last time the entry was synced with an online resource."),
        null=True,
        blank=True,
    )

    # tracks whether changes have been made to any fields since the last save
    tracker = FieldTracker()

    class Meta:
        verbose_name = _("literature")
        verbose_name_plural = _("literature")
        ordering = ["label"]
        default_related_name = "literature"

    def __str__(self):
        return force_str(self.label)

    def save(self, *args, **kwargs):
        # not implemented
        if self.tracker.has_changed("doi"):
            self.objects.resolve(self.doi, self.source)

        if self.tracker.has_changed("year"):
            self.published = date(year=self.year, month=self.month or 1, day=1)
        return super().save(*args, **kwargs)

    @staticmethod
    def autocomplete_search_fields():
        return (
            "title__icontains",
            "authors__family__icontains",
            "label__icontains",
        )


class Collection(TimeStampedModel):
    """
    Model representing a collection of publications.
    """

    class Meta:
        ordering = ("name",)
        verbose_name = _("collection")
        verbose_name_plural = _("collections")

    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"))

    def __str__(self):
        return force_str(self.name)


class SupplementaryMaterial(TimeStampedModel):
    literature = models.ForeignKey(
        to="literature.Literature",
        verbose_name=_("literature"),
        related_name="supplementary",
        on_delete=models.CASCADE,
    )
    file = models.FileField(_("file"))

    class Meta:
        verbose_name = _("supplementary material")
        verbose_name_plural = _("supplementary material")
