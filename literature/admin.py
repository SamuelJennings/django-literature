from django.contrib import admin, messages
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.defaultfilters import pluralize
from django.urls import path
from django.utils.decorators import method_decorator
from django.utils.html import mark_safe
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from requests.exceptions import HTTPError

from .models import Author, Collection, Literature, SupplementaryMaterial
from .widgets import AdminPDFWidget


class SupplementaryInline(admin.TabularInline):
    model = SupplementaryMaterial


class AuthorInline(admin.TabularInline):
    model = Author.literature.through


@admin.register(Literature)
class LiteratureAdmin(admin.ModelAdmin):
    """Django Admin setup for the `literature.Work` model."""

    date_hierarchy = "published"
    raw_id_fields = ("authors",)
    autocomplete_lookup_fields = {"m2m": ["authors"]}
    list_display_links = ("title",)

    list_display = [
        "pdf",
        "article",
        "label",
        "title",
        "container_title",
        "volume",
        "type",
    ]

    list_filter = ["type", "container_title", "language", "source"]
    search_fields = ("doi", "title", "id", "label")
    list_editable = [
        "pdf",
    ]
    readonly_fields = [
        "source",
        "created",
        "modified",
        "last_synced",
    ]

    inlines = [SupplementaryInline, AuthorInline]
    fieldsets = [
        (
            _("Basic"),
            {
                "fields": [
                    "label",
                    # "pdf",
                    "type",
                    "title",
                    "year",
                    "language",
                    "source",
                    "created",
                    "modified",
                    "last_synced",
                    # "authors",
                    # "author_str",
                ]
            },
        ),
        (
            _("Recommended"),
            {
                "fields": [
                    "doi",
                    "url",
                    "container_title",
                    "publisher",
                    "institution",
                    "abstract",
                    "month",
                    "keywords",
                ]
            },
        ),
        (
            _("General"),
            {
                "fields": [
                    "issn",
                    "isbn",
                    "volume",
                    "issue",
                    "pages",
                ]
            },
        ),
        (
            _("Comment"),
            {
                "fields": [
                    "comment",
                ]
            },
        ),
        # (
        #     _("Administrative"),
        #     {
        #         "fields": [
        #             "language",
        #             "source",
        #             "comment",
        #             "created",
        #             "modified",
        #             "last_synced",
        #         ]
        #     },
        # ),
    ]

    formfield_overrides = {
        # models.FileField: {"widget": AdminPDFWidget},
    }

    class Media:

        # css = {"all": ("crossref/css/filer_extra.min.css",)}
        js = (
            "https://kit.fontawesome.com/a08181010c.js",
            # 'crossref/js/pdfInput.js',
        )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("authors")

    def get_urls(self):
        return [
            path(
                "import-bibtex/",
                self.admin_site.admin_view(self.import_bibtex),
                name="import_bibtex",
            ),
            path(
                "add-doi/",
                self.admin_site.admin_view(self.get_doi_or_query_crossref),
                name="add_from_crossref",
            ),
        ] + super().get_urls()

    def get_doi_or_query_crossref(self, request, *args, **kwargs):
        if request.POST:
            form = DOIForm(request.POST)
            if form.is_valid():
                self._get_data_from_crossref(request, form.cleaned_data["DOI"])
            else:
                if form.errors["DOI"][0] == "Work with this DOI already exists.":
                    message = f"An item with that DOI already exists in the database: {form.data['DOI']}"
                else:
                    message = mark_safe("<br>".join(e for e in form.errors["DOI"]))
                self.message_user(request, message, messages.INFO)
        return HttpResponseRedirect("../")

    def _get_data_from_crossref(self, request, doi):
        """Private function that handles retrieving information when a doi
        is provided.

        Args:
            request (HTTPRequest): The request object passed through the Django Admin class
            doi (str): The doi to be queried

        Returns:
            instance: a saved Work instance or False
        """
        errors = []
        try:
            # first, check if the object already exists. If it does
            # do nothing and either retrieve the object from the database,
            # or query crossref for the info
            instance, created = self.get_queryset(request).get_or_query_crossref(doi)
        except HTTPError as e:
            # Something wen't wrong during the request to crossref
            errors.append(e)
            # return None so the calling function knows something went wrong
            return None

        if created:
            message = mark_safe(f"Succesfully added: {instance.bibliographic()}")
            self.message_user(request, message, messages.SUCCESS)
        else:
            message = f"{instance.DOI} already exists in this database"
            self.message_user(request, message, messages.INFO)

        return instance

    def import_errors(self, request, *args, **kwargs):
        return

    @method_decorator(require_POST)
    def import_bibtex(self, request, *args, **kwargs):
        """Admin view that handles user-uploaded bibtex files

        Returns:
            HttpResponseRedirect: redirects to model admins change_list
        """
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            importer = BibtexResource(form.cleaned_data["file"].file, request)
            importer.process()
            if importer.result.has_errors:
                return render(
                    request,
                    "admin/crossref/import_results.html",
                    context={"result": importer.result},
                )
            else:
                report = importer.result.counts()
                if report["crossref"] or report["bibtex"]:
                    self.message_user(
                        request,
                        level=messages.SUCCESS,
                        message=f"Import finished with {report['crossref']} new entr{pluralize(report['crossref'], 'y,ies')} from the CrossRef API and {report['bibtex']} new entr{pluralize(report['bibtex'], 'y,ies')} parsed direct from the bibtex file",
                    )
                if report["skipped"]:
                    self.message_user(
                        request,
                        level=messages.INFO,
                        message=f"{report['skipped']} existing entr{pluralize(report['skipped'], 'y,ies')} were skipped during the import process",
                    )
        else:
            self.message_user(
                request,
                "The uploaded file could not be validated",
                level=messages.ERROR,
            )
        return HttpResponseRedirect("../")

    def article(self, obj):
        if obj.doi:
            return mark_safe(
                '<a href="https://doi.org/{}"><i class="fas fa-globe"></i></a>'.format(
                    obj.doi
                )
            )
        else:
            return ""

    def file(self, obj):
        if obj.pdf:
            return mark_safe(
                f'<a href="{obj.pdf.url}"><i class="fas fa-file-pdf fa-2x"></i></a>'
            )
        else:
            return ""


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    pass


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["family", "given", "ORCID", "created", "modified"]
    pass
