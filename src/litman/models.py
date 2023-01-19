from django.db import models
from django.utils.translation import gettext as _
from sortedm2m.fields import SortedManyToManyField
from django.urls import reverse
from .querysets import AuthorQuerySet
from taggit.managers import TaggableManager
from .choices import MonthChoices
from django.core.validators import FileExtensionValidator


class WorkAuthor(models.Model):
    """An intermediate table for the Work-Author m2m relationship.
    `SortedManyToManyField` automatically creates this table, however, there is no access via querysets. Defining here instead allows us to have access to the intermediate table in order to query author position.
    """
    work = models.ForeignKey("litman.Literature",
                             on_delete=models.CASCADE)
    author = models.ForeignKey(
        "litman.Author",
        related_name='position',
        on_delete=models.CASCADE)
    position = models.IntegerField()

    _sort_field_name = 'position'

    def __str__(self):
        return str(self.position)


class Author(models.Model):
    objects = AuthorQuerySet.as_manager()
    given = models.CharField(
        _('given name'),
        max_length=64,
        blank=True,
        null=True)
    family = models.CharField(
        _('family name'),
        max_length=64, blank=True)
    ORCID = models.CharField(
        "ORCID",
        max_length=64, blank=True, null=True)

    class Meta:
        db_table = 'literature_author'
        verbose_name = _('author')
        verbose_name_plural = _('authors')
        ordering = ['family']

    def __str__(self):
        return self.given_family()

    def get_absolute_url(self):
        return reverse("literature:author_detail", kwargs={"pk": self.pk})

    @staticmethod
    def autocomplete_search_fields():
        return ("family__icontains", "given__icontains",)

    def given_family(self):
        """Returns "John Smith" """
        return f"{self.given} {self.family}"

    def family_given(self):
        """Returns "Smith, John" """
        return f"{self.family}, {self.given}"

    def g_family(self):
        """Returns "J. Smith" """
        return f"{self.given[0]}. {self.family}"

    def f_given(self):
        """Returns "Smith, J." """
        return f"{self.family[0]}, {self.given}."


class Literature(models.Model):
    """Model for storing literature data"""

    abstract = models.TextField(
        _("abstract"),
        blank=True, null=True)
    authors = SortedManyToManyField(
        to="litman.Author",
        verbose_name=_('authors'),
        related_name='works',
        through=WorkAuthor,
        sort_value_field_name='number',
        blank=True)
    author_str = models.TextField(
        _('authors'),
        null=True, blank=True,
        help_text=_(
            'List of authors in the format "LastName, GivenName" separated by semi-colons. E.g Smith, John; Klose, Sarah;')
    )
    comment = models.TextField(
        _('comment'),
        help_text=_(
            'General comments regarding the entry.'),
        blank=True, null=True)
    container_title = models.CharField(
        _("container title"),
        help_text=_('The journal, book or other container title of the entry.'),
        max_length=512,
        null=True, blank=True)
    collections = models.ManyToManyField(
        to='litman.collection',
        verbose_name=_('collection'),
        help_text=_('Add the entry to a collection.'),
        blank=True)
    doi = models.CharField(max_length=255,
                           verbose_name='DOI',
                           blank=True, null=True,
                           unique=True)
    institution = models.CharField(
        _("institution"),
        max_length=255,
        help_text=_('Name of the institution.'),
        blank=True, null=True,)
    issn = models.CharField(
        "ISSN",
        max_length=255,
        null=True, blank=True,
    )
    isbn = models.CharField(
        "ISBN",
        max_length=255,
        null=True, blank=True,
    )
    issue = models.IntegerField(
        _("issue number"),
        blank=True, null=True)
    keywords = TaggableManager(
        verbose_name=_('key words'),
        help_text=_(
            'A list of comma-separated keywords.'),
        blank=True,
    )
    label = models.CharField(
        _('label'),
        help_text=_(
            "A human readable identifier. Whitespace and hyphens will be converted to underscores."),
        max_length=255,
        blank=True,
        unique=True)
    language = models.CharField(
        _("language"),
        max_length=2,
        blank=True,
        null=True)
    month = models.PositiveSmallIntegerField(
        _('month'),
        help_text=_('The month of publication.'),
        choices=MonthChoices.choices,
        blank=True, null=True)

    pages = models.CharField(
        _('pages'),
        help_text=_(
            'Either a single digit indicating the page number or two hyphen-separated digits representing a range.'),
        max_length=32, null=True, blank=True)
    pdf = models.FileField(
        "PDF",
        validators=[FileExtensionValidator(['pdf'])]
    )
    published = models.DateField(
        _("date published"),
        max_length=255, )
    publisher = models.CharField(
        _("publisher"),
        help_text=_('Name of the publisher.'),
        blank=True, null=True,
        max_length=255)
    source = models.CharField(
        _('source'),
        help_text=_(
            'The source of metadata for the entry.'),
        max_length=255,
        default='Admin Upload',
        blank=True)
    title = models.CharField(
        _("title"),
        max_length=512, )
    type = models.CharField(
        _("entry type"),
        max_length=255)
    url = models.URLField(
        "URL",
        help_text=_('A link to the URL resource.'),
        blank=True, null=True)
    volume = models.IntegerField(
        _("volume"),
        blank=True, null=True)
    year = models.PositiveSmallIntegerField(
        _('year'),
        help_text=_(
            'The year of publication.')
    )

    date_added = models.DateTimeField(
        _('date added'), auto_now_add=True,)
    last_modified = models.DateTimeField(
        _('last modified'), auto_now=True)
    last_synced = models.DateTimeField(
        _('last synced'),
        help_text=_('Last time the entry was synced with an online resource.'))

    class Meta:
        db_table = 'literature_entry'
        verbose_name = _('literature')
        verbose_name_plural = _('literature')
        ordering = ['label']
        default_related_name = 'literature'

    def __str__(self):
        return self.label

    def save(self, *args, **kwargs):
        # if not self.pk:
        #     self.objects.resolve(self.doi)
        # if not

        return super().save(*args, **kwargs)

    @staticmethod
    def autocomplete_search_fields():
        return ("title__icontains", "author__family__icontains",
                "label__icontains",)


class Collection(models.Model):
    """
    Model representing a collection of publications.
    """

    class Meta:
        db_table = 'literature_collection'
        ordering = ('name',)
        verbose_name = _('collection')
        verbose_name_plural = _('collections')

    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'))

    def __str__(self):
        return f"{self.name}"


class SupplementaryMaterial(models.Model):
    literature = models.ForeignKey(
        to='litman.Literature',
        verbose_name=_('literature'),
        related_name='supplementary',
        on_delete=models.CASCADE)
    file = models.FileField(_('file'))
    date_added = models.DateTimeField(
        _('date added'), auto_now_add=True,)

    class Meta:
        db_table = 'literature_supplementary_material'
        verbose_name = _('supplementary material')
        verbose_name_plural = _('supplementary material')
