import json

from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from partial_date import PartialDate
from partial_date.fields import PartialDateField

from .choices import CSL_TYPE_CHOICES
from .utils import file_upload_path, suppfile_upload_path
from .utils.date import date_parts_to_iso, parse_date

# with open("tests/data/authors.json") as f:
#     author_schema = json.load(f)

tmp_map = {
    "archive_place": "archive-place",
}


def generate_citation_key(instance):
    return f"{instance.title}"[:10]


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")

    def __str__(self):
        return self.name


class LiteratureItem(models.Model):
    CSL_TYPE_CHOICES = CSL_TYPE_CHOICES
    citation_key = models.CharField(_("key"), max_length=255, unique=True)
    type = models.CharField(_("type"), choices=CSL_TYPE_CHOICES, max_length=22)

    title = models.CharField(max_length=1000, db_index=True, blank=True, null=True)
    issued = PartialDateField(blank=True, null=True)
    item = models.JSONField(default=dict)

    keyword = models.ManyToManyField(
        Tag,
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
        verbose_name = _("literature")
        verbose_name_plural = _("literature")
        ordering = ["-issued"]

    def save(self, *args, **kwargs):
        self.type = self.item.get("type", "article")
        self.title = self.item.get("title", "")
        self.issued = self.save_issued_date()
        # self.key = self.item.get("citation-key", "")
        if not self.citation_key:
            self.citation_key = generate_citation_key(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return force_str(self.title)
        # return render_bibliography(self)

    def as_json(self):
        return json.dumps(self.item)

    def save_issued_date(self):
        if issued := self.item.get("issued", None):
            parsed = parse_date(issued)
            issued_iso = date_parts_to_iso(parsed.get("begin", None))
            return PartialDate(issued_iso)

    def get_absolute_url(self):
        return reverse("literature-detail", kwargs={"pk": self.pk})

    def file_download_link(self):
        if self.file:
            icon = render_to_string("icons/file.svg")
            return mark_safe(f'<a href="{self.file.url}" target="_blank">{icon}</a>')
        # if url := getattr(self.file, "url", None):
        #     icon = render_to_string("icons/file.svg")
        #     return mark_safe(f'<a href="{url}" target="_blank">{icon}</a>')

    file_download_link.short_description = _("file")

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
        to="literature.LiteratureItem",
        verbose_name=_("literature"),
        related_name="supplementary",
        on_delete=models.CASCADE,
    )
    file = models.FileField(_("file"), upload_to=suppfile_upload_path)

    class Meta:
        verbose_name = _("supplementary material")
        verbose_name_plural = _("supplementary material")
