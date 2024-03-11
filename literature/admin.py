from django.contrib import admin
from django.urls import reverse
from django.utils.translation import gettext as _
from rest_framework.permissions import DjangoModelPermissions, IsAdminUser

from .models import Collection, Literature, SupplementaryMaterial


class SupplementaryInline(admin.TabularInline):
    model = SupplementaryMaterial


@admin.register(Literature)
# class LiteratureAdmin(DataTableMixin, admin.ModelAdmin):
class LiteratureAdmin(admin.ModelAdmin):
    """Django Admin setup for the `literature.Literature` model."""

    list_display = ["citation_key", "title", "container_title", "type"]
    list_filter = ["type"]
    inlines = [SupplementaryInline]
    fieldsets = [
        (
            _("Citation"),
            {
                "fields": [
                    "type",
                    # *LiteratureAdminForm.Meta.entangled_fields["CSL"],
                ]
            },
        ),
        (
            _("PDF"),
            {
                "fields": [
                    "pdf",
                    # "CSL",
                ]
            },
        ),
    ]

    endpoint = {
        "fields": ["id", "title", "type", "container_title"],
        "include_str": False,
        "page_size": 1000,
        "permission_classes": [IsAdminUser, DjangoModelPermissions],
    }

    # def get_dt_fields(self):
    #     new_dict = {}
    #     for field, value in sorted(csl_fields.items()):
    #         new_dict[field] = value | {"title": field.replace("_", " ").replace("-", " ")}

    #     return new_dict

    def _pdf(self, obj):
        if obj.pdf:
            return obj.pdf.url

    def citation_key(self, obj):
        return obj.CSL.get("id", "")

    def edit(self, obj):
        return reverse(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_change",
            args=[obj.id],
        )

    # def get_urls(self):
    #     return [
    #         path("search/", self.admin_site.admin_view(self.search_online), name="search"),
    #         path("upload/", self.admin_site.admin_view(self.upload), name="upload"),
    #         *super().get_urls(),
    #     ]

    # def search_online(self, request, *args, **kwargs):
    #     """Admin view that handles user-uploaded bibtex files

    #     Returns:
    #         HttpResponseRedirect: redirects to model admins change_list
    #     """
    #     if request.method == "POST":
    #         form = OnlineSearchForm(request.POST)
    #         if form.is_valid():
    #             bibliography = form.cleaned_data["CSL"]

    #             imported, updated = 0, 0
    #             for item in bibliography:
    #                 imported += 1
    #                 Literature.objects.create(CSL=item)
    #             self.message_user(
    #                 request,
    #                 level=messages.SUCCESS,
    #                 message=(
    #                     f"{imported} literature item{pluralize(imported)} {pluralize(imported,'was,were')} succesfully"
    #                     f" imported and {updated} {pluralize(updated,'has,have')} been updated."
    #                 ),
    #             )
    #             return HttpResponseRedirect("../")

    #     else:
    #         form = OnlineSearchForm(request.GET)

    #     # return TemplateResponse(request, 'admin/change_form.html', {form: form})
    #     return TemplateResponse(
    #         request,
    #         "literature/admin/search.html",
    #         {
    #             "form": form,
    #             "opts": self.opts,
    #         },
    #     )

    # def upload(self, request, *args, **kwargs):
    #     """Admin view that handles user-uploaded bibtex files

    #     Returns:
    #         HttpResponseRedirect: redirects to model admins change_list
    #     """
    #     if request.method == "POST":
    #         form = BibFileUploadForm(request.POST)
    #         if form.is_valid():
    #             bibliography = form.cleaned_data["CSL"]

    #             imported, updated = 0, 0
    #             for item in bibliography:
    #                 imported += 1
    #                 Literature.objects.create(CSL=item)
    #             self.message_user(
    #                 request,
    #                 level=messages.SUCCESS,
    #                 message=(
    #                     f"{imported} literature item{pluralize(imported)} {pluralize(imported,'was,were')} succesfully"
    #                     f" imported and {updated} {pluralize(updated,'has,have')} been updated."
    #                 ),
    #             )
    #             return HttpResponseRedirect("../")

    #     else:
    #         form = BibFileUploadForm(request.GET)

    #     # return TemplateResponse(request, 'admin/change_form.html', {form: form})
    #     return TemplateResponse(
    #         request,
    #         "literature/admin/search.html",
    #         {
    #             "form": form,
    #             "opts": self.opts,
    #         },
    #     )


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    pass
