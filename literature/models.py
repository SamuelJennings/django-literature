from datetime import date

from django.core.validators import FileExtensionValidator, MaxValueValidator
from django.db import models
from django.utils.encoding import force_str
from django.utils.translation import gettext as _
from taggit.managers import TaggableManager

from .choices import TypeChoices
from .utils import pdf_file_renamer


class LiteratureBase(models.Model):
    created = models.DateTimeField(_("created"), auto_now_add=True)
    modified = models.DateTimeField(_("modified"), auto_now=True)

    class Meta:
        abstract = True


class Literature(LiteratureBase):
    """Model for storing literature data"""

    TypeChoices = TypeChoices
    # ARTICLE TYPE
    type = models.CharField(
        _("type"),
        choices=TypeChoices.choices,
        max_length=len(
            max(TypeChoices, key=len),
        ),
    )

    # THE FOLLOWING FIELDS ARE DEFINED HERE AS THEY MAY BENEFIT FROM INDEXING
    title = models.TextField(
        _("title"),
        help_text=_("Primary title of the item."),
        blank=True,
        null=True,
    )
    abstract = models.TextField(_("abstract"), blank=True, null=True)
    container_title = models.CharField(
        _("container title"),
        help_text=_(
            "Title of the container holding the item (e.g. the book title for a book chapter, the journal title for a"
            " journal article; the album title for a recording; the session title for multi-part presentation at a"
            " conference)."
        ),
        max_length=512,
        null=True,
        blank=True,
    )
    keyword = TaggableManager(
        verbose_name=_("key words"),
        help_text=_("Keyword(s) or tag(s) attached to the item."),
        blank=True,
    )

    # DJANGO LITERATURE SPECIFIC FIELDS
    collections = models.ManyToManyField(
        to="literature.collection",
        verbose_name=_("collection"),
        help_text=_("Add the entry to a collection."),
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
        blank=True,
        null=True,
        validators=[MaxValueValidator(date.today)],
    )

    # RAW CSL DATA FIELD
    CSL = models.JSONField(_("Citation Style Language"), blank=True)

    class Meta:
        verbose_name = _("literature")
        verbose_name_plural = _("literature")
        ordering = ["created"]
        default_related_name = "literature"

    def __str__(self):
        return self.title or _("untitled")

    def _author_name(self, author):
        return f"{author.get('family', '')}, {author.get('given', '')}"

    def get_first_author(self):
        if author := self.CSL.get("author", [{}])[0]:
            return self._author_name(author)
        return ""

    def authors(self):
        if authors := self.CSL.get("author", []):
            return ", ".join([self._author_name(a) for a in authors])
        return ""

    def save(self, *args, **kwargs):
        # if self.tracker.has_changed("CSL"):
        self.parse_csl()
        super().save(*args, **kwargs)
        # self.update_identifiers()
        return self

    def parse_csl(self):
        CSL = {k.replace("-", "_"): v for k, v in self.CSL.items()}
        for field in [f.name for f in self._meta.fields]:
            if field == "id":
                continue
            if CSL.get(field):
                setattr(self, field, CSL[field])

    @staticmethod
    def autocomplete_search_fields():
        return ("title__icontains",)


class Collection(LiteratureBase):
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


class SupplementaryMaterial(LiteratureBase):
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
