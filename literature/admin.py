from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin
from django import forms
from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path
from django.utils.translation import gettext as _

from .models import Collection, Literature, Name, SupplementaryMaterial


class LiteratureAdminAddForm(forms.ModelForm):
    DOI = forms.CharField(label=_("DOI"), required=False)

    class Meta:
        model = Literature
        fields = ["DOI"]


class SupplementaryInline(admin.TabularInline):
    model = SupplementaryMaterial
    extra = 1


class NameAdminInline(SortableInlineAdminMixin, admin.TabularInline):
    verbose_name = _("Author")
    verbose_name_plural = _("Authors")
    model = Literature.author.through
    extra = 1


@admin.register(Name)
class NameAdmin(admin.ModelAdmin):
    list_display = ["family", "given", "suffix"]
    search_fields = ["family", "name"]


@admin.register(Literature)
class LiteratureAdmin(SortableAdminBase, admin.ModelAdmin):
    """Django Admin setup for the `literature.Literature` model."""

    list_display = ["file_download_link", "title", "citation_key", "type"]
    list_filter = ["type"]
    list_display_links = ["title"]
    inlines = [NameAdminInline, SupplementaryInline]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "file",
                    "type",
                ]
            },
        ),
    ]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<path:object_id>/add-from/",
                self.admin_site.admin_view(self.intermediate_form_view),
                name="literature-add-from",
            ),
            # path("upload/", self.admin_site.admin_view(self.upload), name="upload"),
        ]
        return custom_urls + urls

    def intermediate_form_view(self, request, object_id):
        obj = self.get_object(request, object_id)
        if request.method == "POST":
            form = LiteratureAdminAddForm(request.POST)
            if form.is_valid():
                # Handle the form processing
                extra_field_value = form.cleaned_data["extra_field"]
                # Do something with the extra_field_value
                self.message_user(request, f"Processed extra data: {extra_field_value}")
                return redirect("admin:app_label_yourmodel_change", object_id)
        else:
            form = LiteratureAdminAddForm()

        context = self.admin_site.each_context(request)
        context["opts"] = self.model._meta
        context["form"] = form
        context["object"] = obj
        return render(request, "admin/literature_add_from.html", context)

    def response_change(self, request, obj):
        if not obj.pk:
            print("Redirecting")
            return redirect("admin:literature-add-from", obj.pk)
        print("Not redirecting")
        return super().response_change(request, obj)

    # def get_urls(self):
    #     return [
    #         path("search/", self.admin_site.admin_view(self.search_online), name="search"),
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
